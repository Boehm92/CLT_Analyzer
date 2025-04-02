import torch
import numpy as np
from sklearn.metrics import f1_score
from torch_geometric.nn import EdgeConv, global_mean_pool
from torch.nn import Sequential as Seq, Dropout, Linear as Lin, ReLU, BatchNorm1d as BN


def MLP(channels):
    return Seq(*[
        Seq(Lin(channels[i - 1], channels[i]), ReLU(), BN(channels[i]))
        for i in range(1, len(channels))
    ])


class DgcnNetwork(torch.nn.Module):
    def __init__(self, dataset, device, hyper_parameter):
        super().__init__()
        self.device = device
        self.aggr = hyper_parameter.aggr
        self.number_conv_layers = hyper_parameter.number_conv_layers
        self.conv_hidden_channels = hyper_parameter.conv_hidden_channels
        self.mlp_hidden_channels = hyper_parameter.mlp_hidden_channels
        self.dropout_probability = hyper_parameter.dropout_probability
        self.batch_size = hyper_parameter.batch_size

        self.conv1 = EdgeConv(
            MLP([int(2 * dataset.num_features), self.conv_hidden_channels, self.conv_hidden_channels]),
            self.aggr)
        self.conv2 = EdgeConv(MLP([int(2 * self.conv_hidden_channels), self.conv_hidden_channels,
                                   self.conv_hidden_channels]), self.aggr)
        if self.number_conv_layers > 2:
            self.conv3 = EdgeConv(MLP([int(2 * self.conv_hidden_channels), self.conv_hidden_channels,
                                       self.conv_hidden_channels]), self.aggr)
        if self.number_conv_layers > 3:
            self.conv4 = EdgeConv(MLP([int(2 * self.conv_hidden_channels), self.conv_hidden_channels,
                                       self.conv_hidden_channels]), self.aggr)

        self.lin = MLP([int(self.number_conv_layers * self.conv_hidden_channels), self.mlp_hidden_channels])
        self.mlp = Seq(MLP([self.mlp_hidden_channels, int(self.mlp_hidden_channels / 4)]),
                       Dropout(self.dropout_probability),
                       MLP([int(self.mlp_hidden_channels / 4), int(self.mlp_hidden_channels / 8)]),
                       Dropout(self.dropout_probability),
                       Lin(int(self.mlp_hidden_channels / 8), 24))

    def forward(self, x, edge_index, batch):

        x1 = self.conv1(x, edge_index)
        x2 = self.conv2(x1, edge_index)

        if self.number_conv_layers == 2:
            x = self.lin(torch.cat([x1, x2], dim=1))
        if self.number_conv_layers > 3:
            x3 = self.conv3(x2, edge_index)
        elif self.number_conv_layers == 3:
            x3 = self.conv3(x2, edge_index)
            x = self.lin(torch.cat([x1, x2, x3], dim=1))
        if self.number_conv_layers == 4:
            x4 = self.conv4(x3, edge_index)
            x = self.lin(torch.cat([x1, x2, x3, x4], dim=1))

        x = global_mean_pool(x, batch)

        x = self.mlp(x)

        return x

    def train_model(self, loader, criterion, optimizer):
        self.train()

        total_loss = 0
        for i, data in enumerate(loader):  # Iterate in batches over the training dataset.
            data = data.to(self.device)
            optimizer.zero_grad()  # Clear gradients.
            out = self(data.x, data.edge_index, data.batch)  # Perform a single forward pass.
            loss = criterion(out, data.y.reshape(self.batch_size, -1))
            total_loss += loss.item() * data.num_graphs
            loss.backward()  # Derive gradients.
            optimizer.step()  # Update parameters based on gradients.

        return total_loss / len(loader.dataset)

    def val_loss(self, loader, criterion):
        self.eval()

        total_loss = 0
        for data in loader:  # Iterate in batches over the training dataset.
            data = data.to(self.device)
            out = self(data.x, data.edge_index, data.batch)  # Perform a single forward pass.
            loss = criterion(out, data.y.reshape(self.batch_size, -1))
            total_loss += loss.item() * data.num_graphs

        return total_loss / len(loader.dataset)

    @torch.no_grad()
    def val_model(self, loader):
        self.eval()

        label_list, prediction_list = [], []
        for data in loader:
            label_list.append(data.y.reshape(self.batch_size, -1))
            out = self(data.x.to(self.device), data.edge_index.to(self.device), data.batch.to(self.device))
            prediction_list.append((out > 0).float().cpu())

        label, prediction = torch.cat(label_list, dim=0).numpy(), torch.cat(prediction_list, dim=0).numpy()
        return f1_score(label, prediction, average='micro') if prediction.sum() > 0 else 0

    @torch.no_grad()
    def test(self, loader):
        self.eval()
        all_predictions = []

        for data in loader:
            out = self(data.x.to(self.device), data.edge_index.to(self.device), data.batch.to(self.device))
            probabilities = torch.sigmoid(out)

            predicted_labels = (probabilities > 0.5).cpu().numpy()
            all_predictions.extend(predicted_labels)

        return np.array(all_predictions)

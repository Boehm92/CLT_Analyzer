import numpy as np
import torch
import torch.nn.functional as f
from torch_geometric.nn import EdgeConv, global_mean_pool
from torch.nn import Sequential as Seq, Dropout, Linear as Lin, ReLU, BatchNorm1d as BN
from sklearn.metrics import r2_score



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
        if self.number_conv_layers > 4:
            self.conv5 = EdgeConv(MLP([int(2 * self.conv_hidden_channels), self.conv_hidden_channels,
                                       self.conv_hidden_channels]), self.aggr)

        self.lin1 = MLP([int(self.number_conv_layers * self.conv_hidden_channels), self.mlp_hidden_channels])
        self.mlp = Seq(MLP([self.mlp_hidden_channels, int(self.mlp_hidden_channels / 4)]),
                       Dropout(self.dropout_probability),
                       MLP([int(self.mlp_hidden_channels / 4), int(self.mlp_hidden_channels / 8)]),
                       Dropout(self.dropout_probability),
                       Lin(int(self.mlp_hidden_channels / 8), 1))

    def forward(self, x, edge_index, data):

        x1 = self.conv1(x, edge_index)

        if self.number_conv_layers > 2:
            x2 = self.conv2(x1, edge_index)
        elif self.number_conv_layers == 2:
            x2 = self.conv2(x1, edge_index)
            out = self.lin1(torch.cat([x1, x2], dim=1))

        if self.number_conv_layers > 3:
            x3 = self.conv3(x2, edge_index)
        elif self.number_conv_layers == 3:
            x3 = self.conv3(x2, edge_index)
            out = self.lin1(torch.cat([x1, x2, x3], dim=1))

        if self.number_conv_layers > 4:
            x4 = self.conv4(x3, edge_index)
        elif self.number_conv_layers == 4:
            x4 = self.conv3(x3, edge_index)
            out = self.lin1(torch.cat([x1, x2, x3, x4], dim=1))

        if self.number_conv_layers == 5:
            x5 = self.conv5(x4, edge_index)
            out = self.lin1(torch.cat([x1, x2, x3, x4, x5], dim=1))

        out = global_mean_pool(out, data.batch)

        out = self.mlp(out)

        return out.squeeze()

    def train_loss(self, loader, criterion, optimizer):
        self.train()
        total_loss = 0
        mae_total_loss = 0

        for i, data in enumerate(loader):  # Iterate in batches over the training dataset.
            data = data.to(self.device)
            optimizer.zero_grad()  # Clear gradients.
            out = self(data.x, data.edge_index, data)  # Perform a single forward pass.
            loss = f.mse_loss(out, data.y)
            mae_loss = f.l1_loss(out, data.y)
            loss.backward()  # Derive gradients.
            optimizer.step()  # Update parameters based on gradients.

            total_loss += loss.item() * data.num_graphs
            mae_total_loss += mae_loss.item() * data.num_graphs

        avg_loss = np.sqrt(total_loss / len(loader.dataset))

        return avg_loss

    def val_loss(self, loader, criterion):
        self.eval()
        total_loss = 0
        mae_total_loss = 0
        y_all = []
        y_pred_all = []

        for data in loader:  # Iterate in batches over the validation dataset.
            data = data.to(self.device)
            out = self(data.x, data.edge_index, data)  # Perform a single forward pass.
            loss = f.mse_loss(out, data.y)
            mae_loss = f.l1_loss(out, data.y)
            total_loss += loss.item() * data.num_graphs
            mae_total_loss += mae_loss.item() * data.num_graphs

            y_all.append(data.y.cpu().detach().numpy())
            y_pred_all.append(out.cpu().detach().numpy())

        y_all = np.concatenate(y_all, axis=0)
        y_pred_all = np.concatenate(y_pred_all, axis=0)

        rmse = np.sqrt(total_loss / len(loader.dataset))
        r2 = r2_score(y_all, y_pred_all)
        avg_mae_loss = mae_total_loss / len(loader.dataset)

        return rmse, avg_mae_loss, r2

    @torch.no_grad()
    def test(self, loader):
        self.eval()

        for data in loader:
            out = self(data.x.to(self.device), data.edge_index.to(self.device), data.to(self.device))

        return out.item()

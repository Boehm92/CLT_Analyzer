import torch
import torch.nn.functional as f
from sklearn.metrics import f1_score
from torch_geometric.nn import GATConv, global_mean_pool
from torch.nn import Linear


class GATNetwork(torch.nn.Module):
    def __init__(self, dataset, device, hyper_parameter):
        super().__init__()
        self.dataset = dataset
        self.device = device
        self.batch_size = hyper_parameter.batch_size
        self.dropout_probability = hyper_parameter.dropout_probability
        self.attention_heads = hyper_parameter.attention_heads
        self.number_conv_layers = hyper_parameter.number_conv_layers
        self.conv_hidden_channels = hyper_parameter.conv_hidden_channels

        self.conv1 = GATConv(dataset.num_features, self.conv_hidden_channels, heads=self.attention_heads,
                             dropout=self.dropout_probability)
        if self.number_conv_layers == 2:
            self.conv2 = GATConv(self.conv_hidden_channels * self.attention_heads, self.conv_hidden_channels,
                                 concat=False)
        elif self.number_conv_layers == 3:
            self.conv2 = GATConv(self.conv_hidden_channels * self.attention_heads,
                                 self.conv_hidden_channels * self.attention_heads,
                                 heads=self.attention_heads, dropout=self.dropout_probability)
            self.conv3 = GATConv(self.conv_hidden_channels * (self.attention_heads ** 2), self.conv_hidden_channels,
                                 concat=False)

        self.lin = Linear(self.conv_hidden_channels, 24)

    def forward(self, x, edge_index, batch):
        x = f.elu(self.conv1(x, edge_index))
        x = f.dropout(x, p=self.dropout_probability, training=self.training)

        if self.number_conv_layers == 2:
            x = self.conv2(x, edge_index)
            x = f.dropout(x, p=self.dropout_probability, training=self.training)
        elif self.number_conv_layers == 3:
            x = f.elu(self.conv2(x, edge_index))
            x = f.dropout(x, p=self.dropout_probability, training=self.training)
            x = self.conv3(x, edge_index)
        x = global_mean_pool(x, batch)  # Aggregiert Knotenrepräsentationen zu einer Graph-Repräsentation
        x = self.lin(x)
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
        response = {}
        for data in loader:
            out = self(data.x.to(self.device), data.edge_index.to(self.device))
            predicted_labels = out.argmax(dim=1).cpu().numpy()  # NumPy-Array

        return predicted_labels

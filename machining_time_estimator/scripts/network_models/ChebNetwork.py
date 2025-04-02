import torch
import torch.nn.functional as f
from torch_geometric.nn import ChebConv
from torch.nn import Linear
from sklearn.metrics import f1_score

class ChebNetwork(torch.nn.Module):
    def __init__(self, dataset, device, hyper_parameter):
        super().__init__()
        self.dataset = dataset
        self.device = device
        self.batch_size = hyper_parameter.batch_size
        self.dropout_probability = hyper_parameter.dropout_probability
        self.number_conv_layers = hyper_parameter.number_conv_layers
        self.hidden_channels = hyper_parameter.conv_hidden_channels
        self.graph_filters = hyper_parameter.graph_filters

        self.conv1 = ChebConv(dataset.num_features, int(self.hidden_channels), self.graph_filters)
        if self.number_conv_layers > 1:
            self.conv2 = ChebConv(int(self.hidden_channels), int(self.hidden_channels * 2), self.graph_filters)
            _hidden_channel = int(self.hidden_channels * 2)
        if self.number_conv_layers > 2:
            self.conv3 = ChebConv(int(self.hidden_channels * 2), int(self.hidden_channels * 4), self.graph_filters)
            _hidden_channel = int(self.hidden_channels * 4)
        if self.number_conv_layers > 3:
            self.conv4 = ChebConv(int(self.hidden_channels * 4), int(self.hidden_channels * 8), self.graph_filters)
            _hidden_channel = int(self.hidden_channels * 8)
        self.lin = Linear(_hidden_channel, dataset.num_classes)

    def forward(self, x, edge_index):
        x = self.conv1(x, edge_index)
        x = f.relu(x)
        x = f.dropout(x, p=self.dropout_probability, training=self.training)
        if self.number_conv_layers > 1:
            x = self.conv2(x, edge_index)
            x = f.relu(x)
            x = f.dropout(x, p=self.dropout_probability, training=self.training)
        if self.number_conv_layers > 2:
            x = self.conv3(x, edge_index)
            x = f.relu(x)
            x = f.dropout(x, p=self.dropout_probability, training=self.training)
        if self.number_conv_layers > 3:
            x = self.conv4(x, edge_index)
            x = f.relu(x)
            x = f.dropout(x, p=self.dropout_probability, training=self.training)
        x = self.lin(x)
        return f.log_softmax(x, dim=1)

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
        mae_avg_loss = mae_total_loss / len(loader.dataset)

        return avg_loss, mae_avg_loss

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

        r2 = r2_score(y_all, y_pred_all)
        rmse = np.sqrt(total_loss / len(loader.dataset))

        avg_loss = total_loss / len(loader.dataset)
        avg_mae_loss = mae_total_loss / len(loader.dataset)

        return avg_loss, avg_mae_loss, rmse, r2

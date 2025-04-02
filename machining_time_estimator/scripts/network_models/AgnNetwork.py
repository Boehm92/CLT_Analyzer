import numpy as np
import torch
import torch.nn.functional as f
from torch_geometric.nn import AGNNConv
from sklearn.metrics import r2_score

class AgnNetwork(torch.nn.Module):
    def __init__(self, dataset, device, hyper_parameter):
        super().__init__()
        self.dataset = dataset
        self.device = device
        self.batch_size = hyper_parameter.batch_size
        self.dropout_probability = hyper_parameter.dropout_probability
        self.number_conv_layers = hyper_parameter.number_conv_layers
        self.hidden_channels = hyper_parameter.hidden_channels

        self.lin1 = torch.nn.Linear(dataset.num_features, self.hidden_channels)
        self.prop1 = AGNNConv(requires_grad=False)
        if self.number_conv_layers > 1:
            self.prop2 = AGNNConv(requires_grad=False)
        if self.number_conv_layers > 2:
            self.prop3 = AGNNConv(requires_grad=False)
        if self.number_conv_layers > 3:
            self.prop4 = AGNNConv(requires_grad=False)
        self.lin2 = torch.nn.Linear(self.hidden_channels, dataset.num_classes)

    def forward(self, x, edge_index):
        x = f.relu(self.lin1(x))
        x = f.dropout(x, p=self.dropout_probability, training=self.training)

        x = self.prop1(x, edge_index)
        if self.number_conv_layers > 1:
            x = self.prop2(x, edge_index)
        if self.number_conv_layers > 2:
            x = self.prop3(x, edge_index)
        if self.number_conv_layers > 3:
            x = self.prop4(x, edge_index)
        x = f.dropout(x, p=self.dropout_probability, training=self.training)

        x = self.lin2(x)
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
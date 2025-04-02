import numpy as np
import torch
import torch.nn.functional as f
from torch_geometric.nn import ARMAConv
from sklearn.metrics import r2_score

class ArmaNetwork(torch.nn.Module):
    def __init__(self, dataset, device, hyper_parameter):
        super().__init__()
        self.dataset = dataset
        self.device = device
        self.batch_size = hyper_parameter.batch_size
        self.dropout_probability = hyper_parameter.dropout_probability
        self.layer_dropout_probability = hyper_parameter.layer_dropout_probability
        self.number_conv_layers = hyper_parameter.number_conv_layers
        self.hidden_channels = hyper_parameter.conv_hidden_channels
        self.num_stacks = hyper_parameter.num_stacks
        self.num_layer = hyper_parameter.num_layer

        self.conv1 = ARMAConv(dataset.num_features, self.hidden_channels, self.num_stacks, self.num_layer, 'store_true',
                              dropout=self.layer_dropout_probability)
        if self.number_conv_layers > 2:
            self.conv2 = ARMAConv(self.hidden_channels, self.hidden_channels, self.num_stacks, self.num_layer,
                                  'store_true', dropout=self.layer_dropout_probability)
        elif self.number_conv_layers == 2:
            self.conv2 = ARMAConv(self.hidden_channels, dataset.num_classes, self.num_stacks, self.num_layer,
                                  'store_true', dropout=self.layer_dropout_probability)

        if self.number_conv_layers > 3:
            self.conv3 = ARMAConv(self.hidden_channels, self.hidden_channels, self.num_stacks, self.num_layer,
                                  'store_true', dropout=self.layer_dropout_probability)
        elif self.number_conv_layers == 3:
            self.conv3 = ARMAConv(self.hidden_channels, dataset.num_classes, self.num_stacks, self.num_layer,
                                  'store_true', dropout=self.layer_dropout_probability)

        if self.number_conv_layers == 4:
            self.conv4 = ARMAConv(self.hidden_channels, dataset.num_classes, self.num_stacks, self.num_layer,
                                  'store_true', dropout=self.layer_dropout_probability)

    def forward(self, x, edge_index):
        x = f.relu(self.conv1(x, edge_index))
        x = f.dropout(x, p=self.dropout_probability, training=self.training)
        x = f.relu(self.conv2(x, edge_index))
        x = f.dropout(x, p=self.dropout_probability, training=self.training)
        if self.number_conv_layers > 2:
            x = f.relu(self.conv3(x, edge_index))
            x = f.dropout(x, p=self.dropout_probability, training=self.training)
        if self.number_conv_layers > 3:
            x = f.relu(self.conv4(x, edge_index))
            x = f.dropout(x, p=self.dropout_probability, training=self.training)
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

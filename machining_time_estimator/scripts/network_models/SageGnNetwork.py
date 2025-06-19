import torch
from statistics import mean
import torch.nn.functional as f
from torch_geometric.nn import SAGEConv, global_mean_pool
from sklearn.metrics import f1_score
from torch.nn import Sequential, Linear, ReLU, Dropout

class SageGnNetwork(torch.nn.Module):
    def __init__(self, dataset, device, hyper_parameter):
        super().__init__()
        self.dataset = dataset
        self.device = device
        self.batch_size = hyper_parameter.batch_size
        self.dropout_probability = hyper_parameter.dropout_probability
        self.number_conv_layers = hyper_parameter.number_conv_layers
        self.hidden_channels = hyper_parameter.hidden_channels
        self.aggr = hyper_parameter.aggr


        self.conv1 = SAGEConv(dataset.num_features, self.hidden_channels, self.aggr)
        if self.number_conv_layers > 1:
            self.conv2 = SAGEConv(self.hidden_channels, self.hidden_channels, self.aggr)
        if self.number_conv_layers > 2:
            self.conv3 = SAGEConv(self.hidden_channels, self.hidden_channels, self.aggr)
        if self.number_conv_layers > 3:
            self.conv4 = SAGEConv(self.hidden_channels, self.hidden_channels, self.aggr)
        if self.number_conv_layers > 4:
            self.conv5 = SAGEConv(self.hidden_channels, dataset.num_classes, self.aggr)

        self.dropout = Dropout(self.dropout_probability)
        self.lin1 = Linear(self.hidden_channels, self.hidden_channels // 2)  # First Linear layer
        self.lin2 = Linear(self.hidden_channels // 2, 1)  # Output layer for regression



    def forward(self, x, edge_index):
        x = self.conv1(x, edge_index)
        x = x.relu()
        x = f.dropout(x, p=self.dropout_probability, training=self.training)
        if self.number_conv_layers > 1:
            x = self.conv2(x, edge_index)
            x = x.relu()
            x = f.dropout(x, p=self.dropout_probability, training=self.training)
        if self.number_conv_layers > 2:
            x = self.conv3(x, edge_index)
            x = x.relu()
            x = f.dropout(x, p=self.dropout_probability, training=self.training)
        if self.number_conv_layers > 3:
            x = self.conv4(x, edge_index)
            x = x.relu()
            x = f.dropout(x, p=self.dropout_probability, training=self.training)
        if self.number_conv_layers > 4:
            x = self.conv5(x, edge_index)
            x = x.relu()
            x = f.dropout(x, p=self.dropout_probability, training=self.training)

        x = global_mean_pool(x, self.batch_size)
        x = self.lin1(x)
        x = x.reLU()()
        x = self.lin2(x)

        return x.squeeze()

    def train_loss(self, loader, criterion, optimizer):
        self.train()

        total_loss = 0
        for i, data in enumerate(loader):  # Iterate in batches over the training dataset.
            data = data.to(self.device)
            optimizer.zero_grad()  # Clear gradients.
            out = self(data.x, data.edge_index)  # Perform a single forward pass.
            print(out)
            loss = criterion(out, data.y)
            loss.backward()  # Derive gradients.
            optimizer.step()  # Update parameters based on gradients.

        return loss

    def val_loss(self, loader, criterion):
        self.eval()

        total_loss = 0
        for data in loader:  # Iterate in batches over the training dataset.
            data = data.to(self.device)
            out = self(data.x, data.edge_index).clamp(min=0, max=50)  # Perform a single forward pass.
            target = data.y.float()
            # print("out: ", out)
            # print("target: ", target)
            loss = f.mse_loss(out, target).sqrt()

        return float(loss)

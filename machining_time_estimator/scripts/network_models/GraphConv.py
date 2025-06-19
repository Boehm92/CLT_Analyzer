import torch
from statistics import mean
import torch.nn.functional as f
from torch.nn import Linear
from torch_geometric.nn import GraphConv as GraphConvLayer
from torch_geometric.nn import global_mean_pool
from torch.nn import Sequential as Seq, Dropout, Linear as Lin, ReLU, BatchNorm1d as BN
from sklearn.metrics import f1_score


class GraphConv(torch.nn.Module):
    def __init__(self, dataset, device, hyper_parameter):
        super().__init__()
        self.device = device
        self.hidden_channels = 8
        self.hyper_parameters = hyper_parameter
        self.dropout_probability = hyper_parameter.dropout_probability
        self.dataset = dataset
        self.batch_size = hyper_parameter.batch_size

        self.conv1 = GraphConvLayer(self.dataset.num_node_features, int(self.hidden_channels))
        self.conv2 = GraphConvLayer(int(self.hidden_channels), int(self.hidden_channels), aggr='mean')
        self.conv3 = GraphConvLayer(int(self.hidden_channels), int(self.hidden_channels), aggr='mean')

        self.lin_out1 = Linear(int(self.hidden_channels), int(self.hidden_channels / 2))
        self.lin_out2 = Linear(int(self.hidden_channels / 2), 1)


    def forward(self, x, edge_index, data):
        x = self.conv1(x, edge_index)
        x = x.relu()
        x = self.conv2(x, edge_index)
        x = x.relu()
        x = self.conv3(x, edge_index)
        x = x.relu()
        x = f.dropout(x, p=self.dropout_probability, training=self.training)

        # 2. Readout layer
        x = global_mean_pool(x, data.batch)

        # 3. Apply a final classifier
        x = f.dropout(x, p=self.dropout_probability, training=self.training)
        x = self.lin_out1(x)
        x = x.relu()
        x = self.lin_out2(x)

        return x

    def train_loss(self, loader, criterion, optimizer):
        self.train()

        total_loss = 0
        for i, data in enumerate(loader):  # Iterate in batches over the training dataset.
            data = data.to(self.device)
            optimizer.zero_grad()  # Clear gradients.
            out = self(data.x, data.edge_index, data)  # Perform a single forward pass.
            loss = f.mse_loss(out.squeeze(), data.y)
            loss.backward()  # Derive gradients.
            optimizer.step()  # Update parameters based on gradients.

        return loss

    def val_loss(self, loader, criterion):
        self.eval()

        for data in loader:  # Iterate in batches over the training dataset.
            data = data.to(self.device)
            out = self(data.x, data.edge_index, data)  # Perform a single forward pass.
            loss = f.mse_loss(out.squeeze(), data.y)

        return float(loss)

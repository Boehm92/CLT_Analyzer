import torch
import torch.nn.functional as f
from sklearn.metrics import f1_score
from torch_geometric.nn import FeaStConv, global_mean_pool
from torch.nn import Linear as Lin


class FeaStNetwork(torch.nn.Module):
    def __init__(self, dataset, device, hyper_parameter):
        super().__init__()
        self.dataset = dataset
        self.device = device
        self.batch_size = hyper_parameter.batch_size
        self.dropout_probability = hyper_parameter.dropout_probability
        self.number_conv_layers = hyper_parameter.number_conv_layers
        self.conv_hidden_channels = hyper_parameter.conv_hidden_channels
        self.lin_hidden_channels = hyper_parameter.lin_hidden_channels
        self.attention_heads = hyper_parameter.attention_heads

        self.fc0 = Lin(dataset.num_features, int(self.conv_hidden_channels))
        self.conv1 = FeaStConv(int(self.conv_hidden_channels), int(self.conv_hidden_channels * 2),
                               heads=self.attention_heads)
        if self.number_conv_layers > 1:
            self.conv2 = FeaStConv(int(self.conv_hidden_channels * 2), int(self.conv_hidden_channels * 4),
                                   heads=self.attention_heads)
            _conv_hidden_channels = int(self.conv_hidden_channels * 4)

        if self.number_conv_layers > 2:
            self.conv3 = FeaStConv(int(self.conv_hidden_channels * 4), int(self.conv_hidden_channels * 8),
                                   heads=self.attention_heads)
            _conv_hidden_channels = int(self.conv_hidden_channels * 8)

        if self.number_conv_layers > 3:
            self.conv4 = FeaStConv(int(self.conv_hidden_channels * 8), int(self.conv_hidden_channels * 16),
                                   heads=self.attention_heads)
            _conv_hidden_channels = int(self.conv_hidden_channels * 16)

        self.fc1 = Lin(_conv_hidden_channels, self.lin_hidden_channels)
        self.fc2 = Lin(self.lin_hidden_channels, 24)

    def forward(self, x, edge_index, batch):
        x = f.elu(self.fc0(x))
        x = f.elu(self.conv1(x, edge_index))
        if self.number_conv_layers > 1:
            x = f.elu(self.conv2(x, edge_index))
        if self.number_conv_layers > 2:
            x = f.elu(self.conv3(x, edge_index))
        if self.number_conv_layers > 3:
            x = f.elu(self.conv4(x, edge_index))

        x = global_mean_pool(x, batch)
        x = f.elu(self.fc1(x))
        x = f.dropout(x, training=self.training)
        x = self.fc2(x)
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

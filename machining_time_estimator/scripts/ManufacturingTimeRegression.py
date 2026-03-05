import os

import madcad as mdc
import numpy as np
import torch
from stl import mesh
from torch_geometric.loader import DataLoader
from utils.DataImporter import DataImporter
from utils.HyperParameter import HyperParameter


class ManufacturingTimeRegression:
    def __init__(self, config):
        self.max_epoch = config.max_epoch
        self.training_dataset = config.training_dataset
        self.network_model = config.network_model
        self.network_model_id = config.network_model_id
        self.train_val_partition = config.train_val_partition
        self.hyper_parameters = HyperParameter(config.network_model_id)
        self.device = config.device
        self.project_name = config.project_name
        self.study_name = config.study_name
        torch.manual_seed(1)

    def training(self):
        _best_epoch = 0
        _best_r2 = 0

        self.training_dataset.shuffle()
        _train_loader = DataLoader(
            self.training_dataset[: self.train_val_partition],
            batch_size=self.hyper_parameters.batch_size,
            shuffle=True,
            drop_last=True,
        )
        _val_loader = DataLoader(
            self.training_dataset[self.train_val_partition :],
            batch_size=self.hyper_parameters.batch_size,
            shuffle=True,
            drop_last=True,
        )

        _network_model = self.network_model(self.training_dataset, self.device, self.hyper_parameters).to(self.device)
        print(_network_model)

        # Configuring learning functions
        criterion = torch.nn.BCELoss()
        optimizer = torch.optim.Adam(_network_model.parameters(), lr=self.hyper_parameters.learning_rate)

        statistics = {"training_loss": [], "val_loss": [], "train_r2": [], "val_r2": []}

        # Training
        for epoch in range(1, self.max_epoch):
            backpropagation_loss = _network_model.train_loss(_train_loader, criterion, optimizer)
            rmse_train_loss, mae_train_loss, r2_train_loss = _network_model.val_loss(_train_loader, criterion)
            rmse_val_loss, mae_val_loss, r2_val_loss = _network_model.val_loss(_val_loader, criterion)

            statistics["training_loss"].append(backpropagation_loss)
            statistics["val_loss"].append(rmse_val_loss)
            statistics["train_r2"].append(r2_train_loss)
            statistics["val_r2"].append(r2_val_loss)

            print(
                f"Epoch: {epoch:03d}, "
                f"train_loss: {backpropagation_loss:.4f}, val_loss: {rmse_val_loss:.4f},"
                f" train_r2: {r2_train_loss:.4f}, val_r2: {r2_val_loss:.4f},"
            )

            if _best_r2 < r2_val_loss:
                torch.save(_network_model.state_dict(), os.getenv("WEIGHTS") + "/mte_weights.pt")
                _best_r2 = r2_val_loss
                _best_epoch = epoch
                print("Saved model due to better R2")

        statistics["best_val_r2"] = _best_r2
        statistics["best_epoch"] = _best_epoch
        with open(os.getenv("WEIGHTS") + "/mte_statistics.json", "w") as f:
            import json

            json.dump(statistics, f, indent=4)

        print("Best validation R2 score: ", _best_r2)
        print("Best epoch: ", _best_epoch)

        return rmse_val_loss

    def test(self):
        _response = 0
        _combined_response = {
            "volume": 0.0,
            "body_center": [0.0, 0.0, 0.0],
            "length": 0.0,
            "width": 0.0,
            "height": 0.0,
            "time": 0.0,
        }

        stl_mesh = mesh.Mesh.from_file(os.path.join(os.getenv("TEST_DATA"), "received.stl"))
        _volume, _cog, _inertia = stl_mesh.get_mass_properties()
        _min_coords = np.min(stl_mesh.vectors, axis=(0, 1))
        _max_coords = np.max(stl_mesh.vectors, axis=(0, 1))
        _length, _width, _height = _max_coords - _min_coords

        _combined_response["volume"] = _volume
        _combined_response["body_center"] = _cog.tolist()
        _combined_response["length"] = _length
        _combined_response["width"] = _width
        _combined_response["height"] = _height

        _test_dataset = DataImporter(os.getenv("TEST_DATA"), os.getenv("TEST_DATA"))
        _test_loader = DataLoader(
            _test_dataset, batch_size=1, shuffle=False, drop_last=True
        )

        _network_model = self.network_model(_test_dataset, self.device, self.hyper_parameters).to(self.device)
        _network_model.load_state_dict(torch.load((os.getenv("WEIGHTS") + "/mte_weights.pt"), torch.device("cuda")))

        _response += _network_model.test(_test_loader)
        os.remove(os.path.join(os.getenv("TEST_DATA"), "processed/mte_data.pt"))
        os.remove(os.path.join(os.getenv("TEST_DATA"), "processed/pre_filter.pt"))
        os.remove(os.path.join(os.getenv("TEST_DATA"), "processed/pre_transform.pt"))
        os.remove(os.path.join(os.getenv("TEST_DATA"), "received.stl"))

        _combined_response["time"] = _response

        del _test_dataset
        del _test_loader
        del _network_model

        return _combined_response

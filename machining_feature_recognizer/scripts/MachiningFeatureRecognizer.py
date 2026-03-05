import os

import madcad as mdc
import torch
from torch_geometric.loader import DataLoader
from utils.DataImporter import DataImporter
from utils.HyperParameter import HyperParameter


class MachiningFeatureRecognizer:
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
        # Hyperparameter optimization
        _best_f1 = 0
        _best_epoch = 0

        self.training_dataset.shuffle()
        train_loader = DataLoader(
            self.training_dataset[: self.train_val_partition],
            batch_size=self.hyper_parameters.batch_size,
            shuffle=True,
            drop_last=True,
        )
        val_loader = DataLoader(
            self.training_dataset[self.train_val_partition :],
            batch_size=self.hyper_parameters.batch_size,
            shuffle=True,
            drop_last=True,
        )

        _network_model = self.network_model(self.training_dataset, self.device, self.hyper_parameters).to(self.device)
        print(_network_model)

        # Configuring learning functions
        criterion = torch.nn.BCEWithLogitsLoss()
        optimizer = torch.optim.Adam(_network_model.parameters(), lr=self.hyper_parameters.learning_rate)

        statistics = {"training_loss": [], "val_loss": [], "train_f1": [], "val_f1": []}

        # Training
        for epoch in range(1, self.max_epoch):
            training_loss = _network_model.train_model(train_loader, criterion, optimizer)
            val_loss = _network_model.val_loss(val_loader, criterion)
            train_f1 = _network_model.val_model(train_loader)
            val_f1 = _network_model.val_model(val_loader)

            statistics["training_loss"].append(training_loss)
            statistics["val_loss"].append(val_loss)
            statistics["train_f1"].append(train_f1)
            statistics["val_f1"].append(val_f1)
            print(
                f"Epoch: {epoch:03d}, training_loss: {training_loss:.4f}, val_loss: {val_loss:.4f}, "
                f"train_F1: {train_f1:.4f}, val_F1: {val_f1:.4f}"
            )

            if _best_f1 < val_f1:
                torch.save(_network_model.state_dict(), os.getenv("WEIGHTS") + "/mfr_weights.pt")
                _best_f1 = val_f1
                _best_epoch = epoch
                print("Saved model due to better F1-Score")

        statistics["best_val_f1"] = _best_f1
        statistics["best_epoch"] = _best_epoch
        with open(os.getenv("WEIGHTS") + "/mfr_statistics.json", "w") as f:
            import json

            json.dump(statistics, f, indent=4)

        print("Best validation F1 score: ", _best_f1)
        print("Best epoch: ", _best_epoch)
        return val_f1

    def test(self):
        _test_dataset = DataImporter(os.getenv("TEST_DATA"), os.getenv("TEST_DATA"))
        _test_loader = DataLoader(_test_dataset, batch_size=1, shuffle=False, drop_last=True)

        _network_model = self.network_model(self.training_dataset, self.device, self.hyper_parameters).to(self.device)
        _network_model.load_state_dict(torch.load((os.getenv("WEIGHTS") + "/mfr_weights.pt"), torch.device("cuda")))

        predicted_labels = _network_model.test(_test_loader)

        os.remove(os.path.join(os.getenv("TEST_DATA"), "processed/mfr_data.pt"))
        os.remove(os.path.join(os.getenv("TEST_DATA"), "processed/pre_filter.pt"))
        os.remove(os.path.join(os.getenv("TEST_DATA"), "processed/pre_transform.pt"))
        os.remove(os.path.join(os.getenv("TEST_DATA"), "received.stl"))

        del _test_dataset
        del _test_loader
        del _network_model

        return predicted_labels

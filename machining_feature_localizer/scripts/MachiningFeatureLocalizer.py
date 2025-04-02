import os
import torch
import wandb
import optuna
import madcad as mdc
from utils.DataImporter import DataImporter
from torch_geometric.loader import DataLoader
from utils.HyperParameter import HyperParameter


class MachiningFeatureLocalizer:
    def __init__(self, config, trial):
        self.max_epoch = config.max_epoch
        self.training_dataset = config.training_dataset
        self.network_model = config.network_model
        self.network_model_id = config.network_model_id
        self.train_val_partition = config.train_val_partition
        self.trial = trial
        self.hyper_parameters = HyperParameter(trial, config.network_model_id)
        self.device = config.device
        self.project_name = config.project_name
        self.study_name = config.study_name
        torch.manual_seed(1)

    def training(self, trial):
        _best_accuracy = 0

        self.training_dataset.shuffle()
        _train_loader = DataLoader(self.training_dataset[:self.train_val_partition],
                                   batch_size=self.hyper_parameters.batch_size, shuffle=True, drop_last=True)
        _val_loader = DataLoader(self.training_dataset[self.train_val_partition:],
                                 batch_size=self.hyper_parameters.batch_size, shuffle=True, drop_last=True)

        _network_model = self.network_model(self.training_dataset, self.device, self.hyper_parameters).to(self.device)
        print(_network_model)

        # Configuring learning functions
        criterion = torch.nn.CrossEntropyLoss()
        optimizer = torch.optim.Adam(_network_model.parameters(), lr=self.hyper_parameters.learning_rate)

        # Setting up hyperparameter function and wandb
        _config = dict(trial.params)
        _config["trial.number"] = trial.number
        wandb.init(project=self.project_name, entity="boehm92", config=_config, group=self.study_name, reinit=True)

        # Training
        for epoch in range(1, self.max_epoch):
            training_loss = _network_model.train_loss(_train_loader, criterion, optimizer)
            val_loss = _network_model.val_loss(_val_loader, criterion)
            train_f1, all_predicted_labels = _network_model.accuracy(_train_loader)
            val_f1, all_predicted_labels = _network_model.accuracy(_val_loader)
            trial.report(val_f1, epoch)

            wandb.log({'training_loss': training_loss, 'val_los': val_loss, 'train_F1': train_f1, 'val_F1': val_f1})

            if (_best_accuracy < val_f1) & ((val_loss - training_loss) < 0.04):
                torch.save(_network_model.state_dict(), os.getenv('WEIGHTS') + '/mfs_weights.pt')
                _best_accuracy = val_f1
                print("Saved model due to better found accuracy")

            if trial.should_prune():
                wandb.run.summary["state"] = "pruned"
                wandb.finish(quiet=True)
                raise optuna.exceptions.TrialPruned()

            if (train_f1 + 0.2) < val_f1:
                wandb.run.summary["state"] = "pruned"
                wandb.finish(quiet=True)
                raise optuna.exceptions.TrialPruned()

            print(f'Epoch: {epoch:03d}, training_loss: {training_loss:.4f}, val_los: {val_loss:.4f}, '
                  f'train_F1: {train_f1:.4f}, val_F1: {val_f1:.4f}')

        wandb.run.summary["Final F-Score"] = val_f1
        wandb.run.summary["state"] = "completed"
        wandb.finish(quiet=True)

        return val_f1

    def test(self):
        _intersecting_models = []
        _combined_response = {"features": [], "predicted_labels": []}
        _offset = 5.000001
        _new_cad_model = mdc.io.read(os.path.join(os.getenv('TEST_DATA'), "received.stl"))
        _new_cad_model.mergeclose()
        _new_cad_model = mdc.segmentation(_new_cad_model)

        for x in range(3):
            for y in range(2):
                for z in range(3):
                    try:
                        _position = [x * 10 + _offset, y * 10 + _offset, z * 10 + _offset]  # Konvertiere zu Liste
                        _cube = mdc.brick(width=mdc.vec3(10)).transform(mdc.vec3(_position))
                        _intersected_model = mdc.intersection(_new_cad_model, _cube).transform(
                            -mdc.vec3(*_position) + _offset)
                        mdc.write(_intersected_model, os.path.join(os.getenv('TEST_DATA'), "received.stl"))

                        _test_dataset = DataImporter(os.getenv('TEST_DATA'), os.getenv('TEST_DATA'))
                        _test_loader = DataLoader(_test_dataset, batch_size=self.hyper_parameters.batch_size,
                                                  shuffle=False, drop_last=True)
                    except FileNotFoundError:
                        print('No CAD test data found.')
                        continue

                    _network_model = self.network_model(_test_dataset, self.device, self.hyper_parameters).to(
                        self.device)
                    _network_model.load_state_dict(
                        torch.load((os.getenv('WEIGHTS') + '/mfs_weights.pt'), torch.device('cuda')))
                    response = _network_model.test(_test_loader)

                    corrected_features = [
                        [f[0] + _position[0] - 5, f[1] + _position[1] - 5, f[2] + _position[2] - 5]
                        for f in response["features"]
                    ]

                    # **Kombinierte Response aktualisieren**
                    _combined_response["features"].extend(corrected_features)
                    _combined_response["predicted_labels"].extend(response["predicted_labels"])

                    os.remove(os.path.join(os.getenv('TEST_DATA'), "processed/mfs_data.pt"))
                    os.remove(os.path.join(os.getenv('TEST_DATA'), "processed/pre_filter.pt"))
                    os.remove(os.path.join(os.getenv('TEST_DATA'), "processed/pre_transform.pt"))
                    os.remove(os.path.join(os.getenv('TEST_DATA'), "received.stl"))
        del _test_dataset
        del _test_loader
        del _network_model

        return _combined_response

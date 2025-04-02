import os
import torch
import wandb
import optuna
import numpy as np
import madcad as mdc
from stl import mesh
from utils.DataImporter import DataImporter
from torch_geometric.loader import DataLoader
from utils.HyperParameter import HyperParameter


class ManufacturingTimeRegression:
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

    def training(self):
        _best_loss = 10

        self.training_dataset.shuffle()
        _train_loader = DataLoader(self.training_dataset[:self.train_val_partition],
                                   batch_size=self.hyper_parameters.batch_size, shuffle=True, drop_last=True)
        _val_loader = DataLoader(self.training_dataset[self.train_val_partition:],
                                 batch_size=self.hyper_parameters.batch_size, shuffle=True, drop_last=True)

        _network_model = self.network_model(self.training_dataset, self.device, self.hyper_parameters).to(self.device)
        print(_network_model)

        # Configuring learning functions
        criterion = torch.nn.BCELoss()
        optimizer = torch.optim.Adam(_network_model.parameters(), lr=self.hyper_parameters.learning_rate)

        # Setting up hyperparameter function and wandb
        _config = dict(self.trial.params)
        _config["trial.number"] = self.trial.number
        wandb.init(project=self.project_name, entity="boehm92", config=_config, group=self.study_name, reinit=True)

        # Training
        for epoch in range(1, self.max_epoch):
            backpropagation_loss = _network_model.train_loss(_train_loader, criterion, optimizer)
            rmse_train_loss, mae_train_loss, r2_train_loss =\
                _network_model.val_loss(_train_loader, criterion)
            rmse_val_loss, mae_val_loss, r2_val_loss = \
                _network_model.val_loss(_val_loader, criterion)

            wandb.log({'backpropagation_loss': backpropagation_loss,
                       'rmse_train_loss': rmse_train_loss, 'rmse_val_loss': rmse_val_loss,
                       'mae_train_loss': mae_train_loss, 'mae_val_loss': mae_val_loss,
                       'r2_train_loss': r2_train_loss, 'r2_val_loss': r2_val_loss})

            if rmse_val_loss < _best_loss:
                torch.save(_network_model.state_dict(), os.getenv('WEIGHTS') + '/mte_weights.pt')
                _best_loss = rmse_val_loss
                print("Saved model due to better found accuracy")

            if self.trial.should_prune():
                wandb.run.summary["state"] = "pruned"
                wandb.finish(quiet=True)
                raise optuna.exceptions.TrialPruned()

            print(f'Epoch: {epoch:03d}, loss: {backpropagation_loss:.4f}, '
                  f'rmse_train_loss: {rmse_train_loss:.4f}, rmse_val_loss: {rmse_val_loss:.4f},'
                  f'mae_train_loss: {mae_train_loss:.4f}, mae_val_loss: {mae_val_loss:.4f}, '
                  f' r2_train_loss: {r2_train_loss:.4f}, r2_val_loss: {r2_val_loss:.4f},')

        wandb.run.summary["Final F-Score"] = rmse_val_loss
        wandb.run.summary["state"] = "completed"
        wandb.finish(quiet=True)

        return rmse_val_loss

    def test(self):
        _intersecting_models = []
        _response = 0
        _combined_response = {
            "volume": 0.0,
            "body_center": [0.0, 0.0, 0.0],
            "length": 0.0,
            "width": 0.0,
            "height": 0.0,
            "time": 0.0
        }
        _offset = 5.000001
        _new_cad_model = mdc.io.read(os.path.join(os.getenv('TEST_DATA'), "received.stl"))
        _new_cad_model.mergeclose()
        _new_cad_model = mdc.segmentation(_new_cad_model)

        stl_mesh = mesh.Mesh.from_file(os.path.join(os.getenv('TEST_DATA'), 'received.stl'))
        _volume, _cog, _inertia = stl_mesh.get_mass_properties()
        _min_coords = np.min(stl_mesh.vectors, axis=(0, 1))
        _max_coords = np.max(stl_mesh.vectors, axis=(0, 1))
        _length, _width, _height = _max_coords - _min_coords

        _combined_response["volume"] = _volume
        _combined_response["body_center"] = _cog.tolist()
        _combined_response["length"] = _length
        _combined_response["width"] = _width
        _combined_response["height"] = _height

        for x in range(3):
            for y in range(2):
                for z in range(3):
                    try:
                        _position = [x * 10 + _offset, y * 10 + _offset, z * 10 + _offset]
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
                        torch.load((os.getenv('WEIGHTS') + '/mte_weights.pt'), torch.device('cuda')))

                    _response += _network_model.test(_test_loader)
                    os.remove(os.path.join(os.getenv('TEST_DATA'), "processed/mte_data.pt"))
                    os.remove(os.path.join(os.getenv('TEST_DATA'), "processed/pre_filter.pt"))
                    os.remove(os.path.join(os.getenv('TEST_DATA'), "processed/pre_transform.pt"))
                    os.remove(os.path.join(os.getenv('TEST_DATA'), "received.stl"))

        _combined_response["time"] = _response

        del _test_dataset
        del _test_loader
        del _network_model

        return _combined_response
import os
import torch
import optuna
import argparse
from utils.RestService import RestService
from utils.DataImporter import DataImporter
from MachiningFeatureLocalizer import MachiningFeatureLocalizer
from network_models.GcNetwork import GcNetwork
from network_models.DgcnNetwork import DgcnNetwork
from network_models.SageGnNetwork import SageGnNetwork
from network_models.FeaStNetwork import FeaStNetwork
from network_models.GATNetwork import GATNetwork
from network_models.GATV2Network import GATV2Network
from network_models.ChebNetwork import ChebNetwork
from network_models.ArmaNetwork import ArmaNetwork
from network_models.AgnNetwork import AgnNetwork


_parser = argparse.ArgumentParser(description='Base configuration of the synthetic data generator')
_parser.add_argument('--application_mode',
                     dest='application_mode', default='training', type=str,
                     help='The application modes has "training" and "test". When set to trained the framework uses the'
                          'TestModel class to train graph neural network. Please note, if you want to test different'
                          'graph conv layer, the TestModel class must be configured with accordingly. For example,'
                          'if you want to use the FeastNet layer please follow the guidelines from '
                          'https://pytorch-geometric.readthedocs.io/en/latest/generated/torch_geometric.nn.conv - '
                          '.FeaStConv.html#torch_geometric.nn.conv.FeaStConv, When set to test, the GraphConvModel is'
                          'used. Here a weights file for a trained model is loaded. When you trained the model first,'
                          'the weights file should be automatically be saved in the given path from the defined'
                          'environment variable WEIGHTS, like described in the README file. Do to the fact, that the'
                          'trained mode utilizes hyperparameter, the model architecture can vary with every program run'
                          'Therefore, make sure that you configure the GraphConvModel accordingly. Also the training '
                          'procedure uses a so called hyperparameter optimization. For more info about this '
                          'optimization process, please visit: https://optuna.org/')
_parser.add_argument('--project_name',
                     dest='project_name', default='CoCadAi_framework', type=str,
                     help='This name belongs to the wandb project which is created when the code is started. The wandb '
                          'code publishes training parameters like train_accuracy to your personal wandb dashboard. You'
                          'just have to register at www.wandb.ai and follow the instructions at: '
                          'https://docs.wandb.ai/quickstart.'
                          '(Not used for testing)')
_parser.add_argument('--study_name',
                     dest='study_name', default='MFS_DGCNN', type=str, #MFS_DGCNN
                     help='The study name defines a subgroup for the wandb project, which is defined above. This helps'
                          'to repeat an experiment or training process without creating every time a new wandb project.'
                          '(Not used for testing)')
_parser.add_argument('--hyperparameter_trials',
                     dest='hyperparameter_trials', default=50, type=int,
                     help='The hyperparameter_trials value defines how often the training procedure is repeated.'
                          'Reason for repeated training is, that this framework applies a hyperparameter optimization '
                          'for the training procedure. Here, an optimization algorithm tries to find the best hyper '
                          'parameters like hidden channels or amount of graph conv layers. To find the best hyper '
                          'parameter, the training procedure has to be conducted multiple times, so the optimization '
                          'algorithms can analyze how different values of each parameter influences the training '
                          'procedure of the network. More information about hyperparameter optimization at:'
                          'https://optuna.org/')
_parser.add_argument('--training_dataset',
                     dest='training_dataset', default=DataImporter(os.getenv('TRAINING_DATASET_SOURCE'),
                                                                   os.getenv('TRAINING_DATASET_DESTINATION')).shuffle(),
                     help='The training_dataset config holds the training data. The data is converted via the'
                          'DataImporter class into a fitting graph representation and then loaded for training. The'
                          'conversion process takes some time, especially for larger data, but it has to be done only'
                          'once, as long as the data doesnt change. '
                          '(Not used for testing)')
_parser.add_argument('--train_val_partition',
                     dest='train_val_partition', default=3, type=int, #115201
                     help='This variable allows you to separate the training data, taken from the "data -> cad ->'
                          'training" folder, into training and validation datasets. For example, if you have 24000 '
                          'cad models, if you type in value 22000 models, then 22000 models will be utilized for '
                          'training and 2000 models for validation. NOTE: The cad models will be first converted into a'
                          'fitting graph representation and saved into the data -> graph -> training folder.'
                          '(Not used for testing)')
_parser.add_argument('--device',
                     dest='device', default=("cuda" if torch.cuda.is_available() else "cpu"), type=str,
                     help='The device variable defines if the code is run on the gpu or the cpu. If you installed the'
                          'cuda toolkit and the related pytorch and pytorch-geometric packages, then the code should '
                          'run on the gpu. If not, the code automatically will run on the cpu, which will be far '
                          'slower. Please note, that in the requirements1 and 2 files, there are example of '
                          'installations setting, however the necessary python packages vary strongly in regard to'
                          'used operation system, python interpreter, used graphic card and installed cuda toolkit.'
                          'So, it may take some time to find the right setting for you. We suggest, for the first '
                          'implementation, to install the packages manually.')
_parser.add_argument('--max_epoch', dest='max_epoch', default=100, type=int,
                     help='The max epoch defines how often the complete training data is run trough. One epoch means'
                          'therefore, that the graph neural network is fitted ones an all available training data. '
                          'More epochs generally decreases the network loss, but can also lead to overfitting,'
                          'memorizing the training data and not be applicable to new data. We utilized 100 epochs for'
                          'most of our experiments')
_parser.add_argument('--network_model', dest='network_model', default=DgcnNetwork,
                     help='GcNetwork, DgcnNetwork, SageGnNetwork, FeaStNetwork, GATNetwork, GATV2Network, ChebNetwork,'
                          'ArmaNetwork, AgnNetwork')
_parser.add_argument('--network_model_id', dest='network_model_id', default="DgcnNetwork", type=str,
                     help='GcNetwork, DgcnNetwork, SageGnNetwork, FeaStNetwork, GATNetwork, GATV2Network, ChebNetwork,'
                          'ArmaNetwork, AgnNetwork')

if __name__ == '__main__':
    _config = _parser.parse_args()
    print("The training is conducted on: ", _config.device)
    _study = optuna.create_study(direction="maximize", study_name=_config.study_name)

    if _config.application_mode == "training":
        _study.optimize(lambda trial: MachiningFeatureLocalizer(_config, trial).training(trial),
                        n_trials=_config.hyperparameter_trials)
    elif _config.application_mode == "test":
        rest_service_instance = RestService(MachiningFeatureLocalizer(_config, None))
        rest_service_instance.app.run(host="0.0.0.0", port=5001, debug=False)

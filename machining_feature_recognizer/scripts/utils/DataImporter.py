import os
import torch
import numpy as np
from abc import ABC
from stl import mesh
from torch_geometric.data import Data
from torch_geometric.data import InMemoryDataset


class DataImporter(InMemoryDataset, ABC):
    def __init__(self, raw_data_root, root, transform=None):
        self.data_list = []
        self.raw_data_root = raw_data_root
        super().__init__(root, transform)
        self.data, self.slices = torch.load(self.processed_paths[0])

    @property
    def num_node_labels(self) -> int:
        if self.data.x is None:
            return 0
        for i in range(self.data.x.size(1)):
            x = self.data.x[:, i:]
            if ((x == 0) | (x == 1)).all() and (x.sum(dim=1) == 1).all():
                return self.data.x.size(1) - i
        return 0

    @property
    def num_node_attributes(self) -> int:
        if self.data.x is None:
            return 0
        return self.data.x.size(1) - self.num_node_labels

    @property
    def num_edge_labels(self) -> int:
        if self.data.edge_attr is None:
            return 0
        for i in range(self.data.edge_attr.size(1)):
            if self.data.edge_attr[:, i:].sum() == self.data.edge_attr.size(0):
                return self.data.edge_attr.size(1) - i
        return 0

    @property
    def num_edge_attributes(self) -> int:
        if self.data.edge_attr is None:
            return 0
        return self.data.edge_attr.size(1) - self.num_edge_labels

    @property
    def processed_file_names(self):
        return ['mfr_data.pt']  # Ensure this is a list

    @staticmethod
    def cad_graph_conversion(cad_directory, file_labels):
        mesh_object = mesh.Mesh.from_file(cad_directory)

        unique_vectors = np.unique(mesh_object.vectors.reshape([-1, 3]), axis=0)
        unique_vectors_map = {tuple(unique_vector): index for index, unique_vector in enumerate(unique_vectors)}

        edge_index = []
        for facet in mesh_object.vectors:
            index_list = []
            for vector in facet:
                index = unique_vectors_map[tuple(vector)]
                index_list.append(index)
            edge_index.append([index_list[0], index_list[1]])
            edge_index.append([index_list[1], index_list[0]])
            edge_index.append([index_list[1], index_list[2]])
            edge_index.append([index_list[2], index_list[1]])
            edge_index.append([index_list[2], index_list[0]])
            edge_index.append([index_list[0], index_list[2]])

        unique_vectors = unique_vectors / np.array([10, 10, 10])

        label_array = np.zeros(24, dtype=np.float32)
        for label in file_labels:
            label_array[label] = 1

        graph = Data(
            x=torch.tensor(unique_vectors, dtype=torch.float),
            edge_index=torch.tensor(edge_index, dtype=torch.long).t().contiguous(),
            y=torch.tensor(label_array, dtype=torch.float)
        )

        return graph

    def process(self):
        for root, dirs, files in os.walk(self.raw_data_root):
            for file in files:
                file_labels = []
                if file.lower().endswith('_bounding_box_label.csv'):
                    with open(f'{root}/{file}', 'r', encoding='utf-8') as f:
                        for line in f.readlines():
                            file_labels.append(int(line.split(",")[-1]))
                        file_name = str(file).replace('_bounding_box_label.csv', '.stl')
                        self.data_list.append(self.cad_graph_conversion(root + '/' + file_name, file_labels))
                        print(file_name)
        data, slices = self.collate(self.data_list)
        torch.save((data, slices), self.processed_paths[0])  # Save both data and slices

    def __repr__(self) -> str:
        return f'{self.__class__.__name__}({len(self)})'

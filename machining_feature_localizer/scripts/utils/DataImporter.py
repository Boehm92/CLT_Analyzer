import os
import torch
import numpy as np
from stl import mesh
from torch_geometric.data import Data
from torch_geometric.data import InMemoryDataset


class DataImporter(InMemoryDataset):
    def __init__(self, raw_data_root, root, transform=None):
        self.data_list = []
        self.raw_data_root = raw_data_root
        super().__init__(root, transform)
        self.data, self.slices = torch.load(self.processed_paths[0], weights_only=False)

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
        return 'mfs_data.pt'

    @staticmethod
    def cad_graph_conversion(file_path, annotations):
        mesh_object = mesh.Mesh.from_file(file_path)
        unique_vectors = np.unique(mesh_object.vectors.reshape([int(mesh_object.vectors.size / 3), 3]), axis=0)
        unique_vectors_map = {str(unique_vector): index for index, unique_vector in enumerate(unique_vectors)}

        edge_index = []
        for facet in mesh_object.vectors:
            index_list = []
            for vector in facet:
                index = unique_vectors_map[str(vector)]
                index_list.append(index)
            # Add every combination of the three vectors belonging to a face. Both directions are needed.
            edge_index.append([index_list[0], index_list[1]])
            edge_index.append([index_list[1], index_list[0]])
            edge_index.append([index_list[1], index_list[2]])
            edge_index.append([index_list[2], index_list[1]])
            edge_index.append([index_list[2], index_list[0]])
            edge_index.append([index_list[0], index_list[2]])

        unique_vectors = unique_vectors / np.array([20000, 600, 3500])

        if annotations is not None:
            graph = Data(
                x=torch.tensor(unique_vectors).float(),
                edge_index=torch.tensor(edge_index).t().contiguous(),
                y=torch.tensor(annotations),
            )
        else:
            graph = Data(x=torch.tensor(unique_vectors).float(), edge_index=torch.tensor(edge_index).t().contiguous())

        return graph

    def process(self):
        for root, dirs, files in os.walk(self.raw_data_root):
            for file in files:
                file_labels = []

                if file.lower().endswith('_vertices_label.csv'):
                    with open(f'{root}/{file}', 'r', encoding='utf-8') as f:

                        for line in f.readlines():
                            file_labels.append(int(line.split(",")[-1]))

                        file_name = str(file).replace('_vertices_label.csv', '.stl')
                        print(file_name)
                        self.data_list.append(self.cad_graph_conversion(root + '/' + file_name, file_labels))
        torch.save(self.collate(self.data_list), self.processed_paths[0])

    def __repr__(self) -> str:
        return f'{self.name}({len(self)})'

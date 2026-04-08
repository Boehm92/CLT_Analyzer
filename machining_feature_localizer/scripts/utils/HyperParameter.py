class HyperParameter:
    def __init__(self, network_model):
        self.params = {
            "batch_size": 32,
            "dropout_probability": 0.2,
            "learning_rate": 0.001,
        }
        if network_model == "DgcnNetwork":
            self.params.update(
                {
                    "number_conv_layers": 3,
                    "conv_hidden_channels": 128,
                    "mlp_hidden_channels": 128,
                    "aggr": "max",
                }
            )
        else:
            raise ValueError(f"Invalid Network: {network_model}")

        self.__dict__.update(self.params)

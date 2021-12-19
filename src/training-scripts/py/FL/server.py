import flwr as fl

# Start Flower server for three rounds of federated learning
if __name__ == "__main__":
    strategy = fl.server.strategy.FedAvg()

    fl.server.start_server("0.0.0.0:8080", config={"num_rounds": 3}, strategy=strategy)

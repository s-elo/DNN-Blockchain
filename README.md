# Decentralized Neural Network Using Blockchain

## Decentralized Learning Simulation

### 0. Set up

**Requirement:** Python 3.7.11

```bash
# at /python_server
pip install -r requirements.txt

# at /src/training-scripts/py/<project name>
# e.g. /src/training-scripts/py/cirfar10
pip install -r requirements.txt
```

### 1. Build the network using Blockchain

**Run IPFS node:**

You might need to install the [IPFS](https://docs.ipfs.io/install/command-line/#system-requirements) and run a daemon in your simulation server as one of the nodes in IPFS so that you can get the training model faster.

```bash
ipfs daemon
```

**Dataset Preparation:**

Put the training dataset at /src/training-scripts/py/modelName/dataset. Use the names of the classes as the sub-folder name

**Account Preparation:**

Create a file call **privateKey.py** at the /src/training-scripts/py/modelName/ and add the private key of your account in the file. It will be used to send the transaction when imutating the state of the smart contract.

```python
private_key = 'your private key'
```

**Run the training nodes:**

```bash
# Run one node
# at /src/training-scripts/py/<modelName>
# e.g. /src/training-scripts/py/cirfar10
python main.py <port> <data set>
# e.g. python main.py 3600 1
```

- You can run multiple nodes with different **port** and **data set**. The default **port** and **data set** is **3250** and **0** respectively by running

```bash
python main.py
```

- The limited number of the nodes and training rounds can be set by modifying the two variables **NODE_NUM** and **ROUND** in the **main.py**. The default values are **2** nodes and **2** rounds.

### 2. Build the network using a server

Everything is the same as that for **Build the network using Blockchain** except:

**Run a server:** (after running the IPFS daemon)

```bash
# at /python_server
python server.py
```

**Run the training nodes:**

```bash
# at /src/training-scripts/py/<modelName_cen>
# e.g. /src/training-scripts/py/cirfar10_cen
python main.py <port> <data set>
# e.g. python main.py 3600 1
```

## Server for Downloading the Training Scripts

### 0. Set up

**Requirement:** nodeJS v16.13.1; npm 8.1.2

```bash
# at the root /, install all the dependencies
npm install
```

### 1. Run the server

```bash
# at the root /, install all the dependencies
npm run start
```

Then you can download the training scripts via http://localhost:3500/get-scripts/(modelName)-(scriptType)

e.g. http://localhost:3500/get-scripts/cifar10-py

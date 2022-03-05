# Decentralized Neural Network Using Blockchain

## Federated learning + blockchain + ipfs

### **1. Set up**

**Requirement:** Python 3.7.11

```bash
# at /src/training-scripts/py/<project name>
# e.g. /src/training-scripts/py/cirfar10
pip install -r requirements.txt
```

### **2. Account Preparation:**

Since you need to provide the private key to make the transiction, you need to create a file called **accounts.py** at /src/training-scripts/py/[modelName]/ and add your account info

e.g. /src/training-scripts/py/cifar10/accounts.py

```python
# this is for single account simulation without the incentive mechanism
accounts = {
    'address': 'your account address',
    'private_key': 'your account private key'
}

# OR
# for multiple accounts simulation (for each user)
accounts = [
    {
        'address': 'first account address',
        'private_key': 'first account private key'
    },
    {
        'address': 'second account address',
        'private_key': 'second account private key'
    }
]
```

### **3. Dataset Preparation:**

**\*This is not necessary any more, since the data will be loaded using tensorflow API for quick simulation**

Put the training dataset at /src/training-scripts/py/modelName/dataset. Use the names of the classes as the sub-folder name

### **4. Run the training nodes:**

Before running the scripts, you might need to run the **init_fetch.py** first to fetch the model from ipfs. Initially, it might take some time to fetch the model, you need to wait a few minutes and you might need to try this a couple of times. Onece you can fetch the model in a short time, then you can run the training scripts for simulation more quickly.

```bash
# intitial fetching
python init_fetch.py

# Run one node
# at /src/training-scripts/py/<modelName>
# e.g. /src/training-scripts/py/cirfar10
python main.py <port> <dataset(user)>
# e.g. python main.py 3600 1
```

- You can run multiple nodes with different **port** and **data set**. The default **port** and **data set** is **3250** and **0** respectively by just running

```bash
python main.py
```

- The limited number of the nodes and training rounds can be set by modifying the two variables **NODE_NUM** and **ROUND** in the **config.py**.

## Federated learning + central server

### **Set up**

```bash
# if you want to do the simulation using the central sever
# with only the federated learning
# at /python_server
pip install -r requirements.txt
```

Everything is the same as that for **Build the network using Blockchain** except:

### **Run IPFS node:**

You might need to install the [IPFS](https://docs.ipfs.io/install/command-line/#system-requirements) and run a daemon in your simulation server as one of the nodes in IPFS so that you can get the training model faster.

```bash
ipfs daemon
```

### **Run a server:** (after running the IPFS daemon)

```bash
# at /python_server
python server.py
```

### **Run the training nodes:**

```bash
# at /src/training-scripts/py/<modelName_cen>
# e.g. /src/training-scripts/py/cirfar10_cen
python main.py <port> <data set>
# e.g. python main.py 3600 1
```

## Server for Downloading the Training Scripts

### Set up

**Requirement:** nodeJS v16.13.1; npm 8.1.2

```bash
# at the root /, install all the dependencies
npm install
```

### Run the server

```bash
# at the root /, install all the dependencies
npm run start
```

Then you can download the training scripts via http://localhost:3500/get-scripts/(modelName)-(scriptType)

e.g. http://localhost:3500/get-scripts/cifar10-py

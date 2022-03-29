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

- You can run multiple nodes with different **port** and **data set**, but make sure run them in a sequential manner (after fetching the model and adding to the network, then run next node). The default **port** and **data set** is **3250** and **0** respectively by just running

```bash
python main.py
```

- The limited number of the nodes and training rounds can be set by modifying the two variables **NODE_NUM** and **ROUND** in the **config.py**.

## Simulation on different applications (models)

If you want to try simulation on differnt models, you can do some changes based on the cifar10 training scripts **/src/training-scripts/py/cirfar10**

### **1. Deploy model**

Firstly we need to deploy the new model **(only for tensorflow models)** on the ipfs.
at /src/ipfs_deploy/ create a new model folder just like **/src/ipfs_deploy/cifar10** which is able to generate the model.json file corresponding to the new model.

After getting the model.json file:

```bash
npm run deploy [new model name(the folder name)]
```

### **2. Add the model hash to blockchain**

After deployment, we should be able to get the hash of the model at /src/ipfs_deploy/deploy_hash.json (the last one), then you need to add this hash to the blockchain by updating the smart contract state
using the explorer [here](https://ropsten.etherscan.io/address/0xecc03bcae3944ff618787c209d64f8f5cfee1456#writeContract). We should be able to use the **addNewModel** function and add the hash with the model name. The testset_hash can just be any string since we dont get the testset from ipfs for simulation.

### **3. Change the dataHandler.py**

After the above deployment, you need to customize how to get your training dataset as what the original cifar10 model does at **/src/training-scripts/py/cirfar10/dataHandler.py**. You can choose to load the dataset using tf API or download the dataset manually.

### **4. Change the train.py**

The train.py at **/src/training-scripts/py/cirfar10/train.py** determines how to compile and optimize the fetched model from ipfs and model evalation which can be also customized.

### **5. Change the config.py**

The config.py at **/src/training-scripts/py/cirfar10/config.py** is used to set some simulation parameters, at this point, the must-do change is the MODEL_NAME param to the name of your new deployed model and feel free to try other different params.

After that, you should be able to do the simulation using the new application.

## Accuracy simulation

At the /acc_simul, you can simulate the model using normal training and federated learning

```bash
# at /acc_simul/[model name]

# normal training
python model_simul.py

# federated learning
python fl_simul.py
```

## Federated learning + central server

**(This might be inconsistent and some issues)**

### **1. Set up**

```bash
# if you want to do the simulation using the central sever
# with only the federated learning
# at /python_server
pip install -r requirements.txt
```

Everything is the same as that for **Build the network using Blockchain** except:

### **2. Run IPFS node:**

You might need to install the [IPFS](https://docs.ipfs.io/install/command-line/#system-requirements) and run a daemon in your simulation server as one of the nodes in IPFS so that you can get the training model faster.

```bash
ipfs daemon
```

### **3. Run a server:** (after running the IPFS daemon)

```bash
# at /python_server
python server.py
```

### **4. Run the training nodes:**

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

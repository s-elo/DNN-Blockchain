pragma solidity >=0.4.21 <0.7.0;

pragma experimental ABIEncoderV2;

// SPDX-License-Identifier: MIT
contract PureDnn {
    struct Model {
        // the model params hash stored in IPFS
        string model_hash;
        // the testset hash stored in IPFS
        string testset_hash;
        // current accuracy
        string accuracy;
        // used to build up the distributed training network
        string[] nodes;
        // to determine if it is added
        bool isAdded;
    }

    struct ModelInfo {
        // the model params hash stored in IPFS
        string model_hash;
        // the testset hash stored in IPFS
        string testset_hash;
        // current accuracy
        string accuracy;
    }

    // indice according to the model name
    mapping(string => Model) public models;

    // maximum 10 nodes
    uint256 max_node_num = 10;

    function addNewModel(
        string memory modelName,
        string memory model_hash,
        string memory testset_hash,
        string memory accuracy
    ) public {
        // if the model doesnt exist
        if (models[modelName].isAdded == false) {
            string[] memory initNodes;

            models[modelName] = Model({
                model_hash: model_hash,
                testset_hash: testset_hash,
                accuracy: accuracy,
                nodes: initNodes,
                isAdded: true
            });
        }
    }

    function addNode(string memory modelName, string memory node) public {
        if (models[modelName].nodes.length < max_node_num) {
            models[modelName].nodes.push(node);
        }
    }

    // only return the model_hash, testset_hash and accuracy
    function getModelInfo(string memory modelName)
        public
        view
        returns (ModelInfo memory)
    {
        Model memory queryModel = models[modelName];

        return
            ModelInfo({
                model_hash: queryModel.model_hash,
                testset_hash: queryModel.testset_hash,
                accuracy: queryModel.accuracy
            });
    }

    function getModelHash(string memory modelName)
        public
        view
        returns (string memory)
    {
        return models[modelName].model_hash;
    }

    function getTestsetHash(string memory modelName)
        public
        view
        returns (string memory)
    {
        return models[modelName].testset_hash;
    }

    function getNodes(string memory modelName)
        public
        view
        returns (string[] memory)
    {
        return models[modelName].nodes;
    }

    function clearNodes(string memory modelName) public {
        delete models[modelName].nodes;
    }

    function updateModel(string memory modelName, string memory model_hash)
        public
    {
        models[modelName].model_hash = model_hash;
    }

    function updateTestset(string memory modelName, string memory testset_hash)
        public
    {
        models[modelName].testset_hash = testset_hash;
    }
}

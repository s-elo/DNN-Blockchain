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
        // the number of current joined node
        uint256 node_num;
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
        models[modelName] = Model({
            model_hash: model_hash,
            testset_hash: testset_hash,
            accuracy: accuracy,
            nodes: new string[](max_node_num),
            node_num: 0
        });
    }

    function addNode(string memory modelName, string memory node) public {
        Model memory queryModel = models[modelName];
        uint256 node_num = queryModel.node_num;

        // just append to the nodes list
        if (node_num < max_node_num) {
            models[modelName].nodes[node_num] = node;
            models[modelName].node_num = node_num + 1;
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

    function getNodes(string memory modelName)
        public
        view
        returns (string[] memory)
    {
        Model memory queryModel = models[modelName];

        // create a new array according to the current number of nodes
        string[] memory ret = new string[](queryModel.node_num);
        for (uint256 i = 0; i < queryModel.node_num; i++) {
            ret[i] = queryModel.nodes[i];
        }

        return ret;
    }

    function clearNodes(string memory modelName) public {
        // just set the node_num as 0
        models[modelName].node_num = 0;
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

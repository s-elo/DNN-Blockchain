pragma solidity >=0.4.21 <0.7.0;

pragma experimental ABIEncoderV2;

// SPDX-License-Identifier: MIT
contract Dnn {
    struct Model {
        // the model params hash stored in IPFS
        string ipfs_hash;
        // the testset hash stored in IPFS
        string testset_hash;
        // current accuracy
        string accuracy;
        // used to build up the distributed training network
        string[] nodes;
        // the number of current joined node
        uint256 node_num;
        // required number of training nodes
        uint256 total_nodes;
    }

    struct ModelInfo {
        // the model params hash stored in IPFS
        string ipfs_hash;
        // the testset hash stored in IPFS
        string testset_hash;
        // current accuracy
        string accuracy;
    }

    // indice according to the model name
    mapping(string => Model) public models;

    function addNewModel(
        string memory modelName,
        string memory ipfs_hash,
        string memory testset_hash,
        string memory accuracy,
        uint256 total_nodes
    ) public {
        models[modelName] = Model({
            ipfs_hash: ipfs_hash,
            testset_hash: testset_hash,
            accuracy: accuracy,
            nodes: new string[](total_nodes),
            total_nodes: total_nodes,
            node_num: 0
        });
    }

    function addNode(string memory modelName, string memory node) public {
        Model memory queryModel = models[modelName];
        uint256 node_num = queryModel.node_num;
        uint256 total_nodes = queryModel.total_nodes;

        if (node_num < total_nodes) {
            models[modelName].nodes[node_num - 1] = node;
            models[modelName].node_num = node_num + 1;
        }
    }

    // only return the ipfs_hash, testset_hash and accuracy
    function getModelInfo(string memory modelName)
        public
        view
        returns (ModelInfo memory)
    {
        Model memory queryModel = models[modelName];

        return
            ModelInfo({
                ipfs_hash: queryModel.ipfs_hash,
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
        delete models[modelName].nodes;
    }
}

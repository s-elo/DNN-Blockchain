pragma solidity >=0.4.21 <0.7.0;

pragma experimental ABIEncoderV2;

// SPDX-License-Identifier: MIT
contract IpArray {
    string[] nodes = ['first ip'];

    function addNode(string memory ipAddress) public returns (string[] memory) {
        nodes.push(ipAddress);

        return nodes;
    }

    function getNodes() public view returns (string[] memory) {
        return nodes;
    }

    function clearNodes() public {
        delete nodes;
    }
}

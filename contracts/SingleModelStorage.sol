// SPDX-License-Identifier: MIT
pragma solidity >=0.4.21 <0.7.0;

contract SingleModelStorage {
    string model;

    function set(string memory new_model) public {
        model = new_model;
    }

    function get() public view returns (string memory) {
        return model;
    }
}

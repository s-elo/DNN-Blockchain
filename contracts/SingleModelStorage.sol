// SPDX-License-Identifier: MIT
pragma solidity >=0.4.21 <0.7.0;

pragma experimental ABIEncoderV2;

contract SingleModelStorage {
    string model;

    mapping(uint256 => uint8) public model_map;

    function initModel(uint8 len) public {
        // model = bytes(new string(len));
        // model = new string(len);
    }

    function set(string memory new_model, uint256 batch) public {
        model = string(concat(model, new_model));
        // bytes memory new_model_byte = bytes(new_model);
        // for (uint256 i = 0; i < new_model_byte.length; i++) {
        //     // model[start++] = new_model[i];
        //     uint256 idx = batch * 1000 + i;

        //     model[idx] = new_model_byte[i];
        // }
    }

    function setMap(uint8[] memory new_model, uint256 batch) public {
        for (uint256 i = 0; i < new_model.length; i++) {
            // model[start++] = new_model[i];
            uint256 idx = batch * 500 + i;

            model_map[idx] = new_model[i];
        }
    }

    function get() public view returns (string memory) {
        return string(model);
    }

    function getMap() public view returns (uint8[] memory) {
        uint256 len = 12719;

        uint8[] memory ret = new uint8[](len);

        for (uint256 i = 0; i < len; i++) {
            ret[i] = model_map[i];
        }

        return ret;
    }

    function concat(string memory s1, string memory s2)
        public
        pure
        returns (bytes memory)
    {
        bytes memory s1_byte = bytes(s1);
        bytes memory s2_byte = bytes(s2);

        string memory concat_str = new string(s1_byte.length + s2_byte.length);

        bytes memory bytes_concat_str = bytes(concat_str);

        uint256 k = 0;

        for (uint256 i = 0; i < s1_byte.length; i++) {
            bytes_concat_str[k++] = s1_byte[i];
        }

        for (uint256 i = 0; i < s2_byte.length; i++) {
            bytes_concat_str[k++] = s2_byte[i];
        }

        return bytes_concat_str;
    }
}

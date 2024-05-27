// SPDX-License-Identifier: UNLICENSED
pragma solidity 0.8.20;

contract GasUsageTest {

    // Private variables, this are saved in storage
    uint private storedData;

    // Function that writes in storage
    function set(uint x) public {
        storedData = x;
    }

    // Function that does only changes in the stack
    function nothing() public pure {
        uint example = 100;
        example = 0;
    }

    // Function that calculates power of 2 
    function powerOfTwo(uint x) public pure returns (uint) {
        uint sum = 1;
        for (uint i = 0; i < x; i++) 
        {
            sum += sum;
        }

        return sum;
    }

    // Function that depends on the length of the params
    function paramLength(uint[] memory list) public pure returns (uint) {
        return list.length;
    }

}

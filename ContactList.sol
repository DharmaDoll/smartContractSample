// SPDX-License-Identifier: MIT
pragma solidity 0.8.18;

contract ContactList {
    uint256 phoneNumber;

    struct Contact {
        // assosiate name with phone number
        string name;
        string phoneNumber;
    }

    Contact[] public contact; //array for list of contacts

    //used to map name to phone number, so you can get phone number using name
    mapping(string => string) public nameToPhoneNumber;


    //retrieve tuple of all contacts
    function retrieve() public view returns (Contact[] memory) {
        return contact;
    }

    function addContact(
        string memory _name,
        string memory _phoneNumber
    ) public {
        contact.push(Contact(_name, _phoneNumber)); //append to  Contact[] array
        nameToPhoneNumber[_name] = _phoneNumber; //use name to get phone number
    }
}
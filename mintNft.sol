pragma solidity 0.8.18;
import "@openzeppelin/contracts/token/ERC721/ERC721.sol";
//OpenZeppelinが提供するヘルパー機能をインポートします。
import "@openzeppelin/contracts/utils/Counters.sol";
import "@openzeppelin/contracts/utils/Base64.sol";

// import "hardhat/console.sol";


contract Web3Mint is ERC721{
    address public owner;
    struct NftAttributes{
        string name;
        string description;
        string imageURL;
    }

    NftAttributes[] Web3Nfts;

    using Counters for Counters.Counter;
    // tokenIdはNFTの一意な識別子で、0, 1, 2, .. N のように付与されます。
    Counters.Counter private _tokenIds;

    constructor() ERC721("NFT","xnft"){
        // console.log("This is my NFT contract.");
        owner = msg.sender;
    }

    // ユーザーが NFT を取得するために実行する関数です。
    function mintIpfsNFT(
            string memory name,
            string memory description,
            string memory imageURI
     ) public{
        uint256 newItemId = _tokenIds.current();
        _safeMint(msg.sender, newItemId);
        
        Web3Nfts.push(NftAttributes({
            name: name,
            description: description,
            imageURL: imageURI
        }));

        // console.log("An NFT w/ ID %s has been minted to %s", newItemId, msg.sender);
        _tokenIds.increment();
    }

    function tokenURI(uint256 _tokenId) public override view returns(string memory){
        string memory json = Base64.encode(
            bytes(
                string(
                    abi.encodePacked(
                        '{"name": "',
                        Web3Nfts[_tokenId].name,
                        ' -- NFT #: ',
                        Strings.toString(_tokenId),
                        '", "description": "An epic NFT", "image": "ipfs://',
                        Web3Nfts[_tokenId].imageURL,'"}'
                    )
                )
            )
        );
        string memory output = string(
            abi.encodePacked("data:application/json;base64,", json)
        );
        return output;
    }
}

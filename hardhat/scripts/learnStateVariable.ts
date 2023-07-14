import { ethers } from "ethers";
import erc20Artifact from '../artifacts/contracts/ERC20.sol/ERC20.json';
import * as dotenv from 'dotenv';
dotenv.config();

async function main(){
    const rpcUrl: string = process.env.SEPOLIA_URL ?? "";
    if (rpcUrl === "") {
        throw new Error('No value set for environement variable SEPOLIA_URL');
    }

    const provider = new ethers.providers.JsonRpcProvider(rpcUrl);
    const contractAddress = "0xc20332742Ad07694805979A2530d66BE707233d4";  // ZNY contract
    const contract = new ethers.Contract(contractAddress, erc20Artifact.abi, provider);

    for (let n of Array.from(Array(10).keys())) {
        const ret = await provider.getStorageAt(contractAddress, n)
        console.log(n, ret)
    }

    // totalSupply
    console.log('totalSupply:', (await contract.totalSupply()).toString())
    const hex0 = await provider.getStorageAt(contractAddress, 0)
    console.log(typeof hex0)
    console.log('totalSupply from storage:', BigInt(hex0))

    // name
    const hex1 = await provider.getStorageAt(contractAddress, 1)
    const length1 = parseInt(hex1.slice(-2), 16)
    const encoded1 = hex1.slice(0, 2 + length1)
    console.log('name from storage:', ethers.utils.toUtf8String(encoded1))

    // decimals and owner
    const hex3 = await provider.getStorageAt(contractAddress, 3)
    const bytesDecimals = hex3.slice(-2)
    const bytesOwner = hex3.slice(-42, -2)
    console.log('decimals from storage:', parseInt(bytesDecimals, 16))
    console.log('owner address from storage:', bytesOwner)

    // balances
    const owner = "8e99dbcb82bdfff516531a326ca54d993af51273"
    console.log('balance of owner account:', (await contract.balanceOf(`0x${owner}`)).toString())
    const key = `000000000000000000000000${owner}`  // 24 + 40 = 64 chars
    const slot4 = `0000000000000000000000000000000000000000000000000000000000000004` // 64 chars
    const hash = ethers.utils.keccak256('0x' + key + slot4)
    const hexKey = await provider.getStorageAt(contractAddress, hash)
    console.log('balance of account from storage:', BigInt(hexKey))

    // allowance
    const owner_ = "8e99dbcb82bdfff516531a326ca54d993af51273"
    const spender = "ee65d21d6d251c48bc7b7e81d672ad8d1dc6e98e"
    console.log('allowance:', (await contract.allowance(`0x${owner_}`, `0x${spender}`)).toString())
    const key1 = `000000000000000000000000${owner_}`
    const key2 = `000000000000000000000000${spender}`
    const slot5 = '0000000000000000000000000000000000000000000000000000000000000005'
    const hasha = ethers.utils.keccak256( '0x' + key2 + ethers.utils.keccak256('0x' + key1 + slot5).slice(2) );
    const hexKeya = await provider.getStorageAt(contractAddress, hasha)
    console.log('allowance from storage:', BigInt(hexKeya))  
}

main().catch((error) => {
    console.error(error);
    process.exitCode = 1
});
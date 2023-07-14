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
    
    // 1. Call view function (balanceOf)
    const owner = "8e99dbcb82bdfff516531a326ca54d993af51273"
    console.log('balance by normal call:', (await contract.balanceOf(`0x${owner}`)).toString())

    const signature = "balanceOf(address)"
    const signatureHash = ethers.utils.id(signature)  // signatureHash = ethers.utils.keccak256(ethers.utils.toUtf8Bytes(signature))
    console.log('signatureHash:', signatureHash)
    const selector = signatureHash.slice(2, 10)
    console.log('function selector:', selector)
    const data = '0x' + selector + '000000000000000000000000' + owner
    console.log('data:', data)
    const ret = await provider.send("eth_call", [{"to": contractAddress, "data": data}, "latest"])
    console.log('return string:', ret)
    console.log('balance by signatureHash:', BigInt(ret))

    // 2. Call write function (transfer)
    const recipient = 'ee65d21d6d251c48bc7b7e81d672ad8d1dc6e98e'
    const amount = '0000000000000000000000000000000000000000000000000000000000abcdef'  // 64 chars
    const tx = await contract.populateTransaction.transfer(`0x${recipient}`, `0x${amount}`)
    console.log('transaction:', tx)

    const signature2 = "transfer(address,uint256)"
    const signatureHash2 = ethers.utils.id(signature2)
    const selector2 = signatureHash2.slice(2, 10)
    const data2 = '0x' + selector2 + '000000000000000000000000' + recipient + amount
    console.log('tx.data is selector + args:', data2 === tx.data)
}

main().catch((error) => {
    console.error(error);
    process.exitCode = 1;
});
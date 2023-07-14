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

    // Event hash
    console.log('Transfer Event Hash:', ethers.utils.id("Transfer(address,address,uint256)"))
    // 0xddf252ad1be2c89b69c2b068fc378daa952ba7f163c4a11628f55a4df523b3ef
    console.log('Approval Event Hash:', ethers.utils.id("Approval(address,address,uint256)"))
    // 0x8c5be1e5ebec7d5bd14f71427d1e84f3dd0314c0f7b2291e5b200ac8c7c3b925

    // Get events
    const eventList = await provider.getLogs({
        fromBlock: 2000000,
        toBlock: 'latest',
        address: contractAddress,
        topics: ["0xddf252ad1be2c89b69c2b068fc378daa952ba7f163c4a11628f55a4df523b3ef", "0x0000000000000000000000000000000000000000000000000000000000000000"]
    })
    console.log(eventList)
}

main().catch((error) => {
    console.error(error);
    process.exitCode = 1;
});
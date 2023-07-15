## Prepare js runtime environment
```sh
curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.3/install.sh | bash
nvm install 18.12.1
node --version
npm --version
```

## install packages
```sh
npm i --save-dev
```

## Compile contract
```sh
npx hardhat compile
```

## Test contract
```sh
npx hardhat test
```


## Deploy ERC20 Token Contract to Test network(sepolia)

### Prepare .env file
```sh
#Test network url(API Key) and Your(Deploy owner) private key(With sepoliaETH in it)
cat <<EOF >.env
SEPOLIA_URL="https://sepolia.infura.io/v3/<API-KEY>"
PRIVATE_KEY="0xac0974bec39a17e36ba4a6b4d238ff944bacb478cbed5efcae784d7bf4f2ff80"
EOF
```
### Sepolia PoW Faucet
- https://sepolia-faucet.pk910.de/  
- https://faucet.sepolia.dev/

### Deploy contract
```sh
npx ts-node scripts/deploy.ts --name Mytoken --symbol MTK --decimals 18

ERC20 contract deploy address 0xb8ec...snip...
Transaction URL: https://sepolia.etherscan.io/tx/0x8xxxxxxxxxx...snip...xxxxxxxxx
Deploy completed
```

### Mint a token to the specified address
```sh
npx ts-node scripts/mint.ts --network sepolia --contractAddress "0xb8ec...snip..." --accountAddress "0x11..<recipient address>.." --amount 1.23

Transaction URL: https://sepolia.etherscan.io/tx/0xaxxxxxxxxxxx...snip...xxxxxxxxxx
completed
Event Name: Transfer
      Args: 0x0000000000000000000000000000000000000000,0x11...snip...,1230000000000000000
```


## Sample Hardhat Project

This project demonstrates a basic Hardhat use case. It comes with a sample contract, a test for that contract, and a script that deploys that contract.

Try running some of the following tasks:

```shell
npx hardhat help
npx hardhat test
REPORT_GAS=true npx hardhat test
npx hardhat node
npx hardhat run scripts/deploy.ts
```

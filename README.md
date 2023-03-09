# smartContractSample

## Prerequirements
### Install solc and web3.py
```sh
pip install py-solc-x web3
```

### Install Geth
```sh
# For Linux(Ubuntu)
sudo add-apt-repository -y ppa:ethereum/ethereum
sudo apt-get update
sudo apt-get install -y ethereum

# For MacOS
brew update
brew upgrade
brew reinstall ethereum
``` 
### Initializing the Geth Database
```sh
mkdir data_privatenet 
geth --datadir data_privatenet init genesis.json
```

### Run Geth 
```sh
geth --networkid 4649 --nodiscover --maxpeers 0 --datadir data_privatenet -- console 2>> data_privatenet/geth.log

# Required for Geth/v1.11.4-unstable-e14043db-20230308/linux-amd64/go1.19.1
# geth --networkid 4649 --nodiscover --maxpeers 0 --rpc.enabledeprecatedpersonal --datadir data_privatenet -- console 2>> data_privatenet/geth.log
```

### Account creation and mining on geth console
```js
personal.newAccount('a')
// Required for Linux only?
//miner.setEtherbase(eth.accounts[0])
miner.start(1)
eth.blockNumber
miner.stop()
```

## Compile .sol file and Deploy to private net
```sh
./deploy.py data_privatenet/geth.ipc
```




### Using Docker
TBC
```sh
# mkdir data_privatenet

# # Install and run docker
# docker pull ethereum/client-go
# docker run --entrypoint="/bin/sh" --rm -it --name ethereum-node -v ${PWD}:/geth ethereum/client-go

# # In Docker

# # Init the Geth Database
# geth --datadir geth/data_privatenet init geth/genesis.json

# # Run Geth(Using http server)
# geth --networkid 4649 --nodiscover --ipcdisable --maxpeers 0 --http --http.addr "localhost" --http.port "8545" --http.api "eth,net,web3,personal" --http.corsdomain "*" --rpc.enabledeprecatedpersonal --datadir geth/data_privatenet console 2>> geth/data_privatenet/geth.log
```
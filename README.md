# smartContractSample

## Prerequirements

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
# For Docker
docker pull ethereum/client-go
``` 
### Initializing the Geth Database
```sh
mkdir data_privatenet && cd data_privatenet
geth --datadir data_privatenet init data_privatenet/genesis.json

# For docker
docker run -it -p 30303:30303 ethereum/client-go <options> ...
```

### Run Geth 
```sh
geth --networkid 4649 --nodiscover --maxpeers 0 --datadir data_privatenet console 2>> data_privatenet/geth.log

# For docker
docker run -it -p 30303:30303 ethereum/client-go <options> ...
```

### Compile .sol file and Deploy 
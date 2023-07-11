from web3 import Web3

# gethのデフォだとうまくいかない
# ipc_path = 'data_privatenet/geth.ipc'
# web3 = Web3(Web3.IPCProvider(ipc_path))

ganache_url = "http://127.0.0.1:8545"
web3 = Web3(Web3.HTTPProvider(ganache_url))
account_1 = '0xAe9593871D59...' # Fill me in
account_2 = '0x2Bc6D8Cbf5b8...' # Fill me in
private_key = '0xe701d33f6577125db638899a2c616f7b53227d4718f6577c7e6144160bd2ead0' # Fill me in

nonce = web3.eth.getTransactionCount(account_1)

tx = {
    'nonce': nonce,
    'to': account_2,
    'value': web3.toWei(1, 'ether'),
    'gas': 2000000,
    'gasPrice': web3.toWei('50', 'gwei'),
}

signed_tx = web3.eth.account.signTransaction(tx, private_key)

tx_hash = web3.eth.sendRawTransaction(signed_tx.rawTransaction)

print(web3.toHex(tx_hash))

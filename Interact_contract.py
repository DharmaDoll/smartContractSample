#! /usr/bin/env python

# Refere to https://coinsbench.com/how-to-deploy-and-interact-with-solidity-contracts-with-python-and-ganache-be63334323e6
# https://k2k2-ethereum.com/programming/python/273/

import sys,os
import json
import re
    
from solcx import compile_standard, install_solc_pragma, compile_source
from web3 import Web3

if len(sys.argv) < 3:
	print(f'''usage: {os.path.basename(__file__)} <ipc path> <contract address> <abi> <called function> <param(dict)>
     ex.  {os.path.basename(__file__)} ./data_privatenet/geth.ipc
     
     Gethを起動しておき、そのipcのファイルを指定する
     Geth networkのアカウントリストの最初のアカウント情報を使う(eth.accounts[0]) passphraseは'a'
''')
	sys.exit()


ipc_path = sys.argv[1]
contract_address = sys.argv[2]
try:
    abi: str = sys.argv[3]
    # abi: dict = json.loads(sys.argv[3])
except Exception:
     print('Parse error. abi cloud not loaded')
     sys.exit(1)
# called_function = sys.argv[4]
# param: dict = {}

passphrase = 'a'

def get_eoa_address_and_private_key(w3) -> tuple:
    eoa_address = w3.geth.personal.list_wallets()[0].accounts[0].address
    keystore_path = w3.geth.personal.list_wallets()[0].accounts[0].url
    with open(re.sub('^keystore://', '', keystore_path, 1), 'r') as f:
        keystore_file =f.read()
    private_key = w3.eth.account.decrypt(keystore_file, passphrase)

    return eoa_address, private_key


#コントラクトに連絡先を追加する
def _addContact(contract_address, abi, number: str, eoa_address, nonce):
    contact_list = w3.eth.contract(address=contract_address, abi=abi)
    # store_contact = contact_list.functions.addContact("name", "+2348112398610").buildTransaction(
    store_contact = contact_list.functions.addContact("name", number).buildTransaction(
        {
            "chainId": w3.eth.chain_id, 
            "from": eoa_address, 
            "gasPrice": w3.eth.gas_price, 
            "nonce": nonce
        }
    )
    # Sign the transaction
    sign_store_contact = w3.eth.account.sign_transaction(store_contact, private_key=private_key)

    # Send the transaction
    send_store_contact = w3.eth.send_raw_transaction(sign_store_contact.rawTransaction)
    tx_receipt = w3.eth.wait_for_transaction_receipt(send_store_contact)

    return contact_list, tx_receipt

if __name__ == '__main__':
    
    ######## Connect Blockchain ############
    w3 = Web3(Web3.IPCProvider(ipc_path))
    eoa_address, private_key = get_eoa_address_and_private_key(w3)
    nonce: int = w3.eth.getTransactionCount(eoa_address)

    print(f'nonce: {nonce}')
    ########## Interacting with the Contract ##############


    input('''# ここでもtxを発行して送信するので、eth.pendingTransactions で確認すると未だ取り込まれてないtxが確認できる
  # ここでもminer.start()が必要になる.続けるにはEnterを押下\n''')
    #コントラクトを操作しようとするときは、コントラクトアドレスとコントラクトABI が必要
    contact_list, tx_receipt = _addContact(contract_address, abi, '+0123456789', eoa_address, nonce)
    print(f'[+] Get Block Number: {w3.eth.blockNumber}')

    #連絡先を取得する
    print(f'[+] retrieve関数を呼びましたよ！\n', contact_list.functions.retrieve().call())

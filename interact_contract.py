#! /usr/bin/env python

# Refere to https://coinsbench.com/how-to-deploy-and-interact-with-solidity-contracts-with-python-and-ganache-be63334323e6
# https://k2k2-ethereum.com/programming/python/273/

import sys,os
import json
import re
    
from solcx import compile_standard, install_solc_pragma, compile_source
from web3 import Web3

if len(sys.argv) < 6:
	print(f'''usage: {os.path.basename(__file__)} <ipc path> <contract address> <abi> <called function> <write/readOnly> <param(dict)>
     ex.  {os.path.basename(__file__)} ./data_privatenet/geth.ipc
     
     Gethを起動しておき、そのipcのファイルを指定する
     Geth networkのアカウントリストの最初のアカウント情報を使う(eth.accounts[0]) passphraseは'a'
''')
	sys.exit()


ipc_path = sys.argv[1]
contract_address = sys.argv[2]
try:
    abi: str = sys.argv[3]
except Exception:
     print('Parse error. abi cloud not loaded')
     sys.exit(1)
called_function_name = sys.argv[4]
read_only = sys.argv[5]
param: dict = sys.argv[6]

passphrase = 'a'

def get_eoa_address_and_private_key(w3) -> tuple:
    eoa_address = w3.geth.personal.list_wallets()[0].accounts[0].address
    keystore_path = w3.geth.personal.list_wallets()[0].accounts[0].url
    with open(re.sub('^keystore://', '', keystore_path, 1), 'r') as f:
        keystore_file =f.read()
    private_key = w3.eth.account.decrypt(keystore_file, passphrase)

    return eoa_address, private_key


if __name__ == '__main__':
    ######## Connect Blockchain ############
    w3 = Web3(Web3.IPCProvider(ipc_path))
    eoa_address, private_key = get_eoa_address_and_private_key(w3)
    nonce: int = w3.eth.getTransactionCount(eoa_address)

    print(f'nonce: {nonce}')


    ########## Interacting with the Contract ##############
    print('''# ここでもtxを発行して送信するので、eth.pendingTransactions で確認すると未だ取り込まれてないtxが確認できる
  # ここでもminer.start()が必要になる。\n''')
    #コントラクトを操作しようとするときは、コントラクトアドレスとコントラクトABI が必要
    contract = w3.eth.contract(address=contract_address, abi=abi)
    # contact_list, tx_receipt = _addContact(contract_address, abi, '+0123456789', eoa_address, nonce)

    called_function = contract.functions.__getattribute__(called_function_name)


    #read onlyの関数を呼ぶ
    if read_only == 'readonly':
        #連絡先を取得する
        print(f'[+] retrieve関数を呼びましたよ！\n', called_function().call())
        # print(f'[+] retrieve関数を呼びましたよ！\n', contract.functions.retrieve().call())
    else:
    #txを送信する場合
        # store_contact = contract.functions.addContact("name", '+0123456789').buildTransaction(
        contract_tx = called_function("name", '+0123456789').buildTransaction(
            {
                "chainId": w3.eth.chain_id, 
                "from": eoa_address, 
                "gasPrice": w3.eth.gas_price, 
                "nonce": nonce
            }
        )

        # Sign the transaction
        sign_contract_tx = w3.eth.account.sign_transaction(contract_tx, private_key=private_key)
        # Send the transaction
        send_contract_tx = w3.eth.send_raw_transaction(sign_contract_tx.rawTransaction)
        tx_receipt = w3.eth.wait_for_transaction_receipt(send_contract_tx)
    
    print(f'[+] Get Block Number: {w3.eth.blockNumber}')



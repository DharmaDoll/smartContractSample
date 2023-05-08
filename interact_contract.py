#! /usr/bin/env python

import sys,os
import re
import json

from web3 import Web3

if len(sys.argv) < 7:
	print(f'''usage: {os.path.basename(__file__)} <ipc path> <contract address> <abi file> <called function> <w/r> <param('a,b,c...')>
     ex.  {os.path.basename(__file__)} ./data_privatenet/geth.ipc '0x54f...' ./abi.json addContact w 'name,+1234...'
     
     Gethを起動しておき、そのipcのファイルを指定する
     Geth networkのアカウントリストの最初のアカウント情報を使う(eth.accounts[0]) passphraseは'a'
''')
	sys.exit()


ipc_path = sys.argv[1]
contract_address = sys.argv[2]
try:
    with open(sys.argv[3],'r') as f:
        abi: str = json.loads(f.read())
except Exception:
     print('Parse error. abi cloud not loaded')
     sys.exit(1)
called_function_name = sys.argv[4]
tx_type = sys.argv[5]
param: list = sys.argv[6].split(',')

passphrase = 'a'

def get_eoa_address_and_private_key(w3) -> tuple:
    eoa_address = w3.geth.personal.list_wallets()[0].accounts[0].address
    keystore_path = w3.geth.personal.list_wallets()[0].accounts[0].url
    with open(re.sub('^keystore://', '', keystore_path, 1), 'r') as f:
        keystore_file =f.read()
    private_key = w3.eth.account.decrypt(keystore_file, passphrase)

    return eoa_address, private_key

# def non_tx_function():
#     pass
# def tx_function():
#     pass

if __name__ == '__main__':
    ######## Connect Blockchain ############
    w3 = Web3(Web3.IPCProvider(ipc_path))
    eoa_address, private_key = get_eoa_address_and_private_key(w3)
    nonce: int = w3.eth.getTransactionCount(eoa_address)

    print(f'nonce: {nonce}')


    ########## Interacting with the Contract ##############
    #コントラクトを操作しようとするときは、コントラクトアドレスとコントラクトABI が必要
    contract = w3.eth.contract(address=contract_address, abi=abi)
    called_function = contract.functions.__getattribute__(called_function_name)

    #txを発行しないread onlyの関数を呼ぶ
    if tx_type == 'r':
    #連絡先を取得する
        print(f'[+] {called_function.fn_name}関数を呼びますよ！\n', called_function().call())
        # print(f'[+] retrieve関数を呼びましたよ！\n', contract.functions.retrieve().call())
    else:
    #txを送信する場合
        print(f'[+] {called_function.fn_name}関数を呼びますよ！\n')
        # store_contact = contract.functions.addContact("name", '+0123456789').buildTransaction(
        # contract_tx = called_function(*["name", '+0123456789']).buildTransaction(
        contract_tx = called_function(*param).buildTransaction(
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
        send_contract_tx_hash = w3.eth.send_raw_transaction(sign_contract_tx.rawTransaction)
        print(f'tx_hash is: {send_contract_tx_hash.hex()}')
        print(f'Sample commands to check.. -> `eth.getTransaction("{send_contract_tx_hash.hex()}")`\n')
        print('''# ここでもtxを発行して送信するので、eth.pendingTransactions で確認すると未だ取り込まれてないtxが確認できる
# ここでもminer.start()が必要になる。\n''')
        tx_receipt = w3.eth.wait_for_transaction_receipt(send_contract_tx_hash)
    
    print(f'[+] Get Block Number: {w3.eth.blockNumber}')

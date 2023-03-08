#! /usr/bin/env python

# Refere to https://coinsbench.com/how-to-deploy-and-interact-with-solidity-contracts-with-python-and-ganache-be63334323e6
# https://k2k2-ethereum.com/programming/python/273/

import sys,os
import json
import re
    
from solcx import compile_standard, install_solc
from web3 import Web3


if len(sys.argv) != 2:
	print(f'''usage: {os.path.basename(__file__)} <ipc path>
     ex.  {os.path.basename(__file__)} ~/sandbox/pywork/gethdegeth/data_privatenet/geth.ipc
     
     Gethを起動しておき、そのipcのファイルを指定する
     Geth networkのアカウントリストの最初のアカウント情報を使う(eth.accounts[0])
     miningが基本止めた状態でGethを起動し、適宜txが送信された時にminer.start/stopで動きを見てみる
     pip install py-solc-x web3 もやっておこう
     compilerのinstallは事前にinstall_solc()でinstallしておこう
     使うcontractは`./ContactList.sol`をcompileしてデプロイするよ.compiled_code.jsonとして./に保存するよ。
     　→code末尾にコードを置いてるから適宜参照してください
     事前にGethでprivate netを立てておき、事前にアカウントを作っておこう.passpraseは'a'とかで作成
       -> accountない場合は作成してしまおう
       -> ここも自動で起動、（ない場合はgenesis.jsonを元に）作成して(genesis.jsonとかをテンプレ別ファイル & passphrase:'a'とかで)やるのでも良いかもね
           ->Gethは自動でマイニングしてくれるオプションをつけると良いかもね
       ->つまり,引数パラメタは無しで、ゴニョゴニョ色々試すようにする？
''')
	sys.exit()


ipc_path = sys.argv[1]
sorce_code = 'ContactList.sol'
passphrase = 'a'


def get_eoa_address_and_private_key(w3) -> tuple:
    eoa_address = w3.geth.personal.list_wallets()[0].accounts[0].address
    keystore_path = w3.geth.personal.list_wallets()[0].accounts[0].url
    with open(re.sub('^keystore://', '', keystore_path, 1), 'r') as f:
        keystore_file =f.read()
    private_key = w3.eth.account.decrypt(keystore_file, passphrase)

    return eoa_address, private_key

def compile_solidity(f) -> dict:
    with open(f,"r") as f:
        solidity_code = f.read()

    compiled_sol: dict  = compile_standard(
        {
            "language": "Solidity",
            "sources": {"ContactList.sol": {"content": solidity_code}},
            "settings": {
                "outputSelection": {
                    "*": {
                        # output needed to interact with and deploy contract
                        "*": ["abi", "metadata", "evm.bytecode", "evm.bytecode.sourceMap"] 
                    }
                }
            },
        },
        solc_version="0.8.18",
    )

    with open("compiled_code.json", "w") as f:
      json.dump(compiled_sol, f)

    return compiled_sol

def extract_binary(compiled: dict) -> tuple[str, str]:
    bytecode = compiled["contracts"]["ContactList.sol"]["ContactList"]["evm"]["bytecode"]["object"]
    abi = json.loads(compiled["contracts"]["ContactList.sol"]["ContactList"]["metadata"])["output"]["abi"]
    return bytecode, abi

#コントラクトに連絡先を追加する
def _addContact(contract_address, abi, number: str):
    contact_list = w3.eth.contract(address=contract_address, abi=abi)
    # store_contact = contact_list.functions.addContact("name", "+2348112398610").buildTransaction(
    store_contact = contact_list.functions.addContact("name", number).buildTransaction(
        {
            "chainId": w3.eth.chain_id, 
            "from": eoa_address, 
            "gasPrice": w3.eth.gas_price, 
            "nonce": nonce + 1
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
    try:
        w3 = Web3(Web3.IPCProvider(ipc_path))
        print(f'[+] Get Block Number: {w3.eth.blockNumber}\n')
    except FileNotFoundError:
        print('[-] Make sure GETH is working properly..')
        print('Run `geth --networkid 4649 --nodiscover --maxpeers 0 --datadir data_privatenet console 2>> data_privatenet/geth.log`')
        sys.exit(1)
    breakpoint()
    if not len(w3.geth.personal.list_wallets()):
        print('No Account... Please create account.')
        # todo create newAccount..
        sys.exit()
    
    eoa_address, private_key = get_eoa_address_and_private_key(w3)
 


    ######## Compile contract(.sol file) ############
    print('[+] Compile and Deploy `./ContactList.sol`\n')
    compiled_sol :dict = compile_solidity(sorce_code)
    ######## Extract smart contract information ############
    bytecode, abi = extract_binary(compiled_sol)
  
    # Get the number of latest transaction
    nonce = w3.eth.getTransactionCount(eoa_address)
    print(f"[+] nounce is {nonce}!!!!")
    # アドレスの「ナンス値」を取得します。ナンス値とは、そのアドレスでトランザクションが行われた回数を示しています。
    # まだ送金をしていないアドレスはゼロが入力されます。このナンス値をトランザクションに含めることで、送受信の順番や重複エラーのチェックが行われています。


    ######## Build Tx for Smart contract ##########  
    # これはsmart contract用のtxを組み立てるよ。EOAが発行する場合は いきなりweb3.eth.account.signTransactionを使えば良さそう
    # txに必要なaddress、nounce値、gasを設定します
    tx = {
        "chainId": w3.eth.chain_id,
        "from": eoa_address,
        "nonce": nonce,
        "gasPrice": w3.eth.gas_price,
    }
 
    ContactList = w3.eth.contract(abi=abi, bytecode=bytecode) # geth consoleだと eth.contract(abi).new({from: eth.accounts[0], data: bytecode})でtx送信までやるぽい
    construct_txn = ContactList.constructor().buildTransaction(tx)
    print(json.dumps(abi))

    ####### Send(Deploy) the transaction #########
    # eoa_addressの持ち主が署名後、txを実行し、そのhash値を取得します。

    # Sign the transaction
    signed_tx = w3.eth.account.sign_transaction(construct_txn, private_key=private_key)
    # txデータとprivate keyを用いて、データに署名を行います。
    # 署名データとは、実際に秘密鍵を有する所有者がこのトランザクション（送金）を行っていることを証明するために付加するデータです。
    print(f"[+] Signed txn!")

    tx_hash = w3.eth.send_raw_transaction(signed_tx.rawTransaction)
    print(f"[+] Send txn to Deploy the contract!! tx_hash is -> {tx_hash.hex()}")
    print(f'[+] Get Block Number: {w3.eth.blockNumber}\n')


    ####### Mining #######
    # イーサリアムの送金が実行されます。署名データとトランザクションデータ、および秘密鍵から生成された公開鍵が、ネットワークに送信されます。
    print('''[+] Wait for the transaction to be mined, and get the transaction receipt...\n\n
  # eth.pendingTransactions で確認すると未だ取り込まれてないtxが確認できる
  # ここで`miner.start(1)してminingして継続します\n''')
    # ネットワークは、署名データを公開鍵を用いて復号し、データが正当な所有者から送信されていることを確認後、ネットワークにトランザクションを記録します。
    ####### Mining #######


    # Display contract address
    tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
    print(f"[+] Contract Address is -> {tx_receipt.contractAddress}")
    print("""  # Gethサーバconsoleで`eth.getTransaction(<txn_hash>)`をやると、txがプロイされ、コントラクトが作成されていることがわかります。
  # eth.getCode(<contract address>)とかでdeployされたcodeの確認ができる
    """)
    print(f'[+] Get Block Number: {w3.eth.blockNumber}\n')


    #Print account balances
    balance = w3.fromWei( w3.eth.getBalance(eoa_address) , "ether")
    print(f'[+] Print account balances(ether): {balance}\n\n')




    ########## Interacting with the Contract ##############
    input('''# Deployしたsmart Contractとやり取りします。続けるにはenterを押す.
  # ここでもtxを発行して送信するので、eth.pendingTransactions で確認すると未だ取り込まれてないtxが確認できる
  # ここでもminer.start()が必要になる\n''')
    
    #コントラクトを操作しようとするときは、コントラクトアドレスとコントラクトABI が必要
    contact_list, tx_receipt = _addContact(tx_receipt.contractAddress, abi, '+0123456789')
    print(f'[+] Get Block Number: {w3.eth.blockNumber}')

    #連絡先を取得する
    print(f'[+] retrieve関数を呼びましたよ！\n', contact_list.functions.retrieve().call())


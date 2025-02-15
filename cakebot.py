from web3 import Web3

import config
import time



def approve(amount):
    busd_contract = web3.eth.contract(address=config.BUSD, abi=config.BUSD_ABI)
    nonce = web3.eth.get_transaction_count(config.sender_address)
    
    #approve BUSD
    txn = {
        'chainId': config.eth_chain_id,
        'nonce': nonce
    }    
    approve_txn = busd_contract.functions.approve(Web3.toChecksumAddress(config.sender_address),amount).buildTransaction(txn)
    signed_txn = web3.eth.account.signTransaction(approve_txn, config.private)
    tx_hash = web3.eth.sendRawTransaction(signed_txn.rawTransaction)
    print('approve txhash', tx_hash)


bsc = "https://bsc-dataseed.binance.org/"
web3 = Web3(Web3.HTTPProvider(bsc))

print(web3.isConnected())

sender_address = config.sender_address
balance = web3.eth.get_balance(sender_address) 
humanReadable = web3.fromWei(balance,'ether')
print('balance: ',humanReadable)
 
#Contract Address of Token we want to buy
# tokenToBuy = web3.toChecksumAddress(input("Enter TokenAddress: "))            
tokenToBuy = web3.toChecksumAddress(config.TOKEN_TO_BUY)            
#web3.toChecksumAddress("0x6615a63c260be84974166a5eddff223ce292cf3d")
spend = web3.toChecksumAddress(config.BUSD)  #wbnb contract
 
#Setup the PancakeSwap contract
contract = web3.eth.contract(address=config.panRouterContractAddress, abi=config.panabi)
nonce = web3.eth.get_transaction_count(sender_address)
 
start = time.time()

amount=Web3.toWei(0.01,'ether')
# approve(amount)
gas = pancakeswap2_txn = contract.functions.swapExactETHForTokens(
    10000000000, # set to 0, or specify minimum amount of tokeny you want to receive - consider decimals!!!
    [spend, tokenToBuy],
    sender_address,
    (int(time.time()) + 10000)
).estimateGas({'value': amount})
print('gas', gas)

#execute swap
pancakeswap2_txn = contract.functions.swapExactETHForTokens(
    10000000000, # set to 0, or specify minimum amount of tokeny you want to receive - consider decimals!!!
    [spend, tokenToBuy],
    sender_address,
    (int(time.time()) + 10000)
).buildTransaction({
    'from': sender_address,
    'value': amount, #This is the Token(BUSD) amount you want to Swap from
    'gas': 250000,
    'gasPrice': web3.toWei('5','gwei'),
    'nonce': nonce
})

end = time.time()
print('time duration: ', end-start)
signed_txn = web3.eth.account.sign_transaction(pancakeswap2_txn, private_key=config.private)
tx_token = web3.eth.send_raw_transaction(signed_txn.rawTransaction)
print('tx_hash',web3.toHex(tx_token))


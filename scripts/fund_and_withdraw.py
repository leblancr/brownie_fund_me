from brownie import FundMe
from scripts.helpful_scripts import get_account


# 
def fund():
    fund_me = FundMe[-1]  # most recently deployed FundMe contract
    account = get_account()  # ganache or config wallet
    print('account', account)
    eth_price = fund_me.getPrice()  # get real Eth price from aggregator
    # conversion_rate =
    print('Eth price', eth_price)
    entrance_fee = fund_me.getEntranceFee()  # 
    print('entrance_fee', entrance_fee)
    
    # send the money
    funders = fund_me.fund({'from': account, 'value': entrance_fee})
    print('funders:', funders)
    print('typefunders:', type(funders))
    
    
def withdraw():
    fund_me = FundMe[-1]  # most recently deployed
    account = get_account()  # account[0] if ganache
    fund_me.withdraw({'from': account})  # fees from account


def main():
    fund()
    fund()
    withdraw()
    
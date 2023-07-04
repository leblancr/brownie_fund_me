from brownie import FundMe, accounts, config, MockV3Aggregator, network
from scripts.helpful_scripts import get_account, deploy_mocks, LOCAL_BLOCKCHAIN_ENVIRONMENTS
from web3 import Web3


# Deploy the FundMe contract with real or mock price feed address
def deploy_fund_me():
    account = get_account()
    print(f"deploying to {account}")
    
    # if persisten network like sepolia use associated address to get real Eth price.
    # else deploy mocks for ganache using fake Eth price of 2000
    if network.show_active() not in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        price_feed_address = config['networks'][network.show_active()]['eth_usd_price_feed']
    else:
        deploy_mocks()
        price_feed_address = MockV3Aggregator[-1].address  # from previously deployed

    # deploy the FundMe contract, price_feed_address goes to FundMe constructor
    fund_me = FundMe.deploy(price_feed_address, {'from': account},
                            publish_source=config['networks'][network.show_active()].get('verify'))
    print(f"contract deployed to {fund_me.address}")
    print("contract deployed to {}".format(fund_me.address))
    return fund_me


# def get_account():
#     print('get_account')
#     print('active network:', network.show_active())
#     if network.show_active() == 'development':
#         return accounts[0]  # local ganache accounts
#     else:
#         return accounts.add(config['wallets']['from_key'])  # config method


def main():
    print('running main()')
    deploy_fund_me()

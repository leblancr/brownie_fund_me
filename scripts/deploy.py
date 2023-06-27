from brownie import FundMe, accounts, config, network
from scripts.helpful_scripts import get_account


def deploy_fund_me():
    account = get_account()
    print(f"deploying to {account}")
    
    if network.show_active() != 'development':
        price_feed_address = config['networks'][network.show_active()]['eth_usd_price_feed']
    
    fund_me = FundMe.deploy({'from': account}, publish_source=False)
    print(f"contract deployed to {fund_me.address}")
    print("contract deployed to {}".format(fund_me.address))


def get_account():
    print('get_account')
    print('active network:', network.show_active())
    if network.show_active() == 'development':
        return accounts[0]  # local ganache accounts
    else:
        return accounts.add(config['wallets']['from_key'])  # config method


def main():
    print('running main()')
    deploy_fund_me()
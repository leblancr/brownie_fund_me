from brownie import accounts, config, network, MockV3Aggregator
from web3 import Web3

FORKED_LOCAL_ENVIRONMENTS = ['mainnet-fork', 'mainnet-fork-alc']
LOCAL_BLOCKCHAIN_ENVIRONMENTS = ['development', 'ganache-local']

DECIMALS = 10
STARTING_PRICE = 200000000000


def deploy_mocks():
    print(f"active network: {network.show_active()}")
    print('deploying mocks...')
    print('len(MockV3Aggregator)', len(MockV3Aggregator))

    # in case if there's already one deployed, MockV3Aggregator list of deployed aggregators
    if len(MockV3Aggregator) <=0:
        print('deploying mocks2...')
        MockV3Aggregator.deploy(
            DECIMALS, STARTING_PRICE, {'from': get_account()},
            publish_source=False)
        print('mocks deployed')


def get_account():
    print('get_account')
    print(f"active network: {network.show_active()}")
    if network.show_active() in LOCAL_BLOCKCHAIN_ENVIRONMENTS or \
       network.show_active() in FORKED_LOCAL_ENVIRONMENTS:
        print('returning accounts[0]')
        return accounts[0]
    else:
        print("returning config['wallets']['from_key']")
        return accounts.add(config['wallets']['from_key'])

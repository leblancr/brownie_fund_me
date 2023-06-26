from brownie import accounts, config, network


def get_account():
    print('get_account')
    print(network.show_active())
    if network.show_active() == 'development':
        return accounts[0]
    else:
        return accounts.add(config['wallets']['from_key'])



from scripts.helpful_scripts import get_account, LOCAL_BLOCKCHAIN_ENVIRONMENTS
from scripts.deploy import deploy_fund_me
from brownie import network
import pytest


def test_can_fund_and_withdrawl():
    account = get_account()
    fund_me = deploy_fund_me()  # deploy.py FundMe object
    entrance_fee = fund_me.getEntranceFee()
    tx = fund_me.fund({'from': account, 'value': entrance_fee})
    tx.wait(1)
    assert fund_me.addressToAmountFunded(account.address) == entrance_fee
    tx2 = fund_me.withdraw({'from': account})
    tx2.wait(1)
    assert fund_me.addressToAmountFunded(account.address) == 0
    
    
def test_only_owner_can_withdrawl():
    if network.show_active() in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        pytest.skip('only for local testing')
     
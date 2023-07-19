from brownie import FundMe, MockV3Aggregator, network, config
from scripts.helpful_scripts import (
    get_account,
    deploy_mocks,
    LOCAL_BLOCKCHAIN_ENVIRONMENTS,
)


def deploy_fund_me():
    account = get_account()
    # pass the price feed address to our fundme contract

    # of we are on a persistent network line goerli, use  the associated address
    # otherwise, deploy mocks
    if network.show_active() not in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        price_feed_address = config["networks"][network.show_active()][
            "eth_usd_price_feed"
        ]
    else:
        # print(f"The active network is {network.show_active()}")
        # print("Deploying Mocks...")
        # if len(MockV3Aggregator) <= 0:
        #     MockV3Aggregator.deploy(Web3.toWei(2000,"ether"), {"from": account})
        # print("Mocks Deployed")
        deploy_mocks()
        price_feed_address = MockV3Aggregator[-1].addresses

    fund_me = FundMe.deploy(
        price_feed_address,
        {"from": account},
        publish_source=config["networks"][network.show_active()].get("verify"),
    )
    print(f"Contract deployed to {fund_me.address}")
    return fund_me


def main():
    deploy_fund_me()


# brownie networks add development mainnet-fork -dev cmd=ganache-cli host=http://127.0.0.1 fork='https://mainnet.infura.io.v3.$WEB3_INFURA_PROJECT_ID accounts=10 mnemonic=browie port=8545'
# brownie networks add development mainnet-fork-dev cmd=ganache-cli host=http://127.0.0.1 fork=https://eth-goerli.g.alchemy.com/v2/4ZWjwSh1LHUvIs2escdJIEqz-Q23Bp0m accounts=10 mnemonic=brownie port=8545

// SPDX-License-Identifier: MIT

// Smart contract that lets anyone deposit ETH into the contract
// Only the owner of the contract can withdraw the ETH
pragma solidity ^0.8.7;

// Get the latest ETH/USD price from chainlink price feed

// IMPORTANT: This contract has been updated to use the Goerli testnet
// Please see: https://docs.chain.link/docs/get-the-latest-price/
// For more information

import "@chainlink/contracts/src/v0.6/interfaces/AggregatorV3Interface.sol";
import "@chainlink/contracts/src/v0.6/vendor/SafeMathChainlink.sol";

contract FundMe {
    // safe math library check uint256 for integer overflows
    using SafeMathChainlink for uint256;

    //mapping to store which address depositeded how much ETH
    mapping(address => uint256) public addressToAmountFunded;
    address[] public funders;  // array of addresses who deposited
    address public owner;  //address of the owner (who deployed the contract)
    AggregatorV3Interface public priceFeed;  //

    // the first person to deploy the contract is the owner
    // 0x694AA1769357215DE4FAC081bf1f309aDC325306
    constructor(address _priceFeed) public {
        priceFeed = AggregatorV3Interface(_priceFeed);
        owner = msg.sender;
    }

    //
    function fund() public payable returns (address[] memory){
        // 18 digit number to be compared with donated amount
        uint256 minimumUSD = 50 * 10**10;
        // is the donated amount less than 50 USD?
        // msg.value = 5000 00000000 0000000000
        // minimumUSD = 50 0000000000
        require(getConversionRate(msg.value) >= minimumUSD,
                "You need to spend more ETH! {msg.value}");

        // add to mapping and funders array
        addressToAmountFunded[msg.sender] += msg.value;
        funders.push(msg.sender);
        return funders;  // it returns a transaction?
    }

     // ethAmount = msg.value
    function getConversionRate(uint256 ethAmount) public view returns (uint256) {
        // require(ethAmount > 5000000000000000000000, "ethAmount not greater than 0");
        // ethAmount = 5000 00000000 0000000000
        uint256 ethPrice = getPrice();  // around 1850 00000000 0000000000
//         require(ethPrice > 1850 00000000 0000000000,
//                 "ethPrice less than");
        // ethPrice ~ 1850, ethAmount ~ 5000
        uint256 ethAmountInUsd = (ethPrice * ethAmount) / 1000000000000000000;
        // the actual ETH/USD conversation rate, after adjusting the extra 0s.
        return ethAmountInUsd;  //  ~ 1850 * 5000
    }

    //
    function getEntranceFee() public view returns (uint256) {
        // minimumUSD
        uint256 minimumUSD = 50 * 10**18;  // 50 0000000000
        uint256 price = getPrice();  // around 1850 00000000 0000000000
        uint256 precision = 1 * 10**18;
        return (minimumUSD * precision) / price + 1;
    }

    function getPrice() public view returns (uint256) {
        (, int256 answer, , , ) = priceFeed.latestRoundData();  // Eth price from aggregator
        // ETH/USD rate in 18 digit
        return uint256(answer * 10000000000);
    }

   // function to get the version of the chainlink pricefeed
    function getVersion() public view returns (uint256) {
        return priceFeed.version();
    }

    //modifier: https://medium.com/coinmonks/solidity-tutorial-all-about-modifiers-a86cf81c14cb
    modifier onlyOwner() {
        //is the message sender owner of the contract?
        require(msg.sender == owner);

        _;
    }

    // onlyOwner modifer will first check the condition inside it
    // and if true, withdraw function will be executed. owner of what?
    function withdraw() public payable onlyOwner {
        // msg.sender.transfer(address(this).balance);
        address payable recipient = payable(msg.sender);
        recipient.transfer(address(this).balance);
        
        //iterate through all the mappings and make them 0
        //since all the deposited amount has been withdrawn
        for (
            uint256 funderIndex = 0;
            funderIndex < funders.length;
            funderIndex++
        ) {
            address funder = funders[funderIndex];
            addressToAmountFunded[funder] = 0;
        }
        //funders array will be initialized to 0
        funders = new address[](0);
    }
}
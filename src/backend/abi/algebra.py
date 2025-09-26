import json

FACTORY_ALGEBRA = json.loads(
    '[{"name":"poolByPair","stateMutability":"view",'
    '"inputs":[{"type":"address"},{"type":"address"}],"outputs":[{"type":"address"}],"type":"function"}]'
)

POOL_ABI_ALGEBRA = json.loads(
    '[{"name":"globalState","stateMutability":"view","inputs":[],'
    '"outputs":[{"components":[{"name":"price","type":"uint160"},{"name":"tick","type":"int24"}],"type":"tuple"}],'
    '"type":"function"}]'
)

FARMING_CENTER = [
    {
        "name": "enterFarming",
        "type": "function",
        "stateMutability": "nonpayable",
        "inputs": [
            {
                "name": "key",
                "type": "tuple",
                "components": [
                    {"name": "rewardToken", "type": "address"},
                    {"name": "bonusRewardToken", "type": "address"},
                    {"name": "pool", "type": "address"},
                    {"name": "nonce", "type": "uint256"},
                ],
            },
            {"name": "tokenId", "type": "uint256"},
        ],
        "outputs": [],
    },
    {
        "name": "exitFarming",
        "type": "function",
        "stateMutability": "nonpayable",
        "inputs": [
            {
                "name": "key",
                "type": "tuple",
                "components": [
                    {"name": "rewardToken", "type": "address"},
                    {"name": "bonusRewardToken", "type": "address"},
                    {"name": "pool", "type": "address"},
                    {"name": "nonce", "type": "uint256"},
                ],
            },
            {"name": "tokenId", "type": "uint256"},
        ],
        "outputs": [],
    },
    {
        "name": "claimReward",
        "type": "function",
        "stateMutability": "nonpayable",
        "inputs": [
            {"name": "rewardToken", "type": "address"},
            {"name": "to", "type": "address"},
            {"name": "amountRequested", "type": "uint256"},
        ],
        "outputs": [{"name": "reward", "type": "uint256"}],
    },
    {
        "name": "multicall",
        "type": "function",
        "stateMutability": "payable",
        "inputs": [{"name": "data", "type": "bytes[]"}],
        "outputs": [{"name": "results", "type": "bytes[]"}],
    },
    {
        "name": "deposits",
        "type": "function",
        "stateMutability": "view",
        "inputs": [{"name": "", "type": "uint256"}],
        "outputs": [{"name": "incentiveId", "type": "bytes32"}],
    },
    {
        "name": "collectRewards",
        "type": "function",
        "stateMutability": "nonpayable",
        "inputs": [
            {
                "name": "key",
                "type": "tuple",
                "components": [
                    {"name": "rewardToken", "type": "address"},
                    {"name": "bonusRewardToken", "type": "address"},
                    {"name": "pool", "type": "address"},
                    {"name": "nonce", "type": "uint256"},
                ],
            },
            {"name": "tokenId", "type": "uint256"},
        ],
        "outputs": [
            {"name": "reward", "type": "uint256"},
            {"name": "bonusReward", "type": "uint256"},
        ],
    },
]

# Algebra NFT-Position-Manager (필요 메서드만)
NFT_PM_ABI_ALGEBRA = [
    {  # positions(uint256)
        "name": "positions",
        "type": "function",
        "stateMutability": "view",
        "inputs": [{"name": "tokenId", "type": "uint256"}],
        "outputs": [
            {"type": "uint96"},
            {"type": "address"},
            {"type": "address"},
            {"type": "address"},
            {"type": "uint24"},
            {"type": "int24"},
            {"type": "int24"},
            {"type": "uint128"},
            {"type": "uint256"},
            {"type": "uint256"},
            {"type": "uint128"},
            {"type": "uint128"},
        ],
    },
    {
        "name": "approveForFarming",
        "type": "function",
        "stateMutability": "payable",
        "inputs": [
            {"name": "tokenId", "type": "uint256"},
            {"name": "approve", "type": "bool"},
            {"name": "farmingAddress", "type": "address"},
        ],
        "outputs": [],
    },
    {
        "name": "decreaseLiquidity",
        "type": "function",
        "stateMutability": "nonpayable",
        "inputs": [
            {
                "name": "params",
                "type": "tuple",
                "components": [
                    {"name": "tokenId", "type": "uint256"},
                    {"name": "liquidity", "type": "uint128"},
                    {"name": "amount0Min", "type": "uint256"},
                    {"name": "amount1Min", "type": "uint256"},
                    {"name": "deadline", "type": "uint256"},
                ],
            }
        ],
        "outputs": [],
    },
    {
        "name": "collect",
        "type": "function",
        "stateMutability": "nonpayable",
        "inputs": [
            {
                "name": "params",
                "type": "tuple",
                "components": [
                    {"name": "tokenId", "type": "uint256"},
                    {"name": "recipient", "type": "address"},
                    {"name": "amount0Max", "type": "uint128"},
                    {"name": "amount1Max", "type": "uint128"},
                ],
            }
        ],
        "outputs": [
            {"name": "collected0", "type": "uint256"},
            {"name": "collected1", "type": "uint256"},
        ],
    },
    {
        "name": "mint",
        "inputs": [
            {
                "components": [
                    {"name": "token0", "type": "address"},
                    {"name": "token1", "type": "address"},
                    {"name": "deployer", "type": "address"},
                    {"name": "tickLower", "type": "int24"},
                    {"name": "tickUpper", "type": "int24"},
                    {"name": "amount0Desired", "type": "uint256"},
                    {"name": "amount1Desired", "type": "uint256"},
                    {"name": "amount0Min", "type": "uint256"},
                    {"name": "amount1Min", "type": "uint256"},
                    {"name": "recipient", "type": "address"},
                    {"name": "deadline", "type": "uint256"},
                ],
                "internalType": "struct INonfungiblePositionManager.MintParams",
                "name": "params",
                "type": "tuple",
            }
        ],
        "outputs": [
            {"name": "tokenId", "type": "uint256"},
            {"name": "liquidity", "type": "uint128"},
            {"name": "amount0", "type": "uint256"},
            {"name": "amount1", "type": "uint256"},
        ],
        "stateMutability": "payable",
        "type": "function",
    },
]

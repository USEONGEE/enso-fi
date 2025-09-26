FIND_TOKEN_BY_POOL = [
    {
        "inputs": [],
        "name": "token0",
        "outputs": [{"internalType": "address", "name": "", "type": "address"}],
        "stateMutability": "view",
        "type": "function",
    },
    {
        "inputs": [],
        "name": "token1",
        "outputs": [{"internalType": "address", "name": "", "type": "address"}],
        "stateMutability": "view",
        "type": "function",
    },
]

POOL_BY_PAIR = [
    {
        "name": "poolByPair",
        "inputs": [{"type": "address"}, {"type": "address"}],
        "outputs": [{"type": "address"}],
        "stateMutability": "view",
        "type": "function",
    }
]

GET_POOL = [
    {
        "inputs": [
            {
                "internalType": "address",
                "name": "tokenA",
                "type": "address",
            },
            {
                "internalType": "address",
                "name": "tokenB",
                "type": "address",
            },
            {"internalType": "uint24", "name": "fee", "type": "uint24"},
        ],
        "name": "getPool",
        "outputs": [
            {
                "internalType": "address",
                "name": "pool",
                "type": "address",
            }
        ],
        "stateMutability": "view",
        "type": "function",
    }
]

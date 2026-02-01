"""
Tombo Blockchain Domain - Blockchain and Cryptocurrency
Provides transactions, smart contracts, mining, consensus
"""

class Block:
    def __init__(self, index=0, data=None, previous_hash='', timestamp=0):
        self.index = index
        self.data = data or {}
        self.previous_hash = previous_hash
        self.timestamp = timestamp
        self.hash = ''
        self.nonce = 0
    
    def calculate_hash(self):
        """Calculate block hash."""
        import hashlib
        content = str(self.index) + str(self.data) + str(self.previous_hash) + str(self.timestamp) + str(self.nonce)
        self.hash = hashlib.sha256(content.encode()).hexdigest()
        return self.hash
    
    def mine_block(self, difficulty=4):
        """Mine block with proof-of-work."""
        target = '0' * difficulty
        while self.hash[:difficulty] != target:
            self.nonce += 1
            self.calculate_hash()
        return True

class Blockchain:
    def __init__(self):
        self.chain = []
        self.pending_transactions = []
        self.difficulty = 4
    
    def add_block(self, data):
        """Add block to chain."""
        index = len(self.chain)
        previous_hash = self.chain[-1].hash if self.chain else '0'
        block = Block(index, data, previous_hash)
        block.mine_block(self.difficulty)
        self.chain.append(block)
        return block
    
    def is_valid(self):
        """Validate blockchain."""
        for i in range(1, len(self.chain)):
            if self.chain[i].previous_hash != self.chain[i-1].hash:
                return False
        return True

class Transaction:
    def __init__(self, sender='', receiver='', amount=0, timestamp=0):
        self.sender = sender
        self.receiver = receiver
        self.amount = amount
        self.timestamp = timestamp
        self.signature = ''
    
    def sign(self, private_key):
        """Sign transaction."""
        self.signature = f"signed_by_{private_key}"
        return True
    
    def is_valid(self):
        """Validate transaction."""
        return len(self.signature) > 0

class Wallet:
    def __init__(self, address=''):
        self.address = address
        self.balance = 0.0
        self.public_key = ''
        self.private_key = ''
    
    def generate_keys(self):
        """Generate key pair."""
        self.public_key = f"public_{self.address}"
        self.private_key = f"private_{self.address}"
        return True
    
    def send_transaction(self, receiver, amount):
        """Send transaction."""
        if self.balance >= amount:
            self.balance -= amount
            return Transaction(self.address, receiver, amount)
        return None

class SmartContract:
    def __init__(self, code=''):
        self.code = code
        self.state = {}
        self.address = ''
    
    def deploy(self):
        """Deploy contract."""
        return True
    
    def call(self, method, args=None):
        """Call contract method."""
        return None

# Blockchain Operations
def tombo_create_blockchain():
    """Create blockchain."""
    return Blockchain()

def tombo_add_block(blockchain, data):
    """Add block to blockchain."""
    return blockchain.add_block(data)

def tombo_get_block(blockchain, index):
    """Get block from blockchain."""
    if 0 <= index < len(blockchain.chain):
        return blockchain.chain[index]
    return None

def tombo_validate_blockchain(blockchain):
    """Validate blockchain."""
    return blockchain.is_valid()

def tombo_get_chain_length(blockchain):
    """Get blockchain length."""
    return len(blockchain.chain)

# Transaction Management
def tombo_create_transaction(sender, receiver, amount):
    """Create transaction."""
    import time
    return Transaction(sender, receiver, amount, time.time())

def tombo_sign_transaction(transaction, private_key):
    """Sign transaction."""
    transaction.sign(private_key)
    return transaction

def tombo_verify_transaction(transaction, public_key):
    """Verify transaction."""
    return transaction.is_valid()

def tombo_add_transaction(blockchain, transaction):
    """Add transaction to pool."""
    blockchain.pending_transactions.append(transaction)
    return True

def tombo_get_pending_transactions(blockchain):
    """Get pending transactions."""
    return blockchain.pending_transactions

def tombo_clear_pending_transactions(blockchain):
    """Clear pending transactions."""
    blockchain.pending_transactions = []
    return True

# Wallet Management
def tombo_create_wallet(address=''):
    """Create wallet."""
    return Wallet(address)

def tombo_generate_keys(wallet):
    """Generate wallet keys."""
    wallet.generate_keys()
    return wallet

def tombo_get_balance(wallet):
    """Get wallet balance."""
    return wallet.balance

def tombo_set_balance(wallet, balance):
    """Set wallet balance."""
    wallet.balance = balance
    return wallet

def tombo_send_transaction_from_wallet(wallet, receiver, amount):
    """Send transaction from wallet."""
    return wallet.send_transaction(receiver, amount)

# Smart Contracts
def tombo_deploy_contract(code):
    """Deploy smart contract."""
    contract = SmartContract(code)
    contract.deploy()
    return contract

def tombo_call_contract(contract, method, args=None):
    """Call contract method."""
    return contract.call(method, args)

def tombo_get_contract_state(contract):
    """Get contract state."""
    return contract.state

def tombo_set_contract_state(contract, key, value):
    """Set contract state."""
    contract.state[key] = value
    return contract

# Consensus Algorithms
def tombo_proof_of_work(blockchain, difficulty=4):
    """Proof of work mining."""
    blockchain.difficulty = difficulty
    return True

def tombo_proof_of_stake(validators, stake_amount=100):
    """Proof of stake."""
    return True

def tombo_delegated_proof_of_stake(voters, candidates):
    """Delegated proof of stake."""
    return True

# Hashing
def tombo_hash_data(data):
    """Hash data."""
    import hashlib
    return hashlib.sha256(str(data).encode()).hexdigest()

def tombo_double_hash(data):
    """Double hash data."""
    hash1 = tombo_hash_data(data)
    return tombo_hash_data(hash1)

def tombo_merkle_root(transactions):
    """Calculate merkle root."""
    if not transactions:
        return tombo_hash_data('')
    hashes = [tombo_hash_data(t) for t in transactions]
    while len(hashes) > 1:
        if len(hashes) % 2 == 1:
            hashes.append(hashes[-1])
        hashes = [tombo_hash_data(hashes[i] + hashes[i+1]) for i in range(0, len(hashes), 2)]
    return hashes[0]

# Address Generation
def tombo_generate_address(public_key):
    """Generate address from public key."""
    return tombo_hash_data(public_key)[:40]

def tombo_validate_address(address):
    """Validate address format."""
    return len(address) == 40

# Cryptocurrency
def tombo_create_coin(name, symbol, supply):
    """Create cryptocurrency."""
    return {'name': name, 'symbol': symbol, 'supply': supply}

def tombo_calculate_transaction_fee(amount, fee_rate=0.001):
    """Calculate transaction fee."""
    return amount * fee_rate

def register(env):
    """Register blockchain domain."""
    env.set('Block', Block)
    env.set('Blockchain', Blockchain)
    env.set('Transaction', Transaction)
    env.set('Wallet', Wallet)
    env.set('SmartContract', SmartContract)
    
    functions = {
        'create_blockchain': tombo_create_blockchain,
        'add_block': tombo_add_block,
        'get_block': tombo_get_block,
        'validate_blockchain': tombo_validate_blockchain,
        'get_chain_length': tombo_get_chain_length,
        'create_transaction': tombo_create_transaction,
        'sign_transaction': tombo_sign_transaction,
        'verify_transaction': tombo_verify_transaction,
        'add_transaction': tombo_add_transaction,
        'get_pending_transactions': tombo_get_pending_transactions,
        'clear_pending_transactions': tombo_clear_pending_transactions,
        'create_wallet': tombo_create_wallet,
        'generate_keys': tombo_generate_keys,
        'get_balance': tombo_get_balance,
        'set_balance': tombo_set_balance,
        'send_transaction_from_wallet': tombo_send_transaction_from_wallet,
        'deploy_contract': tombo_deploy_contract,
        'call_contract': tombo_call_contract,
        'get_contract_state': tombo_get_contract_state,
        'set_contract_state': tombo_set_contract_state,
        'proof_of_work': tombo_proof_of_work,
        'proof_of_stake': tombo_proof_of_stake,
        'delegated_proof_of_stake': tombo_delegated_proof_of_stake,
        'hash_data': tombo_hash_data,
        'double_hash': tombo_double_hash,
        'merkle_root': tombo_merkle_root,
        'generate_address': tombo_generate_address,
        'validate_address': tombo_validate_address,
        'create_coin': tombo_create_coin,
        'calculate_transaction_fee': tombo_calculate_transaction_fee,
    }
    for name, func in functions.items():
        env.set(name, func)

provides = ['blockchain']

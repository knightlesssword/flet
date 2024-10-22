import hashlib
import time
from cryptography.fernet import Fernet

key = Fernet.generate_key()
cipher = Fernet(key)

class Block:
    def __init__(self, index, data, previous_hash):
        encrypted_data = cipher.encrypt(str(data).encode())  # Encrypt data
        self.index = index
        self.timestamp = time.time()
        self.data = encrypted_data.decode()
        self.previous_hash = previous_hash
        self.hash = self.calculate_hash()

    def calculate_hash(self):
        # Create a hash of the block’s content using SHA-256
        block_content = (
            str(self.index) +
            str(self.timestamp) +
            str(self.data) +
            self.previous_hash
        )
        return hashlib.sha256(block_content.encode()).hexdigest()


class Blockchain:
    def __init__(self):
        self.chain = [self.create_genesis_block()]

    def create_genesis_block(self):
        # The first block in the blockchain (index 0)
        return Block(0, "Genesis Block", "0")

    def get_latest_block(self):
        return self.chain[-1]

    def add_block(self, data):
        # Add a new block with the latest data and the hash of the previous block
        previous_block = self.get_latest_block()
        new_block = Block(
            index=previous_block.index + 1,
            data=data,
            previous_hash=previous_block.hash
        )
        self.chain.append(new_block)

    def is_chain_valid(self):
        # Validate the chain by checking the hashes and continuity
        for i in range(1, len(self.chain)):
            current_block = self.chain[i]
            previous_block = self.chain[i - 1]

            if current_block.hash != current_block.calculate_hash():
                return False

            if current_block.previous_hash != previous_block.hash:
                return False

        return True

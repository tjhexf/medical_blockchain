import hashlib
import time
import json
import base64
import os
import sqlite3


# im just storing any files as base64 and putting it on the chain
def file_to_base64(path):
    with open(path, "rb") as f:
        return base64.b64encode(f.read()).decode()

def base64_to_file(base64_data, output_path):
    with open(output_path, "wb") as f:
        f.write(base64.b64decode(base64_data))


class Block:
    def __init__(self, index, timestamp, data, previous_hash):
        self.index = index
        self.timestamp = timestamp
        self.data = data              # data we're storing: medical data here (base64 encoded)
        self.previous_hash = previous_hash
        self.hash = self.calculate_hash()

    # hash calculated based on json with the parameters of the data. just so we dont get duplicates
    # even if someone tries to add a file with the same contents but a different timestamp etc
    def calculate_hash(self):
        block_string = json.dumps({
            "index": self.index,
            "timestamp": self.timestamp,
            "data": self.data,
            "previous_hash": self.previous_hash
        }, sort_keys=True).encode()

        return hashlib.sha256(block_string).hexdigest()

class Blockchain:
    def __init__(self):
        self.chain = [self.create_genesis_block()]

    def create_genesis_block(self):
        return Block(0, time.time(), "Genesis Block", "0")

    def get_latest_block(self):
        return self.chain[-1]

    def add_block(self, data):
        previous_block = self.get_latest_block()
        new_block = Block(
            index=len(self.chain),
            timestamp=time.time(),
            data=data,
            previous_hash=previous_block.hash
        )
        self.chain.append(new_block)

def store_file(db_path, file_path):
    with open(file_path, "rb") as f:
        file_bytes = f.read()

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    cursor.execute(
        "INSERT INTO files (filename, data) VALUES (?, ?)",
        (file_path, file_bytes)
    )

    conn.commit()
    conn.close()

def load_file(db_path, file_id, output_path):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    cursor.execute("SELECT data FROM files WHERE id = ?", (file_id,))
    file_bytes = cursor.fetchone()[0]

    conn.close()

    with open(output_path, "wb") as f:
        f.write(file_bytes)


print("Creating Example Blockchain")

medical_blockchain = Blockchain()

medical_blockchain.add_block(file_to_base64("sample_files/identity.txt"))
medical_blockchain.add_block(file_to_base64("sample_files/example.pdf"))
medical_blockchain.add_block(file_to_base64("sample_files/photo.png"))

print("Creating Example SQLite3 Database")

conn = sqlite3.connect("medical_sql.db")
cursor = conn.cursor()

# Create the 'files' table if it doesn't exist
cursor.execute(
    """CREATE TABLE IF NOT EXISTS files (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        filename TEXT NOT NULL,
        data BLOB NOT NULL
    )"""
)
conn.commit()
conn.close()

store_file("medical_sql.db", "sample_files/identity.txt")
store_file("medical_sql.db", "sample_files/example.pdf")
store_file("medical_sql.db", "sample_files/photo.png")

# Trying to access and modify the databases

## Blockchain
print("Modifying a block")

try:
	medical_blockchain.chain[1].data = base64.b64encode(b'modified data in block 1').decode()
	print("Blockchain data modified (attempted)")
except AttributeError as e:
	print(f"Failed to modify block data: {e}")
except Exception as e:
	print(f"An unexpected error occurred: {e}")

### Blockchain validation
blockchain_intact = True
for b in range(1, len(medical_blockchain.chain)):
	current = medical_blockchain.chain[b]
	previous = medical_blockchain.chain[b - 1]

	if current.hash != current.calculate_hash() or current.previous_hash != previous.hash:
		blockchain_intact = False
		break
if blockchain_intact:
	print("Blockchain intact")
else:
	print("Blockchain compromised!")

## SQLite
try:
	conn = sqlite3.connect("medical_sql.db")
	cursor = conn.cursor()
	cursor.execute("SELECT * FROM files")
	rows = cursor.fetchall()
	conn.close()

	print("SQLite accessed successfully.")
except Exception:
	print(f"Failed to access SQLite database")

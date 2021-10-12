import mysql.connector
import hashlib
import pickle
import time

from Commands import difficulty

MYSQL_PASS = open('.env').read()[6:]

Connection = mysql.connector.connect(host='localhost', username='root', password=MYSQL_PASS, database='Blockchain')
cursor = Connection.cursor()

# Unmined_Transactions
query = """SELECT Transaction_ID FROM Unmined_Transactions;"""
cursor.execute(query)
Unmined_Transactions = list(map(lambda x:x[0], cursor.fetchall()))


block = open("Current Block.block", 'rb')
Current_Block = pickle.load(block)
block.close()

Current_Block.BlockBody['Transactions_IDS'] = Unmined_Transactions

body = Current_Block.BlockBody.copy()

i = 0
print(time.perf_counter())

for i in range(1000000):
	body['Nonce'] = str(i)
	body_str = str(body)
	block_hash = hashlib.sha256(body_str.encode()).hexdigest()
	if (int(eval('0x' + block_hash)) <= difficulty):
		print('Found Valid Nonce:', i)
		break

print(time.perf_counter())

Connection.commit()
cursor.close()
Connection.close()
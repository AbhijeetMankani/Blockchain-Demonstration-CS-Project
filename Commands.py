import mysql.connector
import nacl.signing
import nacl.encoding
import hashlib

import pickle

difficulty = 1e72 # Difficulty for testing
# TODO: Implement Algorithm to update Difficulty with change in length of Chain

MYSQL_PASS = open('.env').read()[6:]

def mine_transaction(T_ID):

	Blockchain_File = open("BlockChain.blockchain", 'rb')
	Blockchain = pickle.load(Blockchain_File)
	Blockchain_File.close()

	BLOCK_MINE_REWARD = Blockchain.Blockchain_KEY

	Connection = mysql.connector.connect(host='localhost', username='root', password=MYSQL_PASS, database='Blockchain')
	cursor = Connection.cursor()

	query = '''SELECT * FROM All_Transactions WHERE Transaction_ID = {T_ID};'''.format(T_ID = T_ID)
	cursor.execute(query)

	Transaction = cursor.fetchone()

	sender_id = Transaction[1]
	receiver_id = Transaction[2]
	amount = Transaction[3]
	mined = Transaction[4]
	Transaction_Message = Transaction[5]
	Transaction_Signature = Transaction[6]

	if (sender_id != BLOCK_MINE_REWARD and not mined):
		VKEY = nacl.signing.VerifyKey(sender_id, encoder=nacl.encoding.HexEncoder)
		signed_message = bytes.fromhex(Transaction_Signature) + Transaction_Message.encode()
		try:
			VKEY.verify(signed_message)
			print('Signature Verified')
		except nacl.signing.exc.BadSignatureError:
			print("Invalid Transaction - Invalid/Corrupt Signature")
			return False
	# else:
	if(not mined):
		query = '''SELECT Balance FROM Users WHERE Public_Key="{Public_Key}";'''.format(Public_Key = sender_id)
		cursor.execute(query)
		NewBal_Sender = cursor.fetchone()[0] - amount

		query = '''SELECT Balance FROM Users WHERE Public_Key="{Public_Key}";'''.format(Public_Key = receiver_id)
		cursor.execute(query)
		NewBal_Receiver = cursor.fetchone()[0] + amount

		query = '''SELECT Transactions_Done FROM Users WHERE Public_Key="{Public_Key}";'''.format(Public_Key = sender_id)
		cursor.execute(query)
		TD_Sender = cursor.fetchone()[0] + 1

		query = '''SELECT Transactions_Done FROM Users WHERE Public_Key="{Public_Key}";'''.format(Public_Key = receiver_id)
		cursor.execute(query)
		TD_Receiver = cursor.fetchone()[0] + 1


		query = '''UPDATE Users SET Balance = {NewBal} WHERE Public_Key = "{Sender_ID}";'''.format(NewBal = NewBal_Sender, Sender_ID = sender_id)
		cursor.execute(query)
		query = '''UPDATE Users SET Balance = {NewBal} WHERE Public_Key = "{Receiver_ID}";'''.format(NewBal = NewBal_Receiver, Receiver_ID = receiver_id)
		cursor.execute(query)


		query = '''UPDATE Users SET Transactions_Done = {TD} WHERE Public_Key = "{Sender_ID}";'''.format(TD = TD_Sender, Sender_ID = sender_id)
		cursor.execute(query)
		query = '''UPDATE Users SET Transactions_Done = {TD} WHERE Public_Key = "{Receiver_ID}";'''.format(TD = TD_Receiver, Receiver_ID = receiver_id)
		cursor.execute(query)

		query = '''UPDATE All_Transactions SET Mined=TRUE WHERE Transaction_ID = {T_ID} AND Mined = FALSE;'''.format(T_ID = T_ID)
		cursor.execute(query)
		
		query = '''DELETE FROM Unmined_Transactions WHERE Transaction_ID = {T_ID};'''.format(T_ID = T_ID)
		cursor.execute(query)

		query = '''INSERT INTO Mined_Transactions VALUES ({T_ID}, "{Sender_ID}", "{Reciever_ID}", {Amount});'''.format(T_ID = T_ID, Sender_ID = sender_id, Reciever_ID = receiver_id, Amount = amount)
		cursor.execute(query)

	Connection.commit()
	cursor.close()
	Connection.close()

def send_reward(Block_ID, User_ID, Amount):
	
	Blockchain_File = open("BlockChain.blockchain", 'rb')
	Blockchain = pickle.load(Blockchain_File)
	Blockchain_File.close()

	BLOCK_MINE_REWARD = Blockchain.Blockchain_KEY

	Connection = mysql.connector.connect(host='localhost', username='root', password=MYSQL_PASS, database='Blockchain')
	cursor = Connection.cursor()

	query = '''SELECT Balance FROM Users WHERE Public_Key="{Public_Key}";'''.format(Public_Key = User_ID)
	cursor.execute(query)
	receiver_bal = cursor.fetchall()

	query = '''UPDATE Users set Rewards_Won=Rewards_Won+1 WHERE Public_Key='{Pubic_Key}';'''.format(Pubic_Key = User_ID)
	cursor.execute(query)

	receiver_bal = receiver_bal[0][0]

	query = '''SELECT COUNT(*) FROM All_Transactions;'''
	cursor.execute(query)
	T_ID = cursor.fetchone()[0]

	# # Transaction in form of json to store in sql
	transaction = "{" + '''"Transaction_ID": {T_ID}, "sender_id": "{BLOCK_MINE_REWARD}", "receiver_id": "{receiver_id}", "amount": "{amount}"'''.format(T_ID = T_ID, BLOCK_MINE_REWARD=BLOCK_MINE_REWARD, receiver_id = User_ID, amount=Amount) + "}"

	signature = hashlib.sha256(transaction.encode()).hexdigest()

	query = '''INSERT INTO All_Transactions VALUES ("{T_ID}", "{BLOCK_MINE_REWARD}", "{Reciever_ID}", {Amount}, FALSE, '{transaction}', "{sign}");'''.format(T_ID = T_ID, BLOCK_MINE_REWARD=BLOCK_MINE_REWARD, Reciever_ID = User_ID, Amount = Amount, transaction = transaction, sign = "BLOCK_MINE_REWARD_" + signature)
	cursor.execute(query)
	query = '''INSERT INTO Unmined_Transactions VALUES ("{T_ID}", "{BLOCK_MINE_REWARD}", "{Reciever_ID}", {Amount});'''.format(T_ID = T_ID, BLOCK_MINE_REWARD=BLOCK_MINE_REWARD, Reciever_ID = User_ID, Amount = Amount)
	cursor.execute(query)

	Connection.commit()

	cursor.close()
	Connection.close()
	print("Reward Succesful; Reward-Transaction ready to be Mined.")


# send_reward(1, '1d482ff9bf39b0f75deab0000575ac5bead1ddd51c7dc81c810bb1204d056f8f', 50)
# mine_transaction(1)
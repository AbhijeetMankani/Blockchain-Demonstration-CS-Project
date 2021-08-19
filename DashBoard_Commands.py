import pandas as pd
import nacl.signing
import nacl.encoding

import mysql.connector



def transaction(sender_id, receiver_id, amount, signing_key):
	if(amount < 0): 
		print("Invalid Amount")
		return
	# Acc = pd.read_csv(r'C:\Users\Sunil\Desktop\Abhijeet\TSS\CS\Grade 12 Project\BlockChain\Accounts.csv')
	Connection = mysql.connector.connect(host='localhost', username='root', password='123456', database='Blockchain')
	cursor = Connection.cursor()
	query = '''SELECT Balance FROM Users WHERE Public_Key="{Public_Key}";"'''.format(Public_Key = sender_id)
	cursor.execute(query)
	sender_bal = cursor.fetchall()
	query = '''SELECT Balance FROM Users WHERE Public_Key="{Public_Key}";"'''.format(Public_Key = receiver_id)
	cursor.execute(query)

	receiver_bal = cursor.fetchall()
	if(len(sender_bal) == 0):
		print("Invalid Sender's ID")
		return
	if(len(receiver_bal) == 0):
		print("Invalid Reciever's ID")
		return
	if(sender_bal < amount):
		print("Insufficient Balance")
		return
	
	receiver_bal = receiver_bal[0][0]
	sender_bal = sender_bal[0][0]

	# Transaction in form of json to store in sql
	transaction = '''{
		"sender_id": "{sender_id}",
		"receiver_id": "{receiver_id}",
		"amount": "{amount}"
	}'''.format(sender_id=sender_id, receiver_id=receiver_id, amount=amount)

	# Regenerating key from hex
	sign_key = nacl.signing.SigningKey(signing_key, encoder=nacl.encoding.HexEncoder)

	signed_transaction = sign_key.sign(transaction)

	
    

def balance(user_id):
	Connection = mysql.connector.connect(host='localhost', username='root', password='123456', database='Blockchain')
	cursor = Connection.cursor()
	query = '''SELECT Balance FROM Users WHERE Public_Key="{Public_Key}";"'''.format(Public_Key = user_id)

	cursor.execute(query)

	bal = cursor.fetchall()[0][0]

	print("Balance:", bal)

def submit_nonce(nonce):
	pass
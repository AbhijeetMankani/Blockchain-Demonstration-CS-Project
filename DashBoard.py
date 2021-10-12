import hashlib
import DashBoard_Commands

import mysql.connector

MYSQL_PASS = open('.env').read()[6:]

Connection = mysql.connector.connect(host='localhost', username='root', password=MYSQL_PASS, database='Blockchain')


if(Connection.is_connected()):
	
	cursor = Connection.cursor()
	# Logging in Process
	pkey_ = input("Enter Public Key: ")
	Hash_priv_ = str(hashlib.sha256(input("Enter Private Key: ").encode()).hexdigest())

	query = '''SELECT Hashed_Private_Key FROM Users WHERE Public_Key="{Public_Key}"'''.format(Public_Key = pkey_)

	cursor.execute(query)

	try:
		Hashed_Private_Key = cursor.fetchall()[0][0]
	except:
		print("Invalid Public Key")

	Connection.close()

	if(Hashed_Private_Key == Hash_priv_):
		print("Login Successful")
	else:
		print("Login Unsuccessful, Incorrect Public/Private Key")
		exit()

	action = ' '

	# Dashboard Commmands
	while(action not in "Ee"):
		print("Enter T to issue a Transaction")
		print("Enter B to Check Balance")
		print("Enter S to Submit Nonce for Ongoing Block")
		print("Enter E to Exit and Log out")
		action = input()	
		if(action not in "TtBbSsEe"):
			print("Invalid Action\n\n")
		elif(action in "Tt"):
			Reciever_ID = input("Enter reciever's ID: ")
			amount = float(input("Enter Transaction Amount: "))
			_priv_key = input("Enter Private Key to authorize transaction: ")
			if(str(hashlib.sha256(_priv_key.encode()).hexdigest()) == Hash_priv_):
				DashBoard_Commands.transaction(pkey_, Reciever_ID, amount, _priv_key)
			else:
				print("You are unauthorized - logging out")
				break
			print('\n')
			#Transaction Code Goes Here
		elif(action in "Bb"):
			DashBoard_Commands.balance(pkey_)

			print('\n\n')
			#Balance Check Code Goes Here
		elif(action in "Ss"):
			nonce = input("Enter the Nonce for current block: ")
			DashBoard_Commands.submit_nonce(nonce, pkey_)
			#Submiting Nonce Code Goes Here

	print("Exited, and Logged out")
else:
	print("There was some error, please try again.")
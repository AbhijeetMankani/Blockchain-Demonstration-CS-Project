import hashlib
import DashBoard_Commands
import pandas as pd

# Logging in Process
pkey_ = input("Enter Public Key: ")
Hash_priv_ = str(hashlib.sha256(input("Enter Private Key: ").encode()).hexdigest())
Acc = pd.read_csv(r'C:\Users\Sunil\Desktop\Abhijeet\TSS\CS\Grade 12 Project\BlockChain\Accounts.csv')

i = Acc.Public_Key.searchsorted(pkey_)

if(Acc.Hashed_Private_Key[i] == Hash_priv_):
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

		DashBoard_Commands.transaction(pkey_, Reciever_ID, amount)

		print('\n')
		#Transaction Code Goes Here
	elif(action in "Bb"):
		DashBoard_Commands.balance(pkey_)

		print('\n\n')
		#Balance Check Code Goes Here
	elif(action in "Ss"):
		pass
		#Submiting Nonce Code Goes Here

print("Exited, and Logged out")
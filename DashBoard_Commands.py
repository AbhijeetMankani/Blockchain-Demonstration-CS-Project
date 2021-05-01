import pandas as pd

def transaction(sender_id, receiver_id, amount):
	if(amount < 0): 
		print("Invalid Amount")
		return
	Acc = pd.read_csv(r'C:\Users\Sunil\Desktop\Abhijeet\TSS\CS\Grade 12 Project\BlockChain\Accounts.csv')

	s_i = None
	r_i = None

	for i in range(len(Acc)):
	    if(Acc.Public_Key[i] == sender_id):
	        s_i = i
	    if(Acc.Public_Key[i] == receiver_id):
	        r_i = i

	if(s_i == None):
		print("Invalid Sender's ID")
		return
	if(r_i == None):
		print("Invalid Reciever's ID")
		return

	if(Acc.Balance[s_i] >= amount):
		Acc_ =  Acc.copy()
		Acc_.loc[s_i, 'Balance'] -= amount

		Acc_.loc[r_i, 'Balance'] += amount
		print("Transaction Successful!")
		Acc_.loc[s_i, 'Transactions_Done'] += 1
		Acc_.loc[r_i, 'Transactions_Done'] += 1
		Acc = Acc_.copy()
		Acc.to_csv('Accounts.csv')
	else:
		print("Insufficient Balance")
    
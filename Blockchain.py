import hashlib
import datetime

class user():
    def __init__(self, Name, Age, DOB):
        today = datetime.date.today()
        self.UserID = hashlib.sha256((Name+DOB+str(today.day)+str(today.month)+str(today.year)).encode()).hexdigest()
        self.User_privKey = hashlib.sha256((Name+DOB+str(today.day)+str(today.month)+str(today.year)).encode()).hexdigest()
        self.balance = 0

    def deposit(self, amount):
        self.balance += amount



class Blockchain():
    def __init__(self):
        self.transactions = ""
        self.previous_blockHash = ""
        self.no_nonce_block = self.previous_blockHash + '\n\n' + self.transactions + '\n\n'
        self.current_reward = 100
        self.rewards_given = 0
        self.changes = 0
    def check_nonce(self, nonce, user):
        if(eval('0x' + hashlib.sha256((self.no_nonce_block+str(hex(i))).encode()).hexdigest())<(difficulty)):
            print("Correct nonce: " + nonce)
            self.reward(user)
            self.previous_blockHash = hashlib.sha256((self.no_nonce_block+str(hex(i))).encode()).hexdigest()
            self.no_nonce_block = self.previous_blockHash + '\n\n' + self.transactions + '\n\n'
            transactions = ""
            self.rewards_given += self.current_reward

            if(self.rewards_given>=10**3 and self.changes==0):
                self.current_reward/=2
                self.changes += 1
            elif(self.rewards_given>=10**4 and self.changes==1):
                self.current_reward/=2
                self.changes += 1
            elif(self.rewards_given>=10**5 and self.changes==2):
                self.current_reward/=2
                self.changes += 1
            
            return True
        else:
            print("Incorrect nonce: " + nonce)
        return False
    def reward(self, user):
        user.deposit(self.current_reward)

    def newTransactions(transaction):
        self.transactions += "\n" + transaction




Abhijeet = user("Abhijeet", "16", "11-01-2005")
print(Abhijeet.balance)
difficulty = 1000000000000000000000000000000000000000000000000000000000000000000000000
MyBloackChain = Blockchain()
for i in range(10000000):
	if(eval('0x' + hashlib.sha256((MyBloackChain.no_nonce_block+str(hex(i))).encode()).hexdigest())<(difficulty)):
		MyBloackChain.check_nonce(str(hex(i)), Abhijeet)
		break
	else:k=i
print(Abhijeet.balance)
	

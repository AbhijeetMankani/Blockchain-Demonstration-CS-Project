import datetime
import hashlib
from random import uniform


Acc = open("C:\\Users\\Sunil\\Desktop\\Abhijeet\\TSS\\CS\\Grade 12 Project\\BlockChain\\Accounts.csv", "a+")

Name = input("Enter Name: ")
Age = input("Enter Age: ")
DOB = input("Enter Date of Birth: \nDate: ")
MOB = input("Month: ")
YOB = input("Year: ")




today = datetime.date.today()

Acc.seek(0,0)
Public_KEY = hashlib.sha256(str(len(Acc.read())).encode()).hexdigest()
Private_KEY = hashlib.sha256((Name+DOB+MOB+YOB+str(today.day)+str(today.month)+str(today.year) + str(uniform(0, 100000000))).encode()).hexdigest()

Acc.seek(2,0)
Acc.write(str(Public_KEY) + ',' + str(hashlib.sha256((Private_KEY).encode()).hexdigest()) + ',0.0,0,0\n')

Acc.close()

print("This is Your Public_KEY:", Public_KEY)
print("This is your Private_KEY(Do not Share):", Private_KEY)
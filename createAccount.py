import datetime
import hashlib
from random import uniform

import pandas as pd

# Digital Signature
import nacl.encoding
import nacl.signing


# Acc = open("C:\\Users\\Sunil\\Desktop\\Abhijeet\\TSS\\CS\\Grade 12 Project\\BlockChain\\Accounts.csv", "a+")

Acc = pd.read_csv(r'C:\Users\Sunil\Desktop\Abhijeet\TSS\CS\Grade 12 Project\BlockChain\Accounts.csv')

Name = input("Enter Name: ")
Age = input("Enter Age: ")
DOB = input("Enter Date of Birth: \nDate: ")
MOB = input("Month: ")
YOB = input("Year: ")


today = datetime.date.today()
import base64

s = Name+DOB+MOB+YOB+str(today.day)+str(today.month)+str(today.year) + str(uniform(0, 100000000000000))

seed = s.encode('utf-32')
seed = seed[:32]


Private_KEY = nacl.signing.SigningKey(seed=seed).generate()
Public_KEY = Private_KEY.verify_key

Private_KEY_hex = Private_KEY.encode(encoder=nacl.encoding.HexEncoder).decode()
Public_KEY_hex = Public_KEY.encode(encoder=nacl.encoding.HexEncoder).decode()

hashedPrivateKey = str(hashlib.sha256((Private_KEY_hex).encode()).hexdigest())

Acc.loc[len(Acc)] = [Public_KEY_hex, hashedPrivateKey, 0, 0, 0]
# Find way to remake the SigningKey Object from the hexcode/bytearray
# DONE

Acc.to_csv(r'C:\Users\Sunil\Desktop\Abhijeet\TSS\CS\Grade 12 Project\BlockChain\Accounts.csv', index=False)

print("This is Your Public_KEY:", Public_KEY_hex)
print("This is your Private_KEY(Do not Share):", Private_KEY_hex)
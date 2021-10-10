import hashlib
import mysql.connector
import Commands
import math
import pickle


MYSQL_PASS = open('.env').read()[6:]

difficulty = 1e60 # Difficulty for testing
# TODO: Implement Algorithm to update Difficulty with change in length of Chain

SQL_COMMANDS = open('Setup SQL.sql')

commands = SQL_COMMANDS.readlines()



def Setup():
    Connection = mysql.connector.connect(host='localhost', username='root', password=MYSQL_PASS)
    cursor = Connection.cursor()
    for command in commands:
        command = command.strip('\n')
        if(command):
            cursor.execute(command)
    
    block = Block(0, [], '')
    Current_Block_File = open('Current Block.block', 'wb')
    pickle.dump(block, Current_Block_File)

    Connection.commit()
    cursor.close()
    Connection.close()

    print("Setup Successful!")
        

class Block():
    def __init__(self, Block_ID, Transactions_IDS, PreiousBlockHash):
        self.Block_ID = Block_ID
        self.Transactions_IDS = Transactions_IDS
        self.PreiousBlockHash = PreiousBlockHash

        self.MiningReward = 50 # TODO: Implement Algorithm to change reward based on Length of Blockchain


        self.BlockBody = {
            'PreiousBlockHash': self.PreiousBlockHash,
            'Block_ID': self.Block_ID,
            'Transactions_IDS': self.Transactions_IDS,
            'Nonce': ''
        }
        self.block = {
            'Body': self.BlockBody,
            'BlockHash': '',
            'Reward Winner': ''
        }
    
    def checkNonce(self, Nonce):
        body = self.BlockBody.copy()
        body['Nonce'] = Nonce
        body_str = str(body)
        block_hash = hashlib.sha256(body_str).hexdigest()
        if (int(eval('0x' + block_hash)) <= difficulty):
            print('Nonce is Valid')
            return True
        else:
            print('Nonce is Invalid')
            return False

    def submitNonce(self, Nonce, User_ID):
        if (self.checkNonce(Nonce)):
            self.BlockBody['Nonce'] = Nonce
            body_str = str(self.BlockBody)
            block_hash = hashlib.sha256(body_str).hexdigest()
            self.block = {
                'Body': self.BlockBody,
                'BlockHash': block_hash,
                'Reward Winner': User_ID
            }
            Commands.send_reward(self.Block_ID, User_ID, self.MiningReward)
            for transaction in self.Transactions_IDS:
                Commands.mine_transaction(transaction)
            Blockchain.addMinedBlock(self)
        

class Blockchain:
    def __init__(self):
        self.Blocks = []
        self.ChainLength = 0

    def addMinedBlock(self, Block):
        Connection = mysql.connector.connect(host='localhost', username='root', password=MYSQL_PASS, database='Blockchain')
        cursor = Connection.cursor()

        self.Blocks.append(Block)
        self.ChainLength += 1
        
        query = """INSERT INTO Blocks VALUES ({Block_ID}, "{Previous_Block_Hash}", "{Transactions}", "{Nonce}", "{Block_Hash}", "{Sumbitter_ID}");""".format(Block_ID=Block.Block_ID, Previous_Block_Hash=Block.Previous_Block_Hash, Transactions=Block.Transactions_IDS, Nonce=Block.block['Body']['Nonce'], Block_Hash=Block.block['BlockHash'], Submitter_ID=Block.block['Reward Winner'])
        cursor.execute(query)

        Connection.commit()
        cursor.close()
        Connection.close()

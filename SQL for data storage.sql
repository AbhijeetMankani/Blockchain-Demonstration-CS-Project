-- Setup initialisation for creating the database
CREATE DATABASE IF NOT EXISTS Blockchain;
use Blockchain;

CREATE TABLE IF NOT EXISTS Users(
	Public_Key CHAR(64) PRIMARY KEY,
	Hashed_Private_Key CHAR(64) UNIQUE KEY NOT NULL,
	Balance FLOAT,
	Transactions_Done INT,
	Rewards_Won INT
);

CREATE TABLE IF NOT EXISTS Blocks(
	Block_ID CHAR(4) PRIMARY KEY,
	Previous_Block_Hash CHAR(64) UNIQUE KEY,
	Transactions JSON,
	Nonce VARCHAR(64),
	Block_Hash CHAR(64) UNIQUE KEY NOT NULL,
	Submitter_ID CHAR(64) NOT NULL
);


CREATE TABLE IF NOT EXISTS Unmined_Transactions(
	Transaction_ID CHAR(4) PRIMARY KEY,
	Sender_ID CHAR(64) NOT NULL,
	Reciever_ID CHAR(64) NOT NULL,
	Amount FLOAT NOT NULL
);

CREATE TABLE IF NOT EXISTS Mined_Transactions(
	Transaction_ID CHAR(4) PRIMARY KEY,
	Sender_ID CHAR(64) NOT NULL,
	Reciever_ID CHAR(64) NOT NULL,
	Amount FLOAT NOT NULL
);

CREATE TABLE IF NOT EXISTS All_Transactions(
	Transaction_ID CHAR(4) PRIMARY KEY,
	Sender_ID CHAR(64) NOT NULL,
	Reciever_ID CHAR(64) NOT NULL,
	Amount FLOAT NOT NULL,
	Mined BOOLEAN NOT NULL
);

ALTER TABLE Unmined_Transactions ADD FOREIGN KEY (Sender_ID) REFERENCES Users(Public_Key);
ALTER TABLE Unmined_Transactions ADD FOREIGN KEY (Reciever_ID) REFERENCES Users(Public_Key);

ALTER TABLE Mined_Transactions ADD FOREIGN KEY (Sender_ID) REFERENCES Users(Public_Key);
ALTER TABLE Mined_Transactions ADD FOREIGN KEY (Reciever_ID) REFERENCES Users(Public_Key);

ALTER TABLE All_Transactions ADD FOREIGN KEY (Sender_ID) REFERENCES Users(Public_Key);
ALTER TABLE All_Transactions ADD FOREIGN KEY (Reciever_ID) REFERENCES Users(Public_Key);


ALTER TABLE Blocks ADD FOREIGN KEY (Previous_Block_Hash) REFERENCES Blocks(Block_Hash);
ALTER TABLE Blocks ADD FOREIGN KEY (Submitter_ID) REFERENCES Users(Public_Key);


-- Setup Ends


-- New Transaction code

INSERT INTO All_Transactions VALUES (T_ID, Sender_ID, Reciever_ID, Amount, FALSE);
INSERT INTO Unmined_Transactions VALUES (T_ID, Sender_ID, Reciever_ID, Amount);


-- Mining Transaction

UPDATE Users SET Balance=Balance-Amount WHERE Public_Key = Sender_ID;
UPDATE Users SET Balance=Balance+Amount WHERE Public_Key = Reciever_ID;

UPDATE All_Transactions SET Mined=TRUE WHERE T_ID = T_ID AND Mined = FALSE;
DELETE FROM Unmined_Transactions WHERE T_ID = T_ID;
INSERT INTO Mined_Transactions VALUES (T_ID, Sender_ID, Reciever_ID, Amount);


-- Create User -- Done
INSERT INTO Users VALUES (Public_Key, Hashed_Private_Key, 0, 0, 0);

-- Logging User in
SELECT Hashed_Private_Key FROM Users WHERE Public_Key=Public_Key;

-- Show Balance
SELECT Balance FROM Users WHERE Public_Key=Public_Key;

-- Adding a Block (After checking if nonce is correct)
INSERT INTO Blocks VALUES (Block_ID, Previous_Block_Hash, Transactions, Nonce, Block_Hash, Sumbitter_ID);

-- Previous Block_Hash for finding Nonce
SELECT Block_Hash from Blocks ORDER BY Block_ID DESC LIMIT 1;
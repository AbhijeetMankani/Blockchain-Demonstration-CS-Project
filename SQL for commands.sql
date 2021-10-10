

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
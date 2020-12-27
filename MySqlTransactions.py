import mysql.connector
from datetime import datetime
from MySqlConnector import MySqlConnector

class MySqlTransaction(MySqlConnector):

    def UpdateBalance(self, discordID, balance):
        cnx = mysql.connector.connect(user=self.username, password=self.password, host=self.host, port=self.port, database=self.database);
        cursor = cnx.cursor()
        checkforusercmd = "SELECT DiscordID FROM userwallet WHERE DiscordID = %(id)s"
        cursor.execute(checkforusercmd, {"id": discordID})
        if cursor.fetchone() is None:
            updatebalancecmd = f'INSERT INTO userwallet (DiscordID,WalletBalance) VALUES ({discordID},{balance})'
        else:
            updatebalancecmd = f'UPDATE userwallet SET WalletBalance = {balance} WHERE DiscordID = {discordID}'
        cursor.execute(updatebalancecmd)
        if cursor.rowcount <= 0:
            raise Exception('Could not update your balance!')
        cnx.commit()
        cursor.close()
        cnx.close()

    def WriteTransactionLog(self, discordID, amount,recipientID, walletAddress):
        cnx = mysql.connector.connect(user=self.username, password=self.password, host=self.host, port=self.port, database=self.database);
        cursor = cnx.cursor()
        writelogcmd = 'INSERT INTO userwalletlog (EntryTime,TransactionAmount,DiscordID,RecipientID,WalletAddress) VALUES (%(time)s, %(amount)s, %(id)s, %(recipient)s, %(address)s)'
        cursor.execute(writelogcmd, {"time": datetime.now(), "amount": amount, "id": discordID, "recipient":recipientID, "address": walletAddress})
        cnx.commit()
        cursor.close()
        cnx.close()

    def GetBalance(self, discordID):
        cnx = mysql.connector.connect(user=self.username, password=self.password, host=self.host, port=self.port, database=self.database);
        cursor = cnx.cursor()
        cmd = "SELECT WalletBalance FROM userwallet WHERE DiscordID = %(id)s"
        cursor.execute(cmd, {"id": discordID})
        row = cursor.fetchone()
        if row is None:
            val = None
        else:
            val = row[0]
        cnx.close()
        return val

    def ReturnAllBalances(self):
        cnx = mysql.connector.connect(user=self.username, password=self.password, host=self.host, port=self.port, database=self.database);
        cursor = cnx.cursor()
        cmd = "SELECT DiscordID,WalletBalance FROM userwallet"
        cursor.execute(cmd)
        data = cursor.fetchall()
        cnx.close()
        return data

    def ReturnLog(self):
        cnx = mysql.connector.connect(user=self.username, password=self.password, host=self.host, port=self.port, database=self.database);
        cursor = cnx.cursor()
        cmd = "SELECT EntryTime,TransactionAmount,DiscordID,RecipientID,WalletAddress FROM userwalletlog"
        cursor.execute(cmd)
        data = cursor.fetchall()
        cnx.close()
        return data
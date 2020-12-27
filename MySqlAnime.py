import mysql.connector
from datetime import datetime
from MySqlConnector import MySqlConnector


class MySqlAnime(MySqlConnector):
    def GetUserList(self, discordID):
        cnx = mysql.connector.connect(user=self.username, password=self.password, host=self.host, port=self.port, database=self.database);
        cursor = cnx.cursor()
        searchcmd = "SELECT * FROM trackedAnime WHERE DiscordID = %(id)s"
        cursor.execute(searchcmd, {"id": discordID})
        result = cursor.fetchall()
        cursor.close()
        cnx.close()
        return result

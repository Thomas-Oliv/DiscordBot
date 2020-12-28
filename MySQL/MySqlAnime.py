import mysql.connector
from datetime import datetime
from MySQL.MySqlConnector import MySqlConnector

class MySqlAnime(MySqlConnector):

    def GetList(self, discordID):
        cnx = mysql.connector.connect(user=self.username, password=self.password, host=self.host, port=self.port, database=self.database)
        cursor = cnx.cursor()
        searchcmd = "SELECT AnimeID, Title FROM trackedanime WHERE DiscordID = %(id)s"
        cursor.execute(searchcmd, {"id": discordID})
        result = cursor.fetchall()
        cursor.close()
        cnx.close()
        return result

    def AddAnime(self, discordID, AnimeID,title):
        cnx = mysql.connector.connect(user=self.username, password=self.password, host=self.host, port=self.port, database=self.database)
        cursor = cnx.cursor()
        checkforentry = "SELECT AnimeID FROM trackedanime WHERE DiscordID = %(discordID)s AND AnimeID = %(animeID)s"
        cursor.execute(checkforentry, {"discordID": discordID, "animeID": AnimeID})
        if cursor.fetchone() is None:
            searchcmd = "INSERT INTO trackedanime (DiscordID, AnimeID, Title) VALUES (%(discordID)s,%(animeID)s,%(title)s)"
            cursor.execute(searchcmd, {"discordID": discordID, "animeID": AnimeID,"title": title})
            cnx.commit()
        cursor.close()
        cnx.close()

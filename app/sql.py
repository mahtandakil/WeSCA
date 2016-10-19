#!/usr/bin/env python
# -*- coding: utf-8 -*-


import os.path
import sqlite3


#---------------------------------------------------------------------------

class SQLConn():
	
	def __init__(self):
		self.conn = None
		
	def __del__(self):
		self.disconnect()


#---------------------------------------------------------------------------

	def connect(self):

		if self.conn == None:
			self.conn = sqlite3.connect(os.path.join(os.getcwd(), "data", "wesca.db"))
			self.conn.text_factory = str
			self.cursor = self.conn.cursor()		


#---------------------------------------------------------------------------

	def commit(self):
		
		self.conn.commit()


#---------------------------------------------------------------------------

	def disconnect(self):
		
		if not self.conn == None:
			self.conn.close()
			self.conn = None


#---------------------------------------------------------------------------

	def insertIntoWebMapLaunch(self, new_id, date, wp_id):

		command = "INSERT INTO 'WebMapLaunch' VALUES ('" + str(new_id) + "','" + date + "', " + str(wp_id) + ");"

		self.connect()
		self.cursor.execute(command)
		self.commit()


#---------------------------------------------------------------------------

	def insertIntoWebMapData(self, webmap_id, webprofile_id, etype, file_name, user, group, size, date, permissions):

		command = "INSERT INTO 'WebMapData' VALUES (NULL, " + str(webmap_id) + ", " + str(webprofile_id) + ", '" + etype + "', '" + file_name + "', '" + user + "', '" + group + "', '" + str(size) + "', '" + str(date) + "', '" + permissions + "');"

		self.connect()
		self.cursor.execute(command)
		

#---------------------------------------------------------------------------

	def deleteWebMapDataByWebmap_id(self, ident):

		command = "DELETE FROM 'WebMapData' WHERE webmap_id=" + str(ident) + ""

		self.connect()
		self.cursor.execute(command)


#---------------------------------------------------------------------------

	def deleteWebProfileById(self, ident):

		command = "DELETE FROM 'WebProfile' WHERE id=" + str(ident) + ""

		self.connect()
		self.cursor.execute(command)


#---------------------------------------------------------------------------

	def deleteWebMapLauchById(self, ident):

		command = "DELETE FROM 'WebMapLaunch' WHERE id=" + str(ident) + ""

		self.connect()
		self.cursor.execute(command)


#---------------------------------------------------------------------------

	def insertIntoServerProfile(self, name, server, port, protocol, user, password):

		command = "INSERT INTO 'ServerProfile' VALUES (NULL,'" + name + "','" + server + "','" + port + "','" + protocol + "','" + user + "','" + password + "');"

		self.connect()
		self.cursor.execute(command)
		self.commit()
	

#---------------------------------------------------------------------------

	def insertIntoWebProfile(self, name, path, server_id):

		self.connect()
		
		command = "INSERT INTO 'WebProfile' VALUES (NULL,'" + name + "','" + path + "'," + str(server_id) + ");"

		self.connect()
		self.cursor.execute(command)
			

#---------------------------------------------------------------------------

	def insertTempCheckData(self, etype, name, folder, user, group, size, date, permissions):

		self.connect()
		
		command = "INSERT INTO 'TempCheckData' VALUES (NULL, '" + etype + "', '" + name + "', '" + folder + "', '" + user + "', '" + group + "', '" + str(size) + "', '" + str(date) + "', '" + permissions + "');"

		self.connect()
		self.cursor.execute(command)
			

#---------------------------------------------------------------------------

	def getServerProfileByName(self, server_name):
	
		command = "SELECT * FROM 'ServerProfile' WHERE name='" + server_name + "';"
		
		self.connect()
		self.cursor.execute(command)
		result = self.cursor.fetchone()
		
		return result
		

#---------------------------------------------------------------------------

	def countWebMapLaunchByWebProfileId(self, ident):
	
		command = "SELECT COUNT (*) FROM WebMapLaunch WHERE WebProfileId=" + str(ident) + ";"
		
		self.connect()
		self.cursor.execute(command)
		result = self.cursor.fetchone()[0]
		
		return result
		

#---------------------------------------------------------------------------

	def getServerProfile(self):
	
		command = "SELECT * FROM 'ServerProfile';"
		
		self.connect()
		self.cursor.execute(command)
		result = self.cursor.fetchall()
		
		return result
		

#---------------------------------------------------------------------------

	def getWebProfile(self):
	
		command = "SELECT * FROM 'WebProfile';"
		
		self.connect()
		self.cursor.execute(command)
		result = self.cursor.fetchall()
		
		return result
		

#---------------------------------------------------------------------------

	def getServerProfileById(self, server_id):
	
		command = "SELECT * FROM 'ServerProfile' WHERE id=" + str(server_id) + ";"
		
		self.connect()
		self.cursor.execute(command)
		result = self.cursor.fetchone()
		
		return result


#---------------------------------------------------------------------------

	def getLastWebMapLaunchId(self):

		command = "SELECT * FROM 'WebMapLaunch' ORDER BY id DESC LIMIT 1;"

		self.connect()
		self.cursor.execute(command)
		result = self.cursor.fetchone()
		
		try:
			return int(result[0])
		except TypeError:
			return -1


#---------------------------------------------------------------------------

	def getLastCheckOrderByIdDesc(self, data):

		command = "SELECT * FROM 'CheckLaunch' WHERE WebProfileId=" + str(data) + " ORDER BY id DESC;"

		self.connect()
		self.cursor.execute(command)
		result = self.cursor.fetchall()

		return result


#---------------------------------------------------------------------------

	def getTempCheckDataPorLaunchId(self, launch_id):
	
		command = "SELECT * FROM 'CheckData' WHERE web_id='" + str(launch_id) + "';"
	
		self.connect()
		self.cursor.execute(command)
		result = self.cursor.fetchall()
		
		return result
		
		
#---------------------------------------------------------------------------

	def getCheckLaunchByWebProfileIdOrderByIdDesc(self, web_id):

		command = "SELECT * FROM 'CheckLaunch' WHERE WebProfileId='" + web_id + "' ORDER BY id DESC;"

		self.connect()
		self.cursor.execute(command)
		result = self.cursor.fetchall()
		
		return result

	
#---------------------------------------------------------------------------

	def getWebProfileByName(self, web_name):
	
		command = "SELECT * FROM 'WebProfile' WHERE name='" + web_name + "';"
		
		self.connect()
		self.cursor.execute(command)
		result = self.cursor.fetchone()
		
		return result
		

#---------------------------------------------------------------------------

	def getWebMapDataByWebMapId(self, webmap_id):
	
		command = "SELECT * FROM 'WebMapData' WHERE webmap_id=" + str(webmap_id) + ";"
		
		self.connect()
		self.cursor.execute(command)
		result = self.cursor.fetchall()
		
		return result
		

#---------------------------------------------------------------------------

	def getWebMapLauchByWebProfileId(self, ident):
	
		command = "SELECT * FROM 'WebMapLaunch' WHERE WebProfileId=" + str(ident) + ";"
		
		self.connect()
		self.cursor.execute(command)
		result = self.cursor.fetchall()
		
		return result
		

#---------------------------------------------------------------------------

	def getTempCheckData(self):

		command = "SELECT * FROM 'TempCheckData';"
		
		self.connect()
		self.cursor.execute(command)
		result = self.cursor.fetchall()
		
		return result


#---------------------------------------------------------------------------

	def cleanTempCheckData(self):

		command = "DELETE FROM 'TempCheckData';"

		self.connect()
		self.cursor.execute(command)
		self.commit()
		
		
#---------------------------------------------------------------------------

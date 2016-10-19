#!/usr/bin/env python
# -*- coding: utf-8 -*-


from app import sql


#---------------------------------------------------------------------------

class Console():
	
	def __init__(self):
		q=0
		
	def __del__(self):
		q=0
		

#---------------------------------------------------------------------------

	def showFolderAnalized(self, folder):
		
		print folder
	
	
#---------------------------------------------------------------------------

	def showLaunchProfile(self, profile, data):
		
		sizes = [0,0]
		header = ["IDs", "Date"]
		limiter = ""		
		
		sizes[0] = len(header[0])
		sizes[1] = len(header[1])

		print profile
		
		for p in data:
			
			if len(str(p[0])) > sizes[0]:
				sizes[0] = len(str(p[0]))

			if len(p[1]) > sizes[1]:
				sizes[1] = len(p[1])			

		limiter = "+--" + "-"*sizes[0] + "+--" + "-"*sizes[1] + "+"

		print limiter
		print "|", self.adjustString(header[0], "left", sizes[0]),
		print "|", self.adjustString(header[1], "left", sizes[1]) + " |"
		print limiter
		for p in data:
			print "|", self.adjustString(p[0], "left", sizes[0]),
			print "|", self.adjustString(p[1], "left", sizes[1]) + " |"

		print limiter


#---------------------------------------------------------------------------

	def showWebProfiles(self, profiles, server_ids):

		sizes = [0,0,0]
		header = ["Profile", "Path", "Server"]
		limiter = ""
		
		sizes[0] = len(header[0])
		sizes[1] = len(header[1])
		sizes[2] = len(header[2])
		
		for p in profiles:
			
			if len(p[1]) > sizes[0]:
				sizes[0] = len(p[1])

			if len(p[2]) > sizes[1]:
				sizes[1] = len(p[2])

			if len(server_ids[p[3]]) > sizes[2]:
				sizes[2] = len(server_ids[p[3]])

		limiter = "+--" + "-"*sizes[0] + "+--" + "-"*sizes[1] + "+--" + "-"*sizes[2] + "+"
		
		print limiter
		print "|", self.adjustString(header[0], "left", sizes[0]),
		print "|", self.adjustString(header[1], "left", sizes[1]),
		print "|", self.adjustString(header[2], "left", sizes[2]) + " |"
		print limiter
		for p in profiles:
			print "|", self.adjustString(p[1], "left", sizes[0]),
			print "|", self.adjustString(p[2], "left", sizes[1]),
			print "|", self.adjustString(server_ids[p[3]], "left", sizes[2]) + " |"

		print limiter

		
#---------------------------------------------------------------------------

	def showServerProfiles(self, profiles):
		
		sizes = [0,0,0,0,0,0]
		header = ["Profile", "Server", "Port", "Protocol", "User", "Password"]
		limiter = ""
		
		sizes[0] = len(header[0])
		sizes[1] = len(header[1])
		sizes[2] = len(header[2])
		sizes[3] = len(header[3])
		sizes[4] = len(header[4])
		sizes[5] = len(header[5])
		
		for p in profiles:
			
			if len(p[1]) > sizes[0]:
				sizes[0] = len(p[1])

			if len(p[2]) > sizes[1]:
				sizes[1] = len(p[2])

			if len(p[3]) > sizes[2]:
				sizes[2] = len(p[3])

			if len(p[4]) > sizes[3]:
				sizes[3] = len(p[4])

			if len(p[5]) > sizes[4]:
				sizes[4] = len(p[5])

		limiter = "+--" + "-"*sizes[0] + "+--" + "-"*sizes[1] + "+--" + "-"*sizes[2] + "+--" + "-"*sizes[3] + "+--" + "-"*sizes[4] + "+--" + "-"*sizes[5] + "+"
		
		print limiter
		print "|", self.adjustString(header[0], "left", sizes[0]),
		print "|", self.adjustString(header[1], "left", sizes[1]),
		print "|", self.adjustString(header[2], "left", sizes[2]),
		print "|", self.adjustString(header[3], "left", sizes[3]),
		print "|", self.adjustString(header[4], "left", sizes[4]),
		print "|", self.adjustString(header[5], "left", sizes[5]) + " |"
		print limiter
		for p in profiles:
			print "|", self.adjustString(p[1], "left", sizes[0]),
			print "|", self.adjustString(p[2], "left", sizes[1]),
			print "|", self.adjustString(p[3], "left", sizes[2]),
			print "|", self.adjustString(p[4], "left", sizes[3]),
			print "|", self.adjustString(p[5], "left", sizes[4]),
			
			if p[6] == None or p[6] == "":
				passwd = "No"
			else:
				passwd = "Yes"

			print "|", self.adjustString(passwd, "left", sizes[5]) + " |"

		print limiter


#---------------------------------------------------------------------------

	def adjustString(self, string, align, size):
		
		string = str(string)
		
		if align == "left":
			while len(string) < size:
				string += " "

		
		return string


#---------------------------------------------------------------------------

	def askYesNo(self, question):
		
		print question
		values = raw_input("y/n> ").lower()
		
		if values == "y" or values == "yes":
			return True
		else:
			return False


#---------------------------------------------------------------------------

#!/usr/bin/env python
# -*- coding: utf-8 -*-


from ftplib import FTP
import util


from datetime import datetime
import re


#---------------------------------------------------------------------------

class FTPConn():
	
	def __init__(self):
		self.ftp = None
		
	def __del__(self):
		self.disconnect()
		
		
#---------------------------------------------------------------------------

	def connect(self, server, port, user, password, path):
		
		self.ftp = FTP(server)
		self.ftp.login(user, password)
		
		if path != None:
			self.ftp.cwd(path)
			

#---------------------------------------------------------------------------

	def disconnect(self):
		
		if self.ftp != None:
			self.ftp.quit()
			self.ftp = None
			
		
#---------------------------------------------------------------------------

	def listDir(self, folder):
		
		ftp_list = []
		ftp_response = []

		expression_permissions = "^(d|-)(r|w|x|t|-){9}"
		expression_unk = "( )*(\d)+( )*"
		expression_user_group = "( )*(\w|-)+( )*(\w|-)+( )*"
		expression_size = "( )*(\d)+( )*"
		expression_mod_date = "([a-zA-Z]){3}( )+(\d)+( )(\d)+\:(\d)+"
		rec_ep = re.compile(expression_permissions)
		rec_u = re.compile(expression_unk)
		rec_ug = re.compile(expression_user_group)
		rec_s = re.compile(expression_unk)
		rec_md = re.compile(expression_mod_date)

		self.ftp.cwd(folder)	
		self.ftp.retrlines('LIST', ftp_response.append)
				
		for elem in ftp_response:
			
			match = rec_ep.search(elem)
			permissions = match.group()
			elem = util.cleanSpaces(elem[len(permissions):])

			match = rec_u.search(elem)
			unk = match.group()
			elem = util.cleanSpaces(elem[len(unk):])
			unk = int(unk)
			
			match = rec_ug.search(elem)
			user_group = match.group()
			user_group = user_group.split(" ")
			user = user_group[0]
			group = user_group[1]
			elem = util.cleanSpaces(elem[len(user):])
			elem = util.cleanSpaces(elem[len(group):])

			match = rec_s.search(elem)
			size = match.group()
			elem = util.cleanSpaces(elem[len(size):])
			size = int(size)

			match = rec_md.search(elem)
			mod_date = match.group()
			elem = util.cleanSpaces(elem[len(mod_date):])
			mod_date =  datetime.strptime(mod_date[:-1], '%b %d %H:%M')

			file_name = elem
			
			
			if not (file_name == '.' or file_name == '..'):
				ftp_list.append([file_name, permissions[0], size, user, group, permissions[1:], mod_date, unk])
		
		return ftp_list
			
		
#---------------------------------------------------------------------------

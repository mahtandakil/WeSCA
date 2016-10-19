#!/usr/bin/env python
# -*- coding: utf-8 -*-


from app import console
from app import sql
from app import ftp


import time
import os.path


#-----------------------------------------------------------------------

class Core:
	
	def __init__(self):
		self.inputs = None
		self.web_map = None
		self.interface = None
		self.sql = sql.SQLConn()
		self.ftp = ftp.FTPConn()
		self.counter = 0
		self.current_webmap = None
		self.previous_webmap = None
		
	def __del__(self):
		q=0


#-----------------------------------------------------------------------

	def start(self, inputs):

		self.inputs = inputs
		self.interface = console.Console()

		if(inputs['commands'].count('help') > 0):
			self.printHelp()

		if(inputs['commands'].count('show-server-profiles') > 0):
			self.showServerProfiles()

		if(inputs['commands'].count('show-web-profiles') > 0):
			self.showWebProfiles()

		if(inputs['commands'].count('show-webmaps') > 0):
			self.showPreviousWebmaps()

		if(inputs['commands'].count('create-server-profile') > 0):
			self.createServerProfile()

		if(inputs['commands'].count('create-web-profile') > 0):
			self.createWebProfile()

		if(inputs['commands'].count('webmap') > 0):
			self.webmap()

		if(inputs['commands'].count('compare-webmaps') > 0):
			self.compareWebmaps()

		if(inputs['commands'].count('delete-webmap') > 0):
			self.deleteWebmap()

		if(inputs['commands'].count('delete-web-profile') > 0):
			self.deleteWebProfile()


#-----------------------------------------------------------------------

	def printHelp(self):

		print """
WeSCA 0.3
		
COMMANDS:
		
--compare-webmaps
    Compares two different webmaps
    Requieres: -id1, -id2, -of

--create-server-profile
    Creates a new profile for an specific web server
    Requieres: -server, -port, -user, -password, -profile-server-name

--create-web-profile
    Creates a new profile for an specific web site in a server
    Requieres: -path, -profile-web-name, -profile-server-name

--delete-webmap
    Deletes a previously stored webmap
    Requieres: -id

--delete-web-profile
    Deletes a web profile and its linked webmaps
    Requieres: -profile-web-name

--help
    Shows this view

--show-server-profiles
    Shows a list with all the stored server profiles

--show-web-profiles
    Shows a list with all the stored web profiles

--show-webmaps
    Shows a list with all the webmaps stored from previous checks
    Requieres: -profile-web-name
    
--webmap
    Looks for modifications
    Requieres: -type[online|changes|backup], -profile-web-name

"""


#-----------------------------------------------------------------------

	def deleteWebProfile(self):
		
		error = False
		
		try:
			web_name = self.inputs["args"]["profile-web-name"]

		except KeyError:
			error = True
			print "ERROR retrieving information, missed value"

		if not error:	
			
			web_id = self.sql.getWebProfileByName(web_name)[0]
			webmaps = self.sql.getWebMapLauchByWebProfileId(web_id)
			
			for wm in webmaps:
				self.sql.deleteWebMapDataByWebmap_id(wm[0])
				self.sql.deleteWebMapLauchById(wm[0])
			
			self.sql.deleteWebProfileById(web_id)
			
			self.sql.commit()
			
			self.interface.message("Web profile deleted")
			
			
#-----------------------------------------------------------------------

	def deleteWebmap(self):
		
		error = False
		
		try:
			ident = self.inputs["args"]["id"]

		except KeyError:
			error = True
			print "ERROR retrieving information, missed value"

		if not error:	
			
			self.sql.deleteWebMapDataByWebmap_id(ident)
			self.sql.deleteWebMapLauchById(ident)
			self.sql.commit()
			
			self.interface.message("Webmap deleted")
	
	
#-----------------------------------------------------------------------

	def compareWebmaps(self):

		error = False
		new = None
		lost = None
		versions = None
		
		try:
			id1 = self.inputs["args"]["id1"]
			id2 = self.inputs["args"]["id2"]
			path = self.inputs["args"]["of"]

		except KeyError:
			error = True
			print "ERROR retrieving information, missed value"
			
		if not error:
			
			webmap1 = self.loadNormalizedWebMap(id1)
			webmap2 = self.loadNormalizedWebMap(id2)

			print
			print "Webmap 1:", len(webmap1)
			print "Webmap 2:", len(webmap2)

			new = self.searchNewElements(webmap1, webmap2)
			print "New items:", len(new)
			lost = self.searchLostElements(webmap1, webmap2)
			print "Lost items:", len(lost)
			versions = self.compareVersions(webmap1, webmap2)
			print "Modified items:", len(versions)

			self.exportWebMapComparison(path, new, lost, versions)
			

#-----------------------------------------------------------------------

	def exportWebMapComparison(self, path, new, lost, versions):
		
		new_list = []
		lost_list = []
		versions_list = []
		
		for n in new:
			new_list.append(n)
		for l in lost:
			lost_list.append(l)
		for v in versions:
			versions_list.append(v)
		new_list.sort()
		lost_list.sort()
		versions_list.sort()
		
		f = open(path, "w")
		
		f.write("New files: " + str(len(new)) + "\n")
		for nl in new_list:
			f.write(nl["file"] + "\n")
		f.write("\n")

		f.write("Lost files: " + str(len(lost)) + "\n")
		for ll in lost_list:
			f.write(ll["file"] + "\n")
		f.write("\n")

		f.write("Modified files: " + str(len(versions)) + "\n")
		for vl in versions_list:
			output = vl["data1"]["file"] + " (" + vl["mismatch"] + ": " + vl["data1"][vl["mismatch"]] + " <> " + vl["data2"][vl["mismatch"]] + " )" + "\n"
			f.write(output)
		
		f.close()


#-----------------------------------------------------------------------

	def compareVersions(self, webmap1, webmap2):
		
		versions = []
		
		for wm1 in webmap1:
			
			if webmap2.has_key(wm1):
				data1 = webmap1[wm1]
				data2 = webmap2[wm1]
				
				changed = False
				
				if not data1["file"] == data2["file"]:
					versions.append({"data1":webmap1[wm1], "data2":webmap2[wm1], "mismatch":"file"})
				if not data1["etype"] == data2["etype"]:
					versions.append({"data1":webmap1[wm1], "data2":webmap2[wm1], "mismatch":"etype"})
				if not data1["user"] == data2["user"]:
					versions.append({"data1":webmap1[wm1], "data2":webmap2[wm1], "mismatch":"user"})
				if not data1["group"] == data2["group"]:
					versions.append({"data1":webmap1[wm1], "data2":webmap2[wm1], "mismatch":"group"})
				if not data1["size"] == data2["size"]:
					versions.append({"data1":webmap1[wm1], "data2":webmap2[wm1], "mismatch":"size"})
				if not data1["date"] == data2["date"]:
					versions.append({"data1":webmap1[wm1], "data2":webmap2[wm1], "mismatch":"date"})
				if not data1["permissions"] == data2["permissions"]:
					versions.append({"data1":webmap1[wm1], "data2":webmap2[wm1], "mismatch":"permissions"})
				
		return versions


#-----------------------------------------------------------------------

	def searchLostElements(self, webmap1, webmap2):

		lost = []
		
		for wm1 in webmap1:
			
			if not webmap2.has_key(wm1):
				lost.append(webmap1[wm1])		
		
		return lost

#-----------------------------------------------------------------------

	def searchNewElements(self, webmap1, webmap2):
		
		new = []
		
		for wm2 in webmap2:
			
			if not webmap1.has_key(wm2):
				new.append(webmap2[wm2])			
			
		return new


#-----------------------------------------------------------------------

	def showPreviousWebmaps(self):
	
		error = False
		
		try:
			web_name = self.inputs["args"]["profile-web-name"]

		except KeyError:
			error = True
			print "ERROR retrieving information, missed value"
			
		if not error:
			web_data = self.sql.getWebProfileByName(web_name)
			web_id = int(web_data[0])
			data = self.sql.getWebMapLauchByWebProfileId(web_id)
			
			self.interface.showLaunchProfile(web_data[1], data)



#-----------------------------------------------------------------------

	def createServerProfile(self):
		
		error = False
		
		try:
			name = self.inputs["args"]["profile-server-name"]
			server = self.inputs["args"]["server"]
			port = self.inputs["args"]["port"]
			user = self.inputs["args"]["user"]
			password = self.inputs["args"]["password"]
			
			protocol = "FTP"

		except KeyError:
			error = True
			print "ERROR creating server profile, missed value"

		if not error:
			self.sql.insertIntoServerProfile(name, server, port, protocol, user, password)


#-----------------------------------------------------------------------

	def createWebProfile(self):
		
		error = False
		
		try:
			path = self.inputs["args"]["path"]
			name = self.inputs["args"]["profile-web-name"]
			server_name = self.inputs["args"]["profile-server-name"]
			
			protocol = "FTP"

		except KeyError:
			error = True
			print "ERROR creating web profile, missed value"

		if not error:
			server_id = self.sql.getServerProfileByName(server_name)[0]
			self.sql.insertIntoWebProfile(name, path, server_id)
			self.sql.commit()
			print "Profile created"
			

#-----------------------------------------------------------------------

	def webmap(self):

		error = False
		
		current_dt =  time.strftime("%c")
		
		try:
			analizer = self.inputs["args"]["type"]
			web_name = self.inputs["args"]["profile-web-name"]


		except KeyError:
			error = True
			print "ERROR creating server profile, missed value"

		else:
			if not (self.inputs["args"]["type"]=="online" or self.inputs["args"]["type"]=="changes" or self.inputs["args"]["type"]=="backup"):
				error = False

		if not error:
			
			new_map_id = self.sql.getLastWebMapLaunchId() + 1
			
			web_data = self.sql.getWebProfileByName(web_name)
			web_id = web_data[0]
			server_id = web_data[3]
			server_data = self.sql.getServerProfileById(server_id)

			self.connectToServer(server_data, web_data)
			webmap = self.createWebMap(server_data, web_data)
			self.ftp.disconnect()
			
			webmap = self.normalizeWebMap(webmap)
			self.saveWebMap(new_map_id, web_id, current_dt, webmap)


#-----------------------------------------------------------------------

	def normalizeWebMap(self, webmap):
		
		normalized_webmap = []
		
		content = webmap["content"]
		
		for c in content:

			register = {"file":content[c]["folder"]+"/"+content[c]["name"], "etype":content[c]["etype"], "user":content[c]["user"], "group":content[c]["group"], "size":content[c]["size"], "date":content[c]["date"], "permissions":content[c]["permissions"]}
			normalized_webmap.append(register)

		for c in content:
			if not content[c]["content"] == None:
				normalized_submap = self.normalizeWebMap(content[c])
				normalized_webmap += normalized_submap
		
		return normalized_webmap

		
#-----------------------------------------------------------------------

	def saveWebMap(self, map_id, web_id, launch_date, normalized_webmap):

		self.sql.insertIntoWebMapLaunch(map_id, launch_date, web_id)

		for nwm in normalized_webmap:
			self.sql.insertIntoWebMapData(map_id, web_id, nwm["etype"], nwm["file"], nwm["user"], nwm["group"], nwm["size"], nwm["date"], nwm["permissions"])

		self.sql.commit()
		

#-----------------------------------------------------------------------

	def loadNormalizedWebMap(self, webmap_id): 
		
		webmap = {}
		data = self.sql.getWebMapDataByWebMapId(webmap_id)

		for d in data:
			webmap[d[4]] = {"file":d[4], "etype":d[3], "user":d[5], "group":d[6], "size":d[7], "date":d[8], "permissions":d[9]}

		return webmap
		

#-----------------------------------------------------------------------

	def loadNormalizedCheckTemp(self): 
		
		webmap = []
		data = self.sql.getTempCheckData()
		
		for d in data:
			webmap.append({"file":d[3]+"/"+d[2], "etype":d[1], "user":d[4], "group":d[5], "size":d[6], "date":d[7], "permissions":d[8]})

		return webmap
		

#-----------------------------------------------------------------------

	def connectToServer(self, server_data, web_data):
		
		self.ftp.connect(server_data[2], server_data[3], server_data[5], server_data[6], web_data[2])
	
	
#-----------------------------------------------------------------------

	def createWebMap(self,server_data, web_data):
		
		map_element_model = {"etype":None, "name":None, "permissions":None, "user":None, "group":None, "size":None, "date":None, "folder":None, "content":None}
		
		root = map_element_model.copy()
		root["etype"] = "R"
		root["name"] = "/" + web_data[2]

		root["content"] = self.getFolderContent(root["name"], root, map_element_model)

		return root
		

#-----------------------------------------------------------------------

	def getFolderContent(self, folder, parent, model):
		
		self.counter += 1
		self.interface.showFolderAnalized(folder)

		content = self.ftp.listDir(folder)
		folder_content = {}
		
		for c in content:
			file_name = c[0]
			etype = c[1]
			size = c[2]
			user = c[3]
			group = c[4]
			permissions = c[5]
			mod_date = c[6]
			
			folder_content[file_name] = model.copy()
			folder_content[file_name]["etype"] = etype
			folder_content[file_name]["name"] = file_name
			folder_content[file_name]["permissions"] = permissions
			folder_content[file_name]["user"] = user
			folder_content[file_name]["group"] = group
			folder_content[file_name]["size"] = size
			folder_content[file_name]["date"] = mod_date
			folder_content[file_name]["folder"] = folder

		for fc in folder_content:
			
			if folder_content[fc]["etype"] == "d":
				new_folder = folder_content[fc]["folder"] + "/" + folder_content[fc]["name"]
				folder_content[fc]["content"] = self.getFolderContent(new_folder, folder_content[file_name], model)
		
		return folder_content


#-----------------------------------------------------------------------

	def saveWebMapToTemp(self, web_map):
		
		self.saveFolderToTemp(web_map["content"])
		
		self.sql.commit()
		self.sql.disconnect()


#-----------------------------------------------------------------------

	def saveFolderToTemp(self, folder_map):
		
		for elem in folder_map:

			self.sql.insertTempCheckData(folder_map[elem]["etype"], folder_map[elem]["name"], folder_map[elem]["folder"], folder_map[elem]["user"], folder_map[elem]["group"], folder_map[elem]["size"], folder_map[elem]["date"], folder_map[elem]["permissions"])

			if folder_map[elem]["etype"] == "d" and folder_map[elem]["content"] != None:
				self.saveFolderToTemp(folder_map[elem]["content"])


#-----------------------------------------------------------------------

	def loadCurrentWebMap(self):
		
		self.current_webmap = []
		
		sql_current_webmap = self.sql.getTempCheckData()
		
		for elem in sql_current_webmap:
			full_name = elem[3] + "/" + elem[2]
			etype = elem[1]
			user = elem[4]
			group = elem[5]
			size = elem[6]
			mod_date = elem[7]
			permissions = elem[8]

			self.current_webmap.append({"full_name":full_name, "etype":etype, "user":user, "group":group, "size":size, "mod_date":mod_date, "permissions":permissions})
		

#-----------------------------------------------------------------------

	def getWebProfilesId(self, check_name):
		
		web_id = self.sql.getWebProfileByName(check_name)[0]		
		return web_id


#-----------------------------------------------------------------------

	def showServerProfiles(self):
		
		profiles = self.sql.getServerProfile()
		self.interface.showServerProfiles(profiles)
		
		
#-----------------------------------------------------------------------

	def showWebProfiles(self):
		
		profiles = self.sql.getWebProfile()
		server_ids = {}
		webs = []
		
		for p in profiles:
			s = self.sql.getServerProfileById(p[3])
			server_ids[s[0]] = s[1]
			webmaps = self.sql.countWebMapLaunchByWebProfileId(p[0])
			webs.append([p[0], p[1], p[2], p[3], webmaps])

		self.interface.showWebProfiles(webs, server_ids)
		
		
#-----------------------------------------------------------------------




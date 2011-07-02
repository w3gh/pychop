# author = uakf.b
# version = 1.0
# name = getgames
# fullname = plugins/pychop/getgames
# description = An example python plugin to retrieve a list of games.
# help = Use !getgames to get the list of games (no access required).

commands = ("getgames", "plugins/pychop/getgames")

import host
import MySQLdb
import plugindb

cursor = 0

def dbReady():
	global cursor
	cursor = plugindb.dbconnect()
	
def init():
	host.registerHandler('ProcessCommand', onCommand, True)
	plugindb.init()
	plugindb.notifyReady(dbReady)
	
def deinit():
	host.unregisterHandler(onCommand)
	plugindb.deinit()

def onCommand(bnet, user, command, payload, nType):
	if command in commands:
		cursor.execute("SELECT gamename, slotstaken, slotstotal FROM gamelist");
		result_set = cursor.fetchall()
		result_string = "Current games: "
		
		num_games = 0
		
		for row in result_set:
			if row[0] != "":
				result_string += str(row[0]) + " (" + str(row[1]) + "/" + str(row[2]) + "), "
				num_games += 1
		
		if num_games > 0:
			result_string = result_string[:-2]
		else:
			result_string += "none"
		
		bnet.queueChatCommand(result_string, user.getName(), nType == 1)
		return False
		
	return True

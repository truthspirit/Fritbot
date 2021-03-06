from twisted.python import log
import zope.interface
 	
def response(f):
	def responder(self, bot, room, user, args):
		out = f(self, bot, room, user, args)

		if out is None:
			return False

		if type(out) == type(u'') or type(out) == type(''):
			if room is not None:
				room.send(out)
			else:
				user.send(out)
			return True

		log.msg("Invalid type returned by function wrapped by @response: {0} - {1}".format(out, type(out)))
		return False

	return responder

def admin(f):
	def admincheck(self, bot, room, user, args):
		if user['admin']:
			return f(self, bot, room, user, args)
		else:
			log.msg("User {0} ({1}) attempted to run a function without authorization.".format(user['nick'], user.uid))
			user.send("That function requires you to be an administrator. You aren't.")
			return True

	return admincheck

def room_only(f):
	def roomcheck(self, bot, room, user, args):
		if room is not None:
			return f(self, bot, room, user, args)
		else:
			user.send("That function only works in a room.")
			return True

	return roomcheck

def user_only(f):
	def roomcheck(self, bot, room, user, args):
		if room is None:
			return f(self, bot, room, user, args)
		else:
			user.send("That function only works directly with me, not in a room. Why don't you try it now?")
			return True

	return roomcheck

class IModule(zope.interface.Interface):
	
	name=zope.interface.Attribute("Name of the module")
	description=zope.interface.Attribute("Description of the module")
	author=zope.interface.Attribute("Author's name, email address if desired.")

	def register(self):
		"""Functionality to register the module with the intent service."""
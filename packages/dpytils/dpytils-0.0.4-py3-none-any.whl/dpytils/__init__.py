import discord
import random

class discordPermissions:

	def __init__(self, data):
		self.perms_nice = data["perms_nice"]
		self.perms_true = data["perms_true"]
		self.perms_false = data["perms_false"]
		self.perms_raw = data["perms_raw"]

class utils:
	
	def __init__(self):
		pass

	def randcolor(self):
		return int("%06x" % random.randint(0, 0xFFFFFF), 16)

	def permsfromvalue(self, value):
		perms = discord.Permissions(permissions=int(value))
		perms_true = sorted([x for x,y in dict(perms).items() if y])
		perms_false = sorted([x for x,y in dict(perms).items() if not y])
		nice_perms = ""
		perms_true_nice = ["\u2705 `" + s for s in perms_true]
		perms_false_nice = ["\u274c `" + s for s in perms_false]
		perms_combined = sorted(perms_true_nice + perms_false_nice, key=lambda x: x.strip('\u2705\u274c'))
		for perm in perms_combined:
			nice_perms = nice_perms + perm.replace("_", " ").capitalize() + "`\n"
		return discordPermissions({
			'perms_nice': nice_perms,
			'perms_true': perms_true,
			'perms_false': perms_false,
			'perms_raw': perms
		})

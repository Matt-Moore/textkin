import random
import xml.etree.ElementTree as ET

class World:
	def __init__(self,path='data/'):
		self.data = {'items':ET.parse(path + 'items.xml').getroot(),'monsters':ET.parse(path + 'monsters.xml').getroot()}
		
		self.items = {}
		self.rooms = {}
		self.monsters = {}
		
		# CREATE items
		# CREATE items : weapons
		for item in self.data['items'].find('weapons'):
			self.items[item.get('id')] = Weapon(item)
		# CREATE items : armour
		for item in self.data['items'].find('armour'):
			self.items[item.get('id')] = Armour(item)
						
		# CREATE monsters
		for monster in self.data['monsters']:
			self.monsters[monster.get('id')] = Monster(monster)
			
		
		# SHUFFLE items
		self.deckItems = list(self.items)
		random.shuffle(self.deckItems)
		
	def drawDeck(self,numDraws):
		for i in range(numDraws):
			player.invPickup(self.items[self.deckItems[0]])
			self.deckItems.remove(self.deckItems[0])
			
		
		
class Item:
	def __init__(self,dataInit):
		stats = dataInit.find('stats')
		
		self.id = dataInit.get('id')
		self.name = dataInit.find('name').text
		self.weight = int(stats.find('weight').text)
		
		self.attack = 0
		self.ac = 0
		self.slot = None
		
		stat = stats.find('attack')
		if (not stat is None):
			self.attack = int(stat.text)

		stat = stats.find('ac')
		if (not stat is None):
			self.ac = int(stat.text)

		stat = stats.find('slot')
		if (not stat is None):
			self.slot = stat.text
		
class Weapon(Item):
	def __init__(self,dataInit):
		super().__init__(dataInit)

class Armour(Item):
	def __init__(self,dataInit):
		super().__init__(dataInit)


		
class Character:
	def actAttack(self,enemy):
		if (type(self).__name__ == "Player"):
			pObj = self
			eObj = enemy
			
			order = 'player'
			order = 'enemy'
		else:
			pObj = enemy
			eObj = self
			
			order = 'enemy'
			
		pAtk = pObj.level + self.stats['attack']
		pDef = pObj.level + self.stats['ac']
		eAtk = eObj.stats['attack']
		eDef = eObj.stats['attack']
		
		pAtkDif = pAtk - eDef
		eAtkDif = eAtk - pDef
		
		if (order == 'player'):
			if (pAtkDif > 0):
				print("  Your attack deals {} damage to the {}.".format(pAtkDif,eObj.name))
				eObj.stats['hp'][0] -= pAtkDif
			else:
				print("  Your attack misses the {}.".format(eObj.name))
				
			if (eAtkDif > 0):
				print("  The {} attacks back, dealing {} damage.".format(eObj.name,eAtkDif))
				pObj.stats['hp'][0] -= eAtkDif
			else:
				print("  The {} attacks back, but misses.".format(eObj.name))
		
		else:
			if (eAtkDif > 0):
				print("  The {} attacks you, dealing {} damage.".format(eObj.name,eAtkDif))
				pObj.stats['hp'][0] -= eAtkDif
			else:
				print("  The {} attacks you, but misses.".format(eObj.name))
		
			if (pAtkDif > 0):
				print("  You attack back, dealing {} damage to the {}.".format(pAtkDif,eObj.name))
				eObj.stats['hp'][0] -= pAtkDif
			else:
				print("  You attack back, but miss the {}.".format(eObj.name))
				
		
		
		
		
		
		
		print (pObj.stats['hp'][0],eObj.stats['hp'][0])
			
		if (pObj.stats['hp'][0] <= 0 and eObj.stats['hp'][0] <= 0):
			if (order == 'player'):
				pObj.stats['hp'][0] = 1
				print("  You manage to slay the {}, but you are left on the brink of death.".format(eObj.name))
			else:
				print("  Your last act has been to kill the {}.".format(eObj.name))
				print("=== END GAME ===")
		elif (pObj.stats['hp'][0] <= 0):
			print("  The {} has slain you.".format(eObj.name))
			print("=== END GAME ===")
		
		elif (eObj.stats['hp'][0] <= 0):
			print("  You have defeated the {}.".format(eObj.name))
			eObj.actDie()
		
		
		
		
		
		
		

class Player(Character):
	def __init__(self):
		self.name = "Sir Cheese"
		self.level = 1
		
		self.inventory = []
		self.equipped = []
		self.slot = {'head':None,'torso':None,'legs':None}
		
		self.stats = {'attack':0,'ac':0,'charisma':0,'weight':[0,7],'hp':[10,10]}
		
	def invPickup(self,item):
		self.inventory.append(item)
		self.inventory.sort(key=lambda item:item.name)


	def invLook(self):
		if (len(self.inventory)):
			print("  You are carrying: {}.\n".format(", ".join(map(lambda item: item.name,self.inventory))))
		else:
			print("  Your inventory is empty.\n")

	def invEquip(self,itemName):
		item = list(filter(lambda item: item.name.lower() == itemName.lower(),self.inventory))
		
		if (len(item)):
			item = item[0]
			if (self.stats['weight'][0] + item.weight <= self.stats['weight'][1]):
				if (not item.slot is None):
					if (not self.slot[item.slot] is None):
						self.invUnequip(self.slot[item.slot].name)
					self.slot[item.slot] = item

				self.equipped.append(item)
				self.equipped.sort(key=lambda item:item.name)
				self.inventory.remove(item)
				
				self.stats['attack'] += item.attack
				self.stats['ac'] += item.ac
				self.stats['weight'][0] += item.weight
			
				print("  You equip the {}.\n".format(item.name))
			else:
				print("  The {} is too heavy for you to equip.\n".format(item.name))
		else:
			print("  There is no {} in your inventory.\n".format(itemName))

	def invUnequip(self,itemName):
		item = list(filter(lambda item: item.name.lower() == itemName.lower(),self.equipped))
		
		if (len(item)):
			item = item[0]
		
			self.inventory.append(item)
			self.inventory.sort(key=lambda item:item.name)
			self.equipped.remove(item)
			
			self.stats['attack'] -= item.attack
			self.stats['ac'] -= item.ac
			self.stats['weight'][0] -= item.weight
			print("  You remove the {}.\n".format(item.name))
		else:
			print("  You don't have {} equipped.\n".format(itemName))
			

			
			
			
class Monster(Character):
	def __init__(self,dataInit):
		stats = dataInit.find('stats')
		
		self.id = dataInit.get('id')
		self.name = dataInit.find('name').text


		self.stats = {'attack':int(stats.find('attack').text),'ac':int(stats.find('attack').text),'charisma':int(stats.find('attack').text),'hp':[int(stats.find('hp').text),int(stats.find('hp').text)],'treasure':int(stats.find('treasure').text)}

		


		
		self.level = 0
		self.aggro = False
		
		stat = stats.find('level')
		if (not stat is None):
			self.level = int(stat.text)
		
		stat = stats.find('aggro')
		if (not stat is None and stat == 'true'):
			self.aggro = True
			
	def actDie(self):
		
		if (self.stats['treasure']):
			if (self.stats['treasure'] > 1):
				print("  Searching the corpse of the {}, you find {} treasures.".format(self.name,self.stats['treasure']))
			else:
				print("  Searching the corpse of the {}, you find 1 treasure.".format(self.name))
			
			world.drawDeck(self.stats['treasure'])
			
		else:
			print("  Searching the corpse of the {}, you find no treasures.".format(self.name))
			
		
		
		
			
		'''	
			<attack>3</attack>
			<treasure>1</treasure>
			<level>1</level>
			
		'''	
			
			
			
			
			
'''

				
				
class Item:
	def __init__(self,dataInit):
		self.id = dataInit.get('id')
		self.name = dataInit.find('name').text
		self.description = dataInit.find('description').text
		
		self.movable = True
		self.container = False
		
		self.owner = abyss
		self.inventory = []
		abyss.inventory.append(self)
		
		
		if (dataInit.find('flags').find('movable') is not None and dataInit.find('flags').find('movable').text == 'False'):
			self.movable = False
		
		if (dataInit.find('flags').find('container') is not None and dataInit.find('flags').find('container').text == 'True'):
			self.container = True

	def actMove(self,target):
		if (self.movable or self.owner == abyss):
			if (target.container or target == abyss):
				self.owner.inventory.remove(self)
				self.owner = target
				
				self.owner.inventory.append(self)
				self.owner.inventory.sort(key=lambda item:item.name)
				
				return [True,self.name]
			else:
				return [False,"nofit"]
		else:
			return [False,"nomove"]
		
	def listInventory(self):
		if (self.container):
			if (len(self.inventory)):
				return [True,", ".join(map(lambda item: item.name,self.inventory))]
			else:
				return [True,""]
		else:
			return [False,"nofit".format(self.name)]
				
				
				
'''
			
'''				
class Player:
	def __init__(self):
		
		self.name = 'Cheese' #input("Enter your name:\n")
		
		self.container = True
		
		
		self.curRoom = world.rooms['0']
		self.inventory = []
	
	# ACTIONS (look)
	
	def actLook(self):
		print("  {} : \n  Looking around, you see {}".format(self.curRoom.name,self.curRoom.description))
		roomInventory = self.curRoom.listInventory()
		if (roomInventory[0]):
			print("  You see: {}".format(roomInventory[1]))
		
	def actLookin(self,objectName):
		container = list(filter(lambda container: container.name.lower() == objectName.lower(),self.curRoom.inventory + self.inventory))

		if (len(container)):
			container = container[0]
			containerInventory = container.listInventory()
			if (containerInventory[0] and len(containerInventory[1])):
				print("  The {} contains: {}.".format(container.name,containerInventory[1]))
			elif (containerInventory[0]):
				print("  The {} has nothing of value.".format(container.name))
			else:
				print("  Nothing can be stored inside the {}".format(container.name))
		else:
			print("  You can't see {}.".format(objectName))
			
	def actLookat(self,objectName):
		item = list(filter(lambda item: item.name.lower() == objectName.lower(),self.curRoom.inventory + self.inventory))
		
		if (len(item)):
			item = item[0]
			print("  The {} {}".format(item.name,item.description))
		else:
			print("  You can't see {}.".format(objectName))
			
			


	
	# ACTIONS (misc)
	
	def actPickup(self,objectName):
		item = list(filter(lambda item: item.name.lower() == objectName.lower(),self.curRoom.inventory))
		
		if(len(item)):
			item = item[0]
			itemMove = item.actMove(self)
			if (itemMove[0]):
				print("  You pick up the {}".format(item.name))
			else:
				print("  You can't pick up the {}".format(item.name))
		else:
			print("  You can't see {}.".format(objectName))
			




	
		
		
		
	
	# INVENTORY
	
	def invLook(self):
		if (len(self.inventory)):
			print("  You are carrying: {}.".format(", ".join(map(lambda item: item.name,self.inventory))))
		else:
			print("  Your inventory is empty.")
			
		
				
				
				
				
'''				
				
				




		

		
		
		
class Room:
	def __init__(self,dataInit):
		self.id = dataInit.get('id')
		self.name = dataInit.find('name').text
		self.description = dataInit.find('description').text
		
		self.movable = False
		self.container = True
		
		self.inventory = []
		
		'''
		if (dataInit.find('flags').find('movable') is not None and dataInit.find('flags').find('movable').text == 'False'):
			self.movable = False
		
		if (dataInit.find('flags').find('container') is not None and dataInit.find('flags').find('container').text == 'True'):
			self.container = True
		'''
		
		
		
	def listInventory(self):
		if (len(self.inventory)):
			return [True,", ".join(map(lambda item: item.name,self.inventory))]
		else:
			return [False,""]
		



	
		
		
		
print("\n")
# CREATE GAME WORLD
# abyss = Abyss()	
world = World()
# CREATE PLAYER CHARACTER	
player = Player()


print("--Picking up Items\n")
player.invPickup(world.items['w001'])
'''
player.invPickup(world.items['weapons']['w002'])
player.invPickup(world.items['armour']['ah001'])
player.invPickup(world.items['armour']['ah002'])
'''
print("Inventory")
player.invLook()

print("== {}\n".format(player.stats))

print("Equip Wooden SwoRD")
player.invEquip("Wooden SwoRD")

print("===")
print("World Deck: {}".format(world.deckItems))
print("Inventory: {}".format(player.inventory))
print("===\n")

print("Attack Bunny")
player.actAttack(world.monsters["m001"])

print("Attack Bunny")
player.actAttack(world.monsters["m001"])

print("\n\n===")
print("World Deck: {}".format(world.deckItems))
print("Inventory: {}".format(player.inventory))
print("===\n")




'''	
print("Look")

player.actLook()

print("Inventory")

player.invLook()

print('Look in Blank key')	

player.actLookin('Blank key')
	
print('Look in bureau')	

player.actLookin('bureau')
	
print('Look in FANCY DESK')	

player.actLookin('FANCY DESK')

print('Pick up fancy key')	

player.actPickup('fancy key')

print('Pick up Blank key')	

player.actPickup('blank key')
	
print('Pick up Bureaus')	

player.actPickup('Bureaus')
	
print('Pick up Bureau')	

player.actPickup('Bureau')
	
print("Look")

player.actLook()

print("Look at Bureau")

player.actLookat('Bureau')

print("Look at Bureaus")

player.actLookat('Bureaus')

print("Inventory")

player.invLook()

'''	
	
	
	

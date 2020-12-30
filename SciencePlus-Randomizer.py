# Planned Features
# 1. Build new tech trees using TechTree.cfg and a seed
# 2. Allow user to type in a seed
# 3. Allow user to generate a random seed
# 4. Hide tech tree nodes after the next node

# Possible Later Features
# 1. Randomize planets, experiment descriptions, starting Kerbals, contracts...
# 2. Randomize science colors
# 3. Starting location could be randomized amongst the launch pads or even planets


# Considerations
# 1. Game must be playable, ergo the starting node either needs to be static or heavily considered
# 2. Starting node needs some kind of command pod, especially a manned command pod
# 3. Starting node doesnt necessarily need a science experiment due to Crew Reports and EVA Reports, but it would be nice
# 4. Look up CTT to see how it handles patching in to the normal tech tree without rewriting files

import ast

TechTreePath = "GameData/Squad/Resources/TechTree.cfg"
newTechTreePath = "GameData/Science+ Randomizer/RandomizedTechTree.cfg"

lines = iter(open(TechTreePath, 'r'))
Lines = []
NodeList = []

class TechNode:
	def __init__(self, id, title, description, cost, hideEmpty,
				nodeName, anyToUnlock, icon, pos, scale, Parent1=None, Parent2=None):

		self.id=id
		self.title=title
		self.description=description
		self.cost=cost
		self.hideEmpty=hideEmpty
		self.nodeName=nodeName
		self.anyToUnlock=anyToUnlock
		self.icon=icon
		self.pos=pos
		self.scale=scale
		self.Parent1=Parent1
		self.Parent2=Parent2

class Parent:
	def __init__(self, parentID, lineFrom, lineTo):

		self.parentID=parentID
		self.lineFrom=lineFrom
		self.lineTo=lineTo

for l in lines:
	Lines.append(l)

for l in range(len(Lines)):
	parent1=None
	parent2=None
	if 'RDNode' in Lines[l]:
		if '{' in Lines[l+1]:
			id = Lines[l+2][7:]
			title = Lines[l+3][10:]
			description = Lines[l+4][16:]
			cost = Lines[l+5][9:]
			hideEmpty = Lines[l+6][14:]
			nodeName = Lines[l+7][13:]
			anyToUnlock = Lines[l+8][16:]
			icon = Lines[l+9][9:]
			pos = Lines[l+10][8:]
			scale = Lines[l+11][10:]
			if 'Parent' in Lines[l+12]:
				parent1_parentID = Lines[l+14][14:]
				parent1_lineFrom = Lines[l+15][14:]
				parent1_lineTo = Lines[l+16][12:]
				parent1 = Parent(parent1_parentID, parent1_lineFrom, parent1_lineTo)
			if 'Parent' in Lines[l+18]:
				parent2_parentID = Lines[l+20][14:]
				parent2_lineFrom = Lines[l+21][14:]
				parent2_lineTo = Lines[l+22][12:]
				parent2 = Parent(parent2_parentID, parent2_lineFrom, parent2_lineTo)

			NodeList.append(TechNode(id, title, description, cost, hideEmpty,
				nodeName, anyToUnlock, icon, pos, scale, parent1, parent2))

with open(newTechTreePath, 'w') as newTechTree:
	newTechTree.write('TechTree\n' + '{\n')
	for node in NodeList:
		newTechTree.write(

			'	RDNode\n' +
			'	{\n'
			'		id = ' + node.id +
			'		title = ' + node.title +
			'		description = ' + node.description +
			'		cost = ' + node.cost +
			'		hideEmpty = ' + node.hideEmpty +
			'		nodeName = ' + node.nodeName +
			'		anyToUnlock = ' + node.anyToUnlock +
			'		icon = ' + node.icon +
			'		pos = ' + node.pos +
			'		scale = ' + node.scale
		)
		if node.Parent1 != None:
			newTechTree.write(
				'		Parent\n' +
				'		{\n' +
				'			parentID = ' + node.Parent1.parentID +
				'			lineFrom = ' + node.Parent1.lineFrom +
				'			lineTo = ' + node.Parent1.lineTo +
				'		}'
			)
		if node.Parent2 != None:
			newTechTree.write(
				'		Parent\n' +
				'		{\n' +
				'			parentID = ' + node.Parent2.parentID +
				'			lineFrom = ' + node.Parent2.lineFrom +
				'			lineTo = ' + node.Parent2.lineTo +
				'		}\n'
			)
		newTechTree.write('\n	}\n')
	newTechTree.write('}')
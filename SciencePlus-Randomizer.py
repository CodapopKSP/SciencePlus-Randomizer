# Possible Later Features
# 1. Randomize planets, experiment descriptions, starting Kerbals, contracts...
# 2. Randomize science colors
# 3. Starting location could be randomized amongst the launch pads or even planets

# Considerations
# 1. Game must be playable, ergo the starting node either needs to be static or heavily considered
# 2. Starting node needs some kind of command pod, especially a manned command pod
# 3. Starting node doesnt necessarily need a science experiment due to Crew Reports and EVA Reports, but it would be nice
# 4. Look up CTT to see how it handles patching in to the normal tech tree without rewriting files

import random
import tkinter as tk
import os

TechTreePath = "GameData/Squad/Resources/TechTree.cfg"
newTechTreePath = "GameData/Science+ Randomizer/RandomizedTechTree.cfg"
KSPDirectoryPath = os.path.dirname(os.path.realpath(__file__))

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

def randomizeMe(seed):
	if seed!='':
		random.seed(seed)
	lines = iter(open(TechTreePath, 'r'))
	Lines = []
	StartlessNodeList = []

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

				if 'start' not in str(id):
					StartlessNodeList.append(TechNode(id, title, description, cost, hideEmpty,
						nodeName, anyToUnlock, icon, pos, scale, parent1, parent2))
				else:
					StartNode = TechNode(id, title, description, cost, hideEmpty,
						nodeName, anyToUnlock, icon, pos, scale, parent1, parent2)

	parent1NodeList = {}
	parent2NodeList = {}

	for n in range(len(StartlessNodeList)):
		if StartlessNodeList[n].Parent1 != None:
			for p in range(len(StartlessNodeList)):
				if StartlessNodeList[n].Parent1.parentID == StartlessNodeList[p].id:
					parent1NodeList[n] = [p]
				if StartlessNodeList[n].Parent1.parentID == 'start':
					parent1NodeList[n] = 'start'
		if StartlessNodeList[n].Parent2 != None:
			for p in range(len(StartlessNodeList)):
				if StartlessNodeList[n].Parent2.parentID == StartlessNodeList[p].id:
					parent2NodeList[n] = [p]
				if StartlessNodeList[n].Parent2.parentID == 'start':
					parent2NodeList[n] = 'start'

	nodeShufleList = {}
	for n in range(len(StartlessNodeList)):
		nodeShufleList[n] = {'id':StartlessNodeList[n].id}
		nodeShufleList[n]['title'] = StartlessNodeList[n].title
		nodeShufleList[n]['description'] = StartlessNodeList[n].description
		nodeShufleList[n]['icon'] = StartlessNodeList[n].icon
		nodeShufleList[n]['nodeName'] = StartlessNodeList[n].nodeName
	random.shuffle(nodeShufleList)
	for n in range(len(StartlessNodeList)):
		StartlessNodeList[n].id = nodeShufleList[n]['id']
		StartlessNodeList[n].title = nodeShufleList[n]['title']
		StartlessNodeList[n].description = nodeShufleList[n]['description']
		StartlessNodeList[n].icon = nodeShufleList[n]['icon']
		StartlessNodeList[n].nodeName = nodeShufleList[n]['nodeName']

	for n in range(len(StartlessNodeList)):
		for p in parent1NodeList:
			if n == p:
				x = str(parent1NodeList[n])
				if x == 'start':
					StartlessNodeList[n].Parent1.parentID = 'start'
				else:
					x = x.replace('[', '')
					x = x.replace(']', '')
					StartlessNodeList[n].Parent1.parentID = StartlessNodeList[int(x)].id
		for p in parent2NodeList:
			if n == p:
				x = str(parent2NodeList[n])
				if x == 'start':
					StartlessNodeList[n].Parent2.parentID = 'start'
				else:
					x = x.replace('[', '')
					x = x.replace(']', '')
					StartlessNodeList[n].Parent2.parentID = StartlessNodeList[int(x)].id

	NodeList = []
	NodeList.append(StartNode)
	for n in range(len(StartlessNodeList)):
		NodeList.append(StartlessNodeList[n])

	if (os.path.isdir(KSPDirectoryPath + '\GameData\Science+ Randomizer')==False):
		os.makedirs(KSPDirectoryPath + '\GameData\Science+ Randomizer')

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


# UI

root = tk.Tk()
root.title("Science+ Randomizer")
root.geometry("400x220+800+300")

if os.path.isdir(KSPDirectoryPath + '\GameData\Science+\Assets'):
	root.iconbitmap(r"" + KSPDirectoryPath + "\\GameData\\Science+\\Assets\\icon.ico")

headerFrame = tk.Frame(root, width=100)
warningFrame = tk.Frame(root, width=100)
seedFrame = tk.Frame(warningFrame, width=100)

def openNewWindow(): 
      
    newWindow = tk.Toplevel(root) 
    newWindow.title("Science+ Randomizer") 
    newWindow.geometry("300x80+850+350")

    def quit():
    	newWindow.destroy()
    	root.destroy()
  
    # A Label widget to show in toplevel 
    tk.Label(newWindow, text ="Randomization Complete!", font='Helvetica 12').pack(side="top", pady=10) 
    tk.Button(newWindow, text="OK", command=quit).pack(side="top")

def buttonCommand():
	openNewWindow()
	randomizeMe(seedInput.get())

title = tk.Label(headerFrame, text="Science+ Randomizer", font='Helvetica 18 bold')
author = tk.Label(headerFrame, text="Created by CodapopKSP", font='Helvetica 10 bold')
warning = tk.Label(warningFrame, text="Warning: It is strongly recommended to only use this mod on new saves.\nPressing this button could very well corrupt your save file!")
seedLabel = tk.Label(seedFrame, text="Seed:", font='Helvetica 10 bold')
seedInput = tk.Entry(seedFrame)
randomizeButton = tk.Button(root, width=20, fg="purple", text="Randomize!", font='Helvetica 12 bold', command=buttonCommand)

title.pack(side="top")
author.pack(side="top")
warning.pack(side="top")
seedLabel.pack(side="left")
seedInput.pack(side="left")
headerFrame.pack(side="top", pady=10)
warningFrame.pack(side="top", pady=10)
seedFrame.pack(side="top", pady=10)
randomizeButton.pack(side="top")

root.mainloop()
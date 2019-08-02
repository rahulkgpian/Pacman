import pygame
from vectors import Vector2D
from constants import *
from stacks import Stack

class Node(object):
	def __init__(self, row, column):
		self.row, self.column = row, column
		self.position = Vector2D(column*TILEWIDTH, row*TILEHEIGHT)
		self.neighbors = {UP:None, DOWN:None, LEFT:None, RIGHT:None}

	def render(self, screen):
		for n in self.neighbors.keys():
			if self.neighbors[n] is not None:
				pygame.draw.line(screen, WHITE, self.position.toTuple(), self.neighbors[n].position.toTuple(), 2)
				pygame.draw.circle(screen, RED, self.position.toTuple(), 7)


class NodeGroup(object):
	def __init__(self, level):
		self.nodeList = []
		self.level = level
		self.grid = None
		self.nodeStack = Stack()
		self.createNodeList(level, self.nodeList)

	def getNode(self, x, y, nodeList=[]):
		for node in nodeList:
			if node.position.x == x and node.position.y == y:
				return node
		return None

	def pathToFollow(self, direction, row, col, path):
		if self.grid[row][col] == path or self.grid[row][col] == "+":
			while self.grid[row][col] != "+":
				if direction is LEFT:
					col -= 1
				elif direction is RIGHT:
					col += 1
				elif direction is UP:
					row -= 1
				elif direction is DOWN:
					row += 1
			return Node(row, col)
		else:
			return None

	def followPath(self, direction, row, col):
		rows = len(self.grid)
		columns = len(self.grid[0])
		if direction == LEFT and col >= 0:
			return self.pathToFollow(LEFT, row, col, "-")
		elif direction == RIGHT and col < columns:
			return self.pathToFollow(RIGHT, row, col, "-")
		elif direction == UP and row >= 0:
			return self.pathToFollow(UP, row, col, "|")
		elif direction == DOWN and row < rows:
			return self.pathToFollow(DOWN, row, col, "|")
		else:
			return None

	def nodeInList(self, node, nodeList):
		for inode in nodeList:
			if node.position.x == inode.position.x and node.position.y == inode.position.y:
				return True
		return False

	def addNodeToStack(self, node, nodeList):
		if node is not None and not self.nodeInList(node, nodeList):
			self.nodeStack.push(node)

	def addNode(self, node, nodeList):
		nodeInList = self.nodeInList(node, nodeList)
		if not nodeInList:
			nodeList.append(node)

	def getPathNode(self, direction, row, col, nodeList):
		tempNode = self.followPath(direction, row, col)
		return self.getNodeFromNode(tempNode, nodeList)

	def getNodeFromNode(self, node, nodeList):
		if node is not None:
			for inode in nodeList:
				if node.row == inode.row and node.column == inode.column:
					return inode
		return node

	def findFirstNode(self, rows, cols):
		nodeFound = False
		for row in range(rows):
			for col in range(cols):
				if self.grid[row][col] == "+":
					return Node(row, col)
		return None

	def createNodeList(self, textFile, nodeList):
		self.grid = self.readMazeFile(textFile)
		startNode = self.findFirstNode(len(self.grid), len(self.grid[0]))
		self.nodeStack.push(startNode)
		while not self.nodeStack.isEmpty():
			node = self.nodeStack.pop()
			self.addNode(node, nodeList)
			leftNode = self.getPathNode(LEFT, node.row, node.column - 1, nodeList)
			rightNode = self.getPathNode(RIGHT, node.row, node.column + 1, nodeList)
			upNode = self.getPathNode(UP, node.row - 1, node.column, nodeList)
			downNode = self.getPathNode(DOWN, node.row + 1, node.column, nodeList)
			node.neighbors[LEFT] = leftNode
			node.neighbors[RIGHT] = rightNode
			node.neighbors[UP] = upNode
			node.neighbors[DOWN] = downNode
			self.addNodeToStack(leftNode, nodeList)
			self.addNodeToStack(rightNode, nodeList)
			self.addNodeToStack(upNode, nodeList)
			self.addNodeToStack(downNode, nodeList)

	def readMazeFile(self, textfile):
		f = open(textfile, "r")
		lines = [line.rstrip('\n') for line in f]
		return [line.split(' ') for line in lines]

	def setupTestNodes(self):
		nodeA = Node(5, 5)
		nodeB = Node(5, 10)
		nodeC = Node(10, 5)
		nodeD = Node(10, 10)
		nodeE = Node(10, 13)
		nodeF = Node(20, 5)
		nodeG = Node(20, 13)
		nodeA.neighbors[RIGHT] = nodeB
		nodeA.neighbors[DOWN] = nodeC
		nodeB.neighbors[LEFT] = nodeA
		nodeB.neighbors[DOWN] = nodeD
		nodeC.neighbors[UP] = nodeA
		nodeC.neighbors[RIGHT] = nodeD
		nodeC.neighbors[DOWN] = nodeF
		nodeD.neighbors[UP] = nodeB
		nodeD.neighbors[LEFT] = nodeC
		nodeD.neighbors[RIGHT] = nodeE
		nodeE.neighbors[LEFT] = nodeD
		nodeE.neighbors[DOWN] = nodeG
		nodeF.neighbors[UP] = nodeC
		nodeF.neighbors[RIGHT] = nodeG
		nodeG.neighbors[UP] = nodeE
		nodeG.neighbors[LEFT] = nodeF
		self.nodeList = [nodeA, nodeB, nodeC, nodeD, nodeE, nodeF, nodeG]

	def render(self, screen):
		for node in self.nodeList:
			node.render(screen)
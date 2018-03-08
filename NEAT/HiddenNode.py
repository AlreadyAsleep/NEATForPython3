# File: HiddenNode.py
# Package: NEAT for Python3
# Author: Ben Heil
# Since: 2/18/18

import Node
import numpy as np

class HiddenNode(Node.Node):
	'''This class defines a hidden node
	in the topology'''

	tag = "Hidden"
	nodeC = None

	def __init__(self, title, nodeC):
		super(HiddenNode, self).__init__(title)
		self.nodeC = nodeC

	def process(self):
		'''sets the output nodes to
		the values based off the table
		below'''
		tally = 0
		for c in self.connections:
			if self.nodeC.get_node(c.input_node).tag == "Input":
				tally += self.nodeC.get_node(c.input_node).state
		for c in self.connections:
			if self.nodeC.get_node(c.output_node).tag == "Output":
				self.nodeC.get_node(c.output_node).state = np.sign(tally)

# File: InputNode.py
# Package: NEAT for Python3
# Author: Ben Heil
# Since: 2/16/18


import Node


class InputNode(Node.Node):
	'''This class defines an input node
	in the topology'''

	tag = "Input"

	def __init__(self, title):
		super(InputNode, self).__init__(title)

	def get_input(self, func, cont):
		'''function decorator for function to
		be defined by implementer'''
		return func(cont)




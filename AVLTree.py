"""A class represnting a node in an AVL tree"""

class AVLNode(object):
	"""Constructor, you are allowed to add more fields. 
	
	@type key: int
	@param key: key of your node
	@type value: string
	@param value: data of your node
	@complexity: O(1) worst case
	"""
	def __init__(self, key, value):
		self.key = key
		self.value = value
		self.left = None
		self.right = None
		self.parent = None
		self.height = -1
		

	"""returns whether self is not a virtual node 

	@rtype: bool
	@returns: False if self is a virtual node, True otherwise.
	@complexity: O(1) worst case
	"""
	def is_real_node(self):
		if self.key == None:
			return False
		return True
	
	
	"""returns if the node is a real leaf Aka not external leaf
	
	@rtype: bool
	@returns: True if node is leaf, False otherwise
	@complexity: O(1) worst case
	"""
	def is_real_leaf(self):
		if(self.height == 0):
			return True
		return False
	

	"""returns the balance factor of the node
	
	@rtype: int
	@returns: an integer representing the node's balance factor
	@complexity: O(1) worst case
	"""
	def balance_factor(self):
		left = self.height - self.left.height
		right = self.height - self.right.height
		return left - right
	

	"""return an integer representing the edges height diffs i.e 12,11,21...
	
	@rtype: int
	@returns: the node's edge's height diffs
	@complexity: O(1) worst case
	"""
	def balance_factor_detailed(self):
		left = self.height - self.left.height
		right = self.height - self.right.height
		return left*10 + right
	

	"""returns the number of real children the node has
	
	@rtype: int
	@returns: the number of real children the node has (Not including external leaves)
	@complexity: O(1) worst case
	"""
	def num_of_real_children(self):
		count = 0
		if (self.left.is_real_node()):
			count += 1
		if (self.right.is_real_node()):
			count += 1

		return count


"""
A class implementing an AVL tree.
"""

class AVLTree(object):

	"""
	Constructor, you are allowed to add more fields.
	@complexity: O(1) worst case
	"""
	def __init__(self):
		self.root = None
		self.maxNode = None
		self.ext_leaf = AVLNode(None,None)
		self.minNode = None
		self.treeSize = 0


	"""searches for a node in the dictionary corresponding to the key (starting at the root)
        
	@type key: int
	@param key: a key to be searched
	@rtype: (AVLNode,int)
	@returns: a tuple (x,e) where x is the node corresponding to key (or None if not found),
	and e is the number of edges on the path between the starting node and ending node+1.
	@Complexity: O(log(n))
	"""
	def search(self, key):
		e = 0
		node = self.root

		while(node and node.key != key and node.is_real_node()):
			if(key > node.key):
				node = node.right
				e += 1
			else:
				node = node.left
				e += 1

		if(node and key == node.key):
			return node, e+1

		return None, e


	"""searches for a node in the dictionary corresponding to the key, starting at the max
        
	@type key: int
	@param key: a key to be searched
	@rtype: (AVLNode,int)
	@returns: a tuple (x,e) where x is the node corresponding to key (or None if not found),
	and e is the number of edges on the path between the starting node and ending node+1.
	@complexity: O(log n)
	"""
	def finger_search(self, key):
		curr = self.maxNode
		edge_count = 0
		while(curr != self.get_root() and curr.parent.key >= key):
			curr = curr.parent
			edge_count += 1
		
		tmp_tree = AVLTree()
		tmp_tree.root = curr
		node,search_count = tmp_tree.search(key)
		return node, search_count + edge_count
	

	"""inserts a new node into the dictionary with corresponding key and value (starting at the root)

	@type key: int
	@pre: key currently does not appear in the dictionary
	@param key: key of item that is to be inserted to self
	@type val: string
	@param val: the value of the item
	@rtype: (AVLNode,int,int)
	@returns: a 3-tuple (x,e,h) where x is the new node,
	e is the number of edges on the path between the starting node and new node before rebalancing,
	and h is the number of PROMOTE cases during the AVL rebalancing
	@complexity: O(log n)
	"""
	def insert(self, key, val):
		x, e, h = self.insert_call(key,val,self.root)
		self.treeSize += 1
		return x, e, h
		
	""" handles the actual insertion of node
	
	@param key: the key of the item to be inserted to self
	@type key: int
	@param val: the value ot the item
	@type val: string
	@param start_root: the node to start the insertion from
	@type start_root: AVLNode
	@rtype: (AVLNode,int,int)
	@returns: a 3-tuple (x,e,h) where x is the new node,
	e is the number of edges on the path between the starting node and new node before rebalancing,
	and h is the number of PROMOTE cases during the AVL rebalancing
	@complexity: O(log n)
	"""
	def insert_call(self, key, val, start_root):
		# create the new node and other variables
		node = AVLNode(key, val)
		node.left = self.ext_leaf  # left child is external leaf
		node.right = self.ext_leaf  # right child is external leaf
		node.height = 0  # it will be a leaf

		edge_couner = 0
		promote_counter = 0
		parent = None

		# case 1: the tree is empty --> set the root to be the new node and finished
		if start_root is None:
			self.root = node
			self.maxNode = node
			self.minNode = node
			return (node, 0, promote_counter)
		
		# maintain maximum pointer
		if self.max_node() != None:
			if key > self.maxNode.key:  # max_node is not None (because tree is not empty)
				self.maxNode = node
		
		# maintain minimum pointer
		if self.min_node() != None:
			if key < self.minNode.key: # max_node is not None (because tree is not empty)
				self.minNode = node

		parent, edge_counter = self.search_parent(key, start_root)
		parent_num_of_children = parent.num_of_real_children()

		node.parent = parent
		if key > parent.key:
				parent.right = node
		else:
			parent.left = node

		# case 2: the parent is not a leaf  -->  insert normally. Resulting tree is a valid AVL tree
		if parent_num_of_children > 0:
			pass

		# case 3: the parent is a leaf
		else:
			self.promote(parent)
			promote_counter += 1
			promote_counter += self.insert_rebalance(parent)

		return (node, (edge_counter + 1), promote_counter)


	"""finds the parent of a given key to be inserted
	
	@param key: key of the item that is to be inserted to self
	@type key: int
	@param start_root: the node to start the search from
	@type start_root: AVLNode
	@rtype: (AVLNode, int)
	@returns: a 2-tuple (y, edge_count) where y is the AVLNode representing the parent,
	and edge_count is the number of edges on the path between the starting node and the new node before rebalancing
	@complexity: O(log n)
	"""
	def search_parent(self,key, start_root):
		y = None  # pointer to previous node
		x = start_root  # pointer to current node
		edge_count = 0

		while x.is_real_node():
			y = x
			if key < x.key:
				x = x.left
			else:
				x = x.right
			edge_count += 1
		
		return y,(edge_count - 1)

	""" perform rebalance after insertion i.e promotions and rotations

	@param node: the node to start rebalance from
	@type node: AVLNode
	@complexity: O(log n) worst case"""
	def insert_rebalance(self, node):
		promote_counter = 0
		good_count = 0  # counter of succesful junctions
		curr = node

		while (good_count < 2) and curr:
			curr_bf = curr.balance_factor_detailed()
			# stop condition
			if curr_bf in [11,12,21]:
				good_count += 1

			# case 1: (0,1) junction
			elif curr_bf in [1,10]: # 1 := 01
				self.promote(curr)
				promote_counter += 1

			# case 2.1: (0,2) junction
			elif curr_bf == 2: # 2 := 02
				x = curr.left
				x_bf = x.balance_factor_detailed()

				# case 2.1.1: child is (1,2)
				if x_bf == 12:
					self.right_rotation(curr)
					
				# case 2.1.2: child is (2,1)
				elif x_bf == 21:
					self.left_rotation(x)
					self.right_rotation(curr)

				#case 2.1.3: child is (1,1)
				elif x_bf == 11:
					self.right_rotation(curr)
				
			
			# case 2.2: (2,0) junction *SYMETRIC TO CASE 2.1*
			elif curr_bf == 20:
				x = curr.right
				x_bf = x.balance_factor_detailed()

				# case 2.2.1: child is (1,2) *SYMETRIC TO CASE 2.1.2
				if x_bf == 12:
					self.right_rotation(x)
					self.left_rotation(curr)
				
				# case 2.2.2: child is (2,1)  *SYMETRIC TO CASE 2.1.1*
				elif x_bf == 21:
					self.left_rotation(curr)
				
				# case 2.2.3: child is (1,1) *SYMMETRIC TO CASE 2.1.3*
				elif x_bf == 11:
					self.left_rotation(curr)
			
			curr = curr.parent 
		
		return promote_counter


	"""inserts a new node into the dictionary with corresponding key and value, starting at the max

	@type key: int
	@pre: key currently does not appear in the dictionary
	@param key: key of item that is to be inserted to self
	@type val: string
	@param val: the value of the item
	@rtype: (AVLNode,int,int)
	@returns: a 3-tuple (x,e,h) where x is the new node,
	e is the number of edges on the path between the starting node and new node before rebalancing,
	and h is the number of PROMOTE cases during the AVL rebalancing
	@complexity: O(log n)
	"""
	def finger_insert(self, key, val):
		# Edge case: if tree is empty --> execute normal insert
		if self.root == None:
			return self.insert(key,val)

		# find the key to start the insert from
		curr = self.max_node()
		edge_count = 0
		while(curr != self.root and curr.parent.key >= key):
			curr = curr.parent
			edge_count += 1

		#insert the new node
		x,e,h = self.insert_call(key,val,curr)
		self.treeSize += 1
		return x,(e+edge_count),h


	"""deletes node from the dictionary

	@type node: AVLNode
	@pre: node is a real pointer to a node in self
	@complexity: O(log n)
	"""
	def delete(self, node, innercall = False):

		if not innercall:
			self.treeSize -= 1  

			# maintain pointer to max node
			if node == self.max_node():
				self.maxNode = self.find_predecessor(node)

			# maintain pointer to min node
			if node == self.minNode:
				self.minNode = self.find_successor(node)

		parent = node.parent

		# edge case - tree is only one node
		if node == self.root and node.height == 0:  
			self.root = None
			self.maxNode = None
			self.minNode = None
			self.treeSize = 0
			return
		
		

		children_count = node.num_of_real_children()
		
		if children_count == 2:
			suc_node = self.find_successor(node)
			self.delete(suc_node, innercall = True)

			suc_node.height = node.height

			# set child - parent relationship
			parent = node.parent

			suc_node.left = node.left
			suc_node.right = node.right
			suc_node.parent = parent
			#assign the suc_node to be it's child parent as well
			suc_node.left.parent = suc_node
			suc_node.right.parent = suc_node

			

			dir = self.node_parent_direction(node)
			if dir == 'R':
				parent.right = suc_node
			if dir == 'L':
				parent.left = suc_node
			if dir == 'N':
				self.root = suc_node


		elif children_count == 1:
			self.delete_one_child(node)

		elif children_count == 0:
			self.delete_zero_child(node)

		# reblance function
		self.delete_rebalance(parent)
	

		"""perfomes the deleteion of a node with zero children (leaf)

		@param node: the node to be deleted from self
		@type node: AVLNode
		@complexity: O(1)
		"""
	def delete_zero_child(self,node):
		parent = node.parent
		parent_bf = parent.balance_factor()
		dir = self.node_parent_direction(node)

		# delete the node
		if dir == 'L':
			parent.left = self.ext_leaf
		elif dir == 'R':
			parent.right = self.ext_leaf

		#further handeling if needed
		if parent_bf != 0:

			if dir == 'L':
				# parent is (1,2)
				if parent_bf == -1:
					self.demote(node.parent)

				# parent is (2,1)
				elif parent_bf == 1:
					pass

			elif dir == 'R':
				# parent is (1,2)
				if parent_bf == -1:
					pass

				# parent is (2,1)
				elif parent_bf == 1:
					self.demote(parent)

		"""perfomes the deleteion of a node with one child

		@param node: the node to be deleted from self
		@type node: AVLNode
		@complexity: O(1)
		"""
	def delete_one_child(self,node):
		# edge case - root is the node (and has only one child which is definitely a leaf)
		# in this case the child will be the new root
		if node == self.root:
			if node.left.is_real_node():
				self.root = node.left
			else:
				self.root = node.right
			return
		
		parent = node.parent
		parent_bf = parent.balance_factor()
		if node.left.is_real_leaf():
			child = node.left
		else:
			child = node.right

		dir = self.node_parent_direction(node)

		# bypass the node
		if dir == 'L':
			parent.left = child
			child.parent = parent
		elif dir == 'R':
			parent.right = child
			child.parent = parent

		if dir == 'L':
			# parent is (1,2)
			if parent_bf == -1:
				self.demote(parent)

			# parent is (2,1)
			elif parent_bf == 1:
				pass

		elif dir == 'R':
			# parent is (1,2)
			if parent_bf == -1:
				pass

			#parent is (2,1)
			elif parent_bf == 1:
				self.demote(parent)


	"""handle rebalance after deleteion of a node from self
	
	@type node: AVLNode
	@pararm node: the node we start rebalancing from 
	@complexity: O(log n)
	"""
	def delete_rebalance(self,node):
		good_node_count = 0 
		curr = node

		while (curr) and (good_node_count < 2):
			curr_bf = curr.balance_factor_detailed()
			# initial check if rebalancing is needed
			if curr_bf in [11,12,21]:
				good_node_count += 1
			
			# (2,2)
			elif curr_bf == 22:
				self.demote(curr)

			# (3,1)
			elif curr_bf == 31:
				right_node = curr.right
				right_node_bf = right_node.balance_factor_detailed()

				# (1,1)
				if right_node_bf == 11:
					self.left_rotation(curr)
					good_node_count = 0

				# (2,1)
				elif right_node_bf == 21:
					self.left_rotation(curr)
					good_node_count = 0

				# (1,2)
				elif right_node_bf == 12:
					self.right_rotation(right_node)
					self.left_rotation(curr)
					good_node_count = 0


			# (1,3)
			elif curr_bf == 13:
				left_node = curr.left
				left_node_bf = left_node.balance_factor_detailed()

				# (1,1)
				if left_node_bf == 11:
					self.right_rotation(curr)
					good_node_count = 0
				
				# (2,1)
				elif left_node_bf == 21:
					self.left_rotation(left_node)
					self.right_rotation(curr)
					good_node_count = 0

				elif left_node_bf == 12:
					self.right_rotation(curr)
					good_node_count = 0

			curr = curr.parent


	"""demote a nodes height by 1
	
	@type node: AVLNode
	@param node: the node to be demoted
	@complexity: O(1)
	"""
	def demote(self,node):
		node.height -= 1


	"""promote a node height by 1
	
	@type node: AVLNode
	@param node: the node to be promoted
	@complexity: O(1)
	"""
	def promote(self,node):
		node.height += 1


	"""returns if the current node is a Left or Right Child of its parent
	
	@rtype: string
	@returns: 'L' if left child, 'R' if right child, 'N' if doesnt have parents
	@complexity: O(1)
	"""
	def node_parent_direction(self,node):
		if node.parent is None:
			return 'N'
		if node.parent.left == node:
			return 'L'
		if node.parent.right == node:
			return 'R'
	

	"""joins self with item and another AVLTree

	@type tree2: AVLTree 
	@param tree2: a dictionary to be joined with self
	@type key: int 
	@param key: the key separting self and tree2
	@type val: string
	@param val: the value corresponding to key
	@pre: all keys in self are smaller than key and all keys in tree2 are larger than key,
	or the opposite way
	@Complexity: O(log(n))
	"""
	def join(self, tree2, key, val):
		new_root = AVLNode(key, val)

		if(self.root == None and tree2.root == None):
			_, _, _ = self.insert(key, val)
			return

		elif(self.root == None):
			self.root = tree2.root
			self.maxNode = tree2.max_node()
			self.minNode = tree2.min_node()
			self.treeSize = tree2.treeSize

			self.insert(new_root.key, new_root.value)
			return
		
		elif(tree2.root == None):
			self.insert(new_root.key, new_root.value)
			return

		if(self.root.key >= tree2.root.key): #check which tree has larger values
			right_tree = self
			left_tree = tree2
		else:
			right_tree = tree2
			left_tree = self

		min = left_tree.minNode
		max = right_tree.maxNode

		if(right_tree.root.height >= left_tree.root.height): #case2: right tree is taller than left tree
			#find node of similar height to other tree
			node = right_tree.root
			parent = node.parent
			while(node.is_real_node() and node.height > left_tree.root.height):
				parent = node
				node = node.left
				
			#join
			new_root.left = left_tree.root
			left_tree.root.parent = new_root

			new_root.right = node
			node.parent = new_root

			if(parent == None):
				right_tree.root = new_root
			else:
				parent.left = new_root
				new_root.parent = parent

			#balance tree
			new_root.height = left_tree.root.height + 1
			p = right_tree.insert_rebalance(new_root)

			#new tree root
			self.root = right_tree.root

		else: #case3: left tree is taller than right tree
			#find node of similar height to other tree
			node = left_tree.root
			parent = node.parent
			while(node.is_real_node() and node.height > right_tree.root.height):
				parent = node
				node = node.right


			#join
			parent.right = new_root
			new_root.parent = parent

			new_root.right = right_tree.root
			right_tree.root.parent = new_root

			new_root.left = node
			node.parent = new_root

			#balance tree
			new_root.height = right_tree.root.height + 1
			p = self.insert_rebalance(new_root.parent)

			#new tree root
			self.root = left_tree.root

		#new tree variables
		self.treeSize = right_tree.treeSize + left_tree.treeSize + 1
		self.minNode = min
		self.maxNode = max

		return
		
	"""splits the dictionary at a given node

	@type node: AVLNode
	@pre: node is in self
	@param node: the node in the dictionary to be used for the split
	@rtype: (AVLTree, AVLTree)
	@returns: a tuple (left, right), where left is an AVLTree representing the keys in the 
	dictionary smaller than node.key, and right is an AVLTree representing the keys in the 
	dictionary larger than node.key.
	@Complexity: O(log(n))
	"""
	def split(self, node):
		#get relevant things from original tree
		split_key = node.key
		left_min = self.minNode
		right_max = self.maxNode

		#build split trees
		left_tree = AVLTree()
		right_tree = AVLTree()

		if(node.left.is_real_node()):
			left_tree.root = node.left
			left_tree.root.parent = None
		if(node.right.is_real_node()):
			right_tree.root = node.right
			right_tree.root.parent = None

		node = node.parent

		#traverse path from split node to root and split tree
		while(node != None):
			left_sub = AVLTree()
			right_sub = AVLTree()

			if(node.key < split_key):
				left_sub.root = node.left
				left_sub.root.parent = None

				left_tree.join(left_sub, node.key, node.value)
			
			else:
				right_sub.root = node.right
				right_sub.root.parent = None

				right_tree.join(right_sub, node.key, node.value)

			node = node.parent

		#update min and max for new trees:
		if(left_tree.root != None):
			left_tree.minNode = left_min
			left_tree.maxNode = left_tree.find_max()
			
		
		if(right_tree.root != None):
			right_tree.minNode = right_tree.find_min()
			right_tree.maxNode = right_max

		return left_tree, right_tree


	"""searches through the tree and returns the minimal node in the dictionary
		@rtype: AVLNode
		@returns: the minimal node, None of the dictionary is empty
		@Complexity: O(log(n))
	"""
	def find_min(self):
		node = self.root

		while(node.left.is_real_node == True):
			node = node.left
		
		return node

	

	"""searches through the tree and returns the maximal node in the dictionary
		@rtype: AVLNode
		@returns: the maximal node, None of the dictionary is empty
		@Complexity: O(log(n))
	"""
	def find_max(self):
		node = self.root

		while(node.right.is_real_node == True):
			node = node.right

		return node
	
	"""returns an array representing dictionary 

	@rtype: list
	@returns: a sorted list according to key of tuples (key, value) representing the data structure
	@complexity: O(n)
	"""
	def avl_to_array(self):
		arr_in_order = []
		self.avl_to_array_rec(self.root, arr_in_order)
		return arr_in_order
	

	"""recursive call for avl_to_array
	@param node: the current node
	@type node: AVLNode
	@param arr: an array using memoization
	@type arr: list
	@complexity: O(n)
	"""
	def avl_to_array_rec(self,node,arr):
		if node and node.is_real_node():
			self.avl_to_array_rec(node.left,arr)
			arr.append((node.key, node.value))  # append array with tuple (key, value)
			self.avl_to_array_rec(node.right,arr)

	"""returns the node with the maximal key in the dictionary

	@rtype: AVLNode
	@returns: the maximal node, None if the dictionary is empty
	complexity: O(1)
	"""
	def max_node(self):
		return self.maxNode
	
	"""Returns the node with the minimal key in the dictionary
	
	@rtype: AVLNode
	@returns: the minimal node, None if the dicionary is empty
	@complexity: O(1)
	"""
	def min_node(self):
		return self.minNode


	"""returns the root of the tree representing the dictionary

	@rtype: AVLNode
	@returns: the root, None if the dictionary is empty
	@complexity: O(1)
	"""
	def get_root(self):
		return self.root
	
	"""returns the number of items in dictionary 

	@rtype: int
	@returns: the number of items in dictionary 
	@complexity: O(1)
	"""
	def size(self):
		return self.treeSize


	"""find the successor of a node

	@type node: AVLNode
	@param node: the node we want to find a successor to
	@rtype: AVLNode
	@returns: the successor node
	@complexity: O(log n)
	"""
	def find_successor(self,node):
		curr = node

		# option 1 - have right child
		if curr.right.is_real_node():
			curr = curr.right
			while curr.left.is_real_node():
				curr = curr.left
			return curr
		
		# option 2 - no right child. climb up
		else:
			curr = node
			while curr.parent and curr == curr.parent.right:
				curr = curr.parent

			#finished climbing up left - now go once right.
			if (not curr.parent): # than the starting node is the maximum
				return node
			else:
				return curr.parent

	"""find the predecessor of a node

	@type node: AVLNode
	@param node: the node we want to find a predecessor to
	@rtype: AVLNode
	@returns: the predecessor node
	@complexity: O(log n)
	"""
	def find_predecessor(self,node):
		curr = node

		# option 1 - have left child
		if curr.left.is_real_node():
			curr = curr.left
			while curr.right.is_real_node():
				curr = curr.right
			return curr
		
		# option 2 - no left child. climb up
		else:
			curr = node
			while curr.parent and curr == curr.parent.left:
				curr = curr.parent

			# finished climbing up right - now go once left.
			if (not curr.parent): # then the starting node is the maximum
				return node
			else:
				return curr.parent

	"""rotates an AVL subtree rooted at the given node once to the right

    @rtype: AVLNode
    @pre: the height difference between the node and its left child is 0
    @returns: None
	@complexity: O(1)
    """
	def right_rotation(self,root):
		# names as shown in lecture notes p.27
		y = root
		x = y.left
		c = y.right
		a = x.left
		b = x.right
		subroot_parent = y.parent  # the node above our subtree
		dir = self.node_parent_direction(y)  # the direction to our parents

		# fix child - parent relationship
		x.left = a
		if a.is_real_node():
			a.parent = x

		x.right = y
		if y.is_real_node():
			y.parent = x

		y.left = b
		if b.is_real_node():
			b.parent = y

		y.right = c
		if c.is_real_node():
			c.parent = y

		x.parent = subroot_parent
		if dir == 'L':
			subroot_parent.left = x
		elif dir == 'R':
			subroot_parent.right = x
		elif dir == 'N':
			self.root = x

		# fix heights
		y.height = max(b.height, c.height) + 1
		x.height = max(a.height, y.height) + 1


	"""rotates an AVL subtree rooted at the given node once to the left

    @rtype: AVLNode
    @pre: the height difference between the node and its right child is 0
    @returns: None
	@complexity: O(1)
    """
	def left_rotation(self,root):
		# names as shown in AVL lecture notes p.27
		x = root
		y = x.right
		a = x.left
		b = y.left
		c = y.right
		subroot_parent = x.parent
		dir = self.node_parent_direction(x)

		# fix child - parent relationship
		y.left = x
		if x.is_real_node():
			x.parent = y

		y.right = c
		if c.is_real_node():
			c.parent = y

		x.left = a
		if a.is_real_node():
			a.parent = x

		x.right = b
		if b.is_real_node():
			b.parent = x

		y.parent = subroot_parent
		if dir == 'L':
			subroot_parent.left = y
		elif dir == 'R':
			subroot_parent.right = y
		elif dir == 'N':
			self.root = y

		# fix heights
		x.height =  max(a.height, b.height) + 1
		y.height = max(x.height, c.height) + 1

                                                                                                                                     
	
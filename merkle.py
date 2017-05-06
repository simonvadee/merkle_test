import argparse
from hashlib import sha256, sha3_256, blake2b

hashing_algorithms = {
	"sha256": sha256,
	"keccak": sha3_256,
	"blake": blake2b
}
class MerkleNode:
	def __init__(self, hash, depth, index):
		self.hash = hash
		self.depth = depth
		self.index = index

class MerkleTree:

	def __init__(self, data=[], algo='sha256'):
		self.hashFunction = hashing_algorithms.get(algo, sha256)
		self.nodeCount = 0
		self.maxDepth = 0
		self.nodes = dict()
		self.rootHash = None

		if type(data) != list:
			raise TypeError("'data' must be a list")

		for element in data:
			hexdigest = self.hashFunction(str(element).encode()).hexdigest()
			self.addNode(hexdigest, -1)
		self.buildTree()

	def __repr__(self):
		ret = "\nDepth = 0 --> "
		current_depth = 0
		for leaf in self.nodes.values():
			if leaf.depth != current_depth:
				ret += '\nDepth = %d --> ' % leaf.depth
			ret += leaf.hash[-6:] + '\t'
			current_depth = leaf.depth
		ret += '\nMAX DEPTH = ' + str(self.height())
		ret += '\nNODE COUNT = ' + str(self.nodeCount)
		ret += '\nROOT = ' + str(self.root())
		return ret

	def addNode(self, hash, depth):
		self.nodes[hash+str(self.nodeCount)] = MerkleNode(hash, depth=depth+1, index=self.nodeCount)
		self.nodeCount += 1

	def buildTree(self):
		depth = 0
		while len(self.nodes) and self.rootHash is None:
			leaves = [x for x in self.nodes.values() if x.depth == depth]
			if len(leaves) <= 1:
				self.rootHash = leaves[0].hash
				self.maxDepth = depth
				return self.rootHash
			iter_leaves = iter(leaves)
			for leaf in iter_leaves:
				try:
					hexdigest = self.hashFunction(leaf.hash.encode() + next(iter_leaves).hash.encode()).hexdigest()
					self.addNode(hexdigest, depth)
				except StopIteration:
					self.addNode(leaf.hash, depth)

			depth += 1

	def getNode(self, index):
		try:
			return list(filter(lambda x: x.index == index, self.nodes.values()))[0]
		except Exception:
			return None

	def root(self):
		return self.rootHash

	def height(self):
		return self.maxDepth

	def level(self, index):
		return [x.hash for x in self.nodes.values() if x.depth == index]

if __name__ == '__main__':

	parser = argparse.ArgumentParser(description='Build and display a merkle tree.')
	parser.add_argument('--data', nargs='*' , help="elements to include in the tree", default=[])
	parser.add_argument('--algo', help="hash function you want to use (can be sha256, keccak, blake) DEFAULT = sha256", default='sha256')
	args = parser.parse_args()
	data_list = vars(args).get('data')
	algo = vars(args).get('algo')
	if args:
		merkleTree = MerkleTree(data_list or [], algo)
		print("Result (only the last 6 bytes of the hashes are displayed):: \n", merkleTree)
	else:
		parser.print_help()
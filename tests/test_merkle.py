import pytest
from hashlib import sha256, sha3_256, blake2b
from .. import merkle

uniform_set = ['a' for _ in range(10)]
even_set = [x for x in range(20)] 
odd_set = [x for x in range(23)]
large_set = [x for x in range(9999)]


def test_none_merkle_tree():
	with pytest.raises(TypeError):
		null_tree = merkle.MerkleTree(data=None)
	
def test_empty_merkle_tree():
	null_tree = merkle.MerkleTree(data=[])
	assert null_tree.nodeCount == 0

def test_uniform_merkle_tree():
	uniform_tree = merkle.MerkleTree(data=uniform_set)
	assert uniform_tree.nodeCount == 21
	for i, e in enumerate(uniform_set):
		assert sha256(str(e).encode()).hexdigest() == uniform_tree.getNode(i).hash
	print(uniform_tree)
	print ("______________________________")

def test_even_merkle_tree():
	even_tree = merkle.MerkleTree(data=even_set, algo="sha256")
	assert even_tree.nodeCount == 41
	for i, e in enumerate(even_set):
		assert sha256(str(e).encode()).hexdigest() == even_tree.getNode(i).hash
	print(even_tree)
	print ("______________________________")

def test_odd_merkle_tree():
	odd_tree = merkle.MerkleTree(data=odd_set, algo="keccak")
	assert odd_tree.nodeCount == 47
	for i, e in enumerate(odd_set):
		assert sha3_256(str(e).encode()).hexdigest() == odd_tree.getNode(i).hash
	print(odd_tree)
	print ("______________________________")
	
def test_large_merkle_tree():
	large_tree = merkle.MerkleTree(data=large_set, algo="blake")
	assert large_tree.nodeCount == 20004
	for i, e in enumerate(large_set):
		assert blake2b(str(e).encode()).hexdigest() == large_tree.getNode(i).hash
	print(large_tree)
	print ("______________________________")

def test_level():
	tree = merkle.MerkleTree(data=odd_set)
	exepected_length = len(odd_set)
	for l in range(tree.maxDepth):
		level = tree.level(l)
		assert len(level) == exepected_length
		exepected_length = int(exepected_length / 2) + (exepected_length % 2)

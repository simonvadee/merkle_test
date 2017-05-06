usage: python3 merkle.py [-h] [--data [DATA [DATA ...]]] [--algo ALGO]

Build and display a merkle tree.

optional arguments:
  -h, --help            show this help message and exit
  --data [DATA [DATA ...]]
                        elements to include in the tree
  --algo ALGO           hash function you want to use (can be sha256, keccak,
                        blake) DEFAULT = sha256


RUN TESTS
# pytest -svv tests/
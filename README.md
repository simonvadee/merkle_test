# RUN FROM COMMAND LINE
```
usage: python3 merkle.py [-h] [--data [DATA [DATA ...]]] [--algo ALGO]

Build and display a merkle tree.

optional arguments:
  -h, --help            show this help message and exit
  --data [DATA [DATA ...]]
                        elements to include in the tree
  --algo ALGO           hash function you want to use (can be sha256, keccak,
                        blake) DEFAULT = sha256
```

# RUN TESTS
`pytest -svv tests/`

# QUESTIONS : 

    I/ Dans l’illustration, imaginons que je possède le Merkle tree. Quelqu’un me donne le bloque de données L2 mais je ne lui fais pas confiance. Comment puis-je vérifier si les données de L2 sont valides?

 Si je possède l’intégralité de l’arbre de merkle ainsi qu’un block L2 dont je veux vérifier la validité, il suffit de comparer le hash de ce block L2 avec le hash de la feuille de l’arbre correspondant à ce block L2 (le block (0-1) de l’illustration) et d’en vérifier l’égalité. Si la fonction de hachage utilisée pour construire l’arbre est résistante aux collisions (ce qui est le cas de sha256 selon les standards actuels), alors on peut considérer que si les hash sont égaux, les données le sont aussi.

    II/ Je possède le bloque L3 un Merkle root. Par contre, je ne possède pas les autres bloques ni le Merkle tree. Quelles informations dois-je obtenir au minimum pour m’assurer que le bloque L3 fait bien partie du Merkle tree qui a pour racine le Merkle root que je possède?

Si je possède seulement le block L3 et la racine de l’arbre de merkle, je ne peux pas vérifier l’appartenance de L3 à l’arbre. Si l’on reprend l’arbre utilisé dans l’illustration, il faut au minimum le block (1-1) et (0) pour pouvoir calculer la racine de l’arbre (on désignera ainsi cette portion une « branche » de l’arbre). On aura donc :
    (1-0) = hash(L3)
    (1) = hash((1-0)+(1-1))
    root = hash((0)+(1))
    L’appartenance de L3 à l’arbre est confirmée si le root hash connu est égal à celui obtenu par les calculs précédemment effectués.

    III/ Quelles sont des exemples d’application pour un Merkle tree?

Les propriétés qui rendent l’arbre de merkle intéressant sont :
    - la possibilité de prouver l’intégrité des données d’un élément présent dans l’arbre (cf question 1)
    - la possibilité de prouver l’appartenance d’une donnée à l’extrémité d’une branche de l’arbre (cf question 2) en disposant seulement d’un nombre réduit de noeuds
    - le peu de ressources nécessaires pour stocker l’arbre (un hash ayant une taille fixe de quelques bytes seulement)
    - le peu de puissance de calcul nécessaire pour effectuer les actions de vérification et d’appartenance des données à l’arbre
    
Ces caractéristiques rendent son utilisation particulièrement utile dans les systèmes distribués ou décentralisés dans lesquels différents acteurs doivent pouvoir maintenir une structure de données et en vérifier l’intégrité de celles-ci sans dépendre d’une autorité centrale. Les protocoles blockchain comme Bitcoin, Ethereum, Hyperledger, Tendermint… utilisent tous les arbres de merkle, mais on peut aussi noter leur utilisation dans le système AntiEntropy de Apache Cassandra, dans le but de prévenir des erreurs lors d’une synchronisation de données entre plusieurs acteurs (noeuds du réseau) concurrents.
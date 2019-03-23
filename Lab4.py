"""
CS2302
Lab4
Purpose: learn how to work with arrays and B-trees
Created on Wed Feb 25, 2019
Last modified  Mar 23, 2019
Olac Fuentes
@author: Nancy Hernandez
"""

#START OF CODE PROVIDED
#######################################################

class BTree(object):
    # Constructor
    def __init__(self, item=[], child=[], isLeaf=True, max_items=2):
        self.item = item
        self.child = child
        self.isLeaf = isLeaf
        if max_items < 3:  # max_items must be odd and greater or equal to 3
            max_items = 3
        if max_items % 2 == 0:  # max_items must be odd and greater or equal to 3
            max_items += 1
        self.max_items = max_items


def FindChild(T, k):
    # Determines value of c, such that k must be in subtree T.child[c], if k is in the BTree
    for i in range(len(T.item)):
        if k < T.item[i]:
            return i
    return len(T.item)


def InsertInternal(T, i):
    # T cannot be Full
    if T.isLeaf:
        InsertLeaf(T, i)
    else:
        k = FindChild(T, i)
        if IsFull(T.child[k]):
            m, l, r = Split(T.child[k])
            T.item.insert(k, m)
            T.child[k] = l
            T.child.insert(k + 1, r)
            k = FindChild(T, i)
        InsertInternal(T.child[k], i)


def Split(T):
    # print('Splitting')
    # PrintNode(T)
    mid = T.max_items // 2
    if T.isLeaf:
        leftChild = BTree(T.item[:mid])
        rightChild = BTree(T.item[mid + 1:])
    else:
        leftChild = BTree(T.item[:mid], T.child[:mid + 1], T.isLeaf)
        rightChild = BTree(T.item[mid + 1:], T.child[mid + 1:], T.isLeaf)
    return T.item[mid], leftChild, rightChild


def InsertLeaf(T, i):
    T.item.append(i)
    T.item.sort()


def IsFull(T):
    return len(T.item) >= T.max_items


def Insert(T, i):
    if not IsFull(T):
        InsertInternal(T, i)
    else:
        m, l, r = Split(T)
        T.item = [m]
        T.child = [l, r]
        T.isLeaf = False
        k = FindChild(T, i)
        InsertInternal(T.child[k], i)


def Search(T, k):
    # Returns node where k is, or None if k is not in the tree
    if k in T.item:
        return T
    if T.isLeaf:
        return None
    return Search(T.child[FindChild(T, k)], k)


def Print(T):
    # Prints items in tree in ascending order
    if T.isLeaf:
        for t in T.item:
            print(t, end=' ')
    else:
        for i in range(len(T.item)):
            Print(T.child[i])
            print(T.item[i], end=' ')
        Print(T.child[len(T.item)])


def PrintD(T, space):
    # Prints items and structure of B-tree
    if T.isLeaf:
        for i in range(len(T.item) - 1, -1, -1):
            print(space, T.item[i])
    else:
        PrintD(T.child[len(T.item)], space + '   ')
        for i in range(len(T.item) - 1, -1, -1):
            print(space, T.item[i])
            PrintD(T.child[i], space + '   ')


def SearchAndPrint(T, k):
    node = Search(T, k)
    if node is None:
        print(k, 'not found')
    else:
        print(k, 'found', end=' ')
        print('node contents:', node.item)

################################################################
#END OF CODE PROVIDED

# NUMBER ONE
#FINDS HEIGHT OF TREE
def height(T):
    if T.isLeaf:
        return 0
    return 1 + height(T.child[0])


#CREATES ARRAY FROM BTREE
# NUMBER TWO
def BTreeToArray(T, L):
    if T.isLeaf:
        #goes through each item and adds it to array
        for i in range(len(T.item)):
            L.append(T.item[i])
    else:
        #goes through each item and adds to array
        for c in range(len(T.item)):
            BTreeToArray(T.child[c], L)
            L.append(T.item[c])
        #Gets last element that is skipped
        BTreeToArray(T.child[-1], L)
    return L

#FINDS SMALLEST NUMBER
# NUMBER THREE
def minimumAtDepthD(T, d):
    if T.isLeaf:
        return T.item[0]
    # if d happens to be root
    if d == 0:
        return T.item[0]
    else:
        return minimumAtDepthD(T.child[0], d - 1)


#FINDS LARGEST NUMBER
# NUMBER FOUR
def maximumAtDepthD(T, d):
    if T.isLeaf:
        return T.item[-1]
    #if d happens to be root
    if d == 0:
        return T.item[-1]
    else:
        return maximumAtDepthD(T.child[-1], d - 1)


#PRINTS NUMBER OF NODES AT A CERTAIN DEPTH
# NUMBER FIVE
def NumberOfNodesAtDepthD(T, d):
    count = 0
    if d == 0:
        return 1
        #Since there can only be one root
    else:
        #For loop that goes to every child
        for i in range(len(T.child)):
            count += NumberOfNodesAtDepthD(T.child[i], d - 1)
    return count


#PRINTS NUMBERS AT GIVEN DEPTH
# NUMBER SIX
def PrintNodesATDepthD(T, d):
    #if d happens to be the root
    if d == 0:
        for t in T.item:
            print(t, end=' ')
    if not T.isLeaf:
        #goes to every child
        for i in range(len(T.child)):
            PrintNodesATDepthD(T.child[i], d - 1)


#COUNTS FULL NODES
# NUMBER SEVEN
def FullNodes(T):
    count = 0
    #keeps track of nodes that are not leafs
    if not T.isLeaf:
        for c in T.child:
            count += FullNodes(c)
    #checks if it has more than the max number of items
    if len(T.item) == T.max_items:
        count += 1
    return count


#COUNTS FULL LEAFS
# NUMBER EIGHT
def FullLeafs(T):
    count = 0
    #keeps track of leafs only
    if T.isLeaf:
        if len(T.item) == T.max_items:
            count += 1
    #if not a leaf then it moves on until it finds one
    else:
        for i in range(len(T.child)):
            count += FullLeafs(T.child[i])
    return count


#FINDS WHERE CERTAIN NUMBER IS LOCATED
# NUMBER NINE
def FindDepth(T, k):
    #if number happens to be root
    if k in T.item:
        return 0
    if T.isLeaf:
        return 0
    #checks what side number is located
    if k > T.item[-1]:
        d = FindDepth(T.child[-1], k)
    else:
        for i in range(len(T.item)):
            if k < T.item[i]:
                d = FindDepth(T.child[i], k)
    #checks to see if theres invalid input
    if d == -1:
        return -1
    return d + 1


L = [30, 50, 10, 20, 60, 70, 110, 120, 1, 11, 3, 4, 5, 105, 115, 200, 2, 45, 6]
T = BTree()
for i in L:
    print('Inserting', i)
    Insert(T, i)
    PrintD(T, '')
    Print(T)
    print('\n####################################')

'''SearchAndPrint(T, 60)
SearchAndPrint(T, 200)
SearchAndPrint(T, 25)
SearchAndPrint(T, 20)'''

# NUMBER ONE
print("Height: ", height(T))
print()

# NUMBER TWO
L1=[]
newList= BTreeToArray(T, L1)
print("BST now converted to sorted list:")
for i in newList:
    print(i, end=' ')
print()
print()

# NUMBER THREE
minimum = minimumAtDepthD(T, 2)
print("Minimum element is: ", minimum)
print()

# NUMBER FOUR
maximum = maximumAtDepthD(T, 2)
print("Maximum element is: ", maximum)
print()

# NUMBER FIVE
print("Number of nodes at this depth are: ")
print(NumberOfNodesAtDepthD(T, 2))
print()

# NUMBER SIX
print("Printing items at this depth: ")
PrintNodesATDepthD(T, 2)
print()

# NUMBER SEVEN
print()
print("Number of full nodes are: ", FullNodes(T))
print()

# NUMBER EIGHT
print("Number of full leafs are: ", FullLeafs(T))
print()

# NUMBER NINE
print("Value is at depth: ", FindDepth(T, 1))

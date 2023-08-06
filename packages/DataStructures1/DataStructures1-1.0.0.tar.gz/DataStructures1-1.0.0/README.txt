This module is build for all those working professionals/students who have basic knowledge of Data Structures and want to save coding time,this module contains various single LinkedList,stack,queue operations.It also contains 5 sorting algorithms and 2 searching algorithms.
__________________________________________
Linked List Operations
------------------------------------------
from data_structure.linkedlist import create,traversal,insertAtEnd,insertBegin,insertMiddle
#Methods to create and Traverse Linked List
create("Hi") #To create node,creates one node at a time
create("How")
create("Are")
create("You")
traversal() #To traverse Linked List

Output:
Hi->How->Are->You->None

#Methods to Insert in Linked List
insertBegin("Hey,") #Insert at Beginning
traversal()
output:
Hey,->Hi->How->Are->You->None

insertMiddle(2,"Bro") #First parameter takes  position,second parameter takes data
traversal()
output:
Hey,->Hi->Bro->How->Are->You->None

insertAtEnd("Doing") #Inserting at end
traversal()
output:
Hey,->Hi->Bro->How->Are->You->Doing->None

__________________________________________
Stack Operations
__________________________________________
from data_structure.stack import Stack
s = Stack()

#To push element in stack
s.push(50)
output:
'50 pushed'
s.push(80)
output:
'80 pushed'

#To peek the stack
s.peek()
output:
80

#To pop elements in stack
s.remove()
output:
80

__________________________________________

Queue Operations

__________________________________________
from data_structure.queue import Queue

q=Queue()

#To insert elements into queue
q.insert(40)
output:
'40 inserted'

q.insert(50)
output:
'50 inserted'

#To remove elements from queue
q.remove()
output:
40

#To check size of Queue
q.size()
output:
1
__________________________________________
Sorting Operations
__________________________________________
This module contains 5 sorting algorithms
which are:

1)bubbleSort.
2)mergeSort.
3)insertionSort.
4)shellSort.
5)selectionSort.

from data_structure.sort import mergeSort,bubbleSort,insertionSort,shellSort,selectionSort
sort = mergeSort([5,101,35,121,55,75])
print(sort)
output:
[5, 35, 55, 75, 101, 121]

sort = selectionSort([5,101,35,121,55,75])
print(sort)
output:
[5, 35, 55, 75, 101, 121]

__________________________________________
Searching Operations
__________________________________________
from data_structure.search import linearSearch,binarySearch
#Linear Search
search = linearSearch([5,101,35,121,55,75],121)
print(search)
#Binary Search, Note list passed should be sorted
search = binarySearch([5, 35, 55, 75, 101, 121],121)
print(search)
output:
Found 121 at index 5
__________________________________________
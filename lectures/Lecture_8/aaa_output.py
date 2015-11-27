Python 3.4.2 (v3.4.2:ab2c023a9432, Oct  5 2014, 20:42:22) 
[GCC 4.2.1 (Apple Inc. build 5666) (dot 3)] on darwin
Type "copyright", "credits" or "license()" for more information.
>>> WARNING: The version of Tcl/Tk (8.5.9) in use may be unstable.
Visit http://www.python.org/download/mac/tcltk/ for current information.
================================ RESTART ================================
>>> 
>>> ================================ RESTART ================================
>>> 
>>> a = Node(2)
>>> LL = LinkedList(a)
>>> LL.head
<__main__.Node object at 0x10504a470>
>>> LL.head.value
2
>>> ================================ RESTART ================================
>>> 
>>> LL = LinkedList([1,2,4])
>>> LL.head.next_node.value
2
>>> ================================ RESTART ================================
>>> 
>>> LL = LinkedList([1,2,4])
>>> LL.length()
3
>>> LL = LinkedList()
>>> LL.length()
0
>>> from aaa import *
>>> LinkedList.length(LL)
0
>>> ================================ RESTART ================================
>>> 
>>> LL = LinkedList([1,2,4,7,4])
>>> LL.apply_function(lambda x: x * 2)
>>> ================================ RESTART ================================
>>> 
>>> LL = LinkedList([1,2,4,7,4])
>>> LL.print()
Traceback (most recent call last):
  File "<pyshell#15>", line 1, in <module>
    LL.print()
AttributeError: 'LinkedList' object has no attribute 'print'
>>> LL.printer()
>>> ================================ RESTART ================================
>>> 
>>> LL = LinkedList([1,2,4,7,4])
>>> LL.print()
>>> ================================ RESTART ================================
>>> 
>>> LL = LinkedList([1,2,4,7,4])
>>> LL.printer()
>>> 
>>> ================================ RESTART ================================
>>> 
>>> LL = LinkedList([1,2,4,7,4])
>>> LL.printer()
1, 2, 4, 7, 4
>>> LL.apply_function(lambda x: x * 2)
>>> LL.printer()
2, 4, 8, 14, 8
>>> ================================ RESTART ================================
>>> 
>>> LL = LinkedList([1,2,4,7,4])
>>> LL.reverse()
>>> LL.print()
Traceback (most recent call last):
  File "<pyshell#28>", line 1, in <module>
    LL.print()
AttributeError: 'LinkedList' object has no attribute 'print'
>>> LL = LinkedList([1,2,4,7,4])
>>> LL.reverse()
>>> LL.printer()
4, 7, 4, 2, 1
>>> ================================ RESTART ================================
>>> 
>>> LL = LinkedList([1,2,4,7,4])
>>> LL.reverse()
>>> LL.reverse()
>>> LL.printer()
1, 2, 4, 7, 4
>>> LL.is_sorted(lambda x, y: x <= y)
Traceback (most recent call last):
  File "<pyshell#36>", line 1, in <module>
    LL.is_sorted(lambda x, y: x <= y)
  File "/Users/ivanteong/Desktop/MIT/COMP9021/Lecture_8/aaa.py", line 63, in is_sorted
    while node.next_node.next_node:
UnboundLocalError: local variable 'node' referenced before assignment
>>> ================================ RESTART ================================
>>> 
>>> LL = LinkedList([1,2,4,7,4])
>>> LL.is_sorted(lambda x, y: x <= y)
Traceback (most recent call last):
  File "<pyshell#38>", line 1, in <module>
    LL.is_sorted(lambda x, y: x <= y)
  File "/Users/ivanteong/Desktop/MIT/COMP9021/Lecture_8/aaa.py", line 63, in is_sorted
    while node.next_node.next_node:
UnboundLocalError: local variable 'node' referenced before assignment
>>> ================================ RESTART ================================
>>> 
>>> LL = LinkedList([1,2,4,7,4])
>>> LL.is_sorted(lambda x, y: x <= y)
False
>>> LL.reverse()
>>> LL.is_sorted(lambda x, y: x <= y)
False
>>> ================================ RESTART ================================
>>> 
>>> LL = LinkedList([1,2,4,7,4])
>>> LL.printer()
1, 2, 4, 7, 4
>>> LL = LinkedList([0,5,10,15,20])
>>> LL.printer()
0, 5, 10, 15, 20
>>> LL.insert_value_before(-5,0)
True
>>> LL.printer()
-5, 0, 5, 10, 15, 20
>>> LL.insert_value_before(19,20)
True
>>> LL.insert_value_before(11,12)
False
>>> LL.printer()
-5, 0, 5, 10, 15, 19, 20
>>> LL.insert_value_before(12,15)
True
>>> LL.printer()
-5, 0, 5, 10, 12, 15, 19, 20
>>> 

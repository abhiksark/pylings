# Lists

Source: https://docs.python.org/3/tutorial/datastructures.html#more-on-lists

This local reference is generated from the official Python documentation and trimmed for pylings.

Lists are mutable ordered collections with methods such as `append`, `pop`, and `sort`.

## Extracted reference

5.1. More on Lists

The list data type has some more methods. Here are all
of the methods of list objects:

list.append(value, /)

Add an item to the end of the list. Similar to `a[len(a):] = [x]`.

list.extend(iterable, /)

Extend the list by appending all the items from the iterable. Similar to
`a[len(a):] = iterable`.

list.insert(index, value, /)

Insert an item at a given position. The first argument is the index of the
element before which to insert, so `a.insert(0, x)` inserts at the front of
the list, and `a.insert(len(a), x)` is equivalent to `a.append(x)`.

list.remove(value, /)

Remove the first item from the list whose value is equal to value. It raises a
`ValueError` if there is no such item.

list.pop(index=-1, /)

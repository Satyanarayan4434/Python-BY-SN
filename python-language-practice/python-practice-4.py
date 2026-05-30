a = 10
b = 10
print(id(a) == id(b))  # True, because small integers are cached by Python and point to the same memory location.

name1 = "Satya"
name2 = "Satya"
print(id(name1) == id(name2))  # True, because string literals are also cached by Python and point to the same memory location.

list1 = [1, 2, 3]
list2 = [1, 2, 3]
print(id(list1) == id(list2))  # False, because lists are mutable and each list is stored at a different memory location.

tuple1 = (1, 2, 3)
tuple2 = (1, 2, 3)
print(id(tuple1) == id(tuple2))  # True, because tuples with the same content may be interned by Python and point to the same memory location.

dict1 = {'a': 1, 'b': 2}
dict2 = {'a': 1, 'b': 2}
print(id(dict1) == id(dict2))  # False, because dictionaries are mutable and each dictionary is stored at a different memory location.

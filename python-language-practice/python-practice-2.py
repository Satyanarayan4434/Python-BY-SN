set1 = set("python")
set2 = set("telusko")

#it prints the common characters in both the sets
print (set1 & set2)

#it prints the characters which are in set1 but not in set2
print (set1 - set2)

#it prints the characters which are in set2 but not in set1
print (set2 - set1) 

#it prints the characters which are in either set1 or set2 but not in both
print (set1 ^ set2)

#it prints the characters which are in either set1 or set2 or both
print (set1 | set2)

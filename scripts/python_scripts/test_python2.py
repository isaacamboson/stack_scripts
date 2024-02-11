#!/usr/bin/python

"""
names = ["Isaac", "Daniel", "Bukola"]
print(len(names))

names = ["Isaac", "Daniel", "Bukola"]
names.append("Olabisi")
names.insert(1, "Saks")
names.insert(3, "Murphy")
print("The length of this list is {}".format(len(names)))
print(names)

names.remove("Daniel")
print("The length of this list is {}".format(len(names)))
print(names)

names.pop()
print("The length of this list is {}".format(len(names)))
print(names)

names.pop(0)
print("The length of this list is {}".format(len(names)))
print(names)

del names[0]
print("The length of this list is {}".format(len(names)))
print(names)

print("Clearing the list")
names.clear()
print(names)


names = ["Isaac", "Daniel", "Bukola", "Yinka", "Nick", "Ola"]
names2 = names.copy()
names3 = ["Jones", "Dave", "Fola"]
names4 = names2 + names3
#print(names)
#print(names2)
#print(names3)
#print(names4)

for x in names:
	names3.append(x)
print(names4)

names = ["Isaac", "Daniel", "Bukola", "Yinka", "Nick", "Ola"]
names2 = ["Jones", "Dave", "Fola"]
names.extend(names2)
print(names)


names = list(("Isaac", "Daniel", "Bukola", "Yinka", "Nick", "Ola"))
print(names)


numbers = [1,1,2,2,3,4,5,6,6,7,8,9,9,10]
new = []
dup = []
for x in numbers:
	if x not in new:
		new.append(x)
	else:
		dup.append(x)
print(dup)

numbers = [1,1,2,2,3,4,5,6,6,7,8,9,9,10]
dup = []
for x in numbers:
	if numbers.count(x) > 1:
		dup.append(x)
print(dup)

numbers = [1,1,2,2,3,4,5,6,6,7,8,9,9,10]
dedup = set(numbers)
print(dup)











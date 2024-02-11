#!/usr/bin/python

import subprocess
import os
import time

cars = {
	"Brand":"Honda",
	"Model":"Accord",
	"Year": 2010
}
"""
print(cars["Brand"])
print(cars.get("Model"))

cars["Year"]=2023
print(cars)

for x in cars:
	print(x)

for x in cars:
	print(x)

for x in cars:
	print(cars[x])

#another way of doing line 23-24
for x in cars.values():
	print(x)

for x,y in cars.items():
	print(x, "=>", y)


if "Brand" in cars:
	print("Brand exist in car dict")

print(len(cars))

cars["Tag"] = "15AGHBN"
print(cars)

cars.pop("Tag")
print(cars)

cars.popitem()
print(cars)

del cars["Model"]
print(cars)

del cars
print(cars)

cars.clear()
print(cars)

cars2 = cars.copy()
print(cars2)

cars3 = dict(cars)
print(cars3)

car1 = {
	"Brand":"Honda",
	"Model":"Accord",
	"Year":2010
	}
car2 = {
	"Brand":"Toyota",
	"Model":"Camry",
	"Year":2005
	}
car3 = {
	"Brand":"Hyundra",
	"Model":"Elantra",
	"Year":2023
}

cars = {
	"car1": car1,
	"car2": car2,
	"car3": car3
}

print(cars["car1"])


name = "Michael"
if name = "Michael":
	pass

#loops
i = 1
while i < 6:
	print(i)
	i += 1

counter = 1
while counter < 6:
	print(counter)
	if counter == 3:
		break
	counter += 1


counter = 0
while counter <= 10:
	print(counter)
	if counter == 11:
		break
	counter += 1

empty_list = []
while 2 > 1: #this could be anything that is true 
	i = int(input("Input a number: "))
	empty_list.append(i)
	if i == 0:
		break
print(empty_list)
"""

while True:
	file_name = "testloop.txt"
	full_path = os.path.join(os.getcwd(), file_name)

	if file_name not in os.listdir():
		print("checking for file - {}".format(file_name))
		time.sleep(1)
	else:
		print("File found.")
		file_ls = subprocess.run("ls -ltr {}".format(full_path), shell=True)
		print(file_ls)

#		OR
#		file_ls = os.system("ls -ltr {}".format(full_path))
#		print(file_ls)

		break

"""
i = 1
while i < 6:
	i += 1
	if i == 3:
		continue  #continue skips that number and continues the loops
	print(i)


i = 1
while i < 6:
	print(i)
	i += 1
else:
	print("i is no longer less than 6")

"""




















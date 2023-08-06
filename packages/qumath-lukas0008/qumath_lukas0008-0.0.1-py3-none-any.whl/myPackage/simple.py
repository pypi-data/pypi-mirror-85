creator = "lukas"
def help():
	print('')

	print('###########################################')
	print('#####       ___  ___      _   _       #####')
	print('#####       |  \\/  |     | | | |      #####')
	print('#####   __ _| .  . | __ _| |_| |__    #####')
	print("#####  / _` | |\\/| |/ _` | __| '_ \\   #####")
	print('##### | (_| | |  | | (_| | |_| | | |  #####')
	print('#####  \\__, \\_|  |_/\\__,_|\\__|_| |_|  #####')
	print('#####     | |                         #####')
	print('#####     |_|                         #####')
	print('###########################################')

	print('')
	print('qMath is a simple package that helps with making math stuff, here is a list of commands for it:\n###!#! always put "qmath." before every function !#!###')
	print('  listLength (returns the amount of variables in a list)')
	print('  average (returns an average of the list inputed)')
	print('  maxAdd (1st variable = the current number, 2nd = number to add, 3rd = the threshold, returns 1st + 2nd while not being able to go over the threshold)')
	return None
def listLength(x):
	y = 0
	for z in x:
		y += 1
	return y
def average(x):
	z = 0
	for y in x:
		z += y
	z = z/listLength(x)
	return z
def maxAdd(x, y, z):
	x += y
	if x > z:
		x = z
	return x
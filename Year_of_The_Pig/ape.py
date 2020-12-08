#!/bin/env/python

mem_words = ['Italy', 'italy', 'Milan', 'milan', 'Savoia', 'savoia', 'Curtiss', 'curtiss', 'Curtis', 'curtis', 'planes', 'Planes', 'Plane', 'Plane']

special_chars = ['!', '@', '#', '$']

count = 0

for words in mem_words:
	for special_char in special_chars:
		while (count <= 99):
			if (count <= 9):
				count = '0' + str(count)
			else:
				count = str(count)
			print(words + count + special_char)
			count = int(count)
			count += 1
		count = 0
			
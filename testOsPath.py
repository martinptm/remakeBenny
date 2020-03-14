import os, os.path

import fnmatch
dirpath = './Images/earth_throw/'

images = fnmatch.filter(os.listdir(dirpath), '*.png')
print(len(images))
[print(im) for im in images]

# path joining version for other paths
#DIR = './Images/earth_jump/'
# print(len([name for name in os.listdir(DIR) if os.path.isfile(os.path.join(DIR, name))]))
# for name in os.listdir(DIR):
# 	 if os.path.isfile(os.path.join(DIR, name)):
# 	 	print(name)

# simple version for working with CWD
#print(len([name for name in os.listdir('.') if os.path.isfile(name)]))

#for name in os.listdir('.'):
#	if os.path.isfile(name):
#		print(name)
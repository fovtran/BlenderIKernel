import pip

def install(package):
    pip.main(['install', package])

try:
	import requests
except:
	install('requests')

try:
	import numpy
except:
	install('numpy')

try:
	import scipy
except:
	install('scipy')

try:
	import ipython
except:
	install('ipython')
#install('sklearn')
#install('pandas')
#install('bpython')

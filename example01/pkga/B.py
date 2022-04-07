from pkga import A as aA
from pkga.pkgb import A as bA

def funcb():
	aA.funca()
	bA.funca()
	print("pkga.funcb")

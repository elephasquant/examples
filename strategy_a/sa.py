def orders():
	with open("strategy_a.csv", "w+") as fp:
		fp.write("#symbol,side,qty\n")
		fp.write("000001.SZ,1,100\n")
		fp.write("000002.SZ,0,100\n")

def table(data,index=False,head="l",value="l",v="|",h="-",dot="+"):
	try:
		if type(data)!=dict:
			data = {
			data[0]:data[1:]
			}
		v=v[:1]
		h=h[:1]
		dot=dot[:1]
		headLen=list()
		heads=list(data.keys())
		values=list(data.values())

		for x in heads:
			headLen.append(len(str(x)))
		for z,x in enumerate(values):
			for y in x:
				if len(str(y))>headLen[z]:
					headLen[z]=len(y)

		if index:
			sums = len(str(len(values[0])))
			headLen.insert(0,sums)
			heads.insert(0,"")
			values.insert(0,list())
			for x in range(len(values[1])):
				values[0].append(x+1)

		print(f"{dot}",end="")
		for x in headLen:
			print(f"{h*(x+1)}{dot}",end="")

		print(f"\n{v}",end="")
		for y,x in enumerate(heads):
			if head.lower()=="r":
				print(f"{' '*(headLen[y]-len(str(x))+1)}{x}{v}",end="")
			else:
				print(f"{x}{' '*(headLen[y]-len(str(x))+1)}{v}",end="")

		print(f"\n{dot}",end="")
		for x in headLen:
			print(f"{h*(x+1)}{dot}",end="")

		print()
		for x in range(len(values[0])):
			for z,y in enumerate(values):
				if value.lower()=="r":
					print(f"{v}{' '*(headLen[z]-len(str(y[x]))+1)}{y[x]}",end="")
				else:
					print(f"{v}{y[x]}{' '*(headLen[z]-len(str(y[x]))+1)}",end="")
			print(f"{v}\n",end="")

		print(f"{dot}",end="")
		for x in headLen:
			print(f"{h*(x+1)}{dot}",end="")
	except Exception as e:
		raise e
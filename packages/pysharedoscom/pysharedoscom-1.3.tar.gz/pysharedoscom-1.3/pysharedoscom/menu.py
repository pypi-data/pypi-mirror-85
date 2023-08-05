import msvcrt,os
def cls(title=None):
	if os.name=="nt":
		os.system("cls")
	else:
		os.system("clear")
	if title is not None:
		print(title)
def menu(*text,title=None,desc=None,index=False,char="»",loc="l",align=True):
	try:
		if len(text)==1 and type(text[0])!=str:
			text=list(text[0])
		else:
			text=list(text)
		if index:
			for y,x in enumerate(text):
				text[y] = f"{y+1}. {x}"
		if align:
			maxi = len(text[0])
			for x in text:
				if len(x)>maxi:
					maxi=len(x)
			for y,x in enumerate(text):
				text[y] = f"{' '*(len(char)+1)}{x}"
				text[y] = f"{text[y]}{' '*(maxi-len(x))}"
		nn=0
		cls(title)
		for y,x in enumerate(text):
			if y==nn:
				if loc.lower()=="lr" or loc.lower()=="rl":
					if align:
						print(f"{char} {x[len(char)+1:]} {char}")
					else:
						print(f"{char} {x} {char}")
				elif loc.lower()=="r":
					if align:
						print(f"{x[len(char)+1:]} {char}")
					else:
						print(f"{x} {char}")
				else:
					if align:
						print(f"{char} {x[len(char)+1:]}")
					else:
						print(f"{char} {x}")
			else:
				if loc.lower()=="r" and align:
					print(x[len(char)+1:])
				else:
					print(x)
		if desc is not None:
			print(desc)
		while True:
			if msvcrt.kbhit():
				n = ord(msvcrt.getch())
				if n==224:
					n = ord(msvcrt.getch())
					if n==72:
						if nn>0:
							nn-=1
						cls(title)
						for y,x in enumerate(text):
							if y==nn:
								if loc.lower()=="lr" or loc.lower()=="rl":
									if align:
										print(f"{char} {x[len(char)+1:]} {char}")
									else:
										print(f"{char} {x} {char}")
								elif loc.lower()=="r":
									if align:
										print(f"{x[len(char)+1:]} {char}")
									else:
										print(f"{x} {char}")
								else:
									if align:
										print(f"{char} {x[len(char)+1:]}")
									else:
										print(f"{char} {x}")
							else:
								if loc.lower()=="r" and align:
									print(x[len(char)+1:])
								else:
									print(x)
						if desc is not None:
							print(desc)
					elif n==80:
						if nn<len(text)-1:
							nn+=1
						cls(title)
						for y,x in enumerate(text):
							if y==nn:
								if loc.lower()=="lr" or loc.lower()=="rl":
									if align:
										print(f"{char} {x[len(char)+1:]} {char}")
									else:
										print(f"{char} {x} {char}")
								elif loc.lower()=="r":
									if align:
										print(f"{x[len(char)+1:]} {char}")
									else:
										print(f"{x} {char}")
								else:
									if align:
										print(f"{char} {x[len(char)+1:]}")
									else:
										print(f"{char} {x}")
							else:
								if loc.lower()=="r" and align:
									print(x[len(char)+1:])
								else:
									print(x)
						if desc is not None:
							print(desc)
				elif n==13:
					break
	except Exception as e:
		raise e
	return nn
r = 0
quit = True
soma = True
while quit:
	i = input()
	i = i.lower()
	i = i.split()
	for split in i:
		if split == "on":
			soma = True
		elif split == "off":
			soma = False
		elif split == "=":
			print("Soma total: ", r)
		else:
			if soma:
				try:
					r += int(split)
				except:
					print("input invalido")
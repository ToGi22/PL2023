# [0-9]{2,3},(M|F),[0-9]{2,3},[0-9]{2,3},[0-9]{2,3},(0|1)

class heart:
	
	def __init__(self):
		with open("myheart.csv") as fp:
			file = fp.readlines()
			file.pop(0)
			self.heart = []
			for i in file:
				x = i.split(",")
				tuple_ = (int(x[0]),x[1],int(x[2]),int(x[3]),int(x[4]),bool(x[5]))
				self.heart.append(tuple_)

	def dist_sexo(self):
		m = 0
		f = 0
		for i in self.heart:
			if i[1] == "M":
				m += 1
			else:
				f += 1
		return m,f

	def dist_ee(self):
		r = {}
		for i in self.heart:
			idade = i[0]-i[0]%5
			try:
				value = r[idade]
				r[idade] = value+1
			except:
				r[idade] = 1
		return r

	def dist_nc(self):
		r = {}
		for i in self.heart:
			colesterol = i[3]-i[3]%10
			try:
				value = r[colesterol]
				r[colesterol] = value+1
			except:
				r[colesterol] = 1
		return r

#print(sorted(heart().dist_ee().items(), key=lambda x:x[0]))
# print(sorted(heart().dist_nc().items(), key=lambda x:x[0]))

# [0-9]{2,3},(M|F),[0-9]{2,3},[0-9]{2,3},[0-9]{2,3},(0|1)
from matplotlib import pyplot as plt
import textwrap

def table(title, rows):

	# calculate the maximum width of each column
	max_widths = [max(len(str(row[i])) for row in rows) for i in range(len(rows[0]))]

	# create the table title
	title_line = '+'.join('-' * (int(len(title)/2)+1) for i in range(len(rows[0])))
	title = textwrap.fill(title, 80)
	title = f"\n{title_line}\n|{title:^{sum(max_widths) + 4}}|\n{title_line}\n"

	# create the separator line
	sep = '+'.join('-' * (max_widths[i] + 2) for i in range(len(rows[0])))

	# create the table rows
	table = ''
	for row in rows:
		table += '\n' + '|'.join(textwrap.wrap(' | '.join(f"{r:<{max_widths[i]}}" for i, r in enumerate(row)), width=80))

	# print the table
	print(f"{title}{table}\n{sep}")

class heart:
	
	def __init__(self):
		with open("./TPC1/myheart.csv") as fp:
			file = fp.readlines()
			file.pop(0)
			self.heart = []
			for i in file:
				x = i.split(",")
				tuple_ = (int(x[0]),x[1],int(x[2]),int(x[3]),int(x[4]), True if x[5] == '1\n' else False)
				self.heart.append(tuple_)

	def dist_sexo(self):
		m = 0
		f = 0
		for i in self.heart:
			if i[5] == True:
				if i[1] == "M":
					m += 1
				else:
					f += 1
		return [(m,f)]

	def dist_ee(self):
		r = {}
		for i in self.heart:
			if i[5] == True:
				idade = i[0]-i[0]%5
				try:
					value = r[idade]
					r[idade] = value+1
				except:
					r[idade] = 1
		return sorted(r.items(), key=lambda x:x[0])

	def dist_nc(self):
		r = {}
		for i in self.heart:
			if i[5] == True:
				colesterol = i[3]-i[3]%10
				try:
					value = r[colesterol]
					r[colesterol] = value+1
				except:
					r[colesterol] = 1
		return sorted(r.items(), key=lambda x:x[0])

h = heart()
dist_sexo = h.dist_sexo()
dist_ee = h.dist_ee()
dist_nc = h.dist_nc()
table("Distribuicao por sexo", dist_sexo)
y1 = ["Masculino", "Feminino"]
y2 = list(h.dist_sexo()[0])
plt.bar(y1, y2, color="red")
plt.xlabel("Género")
plt.ylabel("Número de pessoas com a doença")
plt.title("Distribuição da doença por Género")
plt.show()

table("Distribuicao por idade", dist_ee)
y1 = dict(dist_ee).keys()
y2 = dict(dist_ee).values()
plt.bar(y1, y2, color="red")
plt.xlabel("Faixa Etária (anos)")
plt.ylabel("Número de pessoas com a doença")
plt.title("Distribuição da doença por Idades")
plt.show()

table("Distribuicao por colesterol", dist_nc)
y1 = dict(dist_nc).keys()
y2 = dict(dist_nc).values()
plt.bar(y1, y2, color="red")
plt.xlabel("Faixa Etária (anos)")
plt.ylabel("Número de pessoas com a doença")
plt.title("Distribuição da doença por Idades")
plt.show()
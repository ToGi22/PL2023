"""^\d+::\d{4}-\d{2}-\d{2}::[\w ]+::[\w ]*::[\w ]*::.*::$"""

import re
import os
import json
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

def parse(file):
	processos_por_ano = {}
	estrutura = re.compile(r'^(?P<pastas>\d+)::(?P<data>\d{4}-\d{2}-\d{2})::(?P<nome>[\w ]+)::(?P<pai>[\w ,]*)::(?P<mae>[\w ,]*)::(?P<observacoes>.*)::$')
	with open(file) as proc:
		lines = proc.readlines()
	for line in lines:
		line_dict = estrutura.search(line)
		if line_dict:
			line_dict = line_dict.groupdict()
			pasta = int(line_dict["data"][:4])
			try:
				processos_por_ano[pasta].append(line_dict)
			except:
				processos_por_ano[pasta] = [line_dict]
	return {k: processos_por_ano[k] for k in sorted(processos_por_ano)}

def freq_ano(processos_por_ano):
	r = {}
	for processos in processos_por_ano.items():
		r[processos[0]] = len(processos[1])
	return r

def freq_nomes(processos_por_ano):
	r_nome = {}
	r_apelidos = {}
	for processos in processos_por_ano.items():
		seculo = (processos[0] - (processos[0] % 100)) // 100 + 1
		r_nome[seculo] = {}
		r_apelidos[seculo] = {}
		for i in processos[1]:
			tmp = i["nome"].split()
			nome = tmp[0]
			apelido = tmp[-1]
			try:
				r_nome[seculo][nome] += 1
			except:
				r_nome[seculo][nome] = 1

			try:
				r_apelidos[seculo][apelido] += 1
			except:
				r_apelidos[seculo][apelido] = 1
		r_nome[seculo] = sorted(r_nome[seculo].items(), key=lambda x: x[1], reverse=True)[:5]
		r_apelidos[seculo] = sorted(r_apelidos[seculo].items(), key=lambda x: x[1], reverse=True)[:5]
	return r_nome, r_apelidos

def freq_relacoes(processos_por_ano):
	r = {}
	regex = re.compile(r'(,(?P<relacao>[\w ]+)\. Proc\.\d+)')
	for processos in processos_por_ano.values():
		for i in processos:
			tmp = regex.search(i["observacoes"])
			if tmp:
				tmp = tmp.groupdict()["relacao"]
				try:
					r[tmp] += 1
				except:
					r[tmp] = 1
	return r

def converter_para_json(file):
	r = {}
	estrutura = re.compile(r'^(?P<pastas>\d+)::(?P<data>\d{4}-\d{2}-\d{2})::(?P<nome>[\w ]+)::(?P<pai>[\w ,]*)::(?P<mae>[\w ,]*)::(?P<observacoes>.*)::$')
	with open(file) as proc:
		lines = proc.readlines()
	i = 0
	for line in lines:
		line_dict = estrutura.search(line)
		if line_dict:
			line_dict = line_dict.groupdict()
			pasta = int(line_dict["data"][:4])
			try:
				r[pasta].append(line_dict)
			except:
				r[pasta] = [line_dict]
			i += 1
			if i == 20:
				break
	return json.dumps(r, indent=4)
	

def main():
	file = "./TPC3/processos.txt"
	processos_por_ano = parse(file)
	os.system('clear')
	while True:
		print("---------Deseja visualizar qual dos exercicios---------")
		print("1 - Frequência de processos por ano" )
		print("2a - Frequência de Nomes próprios" )
		print("2b - Frequência de Apelidos" )
		print("3 - Frequêcia dos tipos de relações" )
		print("4 - Converter os 20 primeiros registos em um ficheiro json" )
		string = input()
		os.system('clear')
		match string:
			case "1":
				freq_por_ano = freq_ano(processos_por_ano)
				table("Frequencia de processos por ano", sorted(freq_por_ano.items(), key=lambda x:x[0]))
			case "2a":
				freq_por_nomes, freq_por_apelidos = freq_nomes(processos_por_ano)
				for k,v in freq_por_nomes.items():
					table("Seculo - " + str(k), v)

			case "2b":
				freq_por_nomes, freq_por_apelidos = freq_nomes(processos_por_ano)
				for k,v in freq_por_apelidos.items():
					table("Seculo - " + str(k), v)
				
			case "3":
				freq_por_relacao = freq_relacoes(processos_por_ano)
				table("Frequencia das relacoes", sorted(freq_por_relacao.items(), key=lambda x:x[0]))

			case "4":
				json_ = converter_para_json(file)
				print(json_)
				with open("./TPC3/d).json", "w") as fp:
					fp.write(json_)

			case "q":
				break

if __name__ == "__main__":
	main()
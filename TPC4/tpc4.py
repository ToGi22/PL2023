import re
import json
import math
import statistics

csv_file_path = './TPC4/asd.csv'
json_file_path = './TPC4/asd.json'

# Read CSV file with detected encoding and convert it to a list of dictionaries
with open(csv_file_path, encoding='utf-8') as csv_file:
    file = csv_file.readlines()

first_line = re.findall(r'(\w+(\{\d+,\d+\}[:\w]*,+|\{\d+\}[:\w]*,+)?)', file[0])

config = {}

expressao = r'^'

listas = {}
for iterador in first_line:
    if len(iterador[1]) == 0:
        # config[i[0]] = [0,0]
        expressao += fr'(?P<{iterador[0]}>[\w\d ]+),'
    else:
        tmp = re.split(r'}|{', iterador[0])
        nome = tmp[0]
        func = ""
        if "::" in tmp[2]:
            func = tmp[2][2:]
            func = re.match(r'\w+', func).group()
            nome = f"{nome}_{func}"
        tmp = tmp[1]
        if "," in tmp:
            # config[i[0]] = [int(tmp)*(-1),-1]
            tmp = tmp.split(",")
            expressao += fr'(?P<{nome}>([\w\d ]*,?){{{tmp[0]},{int(tmp[1])-1}}}[\w\d ]*),'
            if len(func) != 0:
                listas[nome] = func
            else:
                listas[nome] = ""
        else:
            # tmp = tmp.split(",")
            # config[i[0]] = [int(tmp[1]),int(tmp[0])]
            expressao += fr'(?P<{nome}>([\w\d ]+,?){{{int(tmp)-1}}}[\w\d ]+),'
            if len(func) != 0:
                listas[nome] = func
            else:
                listas[nome] = ""

expressao = expressao[:-1]+r'$'

expressao = re.compile(expressao)

r_file = []

for iterador in file:
    try:
        tmp = expressao.search(iterador).groupdict()
        for i in listas:
            x = tmp[i].split(",")
            if len(listas[i]) == 0:
                tmp[i] = x
            else:
                match (listas[i]):
                    case "sum":
                        x = sum(x)
                        tmp[i] = x
                    case "media":
                        x = statistics.mean(x)
                        tmp[i] = x
                    case "produto":
                        x = math.prod(x)
                        tmp[i] = x
                    case "mediana":
                        x = statistics.median(x)
                        tmp[i] = x
                    case "moda":
                        x = statistics.mode(x)
                        tmp[i] = x
        r_file.append(tmp)
    except:
        pass

with open(json_file_path, "w", encoding="utf-8") as fp:
    fp.write(json.dumps(r_file, indent=4))
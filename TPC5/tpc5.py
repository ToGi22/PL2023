import re
import math

def log(msg):
    print(f"maq: \"{msg}\"")
    
def print_saldo(saldo):
    r = math.modf(saldo)
    return f"{str(int(r[1]))}e{str(int(r[0]*100))}c"

def soma_saldo(moedas):
    saldo = 0
    for i in moedas:
        if i["tipo"] == "c":
            saldo += int(i["moeda"])/100
        else:
            saldo += int(i["moeda"])
    return saldo

moedas = re.compile(r"((?P<moeda>10?|20?|50?)(?P<tipo>c|e))\.?")

operacoes = [
    "LEVANTAR",
    "POUSAR",
    "MOEDA",
    "T=",
    "ABORTAR"
]

operacao = r"|".join(operacoes)

operacao = re.compile(operacao)

estado = False

saldo = 0

while(line := input()):
    if(operacao_atual := operacao.search(line)):
        operacao_atual = operacao_atual.group()
        if (operacao_atual == "LEVANTAR"):
            if estado:
                log("O telefone já está levantado! Por favor insira moedas ou ligue para um número!")
                print_saldo(saldo)
            else:
                estado = True
                log("Introduza moedas.")
        elif (operacao_atual == "POUSAR") and estado:
            log(f"troco={print_saldo(saldo)}; Volte sempre!")
            estado = False
            saldo = 0
        elif (operacao_atual == "MOEDA") and estado:
            x = re.split(",| ", line)
            moedas_invalidas = []
            moedas_introduzidas = []
            for i in x:
                try:
                    moedas_introduzidas.append(moedas.match(i).groupdict())
                except:
                    if i:
                        moedas_invalidas.append(i)
            saldo += soma_saldo(moedas_introduzidas)
            moedas_invalidas = moedas_invalidas[1:]
            if moedas_invalidas:
                tmp = ""
                for i in moedas_invalidas:
                    tmp += f"{i} - moeda inválida; "
                log(f"{tmp}saldo = {print_saldo(saldo)}")
            else:
                log(f"saldo = {print_saldo(saldo)}")
        elif (operacao_atual == "T=") and estado:
            custo = 0
            if re.fullmatch(r"T=(0{2})?\d{9}", line):
                line = line[2:]
                if re.match(r"601", line) or re.match(r"641", line):
                    log("Esse número não é permitido neste telefone. Queira discar novo número!")
                    custo = None
                elif re.match(r"00", line):
                    custo += 1.5
                elif re.match(r"2", line):
                    custo += 0.25
                elif re.match(r"808", line):
                    custo += 0.10
                elif re.match(r"800", line):
                    custo += 0
                else:
                    log("O número para o qual ligou não está atribuído!")
                    custo = None
                if custo!=None:
                    if (saldo - custo) < 0:
                        log("Saldo Insuficiente! Por favor introduza mais moedas.")
                    else:
                        saldo -= custo
                        log(f"saldo = {print_saldo(saldo)}")
            else:
                log("O número apresentado não apresenta um formato correto! Por favor insira um novo número!")
            
        elif (operacao_atual == "ABORTAR") and estado:
            estado = False
            log(f"troco={print_saldo(saldo)}; Volte sempre!")
            saldo = 0
        else:
            log("Levante o telefone primeiro!")
    else:
        log("Operação Inválida")

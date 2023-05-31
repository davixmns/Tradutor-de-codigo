import re
from tkinter import filedialog

entrada = filedialog.askopenfile(title="SELECIONE O ARQUIVO DE ENTRADA")
saida = open("saida.js", "w")

tabs = 0
tabsContados = 0
palavrasChave = ['%', "<",">", "in", "range", "/", "-", "+", "*", "if", "else", "elif", "while", 'for', "print", "int(", "str(", "float(", "input(", "range(", ":", "and", "or", "console"]
palavras = []
variaveis_declaradas = []

def darTabs(linha):
    global tabs
    global tabsContados
    num_spaces = len(re.match(r'^\s*', linha).group(0))
    tabsContados = num_spaces // 4
    if tabsContados < tabs:
        while tabsContados < tabs:
            tabs -= 1
            novaLinha = '\t' * tabs + '}\n'
            saida.write(novaLinha)
            tabsContados += 1

for linha in entrada:
    darTabs(linha)

    if "while" in linha:
        linha = linha.replace(":", ") {")
        linha = linha.replace("while", "while (")
        tabs += 1
        saida.write(linha)
    
    if "if" in linha:
        if "and" in linha:
            linha = linha.replace("and", "&&")
        elif "or" in linha:
            linha = linha.replace("or", "||")
        linha = linha.replace(":", ") {")
        linha = linha.replace("if", "if (")
        tabs += 1
        saida.write(linha)
    
    if "else" in linha:
        linha = linha.replace("else:", "else {")
        tabs += 1
        saida.write(linha)

    if "elif" in linha:
        linha = linha.replace(":", ") {")
        linha = linha.replace("elif", "else if (")
        tabs += 1
        saida.write(linha)

    if "print" in linha:
        linha = linha.replace("print", "console.log")
        saida.write(linha)

    if "int(" in linha:
        linha = linha.replace("int(", "parseInt(")
    if "str(" in linha:
        linha = linha.replace("str(", "String(")
    if "float(" in linha:
        linha = linha.replace("float(", "parseFloat(")
    if "input(" in linha:
        linha = linha.replace("input(", "prompt(")

    if "for" in linha:
        tabs += 1
        palavras = linha.split(" ")
        palavras = list(filter(lambda a: a != "", palavras))
        variable = palavras[1]
        range_value = palavras[3].replace("range(", "").replace(")", "")
        linha = f"for (var {variable} = 0; {variable} <= {range_value}; {variable}++) {{\n"
        linha = linha.replace(',', '')
        linha = ('\t' * (tabs-1)) + linha
        saida.write(linha)

    if '=' in linha:
        palavrasDaLinha = linha.split(" ")
        palavrasDaLinha = list(filter(lambda a: a != "", palavrasDaLinha))
        variavel = palavrasDaLinha[0]
        flag = True
        variavel = variavel.strip()

        if variavel not in variaveis_declaradas:

            for pl in palavrasDaLinha:
                if pl in palavrasChave:
                    flag = False
            
            for vd in variaveis_declaradas:
                for pc in palavrasChave:
                    if pc in vd or pc in vd:
                        flag = False

            if flag:
                variaveis_declaradas.append(variavel)
                novaLinha =  ('\t' * tabs) + f"var {variavel} = " + " ".join(palavrasDaLinha[2:])
                saida.write(novaLinha)
        else:
            saida.write(linha)
            
        
                
saida.write('\n')
while tabs > 0:
    tabs -= 1
    saida.write('\t' * tabs + '}\n')

entrada.close()
saida.close()
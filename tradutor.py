import re
from tkinter import filedialog

entrada = filedialog.askopenfile(title="SELECIONE O ARQUIVO DE ENTRADA")
saida = open("saida.js", "w")

tabs = 0
tabsContados = 0
palavrasChave = ["<",">", "in", "range", "/", "-", "+", "*", "if", "else", "elif", "while", "for", "print", "int(", "str(", "float(", "input(", "range(", ":", "and", "or"]
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
    
    elif "if" in linha:
        if "and" in linha:
            linha = linha.replace("and", "&&")
        elif "or" in linha:
            linha = linha.replace("or", "||")
        linha = linha.replace(":", ") {")
        linha = linha.replace("if", "if (")
        tabs += 1
        saida.write(linha)
    
    elif "else" in linha:
        linha = linha.replace("else:", "else {")
        tabs += 1
        saida.write(linha)

    elif "elif" in linha:
        linha = linha.replace(":", ") {")
        linha = linha.replace("elif", "else if (")
        tabs += 1
        saida.write(linha)

    elif "print" in linha:
        linha = linha.replace("print", "console.log")
        saida.write(linha)

    elif "int(" in linha:
        linha = linha.replace("int(", "parseInt(")
    elif "str(" in linha:
        linha = linha.replace("str(", "String(")
    elif "float(" in linha:
        linha = linha.replace("float(", "parseFloat(")
    elif "input(" in linha:
        linha = linha.replace("input(", "prompt(")

    elif "for" in linha:
        tabs += 1
        palavras = linha.split(" ")
        palavras = list(filter(lambda a: a != "", palavras))
        variable = palavras[1]
        range_value = palavras[3].replace("range(", "").replace(")", "")
        linha = f"for (var {variable} = 0; {variable} <= {range_value}; {variable}++) {{\n"
        linha = linha.replace(',', '')
        linha = ('\t' * (tabs-1)) + linha
        saida.write(linha)

    elif "=" in linha:
        palavrasDaLinha = linha.split(" ")
        palavrasDaLinha = list(filter(lambda a: a != "", palavrasDaLinha))
        variavel = palavrasDaLinha[0]

        for palavra in palavrasDaLinha:
            if palavra in palavrasChave:
                break
        if variavel not in variaveis_declaradas:
            variaveis_declaradas.append(variavel)
            novaLinha =  ('\t' * tabs) + f"var {variavel} = " + " ".join(palavrasDaLinha[2:])
            saida.write(novaLinha)

    
saida.write('\n')
while tabs > 0:
    tabs -= 1
    saida.write('\t' * tabs + '}\n')
    
entrada.close()
saida.close()
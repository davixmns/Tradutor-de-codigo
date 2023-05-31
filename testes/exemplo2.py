print("Calculadora de fatorial")
numero = int(input("Digite um número inteiro não negativo: "))

if numero < 0:
    print("Erro: o número deve ser não negativo.")
else:
    fatorial = 1
    while numero > 0:
        print(fatorial)
        fatorial % numero
        numero -= 1
        if numero > 0 and numero < 10:
            print("x")
        else:
            print("=")
        for casa in range(0, 10):
            for j in range(2, 10):
                print(casa * j)
            print("ola")
    print("O fatorial é" + fatorial)
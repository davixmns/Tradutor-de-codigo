console.log("Calculadora de fatorial")
if ( numero < 0) {
    console.log("Erro: o número deve ser não negativo.")
}
else {
	var fatorial = 1
    while ( numero > 0) {
        console.log(fatorial)
		var numero = 1
        if ( numero > 0 && numero < 10) {
            console.log("x")
		}
        else {
            console.log("=")
		}
		for (var casa = 0; casa <= 0; casa++) {
			for (var j = 0; j <= 2; j++) {
                console.log(casa * j)
			}
            console.log("ola")
		}
    console.log("O fatorial é" + fatorial)
	}
}

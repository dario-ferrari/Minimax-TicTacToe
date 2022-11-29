flag_aviso = True

def main():
    
    v = ""
    while v != "1" and v != "2":
        v = input("En que turno queres jugar?: ")
    tateti = Tateti(int(v))
    
    posicion = ""
    
    if(int(v) == 1):
        while not validar_entrada(posicion):
            posicion = input("Inserte posicion a llenar en formato FILA COLUMNA: ")
    else:
        while not validar_entrada(posicion):
            posicion = input("Inserte posicion para la maquina en formato FILA COLUMNA: ")
            
    jugada = posicion.split(" ")
    jugada[0] = int(jugada[0]) - 1
    jugada[1] = int(jugada[1]) - 1
    tateti.jugar(jugada)
    
def validar_entrada(entrada):
    inputs_validos = ["1 1","1 2","1 3","2 1","2 2","2 3","3 1","3 2","3 3"]
    if(entrada in inputs_validos):
        return True
    return False

def gano(estado,jugador):
    estados_victoria = [
        [estado[0][0], estado[0][1], estado[0][2]],
        [estado[1][0], estado[1][1], estado[1][2]],
        [estado[2][0], estado[2][1], estado[2][2]],
        [estado[0][0], estado[1][0], estado[2][0]],
        [estado[0][1], estado[1][1], estado[2][1]],
        [estado[0][2], estado[1][2], estado[2][2]],
        [estado[0][0], estado[1][1], estado[2][2]],
        [estado[2][0], estado[1][1], estado[0][2]],
    ]
    if [jugador, jugador, jugador] in estados_victoria:
        return True
    else:
        return False
        
def celdasVacias(estado):
    celdas = []
    for x, fila in enumerate(estado):
        for y, celda in enumerate(fila):
            if celda == 0:
                celdas.append([x, y])
    return celdas

def minimax(estado,profundidad, nivel):
    global flag_aviso
    if(gano(estado,2)):
        return 1
    if(gano(estado,1)):
        return -1
    if(celdasVacias(estado) == []):
        return 0
    if(nivel == "MAX"):
        valor = float("-inf")
    else:
        valor = float("inf")
    for celda in celdasVacias(estado):      
        if(nivel == "MAX"):
            sig = estado
            sig[celda[0]][celda[1]] = 2
            valor = max(valor,minimax(sig,profundidad+1,"MIN"))
            sig[celda[0]][celda[1]] = 0
        else:
            sig = estado
            sig[celda[0]][celda[1]] = 1
            valor = min(valor,minimax(sig,profundidad+1,"MAX"))
            sig[celda[0]][celda[1]] = 0
    if(valor > 0 and profundidad == 0 and flag_aviso == True):
        print("Ya perdiste no hay forma de que empates")
        flag_aviso = False
    return valor

def mejor_movimiento(estado):
    mejorValor = -1000
    movimiento = (-1, -1)
    for c in celdasVacias(estado):
        estado[c[0]][c[1]] = 2
        valor = minimax(estado,0,"MIN")
        estado[c[0]][c[1]] = 0

        if(valor > mejorValor):
            movimiento = c
            mejorValor = valor
    print("El mejor mov es " + str(movimiento))
    return movimiento



class Tateti:
    def __init__(self,turno):
        self.estado = [[0,0,0],[0,0,0],[0,0,0]]
        self.turno = turno
        
    def jugar(self,posicion):
        inicial = 0
        while not self.resultado():
            if(self.turno == 1):
                if(inicial == 0):
                    self.estado[posicion[0]][posicion[1]] = 1
                else:
                    self.pedir_jugada()
                if(self.resultado()):
                    break
                movimiento = mejor_movimiento(self.estado)
                self.estado[movimiento[0]][movimiento[1]] = 2
                self.imprimirEstado()
                self.turno = 2
                inicial += 1
            else:
                if(inicial == 0):
                    self.estado[posicion[0]][posicion[1]] = 2
                    self.imprimirEstado()
                self.pedir_jugada()
                if(self.resultado()):
                    break
                movimiento = mejor_movimiento(self.estado)
                self.estado[movimiento[0]][movimiento[1]] = 2
                self.imprimirEstado()
                self.turno = 1
                inicial += 1


    def pedir_jugada(self):
        
        movJugador = ""
        while (not validar_entrada(movJugador)) or ([int(x) - 1 for x in movJugador.split(" ")]) not in celdasVacias(self.estado):
            movJugador = input("Inserte posicion a llenar en formato FILA COLUMNA: ")
        jugada = movJugador.split(" ")
        self.estado[int(jugada[0]) - 1][int(jugada[1])- 1] = 1
        return
    
    def resultado(self):
        if(gano(self.estado,2)):
            print("Perdiste")
            return True
        elif(celdasVacias(self.estado) == []):
            print("Empataste")
            return True
        else:
            return False
        
    def imprimirEstado(self):
        for f in self.estado:
            linea = ""
            for c in f:
                
                if c == 0:
                    linea += "   "
                elif c == 1:
                    linea += " O "
                else:
                    linea += " X "
            print(linea)        

    
main()
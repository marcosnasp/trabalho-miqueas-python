# 1.9. Escreva um programa que leia uma matriz A3x3 e calcule a sua inversa.
a_11 = 5
a_12 = 10
a_13 = 2

a_21 = 1
a_22 = 2
a_23 = 3

a_31 = 2
a_32 = 3
a_33 = 4

matriz_3_3 = [[a_11, a_12, a_13], [a_21, a_22, a_23], [a_31, a_32, a_33]]
matriz_identidade = [[1, 0, 0], [0, 1, 0], [0, 0, 1]]

#inversa = [[ai_11, ai_12, ai_13], [ai_21, ai_22, ai_23], [ai_31, ai_32, ai_33]]

inversa = [[0 for x in range(3)] for y in range(3)]
res = [[0 for x in range(3)] for y in range(3)]

print(res)
# explicit for loops
for i in range(len(matriz_3_3)):
    for j in range(len(matriz_identidade[0])):
        for k in range(len(matriz_identidade)):
            # resulted matrix
            res[i][j] += matriz_3_3[i][k] * matriz_identidade[k][j]

print(res)

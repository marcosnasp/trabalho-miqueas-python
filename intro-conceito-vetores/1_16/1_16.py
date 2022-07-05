
import random

num_total_alunos = input('Informe o total de alunos da turma')

notas_aluno = []

numero_questoes = 30
for x in range(numero_questoes):
    # Gerando notas aleatorias num intervalo de A a E, totalizando 30 questoes e
    # armazenando em notas_aluno
    notas_aluno.append(chr(random.randint(ord('A'), ord('E'))))


gabarito = ['A', 'C', 'D', 'E', 'A',
            'B', 'C', 'E', 'A', 'E',
            'C', 'E', 'A', 'A', 'E',
            'B', 'C', 'A', 'E', 'A',
            'E', 'E', 'A', 'C', 'B',
            'A', 'B', 'D', 'E', 'E']


b = [i for i, j in zip(notas_aluno, gabarito) if i == j]
print(b)
print('Total de acertos é: ', len(b))

#a = list(set(gabarito).intersection(set(gabarito)))
# print(a)

#print('Numero de acertos do Aluno 1: ', acertos_aluno_1)

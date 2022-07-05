
import math

total_horas_motorista = int(input(
    'Informe o total de horas trabalhadas pelo motorista no mês: '))
numero_horas_extras_permitidas = 20

print("O número de horas trabalhadas pelo motorista no mês é: ", total_horas_motorista)

print("Analisando carga horária total")

horas_excedentes = total_horas_motorista - 160
horas_excedentes_alem_das_permitidas = 0
contagem_dias_inteiros_excedentes = 0

if (horas_excedentes > 0):
    print("Número de horas trabalhadas excedentes é: ", horas_excedentes)
    if (horas_excedentes > numero_horas_extras_permitidas):
        horas_excedentes_alem_das_permitidas = horas_excedentes - \
            numero_horas_extras_permitidas
        print("Excedeu o total de {0} horas extras permitidas em {1}".format(
            numero_horas_extras_permitidas, horas_excedentes_alem_das_permitidas))
        print("Terá direito a {0} horas extras excedentes de pagamento em dinheiro".format(
            numero_horas_extras_permitidas))
        contagem_dias_inteiros_excedentes = math.trunc(
            horas_excedentes_alem_das_permitidas / 8)
        print("Terá {0} dias de folga".format(
            contagem_dias_inteiros_excedentes))
        horas_restantes_dias_inteiros = horas_excedentes_alem_das_permitidas % 8
        print("Horas Restantes depois da contagem dos dias de folga: {0}".format(
            horas_restantes_dias_inteiros))
        if (horas_restantes_dias_inteiros > 0):
            print("Somando {0} horas restantes a {1} horas extras totais recebidas, totalizando a quantidade de horas extras de {2}".format(
                horas_restantes_dias_inteiros, numero_horas_extras_permitidas, (horas_restantes_dias_inteiros + numero_horas_extras_permitidas)))
    elif (horas_excedentes <= numero_horas_extras_permitidas):
        print("Terá direito a {0} horas extras excedentes de pagamento em dinheiro".format(
            numero_horas_extras_permitidas - horas_excedentes))

class Cliente:
    def __init__(self, id, nome, saldo, valor_rendimento) -> None:
        self.id = id
        self.nome = nome
        self.saldo = saldo
        self.valor_rendimento = valor_rendimento

    def sacar(valorSaque):
        if self.saldo >= 0 and valorSaque <= self.saldo:
            self.saldo = self.saldo - valorSaque

    def depositar(valorDeposito):
        self.saldo = self.saldo + valorDeposito

from tokenize import Double


class Cliente:
    def __init__(self, id, nome, saldo, valor_rendimento) -> None:
        self.id = int(id)
        self.nome = str(nome)
        self.saldo = saldo
        self.valor_rendimento = valor_rendimento

    @classmethod
    def sacar(valorSaque):
        if self.saldo > 0 and valorSaque <= self.saldo:
            self.saldo = self.saldo - valorSaque

    @classmethod
    def depositar(valorDeposito):
        self.saldo = self.saldo + valorDeposito

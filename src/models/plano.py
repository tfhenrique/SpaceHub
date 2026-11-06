class PlanoSubscricao:
    """Um plano de subscrição (tabela PlanoSubscricao)."""

    def __init__(self, nome, tipo, preco_mensal, horas_sala_incl=0,
                 max_convidados=0, id=None):
        self.id = id
        self.nome = nome
        self.tipo = tipo                      # Flex, Dedicado ou Escritorio
        self.preco_mensal = preco_mensal
        self.horas_sala_incl = horas_sala_incl
        self.max_convidados = max_convidados
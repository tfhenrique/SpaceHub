class Sala:
    """Uma sala de reunião (tabela Sala)."""

    def __init__(self, nome, capacidade, equipamentos, preco_hora_extra, id=None):
        self.id = id
        self.nome = nome
        self.capacidade = capacidade
        self.equipamentos = equipamentos
        self.preco_hora_extra = preco_hora_extra
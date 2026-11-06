class Posto:
    """Um posto de trabalho (tabela Posto)."""

    def __init__(self, numero, tipo, ativo=True, descricao=None, id=None):
        self.id = id
        self.numero = numero
        self.tipo = tipo              # 'flex' ou 'dedicado'
        self.ativo = ativo
        self.descricao = descricao

    
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

    @classmethod
    def de_linha(cls, r):
        """Cria um objeto a partir de uma linha devolvida pela base de dados."""
        return cls(r.nome, r.tipo, r.preco_mensal, r.horas_sala_incl,
                   r.max_convidados, r.id)

    @classmethod
    def listar(cls, conn):
        cursor = conn.cursor()
        cursor.execute(
            'SELECT id, nome, tipo, preco_mensal, horas_sala_incl, max_convidados'
            ' FROM PlanoSubscricao ORDER BY preco_mensal'
        )
        planos = [cls.de_linha(r) for r in cursor.fetchall()]
        cursor.close()
        return planos

    @classmethod
    def obter(cls, conn, id):
        cursor = conn.cursor()
        cursor.execute(
            'SELECT id, nome, tipo, preco_mensal, horas_sala_incl, max_convidados'
            ' FROM PlanoSubscricao WHERE id = ?', (id,)
        )
        r = cursor.fetchone()
        cursor.close()
        return cls.de_linha(r) if r else None

    def obter_beneficios(self):
        """Texto com os benefícios do plano."""
        return (f'{self.nome}: {self.preco_mensal} €/mês, '
                f'{self.horas_sala_incl} h de sala incluídas, '
                f'até {self.max_convidados} convidados.')

    def __str__(self):
        return f'[{self.id}] {self.nome} ({self.tipo}) - {self.preco_mensal} €/mês'
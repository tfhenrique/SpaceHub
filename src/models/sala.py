class Sala:
    """Uma sala de reunião (tabela Sala)."""

    def __init__(self, nome, capacidade, equipamentos, preco_hora_extra, id=None):
        self.id = id
        self.nome = nome
        self.capacidade = capacidade
        self.equipamentos = equipamentos
        self.preco_hora_extra = preco_hora_extra

    @classmethod
    def de_linha(cls, r):
        return cls(r.nome, r.capacidade, r.equipamentos, r.preco_hora_extra, r.id)

    @classmethod
    def listar(cls, conn):
        cursor = conn.cursor()
        cursor.execute('SELECT id, nome, capacidade, equipamentos, preco_hora_extra'
                       ' FROM Sala ORDER BY capacidade')
        salas = [cls.de_linha(r) for r in cursor.fetchall()]
        cursor.close()
        return salas

    def esta_livre(self, conn, data, hora_inicio, hora_fim):
        """True se a sala não tem reservas confirmadas nesse horário."""
        cursor = conn.cursor()
        cursor.execute(
            "SELECT COUNT(*) AS n FROM Reserva"
            " WHERE sala_id = ? AND estado = 'Confirmada' AND data = ?"
            " AND hora_inicio < ? AND hora_fim > ?",
            (self.id, data, hora_fim, hora_inicio)
        )
        livre = cursor.fetchone().n == 0
        cursor.close()
        return livre

    @classmethod
    def listar_livres(cls, conn, data, hora_inicio, hora_fim, participantes=1):
        """Salas livres, com capacidade para o número de participantes (RF03)."""
        cursor = conn.cursor()
        cursor.execute(
            "SELECT s.id, s.nome, s.capacidade, s.equipamentos, s.preco_hora_extra"
            " FROM Sala s"
            " WHERE s.capacidade >= ?"
            " AND NOT EXISTS (SELECT 1 FROM Reserva r"
            "                 WHERE r.sala_id = s.id AND r.estado = 'Confirmada'"
            "                 AND r.data = ? AND r.hora_inicio < ? AND r.hora_fim > ?)"
            " ORDER BY s.capacidade",
            (participantes, data, hora_fim, hora_inicio)
        )
        salas = [cls.de_linha(r) for r in cursor.fetchall()]
        cursor.close()
        return salas

    def __str__(self):
        return f'{self.nome} ({self.capacidade} pessoas) - {self.equipamentos}'
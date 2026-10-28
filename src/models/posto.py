class Posto:
    """Um posto de trabalho (tabela Posto)."""

    def __init__(self, numero, tipo, ativo=True, descricao=None, id=None):
        self.id = id
        self.numero = numero
        self.tipo = tipo              # 'flex' ou 'dedicado'
        self.ativo = ativo
        self.descricao = descricao

    @classmethod
    def de_linha(cls, r):
        return cls(r.numero, r.tipo, bool(r.ativo), r.descricao, r.id)

    @classmethod
    def listar(cls, conn, tipo=None):
        sql = 'SELECT id, numero, tipo, ativo, descricao FROM Posto'
        params = []
        if tipo:
            sql += ' WHERE tipo = ?'
            params.append(tipo)
        sql += ' ORDER BY numero'
        cursor = conn.cursor()
        cursor.execute(sql, params)
        postos = [cls.de_linha(r) for r in cursor.fetchall()]
        cursor.close()
        return postos

    def esta_livre(self, conn, data, hora_inicio, hora_fim):
        """True se o posto está ativo e sem reservas confirmadas nesse horário."""
        if not self.ativo:
            return False
        cursor = conn.cursor()
        cursor.execute(
            "SELECT COUNT(*) AS n FROM Reserva"
            " WHERE posto_id = ? AND estado = 'Confirmada' AND data = ?"
            " AND hora_inicio < ? AND hora_fim > ?",
            (self.id, data, hora_fim, hora_inicio)
        )
        livre = cursor.fetchone().n == 0
        cursor.close()
        return livre

    @classmethod
    def listar_livres(cls, conn, data, hora_inicio, hora_fim, tipo='flex'):
        """Postos livres num dia e intervalo de horas (RF03).
        Os postos dedicados são de reserva mensal, por isso o normal é 'flex'."""
        cursor = conn.cursor()
        cursor.execute(
            "SELECT p.id, p.numero, p.tipo, p.ativo, p.descricao FROM Posto p"
            " WHERE p.ativo = 1 AND p.tipo = ?"
            " AND NOT EXISTS (SELECT 1 FROM Reserva r"
            "                 WHERE r.posto_id = p.id AND r.estado = 'Confirmada'"
            "                 AND r.data = ? AND r.hora_inicio < ? AND r.hora_fim > ?)"
            " ORDER BY p.numero",
            (tipo, data, hora_fim, hora_inicio)
        )
        postos = [cls.de_linha(r) for r in cursor.fetchall()]
        cursor.close()
        return postos

    def __str__(self):
        return f'Posto {self.numero} ({self.tipo})'
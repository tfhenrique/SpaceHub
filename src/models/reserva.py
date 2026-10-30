import pyodbc
from datetime import datetime, date
from decimal import Decimal, ROUND_HALF_UP
from db import mensagem_erro


def euros(valor):
    """Arredonda para 2 casas decimais."""
    return Decimal(valor).quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)


class Reserva:
    """Uma reserva de um posto OU de uma sala (tabela Reserva)."""

    def __init__(self, membro_id, data, hora_inicio, hora_fim, posto_id=None,
                 sala_id=None, estado='Confirmada', custo_calculado=0, id=None):
        self.id = id
        self.membro_id = membro_id
        self.posto_id = posto_id
        self.sala_id = sala_id
        self.data = data
        self.hora_inicio = hora_inicio
        self.hora_fim = hora_fim
        self.estado = estado
        self.custo_calculado = Decimal(custo_calculado)
        self.recurso = None        # nome do posto/sala (só quando vem de uma listagem)

    @classmethod
    def de_linha(cls, r):
        reserva = cls(r.membro_id, r.data, r.hora_inicio, r.hora_fim, r.posto_id,
                      r.sala_id, r.estado, r.custo_calculado, r.id)
        reserva.recurso = getattr(r, 'recurso', None)
        return reserva

    # ------------------------------------------------- cálculos (sem BD)
    @staticmethod
    def minutos_entre(hora_inicio, hora_fim):
        hoje = date.today()
        dif = datetime.combine(hoje, hora_fim) - datetime.combine(hoje, hora_inicio)
        return int(dif.total_seconds() // 60)

    @staticmethod
    def calcular_custo_sala(minutos_usados, minutos_novos, horas_incluidas, preco_hora):
        """Só se paga o que passar das horas de sala incluídas no plano (no mês).
        REGRA PROVISÓRIA: confirmar com o Product Owner."""
        incluido = horas_incluidas * 60
        extra_antes = max(0, minutos_usados - incluido)
        extra_depois = max(0, minutos_usados + minutos_novos - incluido)
        minutos_extra = extra_depois - extra_antes
        return euros(Decimal(minutos_extra) / 60 * Decimal(preco_hora))

    @staticmethod
    def custo_cancelamento(valor_reserva, inicio, agora):
        """RF12: com 24 h ou mais de antecedência não custa nada;
        com menos de 24 h cobra 50% do valor da reserva."""
        horas_ate_inicio = (inicio - agora).total_seconds() / 3600
        if horas_ate_inicio >= 24:
            return Decimal('0.00')
        return euros(Decimal(valor_reserva) * Decimal('0.5'))

    # ------------------------------------------------------- com a BD
    def calcular_custo(self, conn):
        """Custo da reserva. Postos: 0 (incluídos no plano - regra provisória).
        Salas: só as horas acima das incluídas no plano do membro, no mês."""
        if self.posto_id is not None:
            return Decimal('0.00')

        cursor = conn.cursor()
        cursor.execute('SELECT preco_hora_extra FROM Sala WHERE id = ?', (self.sala_id,))
        sala = cursor.fetchone()
        cursor.execute(
            'SELECT p.horas_sala_incl FROM Membro m'
            ' INNER JOIN PlanoSubscricao p ON p.id = m.plano_id WHERE m.id = ?',
            (self.membro_id,)
        )
        plano = cursor.fetchone()
        cursor.execute(
            "SELECT ISNULL(SUM(DATEDIFF(MINUTE, hora_inicio, hora_fim)), 0) AS minutos"
            " FROM Reserva WHERE membro_id = ? AND sala_id IS NOT NULL"
            " AND estado = 'Confirmada' AND YEAR(data) = ? AND MONTH(data) = ?",
            (self.membro_id, self.data.year, self.data.month)
        )
        usados = cursor.fetchone().minutos
        cursor.close()

        if sala is None or plano is None:
            return Decimal('0.00')      # a validação a sério é feita em criar()
        novos = self.minutos_entre(self.hora_inicio, self.hora_fim)
        return self.calcular_custo_sala(usados, novos, plano.horas_sala_incl,
                                        sala.preco_hora_extra)

    def ha_conflito(self, conn):
        """True se já existir outra reserva confirmada que se sobreponha."""
        cursor = conn.cursor()
        cursor.execute(
            "SELECT COUNT(*) AS n FROM Reserva"
            " WHERE estado = 'Confirmada' AND data = ?"
            " AND ((? IS NOT NULL AND posto_id = ?) OR (? IS NOT NULL AND sala_id = ?))"
            " AND hora_inicio < ? AND hora_fim > ? AND id <> ?",
            (self.data, self.posto_id, self.posto_id, self.sala_id, self.sala_id,
             self.hora_fim, self.hora_inicio, self.id or 0)
        )
        conflito = cursor.fetchone().n > 0
        cursor.close()
        return conflito

    def criar(self, conn):
        """Cria a reserva (RF04/RF05). A verificação de conflitos e a gravação
        são feitas pelo procedimento sp_CriarReserva, numa só transação,
        por isso não há dupla reserva mesmo com acessos simultâneos (RNF01)."""
        if (self.posto_id is None) == (self.sala_id is None):
            print('Erro: indique um posto OU uma sala.')
            return False
        try:
            self.custo_calculado = self.calcular_custo(conn)
            conn.commit()                 # termina a leitura anterior
            conn.autocommit = True        # o procedimento trata da sua transação
            cursor = conn.cursor()
            cursor.execute(
                'SET NOCOUNT ON; DECLARE @id INT;'
                ' EXEC dbo.sp_CriarReserva @membro_id = ?, @posto_id = ?, @sala_id = ?,'
                ' @data = ?, @hora_inicio = ?, @hora_fim = ?, @custo_calculado = ?,'
                ' @nova_reserva_id = @id OUTPUT;'
                ' SELECT @id;',
                (self.membro_id, self.posto_id, self.sala_id, self.data,
                 self.hora_inicio, self.hora_fim, self.custo_calculado)
            )
            self.id = cursor.fetchone()[0]
            cursor.close()
            return True
        except pyodbc.Error as e:
            print('Não foi possível reservar:', mensagem_erro(e))
            return False
        finally:
            conn.autocommit = False

    def cancelar(self, conn):
        """Cancela a reserva aplicando a política das 24 h (RF12).
        Devolve o custo do cancelamento, ou None se não foi possível cancelar."""
        cursor = conn.cursor()
        try:
            cursor.execute(
                'SELECT r.estado, r.data, r.hora_inicio, r.hora_fim, s.preco_hora_extra'
                ' FROM Reserva r LEFT JOIN Sala s ON s.id = r.sala_id WHERE r.id = ?',
                (self.id,)
            )
            r = cursor.fetchone()
            if r is None:
                print('Reserva não encontrada.')
                return None
            if r.estado == 'Cancelada':
                print('Esta reserva já está cancelada.')
                return None

            inicio = datetime.combine(r.data, r.hora_inicio)
            agora = datetime.now()
            if inicio <= agora:
                print('Não é possível cancelar: a reserva já começou ou já passou.')
                return None

            # valor da reserva: horas x preço da sala (os postos não têm preço)
            if r.preco_hora_extra is None:
                valor = Decimal('0.00')
            else:
                horas = Decimal(self.minutos_entre(r.hora_inicio, r.hora_fim)) / 60
                valor = euros(horas * Decimal(r.preco_hora_extra))

            custo = self.custo_cancelamento(valor, inicio, agora)
            cursor.execute(
                "UPDATE Reserva SET estado = 'Cancelada', custo_calculado = ?"
                " WHERE id = ? AND estado = 'Confirmada'", (custo, self.id)
            )
            conn.commit()
            self.estado = 'Cancelada'
            self.custo_calculado = custo
            return custo
        except pyodbc.Error as e:
            conn.rollback()
            print('Erro na base de dados:', mensagem_erro(e))
            return None
        finally:
            cursor.close()

    @classmethod
    def listar_do_membro(cls, conn, membro_id, futuras=None):
        """Agenda pessoal (RF06). futuras=True só futuras, False só passadas."""
        sql = ("SELECT r.id, r.membro_id, r.posto_id, r.sala_id, r.data, r.hora_inicio,"
               " r.hora_fim, r.estado, r.custo_calculado,"
               " COALESCE(N'Posto ' + CAST(p.numero AS NVARCHAR(5)), s.nome) AS recurso"
               " FROM Reserva r"
               " LEFT JOIN Posto p ON p.id = r.posto_id"
               " LEFT JOIN Sala s ON s.id = r.sala_id"
               " WHERE r.membro_id = ?")
        params = [membro_id]
        if futuras is True:
            sql += ' AND r.data >= ?'
            params.append(date.today())
        elif futuras is False:
            sql += ' AND r.data < ?'
            params.append(date.today())
        sql += ' ORDER BY r.data DESC, r.hora_inicio'
        cursor = conn.cursor()
        cursor.execute(sql, params)
        reservas = [cls.de_linha(r) for r in cursor.fetchall()]
        cursor.close()
        return reservas

    def __str__(self):
        onde = self.recurso or (f'posto {self.posto_id}' if self.posto_id else f'sala {self.sala_id}')
        return (f'[{self.id}] {onde} em {self.data} '
                f'{self.hora_inicio:%H:%M}-{self.hora_fim:%H:%M} ({self.estado}, {self.custo_calculado} €)')

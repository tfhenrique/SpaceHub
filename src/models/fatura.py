import calendar
import pyodbc
from datetime import date, timedelta
from decimal import Decimal
from db import mensagem_erro


def adicionar_dias_uteis(data, n):
    """Soma n dias úteis (segunda a sexta). Os feriados não são contados."""
    while n > 0:
        data += timedelta(days=1)
        if data.weekday() < 5:
            n -= 1
    return data


class Fatura:
    """A fatura mensal de um membro (tabela Fatura).
    O total não está na tabela: calcula-se com calcular_total()."""

    def __init__(self, membro_id, mes, ano, valor_base, valor_extras=0,
                 data_vencimento=None, pago=False, data_pagamento=None, id=None):
        self.id = id
        self.membro_id = membro_id
        self.mes = mes
        self.ano = ano
        self.valor_base = Decimal(valor_base)
        self.valor_extras = Decimal(valor_extras)
        self.data_vencimento = data_vencimento
        self.pago = pago
        self.data_pagamento = data_pagamento
        self.membro = None        # nome do membro (só quando vem de uma listagem)

    @classmethod
    def de_linha(cls, r):
        f = cls(r.membro_id, r.mes, r.ano, r.valor_base, r.valor_extras,
                r.data_vencimento, bool(r.pago), r.data_pagamento, r.id)
        f.membro = getattr(r, 'membro', None)
        return f

    def calcular_total(self):
        return self.valor_base + self.valor_extras

    # ------------------------------------------------------- RF08
    @classmethod
    def gerar(cls, conn, membro_id, mes, ano):
        """Gera a fatura de um membro para um mês (plano + extras).
        Devolve a Fatura criada, ou None se não foi possível."""
        cursor = conn.cursor()
        try:
            cursor.execute('SELECT id FROM Fatura WHERE membro_id = ? AND mes = ? AND ano = ?',
                           (membro_id, mes, ano))
            if cursor.fetchone():
                print(f'O membro {membro_id} já tem fatura de {mes:02d}/{ano}.')
                return None

            cursor.execute(
                'SELECT p.preco_mensal FROM Membro m'
                ' INNER JOIN PlanoSubscricao p ON p.id = m.plano_id WHERE m.id = ?',
                (membro_id,)
            )
            plano = cursor.fetchone()
            if plano is None:
                print('Membro não encontrado.')
                return None
            valor_base = plano.preco_mensal      # REGRA PROVISÓRIA: sem proporcional

            # extras = serviços ainda sem fatura nesse mês + custos das reservas do mês
            cursor.execute(
                'SELECT ISNULL(SUM(quantidade * custo_unit), 0) AS total FROM ServicoExtra'
                ' WHERE membro_id = ? AND fatura_id IS NULL'
                ' AND YEAR(data_servico) = ? AND MONTH(data_servico) = ?',
                (membro_id, ano, mes)
            )
            extras_servicos = Decimal(cursor.fetchone().total)
            cursor.execute(
                'SELECT ISNULL(SUM(custo_calculado), 0) AS total FROM Reserva'
                ' WHERE membro_id = ? AND YEAR(data) = ? AND MONTH(data) = ?',
                (membro_id, ano, mes)
            )
            extras_reservas = Decimal(cursor.fetchone().total)
            valor_extras = extras_servicos + extras_reservas

            # vencimento: dia 5 do mês seguinte (REGRA PROVISÓRIA)
            ano_v, mes_v = (ano + 1, 1) if mes == 12 else (ano, mes + 1)
            vencimento = date(ano_v, mes_v, 5)

            cursor.execute(
                'INSERT INTO Fatura (membro_id, mes, ano, valor_base, valor_extras, data_vencimento)'
                ' OUTPUT INSERTED.id VALUES (?, ?, ?, ?, ?, ?)',
                (membro_id, mes, ano, valor_base, valor_extras, vencimento)
            )
            novo_id = cursor.fetchone()[0]
            cursor.execute(
                'UPDATE ServicoExtra SET fatura_id = ? WHERE membro_id = ? AND fatura_id IS NULL'
                ' AND YEAR(data_servico) = ? AND MONTH(data_servico) = ?',
                (novo_id, membro_id, ano, mes)
            )
            conn.commit()
            return cls(membro_id, mes, ano, valor_base, valor_extras, vencimento, False, None, novo_id)
        except pyodbc.Error as e:
            conn.rollback()
            print('Erro na base de dados. Nada foi gravado:', mensagem_erro(e))
            return None
        finally:
            cursor.close()

    @classmethod
    def gerar_mensal(cls, conn, mes, ano):
        """Gera as faturas de todos os membros que estiveram ativos nesse mês.
        Devolve a lista de faturas criadas."""
        primeiro = date(ano, mes, 1)
        ultimo = date(ano, mes, calendar.monthrange(ano, mes)[1])
        cursor = conn.cursor()
        cursor.execute('SELECT id FROM Membro WHERE data_inicio <= ?'
                       ' AND (data_fim IS NULL OR data_fim >= ?) ORDER BY id',
                       (ultimo, primeiro))
        ids = [r.id for r in cursor.fetchall()]
        cursor.close()

        criadas = []
        for membro_id in ids:
            fatura = cls.gerar(conn, membro_id, mes, ano)
            if fatura:
                criadas.append(fatura)
        return criadas

    # --------------------------------------------------- outras ações
    def marcar_como_paga(self, conn, data_pagamento=None):
        data_pagamento = data_pagamento or date.today()
        cursor = conn.cursor()
        try:
            cursor.execute('UPDATE Fatura SET pago = 1, data_pagamento = ?'
                           ' WHERE id = ? AND pago = 0', (data_pagamento, self.id))
            conn.commit()
            if cursor.rowcount == 1:
                self.pago = True
                self.data_pagamento = data_pagamento
                return True
            print('A fatura não existe ou já estava paga.')
            return False
        except pyodbc.Error as e:
            conn.rollback()
            print('Erro na base de dados:', mensagem_erro(e))
            return False
        finally:
            cursor.close()

    def gerar_pdf(self):
        """RF10 - a fazer mais tarde (por exemplo com a biblioteca reportlab)."""
        raise NotImplementedError('A geração de PDF ainda não foi implementada.')

    @classmethod
    def listar_do_membro(cls, conn, membro_id):
        cursor = conn.cursor()
        cursor.execute(
            'SELECT id, membro_id, mes, ano, valor_base, valor_extras, pago,'
            ' data_vencimento, data_pagamento FROM Fatura WHERE membro_id = ?'
            ' ORDER BY ano DESC, mes DESC', (membro_id,)
        )
        faturas = [cls.de_linha(r) for r in cursor.fetchall()]
        cursor.close()
        return faturas

    @classmethod
    def listar_em_atraso(cls, conn):
        """RF11 - faturas por pagar há mais de 5 dias úteis após o vencimento."""
        hoje = date.today()
        cursor = conn.cursor()
        cursor.execute(
            'SELECT f.id, f.membro_id, m.nome AS membro, f.mes, f.ano, f.valor_base,'
            ' f.valor_extras, f.pago, f.data_vencimento, f.data_pagamento'
            ' FROM Fatura f INNER JOIN Membro m ON m.id = f.membro_id'
            ' WHERE f.pago = 0 AND f.data_vencimento < ? ORDER BY f.data_vencimento',
            (hoje,)
        )
        em_atraso = [cls.de_linha(r) for r in cursor.fetchall()
                     if hoje > adicionar_dias_uteis(r.data_vencimento, 5)]
        cursor.close()
        return em_atraso

    def __str__(self):
        estado = 'paga' if self.pago else 'por pagar'
        return (f'Fatura {self.mes:02d}/{self.ano} (membro {self.membro_id}): '
                f'{self.valor_base} + {self.valor_extras} = {self.calcular_total()} € ({estado})')

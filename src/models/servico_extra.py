import pyodbc
from datetime import date
from decimal import Decimal
from db import mensagem_erro

# Preços de exemplo (a confirmar com o cliente): ficam gravados em custo_unit
# no momento do registo, por isso mudar aqui não altera serviços já registados.
PRECOS = {
    'Impressao':   Decimal('0.10'),
    'CafePremium': Decimal('1.50'),
    'Correio':     Decimal('2.00'),
}


class ServicoExtra:
    """Um serviço extra consumido por um membro (tabela ServicoExtra)."""

    def __init__(self, membro_id, tipo, quantidade, data_servico=None,
                 custo_unit=None, fatura_id=None, id=None):
        self.id = id
        self.membro_id = membro_id
        self.fatura_id = fatura_id
        self.tipo = tipo                  # Impressao, CafePremium ou Correio
        self.data_servico = data_servico or date.today()
        self.quantidade = quantidade
        self.custo_unit = Decimal(custo_unit) if custo_unit is not None else PRECOS.get(tipo)

    @classmethod
    def de_linha(cls, r):
        return cls(r.membro_id, r.tipo, r.quantidade, r.data_servico,
                   r.custo_unit, r.fatura_id, r.id)

    def calcular_custo(self):
        """quantidade x custo unitário."""
        return self.quantidade * self.custo_unit

    def registar(self, conn):
        """Grava o serviço extra (RF07). Devolve True/False."""
        if self.tipo not in PRECOS:
            print('Erro: tipo inválido. Use:', ', '.join(PRECOS))
            return False
        if self.quantidade <= 0:
            print('Erro: a quantidade tem de ser maior que 0.')
            return False

        cursor = conn.cursor()
        try:
            cursor.execute('SELECT ativo FROM Membro WHERE id = ?', (self.membro_id,))
            membro = cursor.fetchone()
            if membro is None or not membro.ativo:
                print('Erro: membro inexistente ou inativo.')
                return False
            cursor.execute(
                'INSERT INTO ServicoExtra (membro_id, tipo, data_servico, quantidade, custo_unit)'
                ' OUTPUT INSERTED.id VALUES (?, ?, ?, ?, ?)',
                (self.membro_id, self.tipo, self.data_servico, self.quantidade, self.custo_unit)
            )
            self.id = cursor.fetchone()[0]
            conn.commit()
            return True
        except pyodbc.Error as e:
            conn.rollback()
            print('Erro na base de dados:', mensagem_erro(e))
            return False
        finally:
            cursor.close()

    @classmethod
    def listar_do_membro(cls, conn, membro_id, mes=None, ano=None):
        sql = ('SELECT id, membro_id, fatura_id, tipo, data_servico, quantidade, custo_unit'
               ' FROM ServicoExtra WHERE membro_id = ?')
        params = [membro_id]
        if mes and ano:
            sql += ' AND MONTH(data_servico) = ? AND YEAR(data_servico) = ?'
            params += [mes, ano]
        sql += ' ORDER BY data_servico'
        cursor = conn.cursor()
        cursor.execute(sql, params)
        servicos = [cls.de_linha(r) for r in cursor.fetchall()]
        cursor.close()
        return servicos

    def __str__(self):
        return (f'{self.data_servico} {self.tipo} x{self.quantidade} '
                f'= {self.calcular_custo()} €')

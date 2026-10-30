import pyodbc
from datetime import date, datetime
from db import mensagem_erro


class Visitante:
    """Um convidado registado por um membro (tabela Visitante)."""

    def __init__(self, membro_id, nome, empresa=None, data_visita=None,
                 hora_entrada=None, hora_saida=None, id=None):
        self.id = id
        self.membro_id = membro_id
        self.nome = nome
        self.empresa = empresa
        self.data_visita = data_visita or date.today()
        self.hora_entrada = hora_entrada or datetime.now().time().replace(microsecond=0)
        self.hora_saida = hora_saida

    @classmethod
    def de_linha(cls, r):
        return cls(r.membro_id, r.nome, r.empresa, r.data_visita,
                   r.hora_entrada, r.hora_saida, r.id)

    def registar(self, conn):
        """Regista o convidado (RF14), respeitando o limite do plano.
        REGRA PROVISÓRIA: o limite conta convidados por dia, por membro."""
        if not self.nome:
            print('Erro: o nome do convidado é obrigatório.')
            return False

        cursor = conn.cursor()
        try:
            cursor.execute(
                'SELECT p.max_convidados FROM Membro m'
                ' INNER JOIN PlanoSubscricao p ON p.id = m.plano_id WHERE m.id = ?',
                (self.membro_id,)
            )
            plano = cursor.fetchone()
            if plano is None:
                print('Erro: membro não encontrado.')
                return False

            cursor.execute('SELECT COUNT(*) AS n FROM Visitante'
                           ' WHERE membro_id = ? AND data_visita = ?',
                           (self.membro_id, self.data_visita))
            ja_registados = cursor.fetchone().n
            if ja_registados >= plano.max_convidados:
                print(f'Limite do plano atingido: {plano.max_convidados} convidado(s) por dia.')
                return False

            cursor.execute(
                'INSERT INTO Visitante (membro_id, nome, empresa, data_visita, hora_entrada, hora_saida)'
                ' OUTPUT INSERTED.id VALUES (?, ?, ?, ?, ?, ?)',
                (self.membro_id, self.nome, self.empresa, self.data_visita,
                 self.hora_entrada, self.hora_saida)
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
    def listar_do_membro(cls, conn, membro_id):
        cursor = conn.cursor()
        cursor.execute('SELECT id, membro_id, nome, empresa, data_visita, hora_entrada, hora_saida'
                       ' FROM Visitante WHERE membro_id = ? ORDER BY data_visita DESC', (membro_id,))
        visitantes = [cls.de_linha(r) for r in cursor.fetchall()]
        cursor.close()
        return visitantes

    def __str__(self):
        return f'{self.nome} ({self.empresa or "sem empresa"}) em {self.data_visita}'

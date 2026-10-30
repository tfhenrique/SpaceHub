import pyodbc
from datetime import date
from db import mensagem_erro

COLUNAS = ('id, plano_id, nome, empresa, nif, email, telemovel, data_inicio,'
           ' data_fim, ativo, consent_data, consent_versao')


class Membro:
    """Um membro do SpaceHub (tabela Membro)."""

    def __init__(self, nome, empresa, nif, email, plano_id, telemovel=None,
                 data_inicio=None, data_fim=None, ativo=True,
                 consent_data=None, consent_versao='v1.0', id=None):
        self.id = id
        self.plano_id = plano_id
        self.nome = nome
        self.empresa = empresa
        self.nif = nif
        self.email = email
        self.telemovel = telemovel
        self.data_inicio = data_inicio or date.today()
        self.data_fim = data_fim
        self.ativo = ativo
        self.consent_data = consent_data or date.today()   # RGPD
        self.consent_versao = consent_versao                # RGPD

    @classmethod
    def de_linha(cls, r):
        return cls(r.nome, r.empresa, r.nif, r.email, r.plano_id, r.telemovel,
                   r.data_inicio, r.data_fim, bool(r.ativo),
                   r.consent_data, r.consent_versao, r.id)

    # ------------------------------------------------------------ consultas
    @classmethod
    def obter(cls, conn, id):
        cursor = conn.cursor()
        cursor.execute(f'SELECT {COLUNAS} FROM Membro WHERE id = ?', (id,))
        r = cursor.fetchone()
        cursor.close()
        return cls.de_linha(r) if r else None

    @classmethod
    def listar(cls, conn, ativo=None, plano_id=None):
        """Lista membros (RF09). ativo=True/False e plano_id são filtros opcionais."""
        sql = f'SELECT {COLUNAS} FROM Membro WHERE 1 = 1'
        params = []
        if ativo is not None:
            sql += ' AND ativo = ?'
            params.append(1 if ativo else 0)
        if plano_id is not None:
            sql += ' AND plano_id = ?'
            params.append(plano_id)
        sql += ' ORDER BY nome'
        cursor = conn.cursor()
        cursor.execute(sql, params)
        membros = [cls.de_linha(r) for r in cursor.fetchall()]
        cursor.close()
        return membros

    # -------------------------------------------------------------- ações
    def registar(self, conn):
        """Grava o novo membro na base de dados (RF01). Devolve True/False."""
        if not (self.nome and self.empresa and self.nif and self.email):
            print('Erro: nome, empresa, NIF e email são obrigatórios.')
            return False

        cursor = conn.cursor()
        try:
            cursor.execute(
                'INSERT INTO Membro (plano_id, nome, empresa, nif, email, telemovel,'
                ' data_inicio, data_fim, ativo, consent_data, consent_versao)'
                ' OUTPUT INSERTED.id'
                ' VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)',
                (self.plano_id, self.nome, self.empresa, self.nif, self.email,
                 self.telemovel, self.data_inicio, self.data_fim,
                 1 if self.ativo else 0, self.consent_data, self.consent_versao)
            )
            self.id = cursor.fetchone()[0]
            conn.commit()
            return True
        except pyodbc.IntegrityError as e:
            conn.rollback()
            texto = str(e)
            if 'UQ_Membro_email' in texto:
                print(f'Erro: já existe um membro com o email {self.email}.')
            elif 'CK_Membro_nif' in texto:
                print('Erro: o NIF tem de ter 9 dígitos.')
            elif 'FK_Membro_Plano' in texto:
                print('Erro: o plano indicado não existe.')
            else:
                print('Erro de integridade:', mensagem_erro(e))
            return False
        except pyodbc.Error as e:
            conn.rollback()
            print('Erro na base de dados:', mensagem_erro(e))
            return False
        finally:
            cursor.close()

    def editar(self, conn):
        """Guarda as alterações feitas ao objeto (nome, empresa, NIF, email, ...)."""
        if self.id is None:
            print('Erro: o membro ainda não foi registado.')
            return False
        cursor = conn.cursor()
        try:
            cursor.execute(
                'UPDATE Membro SET plano_id = ?, nome = ?, empresa = ?, nif = ?,'
                ' email = ?, telemovel = ? WHERE id = ?',
                (self.plano_id, self.nome, self.empresa, self.nif, self.email,
                 self.telemovel, self.id)
            )
            conn.commit()
            return cursor.rowcount == 1
        except pyodbc.IntegrityError as e:
            conn.rollback()
            print('Erro de integridade (email repetido, NIF ou plano inválido):',
                  mensagem_erro(e))
            return False
        except pyodbc.Error as e:
            conn.rollback()
            print('Erro na base de dados:', mensagem_erro(e))
            return False
        finally:
            cursor.close()

    def _reservas_futuras(self, cursor):
        cursor.execute(
            "SELECT COUNT(*) AS total FROM Reserva"
            " WHERE membro_id = ? AND estado = 'Confirmada' AND data >= ?",
            (self.id, date.today())
        )
        return cursor.fetchone().total

    def desativar(self, conn):
        """Marca o membro como inativo (não apaga nada). Não deixa se
        ainda tiver reservas futuras confirmadas."""
        cursor = conn.cursor()
        try:
            futuras = self._reservas_futuras(cursor)
            if futuras > 0:
                print(f'Não é possível desativar: tem {futuras} reserva(s) futura(s).')
                return False
            hoje = date.today()
            cursor.execute('UPDATE Membro SET ativo = 0, data_fim = COALESCE(data_fim, ?)'
                           ' WHERE id = ?', (hoje, self.id))
            cursor.execute('UPDATE Utilizador SET ativo = 0 WHERE membro_id = ?', (self.id,))
            conn.commit()
            self.ativo = False
            self.data_fim = self.data_fim or hoje
            return True
        except pyodbc.Error as e:
            conn.rollback()
            print('Erro na base de dados:', mensagem_erro(e))
            return False
        finally:
            cursor.close()

    def anonimizar(self, conn):
        """Direito ao apagamento (RGPD, RNF04): remove os dados pessoais mas
        mantém as faturas e reservas. (Prazos legais de conservação: a confirmar.)"""
        cursor = conn.cursor()
        try:
            if self._reservas_futuras(cursor) > 0:
                print('Não é possível anonimizar: tem reservas futuras confirmadas.')
                return False
            hoje = date.today()
            cursor.execute(
                "UPDATE Membro SET nome = N'Anonimizado', empresa = N'Anonimizado',"
                " nif = '000000000', email = ?, telemovel = NULL, ativo = 0,"
                " data_fim = COALESCE(data_fim, ?) WHERE id = ?",
                (f'anonimo_{self.id}@anonimo.invalid', hoje, self.id)
            )
            cursor.execute(
                "UPDATE Utilizador SET login = ?, password_hash = '', ativo = 0"
                " WHERE membro_id = ?", (f'anonimo_{self.id}', self.id)
            )
            cursor.execute(
                "UPDATE Visitante SET nome = N'Anonimizado', empresa = NULL"
                " WHERE membro_id = ?", (self.id,)
            )
            conn.commit()
            self.nome = self.empresa = 'Anonimizado'
            self.nif = '000000000'
            self.email = f'anonimo_{self.id}@anonimo.invalid'
            self.telemovel = None
            self.ativo = False
            return True
        except pyodbc.Error as e:
            conn.rollback()
            print('Erro na base de dados:', mensagem_erro(e))
            return False
        finally:
            cursor.close()

    def __str__(self):
        estado = 'ativo' if self.ativo else 'inativo'
        return f'[{self.id}] {self.nome} ({self.empresa}) - {self.email} - {estado}'

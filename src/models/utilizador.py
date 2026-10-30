import pyodbc
from werkzeug.security import generate_password_hash, check_password_hash
from db import mensagem_erro


class Utilizador:
    """Uma conta de acesso ao sistema (tabela Utilizador).
    A palavra-passe nunca é guardada: só o hash (RNF03)."""

    def __init__(self, login, perfil, membro_id=None, ativo=True,
                 password_hash=None, id=None):
        self.id = id
        self.membro_id = membro_id        # None para a Gestora
        self.login = login
        self.password_hash = password_hash
        self.perfil = perfil              # 'Membro' ou 'Gestor'
        self.ativo = ativo

    @classmethod
    def de_linha(cls, r):
        return cls(r.login, r.perfil, r.membro_id, bool(r.ativo), r.password_hash, r.id)

    @classmethod
    def criar(cls, conn, login, password, perfil, membro_id=None):
        """Cria uma conta nova. Devolve o Utilizador ou None."""
        if not login or not password:
            print('Erro: login e palavra-passe são obrigatórios.')
            return None
        cursor = conn.cursor()
        try:
            hash_ = generate_password_hash(password)
            cursor.execute(
                'INSERT INTO Utilizador (membro_id, login, password_hash, perfil)'
                ' OUTPUT INSERTED.id VALUES (?, ?, ?, ?)',
                (membro_id, login, hash_, perfil)
            )
            novo_id = cursor.fetchone()[0]
            conn.commit()
            return cls(login, perfil, membro_id, True, hash_, novo_id)
        except pyodbc.IntegrityError as e:
            conn.rollback()
            texto = str(e)
            if 'UQ_Utilizador_login' in texto:
                print('Erro: esse login já existe.')
            elif 'UX_Utilizador_membro' in texto:
                print('Erro: esse membro já tem uma conta.')
            else:
                print('Erro de integridade:', mensagem_erro(e))
            return None
        except pyodbc.Error as e:
            conn.rollback()
            print('Erro na base de dados:', mensagem_erro(e))
            return None
        finally:
            cursor.close()

    @classmethod
    def definir_password(cls, conn, login, password):
        """Troca a palavra-passe (serve também para substituir os hashes de
        exemplo dos dados de teste)."""
        cursor = conn.cursor()
        try:
            cursor.execute('UPDATE Utilizador SET password_hash = ? WHERE login = ?',
                           (generate_password_hash(password), login))
            conn.commit()
            return cursor.rowcount == 1
        except pyodbc.Error as e:
            conn.rollback()
            print('Erro na base de dados:', mensagem_erro(e))
            return False
        finally:
            cursor.close()

    @classmethod
    def autenticar(cls, conn, login, password):
        """Devolve o Utilizador se o login e a palavra-passe estiverem certos,
        ou None. A mensagem de erro é sempre a mesma, para não dar pistas."""
        cursor = conn.cursor()
        cursor.execute(
            'SELECT id, membro_id, login, password_hash, perfil, ativo'
            ' FROM Utilizador WHERE login = ? AND ativo = 1', (login,)
        )
        r = cursor.fetchone()
        cursor.close()
        if r is None:
            return None
        try:
            if check_password_hash(r.password_hash, password):
                return cls.de_linha(r)
        except ValueError:
            pass        # hash inválido (por exemplo, o texto de exemplo)
        return None

    def tem_permissao(self, perfil_necessario):
        """O Gestor pode tudo; o Membro só o que é de Membro."""
        if self.perfil == 'Gestor':
            return True
        return perfil_necessario == 'Membro'

    def __str__(self):
        return f'{self.login} ({self.perfil})'
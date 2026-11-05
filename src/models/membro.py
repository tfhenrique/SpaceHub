import pyodbc
from datetime import date

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
        self.consent_data = consent_data or date.today()
        self.consent_versao = consent_versao                

    def __str__(self):
        estado = 'ativo' if self.ativo else 'inativo'
        return f'[{self.id}] {self.nome} ({self.empresa}) - {self.email} - {estado}'

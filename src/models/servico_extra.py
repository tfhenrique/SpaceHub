from datetime import date
from decimal import Decimal

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
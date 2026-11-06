from decimal import Decimal

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

    
from datetime import datetime, date
from decimal import Decimal, ROUND_HALF_UP


def euros(valor):
    """Arredonda para 2 casas decimais."""
    return Decimal(valor).quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)


class Reserva:

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
        self.recurso = None        
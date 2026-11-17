from typing import Protocol


class Exibivel(Protocol):
    """Contrato para qualquer objeto que saiba se descrever em uma linha de texto."""

    def resumo(self) -> str:
        """Retorna um texto curto para exibição no terminal."""
        ...

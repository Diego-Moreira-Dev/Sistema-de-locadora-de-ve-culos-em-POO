from abc import ABC, abstractmethod


class Veiculo(ABC):
    """Classe base abstrata com o que todo veículo da frota tem em comum."""

    def __init__(self, placa: str, modelo: str) -> None:
        placa = placa.strip().upper()
        if not Veiculo.validar_placa(placa):
            raise ValueError(f"Placa '{placa}' inválida. Use o formato ABC1234 ou ABC1D23.")
        self.__placa = placa
        self.modelo = modelo
        self._disponivel = True

    @staticmethod
    def validar_placa(placa: str) -> bool:
        """Retorna True se a placa seguir o padrão antigo (ABC1234) ou Mercosul (ABC1D23)."""
        return (
            len(placa) == 7
            and placa[:3].isalpha()
            and placa[3].isdigit()
            and placa[4].isalnum()
            and placa[5:].isdigit()
        )

    @property
    def placa(self) -> str:
        return self.__placa

    @property
    def modelo(self) -> str:
        return self._modelo

    @modelo.setter
    def modelo(self, valor: str) -> None:
        if not valor.strip():
            raise ValueError("O modelo do veículo não pode ficar vazio.")
        self._modelo = valor.strip()

    @property
    def disponivel(self) -> bool:
        return self._disponivel

    def marcar_alugado(self) -> None:
        """Retira o veículo da lista de disponíveis."""
        self._disponivel = False

    def marcar_devolvido(self) -> None:
        """Coloca o veículo de volta na lista de disponíveis."""
        self._disponivel = True

    @abstractmethod
    def cnh_exigida(self) -> str:
        """Categoria de CNH necessária para dirigir o veículo."""

    @abstractmethod
    def calcular_aluguel(self, dias: int) -> float:
        """Valor total do aluguel pela quantidade de dias."""

    def resumo(self) -> str:
        """Parte comum do resumo, completada por cada subclasse."""
        situacao = "Disponível" if self._disponivel else "Alugado"
        return f"Placa {self.__placa} | CNH {self.cnh_exigida()} | R$ {self.calcular_aluguel(1):.2f}/dia | {situacao}"


class Carro(Veiculo):
    """Carro de passeio: tem desconto em locações de 7 dias ou mais."""

    DIARIA = 120.0
    DESCONTO_SEMANAL = 0.10

    def __init__(self, placa: str, modelo: str, portas: int) -> None:
        super().__init__(placa, modelo)
        self._portas = portas

    def cnh_exigida(self) -> str:
        return "B"

    def calcular_aluguel(self, dias: int) -> float:
        total = Carro.DIARIA * dias
        if dias >= 7:
            total -= total * Carro.DESCONTO_SEMANAL
        return total

    def resumo(self) -> str:
        return f"🚗 Carro {self.modelo} ({self._portas} portas) | {super().resumo()}"


class Moto(Veiculo):
    """Moto: tem acréscimo na diária quando a cilindrada é alta."""

    DIARIA = 70.0
    LIMITE_CILINDRADAS = 400
    ACRESCIMO_ALTA_CILINDRADA = 0.20

    def __init__(self, placa: str, modelo: str, cilindradas: int) -> None:
        super().__init__(placa, modelo)
        self._cilindradas = cilindradas

    def cnh_exigida(self) -> str:
        return "A"

    def calcular_aluguel(self, dias: int) -> float:
        total = Moto.DIARIA * dias
        if self._cilindradas > Moto.LIMITE_CILINDRADAS:
            total += total * Moto.ACRESCIMO_ALTA_CILINDRADA
        return total

    def resumo(self) -> str:
        return f"🏍️ Moto {self.modelo} ({self._cilindradas} cc) | {super().resumo()}"


class Caminhao(Veiculo):
    """Caminhão: a diária aumenta conforme o número de eixos."""

    DIARIA = 200.0
    TAXA_POR_EIXO = 50.0

    def __init__(self, placa: str, modelo: str, eixos: int) -> None:
        super().__init__(placa, modelo)
        self._eixos = eixos

    def cnh_exigida(self) -> str:
        return "C"

    def calcular_aluguel(self, dias: int) -> float:
        return (Caminhao.DIARIA + Caminhao.TAXA_POR_EIXO * self._eixos) * dias

    def resumo(self) -> str:
        return f"🚚 Caminhão {self.modelo} ({self._eixos} eixos) | {super().resumo()}"

from excecoes import CnhIncompativelErro, LocadoraErro, VeiculoIndisponivelErro
from modelos.cliente import Cliente
from modelos.veiculos import Veiculo


class Locacao:
    """Aluguel de um veículo por um cliente durante alguns dias."""

    LIMITE_DIAS = 30
    total_criadas = 0

    def __init__(self, cliente: Cliente, veiculo: Veiculo, dias: int) -> None:
        if not veiculo.disponivel:
            raise VeiculoIndisponivelErro(f"O veículo {veiculo.placa} já está alugado.")
        if not cliente.pode_dirigir(veiculo.cnh_exigida()):
            raise CnhIncompativelErro(
                f"{cliente.nome} tem CNH {cliente.cnh}, mas este veículo exige CNH {veiculo.cnh_exigida()}."
            )
        self.dias = dias
        Locacao.total_criadas += 1
        self._codigo = Locacao.total_criadas
        self._cliente = cliente
        self._veiculo = veiculo
        self._ativa = True
        veiculo.marcar_alugado()

    @property
    def codigo(self) -> int:
        return self._codigo

    @property
    def cliente(self) -> Cliente:
        return self._cliente

    @property
    def veiculo(self) -> Veiculo:
        return self._veiculo

    @property
    def ativa(self) -> bool:
        return self._ativa

    @property
    def dias(self) -> int:
        return self._dias

    @dias.setter
    def dias(self, valor: int) -> None:
        if not 1 <= valor <= Locacao.LIMITE_DIAS:
            raise ValueError(f"Quantidade de dias {valor} inválida. Use de 1 a {Locacao.LIMITE_DIAS}.")
        self._dias = valor

    @property
    def valor_total(self) -> float:
        """Valor calculado pelo próprio veículo, de acordo com o tipo dele."""
        return self._veiculo.calcular_aluguel(self._dias)

    def finalizar(self) -> None:
        """Encerra a locação e libera o veículo."""
        if not self._ativa:
            raise LocadoraErro(f"A locação #{self._codigo} já foi finalizada.")
        self._ativa = False
        self._veiculo.marcar_devolvido()

    def resumo(self) -> str:
        """Retorna um texto curto para exibição no terminal."""
        situacao = "Ativa" if self._ativa else "Finalizada"
        return (
            f"📄 Locação #{self._codigo} | {self._cliente.nome} | {self._veiculo.modelo} "
            f"| {self._dias} dia(s) | R$ {self.valor_total:.2f} | {situacao}"
        )

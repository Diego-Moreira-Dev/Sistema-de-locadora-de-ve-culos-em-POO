from excecoes import CadastroDuplicadoErro, NaoEncontradoErro
from modelos.cliente import Cliente
from modelos.locacao import Locacao
from modelos.veiculos import Veiculo


class Locadora:
    """Reúne clientes, frota e locações, e concentra as operações do negócio."""

    def __init__(self, nome: str) -> None:
        self._nome = nome
        self._clientes: dict[str, Cliente] = {}
        self._veiculos: dict[str, Veiculo] = {}
        self._locacoes: list[Locacao] = []

    @property
    def nome(self) -> str:
        return self._nome

    def cadastrar_cliente(self, cliente: Cliente) -> None:
        """Adiciona um cliente, impedindo CPF repetido."""
        if cliente.cpf in self._clientes:
            raise CadastroDuplicadoErro(f"Já existe um cliente com o CPF {cliente.cpf}.")
        self._clientes[cliente.cpf] = cliente

    def cadastrar_veiculo(self, veiculo: Veiculo) -> None:
        """Adiciona um veículo à frota, impedindo placa repetida."""
        if veiculo.placa in self._veiculos:
            raise CadastroDuplicadoErro(f"Já existe um veículo com a placa {veiculo.placa}.")
        self._veiculos[veiculo.placa] = veiculo

    def buscar_cliente(self, cpf: str) -> Cliente:
        """Retorna o cliente pelo CPF ou lança NaoEncontradoErro."""
        cliente = self._clientes.get(cpf.strip())
        if cliente is None:
            raise NaoEncontradoErro(f"Nenhum cliente com o CPF {cpf}.")
        return cliente

    def buscar_veiculo(self, placa: str) -> Veiculo:
        """Retorna o veículo pela placa ou lança NaoEncontradoErro."""
        veiculo = self._veiculos.get(placa.strip().upper())
        if veiculo is None:
            raise NaoEncontradoErro(f"Nenhum veículo com a placa {placa}.")
        return veiculo

    def listar_clientes(self) -> list[Cliente]:
        """Retorna todos os clientes cadastrados."""
        return list(self._clientes.values())

    def listar_veiculos(self) -> list[Veiculo]:
        """Retorna toda a frota (carros, motos e caminhões misturados)."""
        return list(self._veiculos.values())

    def listar_locacoes(self) -> list[Locacao]:
        """Retorna todas as locações, ativas e finalizadas."""
        return list(self._locacoes)

    def alugar(self, cpf: str, placa: str, dias: int) -> Locacao:
        """Cria uma locação ligando um cliente a um veículo."""
        locacao = Locacao(self.buscar_cliente(cpf), self.buscar_veiculo(placa), dias)
        self._locacoes.append(locacao)
        return locacao

    def devolver(self, placa: str) -> Locacao:
        """Finaliza a locação ativa do veículo informado."""
        veiculo = self.buscar_veiculo(placa)
        for locacao in self._locacoes:
            if locacao.ativa and locacao.veiculo is veiculo:
                locacao.finalizar()
                return locacao
        raise NaoEncontradoErro(f"O veículo {veiculo.placa} não está alugado.")

    @property
    def faturamento_total(self) -> float:
        """Soma do valor de todas as locações registradas."""
        return sum(locacao.valor_total for locacao in self._locacoes)

    @property
    def ocupacao(self) -> float:
        """Percentual da frota que está alugada no momento."""
        if not self._veiculos:
            return 0.0
        alugados = sum(1 for veiculo in self._veiculos.values() if not veiculo.disponivel)
        return alugados / len(self._veiculos) * 100

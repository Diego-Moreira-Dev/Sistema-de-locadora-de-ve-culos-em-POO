from menu import Menu
from modelos import Caminhao, Carro, Cliente, Locadora, Moto


def carregar_dados_exemplo(locadora: Locadora) -> None:
    """Preenche a locadora com clientes, veículos e locações para a demonstração."""
    for texto in ("Ana Souza;12345678901;B", "Bruno Lima;98765432100;AB", "Carla Dias;11122233344;C"):
        locadora.cadastrar_cliente(Cliente.from_string(texto))

    locadora.cadastrar_veiculo(Carro("ABC1D23", "Fiat Argo", 4))
    locadora.cadastrar_veiculo(Carro("BRA2E19", "Renault Kwid", 4))
    locadora.cadastrar_veiculo(Moto("MOT0A12", "Honda CG 160", 160))
    locadora.cadastrar_veiculo(Moto("MTZ6G07", "Yamaha MT-07", 689))
    locadora.cadastrar_veiculo(Caminhao("CAM4C56", "Volvo FH", 3))

    locadora.alugar("12345678901", "ABC1D23", 3)
    locadora.alugar("98765432100", "MOT0A12", 7)
    locadora.alugar("11122233344", "CAM4C56", 2)
    locadora.devolver("CAM4C56")


def main() -> None:
    """Ponto de entrada do sistema."""
    locadora = Locadora("Locadora POO")
    carregar_dados_exemplo(locadora)
    Menu(locadora).executar()


if __name__ == "__main__":
    main()

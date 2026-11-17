from collections.abc import Sequence

from excecoes import LocadoraErro
from interfaces import Exibivel
from modelos import Caminhao, Carro, Cliente, Locadora, Moto, Veiculo


class Menu:
    """Terminal interativo: lê os dados, chama a Locadora e mostra o resultado."""

    TEXTO_MENU = """
========== LOCADORA DE VEÍCULOS ==========
1 - Cadastrar cliente
2 - Cadastrar veículo
3 - Listar clientes
4 - Listar veículos
5 - Buscar veículo por placa
6 - Alugar veículo
7 - Devolver veículo
8 - Relatório da locadora
0 - Sair"""

    def __init__(self, locadora: Locadora) -> None:
        self._locadora = locadora

    def executar(self) -> None:
        """Mantém o menu em loop até o usuário escolher 0."""
        while True:
            print(Menu.TEXTO_MENU)
            opcao = input("Escolha uma opção: ").strip()
            if opcao == "0":
                print("👋 Até a próxima!")
                break
            try:
                self._tratar_opcao(opcao)
            except (LocadoraErro, ValueError) as erro:
                print(f"❌ {erro}")

    def _tratar_opcao(self, opcao: str) -> None:
        if opcao == "1":
            self._cadastrar_cliente()
        elif opcao == "2":
            self._cadastrar_veiculo()
        elif opcao == "3":
            self._exibir(self._locadora.listar_clientes())
        elif opcao == "4":
            self._exibir(self._locadora.listar_veiculos())
        elif opcao == "5":
            self._buscar_veiculo()
        elif opcao == "6":
            self._alugar()
        elif opcao == "7":
            self._devolver()
        elif opcao == "8":
            self._relatorio()
        else:
            print("❌ Opção inválida.")

    def _cadastrar_cliente(self) -> None:
        nome = input("Nome: ")
        cpf = input("CPF (só números): ")
        cnh = input(f"Categoria da CNH ({'/'.join(Cliente.CATEGORIAS_CNH)}): ")
        cliente = Cliente(nome, cpf, cnh)
        self._locadora.cadastrar_cliente(cliente)
        print(f"✅ Cliente cadastrado: {cliente.resumo()}")

    def _cadastrar_veiculo(self) -> None:
        tipo = input("Tipo (1-Carro, 2-Moto, 3-Caminhão): ").strip()
        if tipo not in ("1", "2", "3"):
            raise ValueError("Tipo de veículo inválido.")
        placa = input("Placa: ")
        modelo = input("Modelo: ")
        veiculo: Veiculo
        if tipo == "1":
            veiculo = Carro(placa, modelo, self._ler_inteiro("Número de portas: "))
        elif tipo == "2":
            veiculo = Moto(placa, modelo, self._ler_inteiro("Cilindradas: "))
        else:
            veiculo = Caminhao(placa, modelo, self._ler_inteiro("Número de eixos: "))
        self._locadora.cadastrar_veiculo(veiculo)
        print(f"✅ Veículo cadastrado: {veiculo.resumo()}")

    def _buscar_veiculo(self) -> None:
        veiculo = self._locadora.buscar_veiculo(input("Placa: "))
        print(veiculo.resumo())

    def _alugar(self) -> None:
        cpf = input("CPF do cliente: ")
        placa = input("Placa do veículo: ")
        dias = self._ler_inteiro("Quantidade de dias: ")
        locacao = self._locadora.alugar(cpf, placa, dias)
        print(f"✅ Locação #{locacao.codigo} registrada. Valor: R$ {locacao.valor_total:.2f}")

    def _devolver(self) -> None:
        locacao = self._locadora.devolver(input("Placa do veículo: "))
        print(f"✅ Locação #{locacao.codigo} finalizada. {locacao.veiculo.modelo} está disponível novamente.")

    def _relatorio(self) -> None:
        print("---------- RELATÓRIO ----------")
        self._exibir(self._locadora.listar_locacoes())
        print(f"🚦 Ocupação da frota: {self._locadora.ocupacao:.0f}%")
        print(f"💰 Faturamento total: R$ {self._locadora.faturamento_total:.2f}")

    @staticmethod
    def _exibir(itens: Sequence[Exibivel]) -> None:
        if not itens:
            print("Nenhum registro encontrado.")
        for item in itens:
            print(item.resumo())

    @staticmethod
    def _ler_inteiro(mensagem: str) -> int:
        texto = input(mensagem).strip()
        if not texto.isdigit():
            raise ValueError(f"'{texto}' não é um número inteiro válido.")
        return int(texto)

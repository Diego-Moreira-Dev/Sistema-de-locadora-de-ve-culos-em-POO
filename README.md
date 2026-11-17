# Locadora de Veículos – Trabalho de Programação Orientada a Objetos

## Integrantes

- Nome do integrante 1
- Nome do integrante 2
- Nome do integrante 3

## Descrição do cenário

Sistema de terminal para uma locadora que aluga **carros, motos e caminhões**. A locadora cadastra clientes e veículos, registra aluguéis, recebe devoluções e emite um relatório de ocupação da frota e faturamento.

### Regras de negócio

- O cliente é identificado pelo **CPF** (11 dígitos, sem repetição) e o veículo pela **placa** (formato `ABC1234` ou `ABC1D23`, sem repetição).
- A CNH do cliente deve ser `A`, `B`, `AB` ou `C`.
- Cada tipo de veículo exige uma CNH:

| Veículo | CNH exigida | Diária | Regra de preço |
|---|---|---|---|
| Carro | B | R$ 120,00 | 10% de desconto em locações de 7 dias ou mais |
| Moto | A | R$ 70,00 | Acréscimo de 20% se tiver mais de 400 cc |
| Caminhão | C | R$ 200,00 + R$ 50,00 por eixo | Sem desconto |

- Só é possível alugar um veículo **disponível**; ao alugar ele fica indisponível, e ao devolver volta a ficar disponível.
- A locação dura de **1 a 30 dias**.
- O valor da locação é calculado pelo próprio veículo (polimorfismo).
- Relatório: lista de locações, **ocupação da frota** (% de veículos alugados) e **faturamento total**.

## Como executar

Requisito: Python 3.9 ou superior. Não usa bibliotecas externas.

```bash
python src/main.py
```

O sistema já inicia com 3 clientes, 5 veículos e 3 locações de exemplo.

## Estrutura do projeto

```
├── README.md
├── docs/
│   └── diagrama-classes.md
└── src/
    ├── main.py
    ├── menu.py
    ├── excecoes.py
    ├── interfaces.py
    └── modelos/
        ├── __init__.py
        ├── cliente.py
        ├── veiculos.py
        ├── locacao.py
        └── locadora.py
```

## Diagrama de classes

Veja [docs/diagrama-classes.md](docs/diagrama-classes.md). Resumo:

```
                Veiculo (ABC)                     Exibivel (Protocol)
              /      |       \                     cumprido por Cliente,
          Carro     Moto    Caminhao               Veiculo e Locacao

Locadora ◆── Cliente
         ◆── Veiculo
         ◆── Locacao ◇── Cliente
                     ◇── Veiculo
```

## Mapeamento das entidades

| Entidade | Atributos | Comportamentos (métodos) |
|---|---|---|
| `Veiculo` *(abstrata)* | placa, modelo, disponível | `cnh_exigida()` *(abstrato)*, `calcular_aluguel()` *(abstrato)*, `marcar_alugado()`, `marcar_devolvido()`, `resumo()` |
| `Carro` *(herda de Veiculo)* | portas | `cnh_exigida()`, `calcular_aluguel()`, `resumo()` |
| `Moto` *(herda de Veiculo)* | cilindradas | `cnh_exigida()`, `calcular_aluguel()`, `resumo()` |
| `Caminhao` *(herda de Veiculo)* | eixos | `cnh_exigida()`, `calcular_aluguel()`, `resumo()` |
| `Cliente` | nome, cpf, cnh | `pode_dirigir()`, `from_string()`, `validar_cpf()`, `resumo()` |
| `Locacao` | código, cliente, veículo, dias, ativa | `valor_total` *(property calculada)*, `finalizar()`, `resumo()` |
| `Locadora` | nome, clientes, veículos, locações | `cadastrar_cliente()`, `cadastrar_veiculo()`, `buscar_cliente()`, `buscar_veiculo()`, `alugar()`, `devolver()`, `faturamento_total`, `ocupacao` |
| `Exibivel` *(Protocol)* | – | `resumo()` |
| `LocadoraErro` e filhas | – | Exceções de regra de negócio |

## Onde cada requisito foi aplicado

| # | Requisito | Onde |
|---|---|---|
| R1 | Classes e objetos | `src/modelos/`: `Cliente`, `Veiculo`, `Carro`, `Moto`, `Caminhao`, `Locacao`, `Locadora`, todas com `__init__` e `self` |
| R2 | Composição | `Locadora` guarda dicts de `Cliente` e `Veiculo` e a lista de `Locacao` (`locadora.py`); `Locacao` guarda um `Cliente` e um `Veiculo` (`locacao.py`) |
| R3 | Encapsulamento | `Cliente.__cpf` e `Veiculo.__placa` (privados); `_nome`, `_cnh`, `_modelo`, `_disponivel`, `_dias`, `_ativa` (protegidos), acessados por properties e métodos |
| R4 | `@classmethod` e `@staticmethod` | `Cliente.from_string` (classmethod); `Cliente.validar_cpf` e `Veiculo.validar_placa` (staticmethod) |
| R5 | Properties | Com setter validando: `Cliente.nome`, `Cliente.cnh`, `Veiculo.modelo`, `Locacao.dias`. Calculadas: `Locacao.valor_total`, `Locadora.faturamento_total`, `Locadora.ocupacao` |
| R6 | Atributos de classe | `Cliente.CATEGORIAS_CNH`, `Carro.DIARIA`, `Moto.LIMITE_CILINDRADAS`, `Caminhao.TAXA_POR_EIXO`, `Locacao.LIMITE_DIAS` e o contador `Locacao.total_criadas` |
| R7 | Herança e `super()` | `Veiculo` → `Carro`, `Moto`, `Caminhao` (`veiculos.py`), com `super().__init__()` e `super().resumo()` |
| R8 | Sobrescrita e polimorfismo | `cnh_exigida()`, `calcular_aluguel()` e `resumo()` reescritos nas três subclasses; `Menu._exibir` e `Locacao.valor_total` os chamam sem saber o tipo |
| R9 | Classe abstrata | `Veiculo(ABC)` com `@abstractmethod` em `cnh_exigida()` e `calcular_aluguel()` |
| R10 | Interface / Protocol | `Exibivel` em `src/interfaces.py`, cumprido por `Cliente`, `Veiculo` e `Locacao` (sem herança entre elas) e usado em `Menu._exibir` |

## Terminal interativo

| Opção | Função | Requisito do menu |
|---|---|---|
| 1 | Cadastrar cliente | Cadastro (tipo 1) |
| 2 | Cadastrar veículo (carro, moto ou caminhão) | Cadastro (tipo 2) |
| 3 | Listar clientes | Listagem |
| 4 | Listar veículos | Listagem polimórfica |
| 5 | Buscar veículo por placa | Busca por identificador |
| 6 | Alugar veículo | Operação de negócio |
| 7 | Devolver veículo | Operação de negócio |
| 8 | Relatório da locadora | Relatório / cálculo |
| 0 | Sair | – |

As regras de negócio ficam nas classes de domínio. O menu (`src/menu.py`) apenas lê os dados, chama os métodos e exibe o resultado ou o erro.

## Exemplo de execução

```
Escolha uma opção: 6
CPF do cliente: 11122233344
Placa do veículo: BRA2E19
Quantidade de dias: 2
❌ Carla Dias tem CNH C, mas este veículo exige CNH B.

Escolha uma opção: 8
---------- RELATÓRIO ----------
📄 Locação #1 | Ana Souza | Fiat Argo | 3 dia(s) | R$ 360.00 | Ativa
📄 Locação #2 | Bruno Lima | Honda CG 160 | 7 dia(s) | R$ 490.00 | Ativa
📄 Locação #3 | Carla Dias | Volvo FH | 2 dia(s) | R$ 700.00 | Finalizada
🚦 Ocupação da frota: 40%
💰 Faturamento total: R$ 1550.00
```

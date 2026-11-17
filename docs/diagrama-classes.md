# Diagrama de Classes – Locadora de Veículos

```mermaid
classDiagram
    direction TB

    class Exibivel {
        <<Protocol>>
        +resumo() str
    }

    class Veiculo {
        <<abstract>>
        -__placa: str
        -_modelo: str
        -_disponivel: bool
        +placa: str
        +modelo: str
        +disponivel: bool
        +validar_placa(placa)$ bool
        +marcar_alugado()
        +marcar_devolvido()
        +cnh_exigida()* str
        +calcular_aluguel(dias)* float
        +resumo() str
    }

    class Carro {
        +DIARIA: float = 120.0
        +DESCONTO_SEMANAL: float = 0.10
        -_portas: int
        +cnh_exigida() str
        +calcular_aluguel(dias) float
        +resumo() str
    }

    class Moto {
        +DIARIA: float = 70.0
        +LIMITE_CILINDRADAS: int = 400
        +ACRESCIMO_ALTA_CILINDRADA: float = 0.20
        -_cilindradas: int
        +cnh_exigida() str
        +calcular_aluguel(dias) float
        +resumo() str
    }

    class Caminhao {
        +DIARIA: float = 200.0
        +TAXA_POR_EIXO: float = 50.0
        -_eixos: int
        +cnh_exigida() str
        +calcular_aluguel(dias) float
        +resumo() str
    }

    class Cliente {
        +CATEGORIAS_CNH: tuple
        -__cpf: str
        -_nome: str
        -_cnh: str
        +cpf: str
        +nome: str
        +cnh: str
        +from_string(texto)$ Cliente
        +validar_cpf(cpf)$ bool
        +pode_dirigir(categoria) bool
        +resumo() str
    }

    class Locacao {
        +LIMITE_DIAS: int = 30
        +total_criadas: int
        -_codigo: int
        -_dias: int
        -_ativa: bool
        +codigo: int
        +dias: int
        +ativa: bool
        +valor_total: float
        +finalizar()
        +resumo() str
    }

    class Locadora {
        -_nome: str
        -_clientes: dict
        -_veiculos: dict
        -_locacoes: list
        +faturamento_total: float
        +ocupacao: float
        +cadastrar_cliente(cliente)
        +cadastrar_veiculo(veiculo)
        +buscar_cliente(cpf) Cliente
        +buscar_veiculo(placa) Veiculo
        +listar_clientes() list
        +listar_veiculos() list
        +listar_locacoes() list
        +alugar(cpf, placa, dias) Locacao
        +devolver(placa) Locacao
    }

    class LocadoraErro
    class CadastroDuplicadoErro
    class NaoEncontradoErro
    class VeiculoIndisponivelErro
    class CnhIncompativelErro

    Veiculo <|-- Carro
    Veiculo <|-- Moto
    Veiculo <|-- Caminhao

    Locadora *-- "0..*" Cliente
    Locadora *-- "0..*" Veiculo
    Locadora *-- "0..*" Locacao
    Locacao o-- "1" Cliente
    Locacao o-- "1" Veiculo

    Exibivel <.. Cliente : cumpre
    Exibivel <.. Veiculo : cumpre
    Exibivel <.. Locacao : cumpre

    LocadoraErro <|-- CadastroDuplicadoErro
    LocadoraErro <|-- NaoEncontradoErro
    LocadoraErro <|-- VeiculoIndisponivelErro
    LocadoraErro <|-- CnhIncompativelErro
```

## Legenda

| Símbolo | Significado |
|---|---|
| `<\|--` | Herança ("é um") |
| `*--` | Composição: a `Locadora` possui os objetos |
| `o--` | Agregação: a `Locacao` referencia um cliente e um veículo que existem por conta própria |
| `<..` | O `Protocolo` é cumprido sem herança |
| `$` | Método estático ou de classe |
| `*` | Método abstrato |
| `-` / `+` | Atributo protegido ou privado / público |

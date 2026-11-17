class Cliente:
    """Cliente da locadora, identificado pelo CPF."""

    CATEGORIAS_CNH = ("A", "B", "AB", "C")

    def __init__(self, nome: str, cpf: str, cnh: str) -> None:
        cpf = cpf.strip()
        if not Cliente.validar_cpf(cpf):
            raise ValueError(f"CPF '{cpf}' inválido. Use 11 dígitos, sem pontos ou traço.")
        self.__cpf = cpf
        self.nome = nome
        self.cnh = cnh

    @classmethod
    def from_string(cls, texto: str) -> "Cliente":
        """Cria um cliente a partir de um texto no formato 'nome;cpf;cnh'."""
        nome, cpf, cnh = texto.split(";")
        return cls(nome, cpf, cnh)

    @staticmethod
    def validar_cpf(cpf: str) -> bool:
        """Retorna True se o CPF tiver exatamente 11 dígitos."""
        return len(cpf) == 11 and cpf.isdigit()

    @property
    def cpf(self) -> str:
        return self.__cpf

    @property
    def nome(self) -> str:
        return self._nome

    @nome.setter
    def nome(self, valor: str) -> None:
        if not valor.strip():
            raise ValueError("O nome do cliente não pode ficar vazio.")
        self._nome = valor.strip()

    @property
    def cnh(self) -> str:
        return self._cnh

    @cnh.setter
    def cnh(self, valor: str) -> None:
        valor = valor.strip().upper()
        if valor not in Cliente.CATEGORIAS_CNH:
            raise ValueError(f"CNH '{valor}' inválida. Categorias aceitas: {', '.join(Cliente.CATEGORIAS_CNH)}.")
        self._cnh = valor

    def pode_dirigir(self, categoria: str) -> bool:
        """Retorna True se a CNH do cliente inclui a categoria exigida."""
        return categoria in self._cnh

    def resumo(self) -> str:
        """Retorna um texto curto para exibição no terminal."""
        return f"👤 {self._nome} | CPF {self.__cpf} | CNH {self._cnh}"

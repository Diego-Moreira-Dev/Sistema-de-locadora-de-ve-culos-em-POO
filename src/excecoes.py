class LocadoraErro(Exception):
    """Erro base de todas as regras de negócio da locadora."""


class CadastroDuplicadoErro(LocadoraErro):
    """Cliente ou veículo já cadastrado."""


class NaoEncontradoErro(LocadoraErro):
    """Cliente, veículo ou locação não encontrado."""


class VeiculoIndisponivelErro(LocadoraErro):
    """Veículo já está alugado."""


class CnhIncompativelErro(LocadoraErro):
    """Cliente não possui a CNH exigida pelo veículo."""

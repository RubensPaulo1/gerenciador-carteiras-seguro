class Registro:
    def __init__(self, id, endereco, senha_hash):
        self.id = id
        self.endereco = endereco
        self.senha_hash = senha_hash

    def to_dict(self):
        return {
            "id": self.id,
            "endereco": self.endereco,
            "senha_hash": self.senha_hash
        }

    @staticmethod
    def from_dict(dados):
        return Registro(
            dados["id"],
            dados["endereco"],
            dados["senha_hash"]
        )
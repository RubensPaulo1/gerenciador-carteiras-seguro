import json
import os
from registro import Registro
from seguranca import criptografar, descriptografar

ARQUIVO = "dados.enc"


def salvar(registros, chave):
    dados = [r.to_dict() for r in registros]
    json_str = json.dumps(dados)
    dados_criptografados = criptografar(json_str, chave)

    with open(ARQUIVO, "wb") as f:
        f.write(dados_criptografados)


def carregar(chave):
    if not os.path.exists(ARQUIVO):
        return []

    with open(ARQUIVO, "rb") as f:
        dados_criptografados = f.read()

    json_str = descriptografar(dados_criptografados, chave)
    dados = json.loads(json_str)

    return [Registro.from_dict(d) for d in dados]

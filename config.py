import json
import os
import time

CONFIG_FILE = "config.json"


def salvar_config(dados):
    with open(CONFIG_FILE, "w") as f:
        json.dump(dados, f)


def carregar_config():
    if not os.path.exists(CONFIG_FILE):
        return None

    with open(CONFIG_FILE, "r") as f:
        return json.load(f)


def registrar_tentativa_falha():
    config = carregar_config()

    config["tentativas"] += 1

    # Backoff exponencial
    delay = min(2 ** config["tentativas"], 300)  # máximo 5 minutos
    config["bloqueado_ate"] = time.time() + delay

    salvar_config(config)


def resetar_tentativas():
    config = carregar_config()
    config["tentativas"] = 0
    config["bloqueado_ate"] = 0
    salvar_config(config)

import hashlib
import base64
import re
from cryptography.fernet import Fernet


def validar_senha_forte(senha):
    if len(senha) < 8:
        return False
    if not re.search(r"[A-Z]", senha):
        return False
    if not re.search(r"[a-z]", senha):
        return False
    if not re.search(r"[0-9]", senha):
        return False
    return True


def hash_senha(senha):
    return hashlib.sha256(senha.encode()).hexdigest()


def gerar_chave(senha_mestre):
    hash_bytes = hashlib.sha256(senha_mestre.encode()).digest()
    return base64.urlsafe_b64encode(hash_bytes)


def criptografar(dados_str, chave):
    f = Fernet(chave)
    return f.encrypt(dados_str.encode())


def descriptografar(dados_bytes, chave):
    f = Fernet(chave)
    return f.decrypt(dados_bytes).decode()

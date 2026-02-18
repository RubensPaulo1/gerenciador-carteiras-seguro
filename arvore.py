class No:
    def __init__(self, registro):
        self.registro = registro
        self.esquerda = None
        self.direita = None


class ArvoreBST:
    def __init__(self):
        self.raiz = None

    def inserir(self, registro):
        if self.buscar(registro.id):
            raise ValueError("ID já existe.")
        self.raiz = self._inserir(self.raiz, registro)

    def _inserir(self, no, registro):
        if no is None:
            return No(registro)

        if registro.id < no.registro.id:
            no.esquerda = self._inserir(no.esquerda, registro)
        else:
            no.direita = self._inserir(no.direita, registro)

        return no

    def buscar(self, id):
        return self._buscar(self.raiz, id)

    def _buscar(self, no, id):
        if no is None:
            return None

        if id == no.registro.id:
            return no.registro
        elif id < no.registro.id:
            return self._buscar(no.esquerda, id)
        else:
            return self._buscar(no.direita, id)

    def listar(self):
        registros = []
        self._in_order(self.raiz, registros)
        return registros

    def _in_order(self, no, lista):
        if no:
            self._in_order(no.esquerda, lista)
            lista.append(no.registro)
            self._in_order(no.direita, lista)

    def remover(self, id):
        self.raiz = self._remover(self.raiz, id)

    def _remover(self, no, id):
        if no is None:
            return None

        if id < no.registro.id:
            no.esquerda = self._remover(no.esquerda, id)
        elif id > no.registro.id:
            no.direita = self._remover(no.direita, id)
        else:
            if no.esquerda is None:
                return no.direita
            if no.direita is None:
                return no.esquerda

            sucessor = self._minimo(no.direita)
            no.registro = sucessor.registro
            no.direita = self._remover(no.direita, sucessor.registro.id)

        return no

    def _minimo(self, no):
        while no.esquerda:
            no = no.esquerda
        return no

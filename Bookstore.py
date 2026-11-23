# Declaração de autoria
# Autores: Anthony Cesar e Mateus Cerqueira
# Declaro que este código foi desenvolvido por Anthony Cesar e Mateus Cerqueira, com base no nosso próprio
# entendimento e esforço. Não houve plágio ou cópia integral de terceiros.
# Ferramentas de IA, quando utilizadas, foram apenas como apoio ao aprendizado
# e não para a geração integral deste código.

# ===== TDE 2: VERSÃO OTIMIZADA DA LIVRARIA =====
# Mudanças em relação ao TDE 1:
#   - Árvore AVL (balanceada) guarda os livros ordenados por ISBN
#   - Percursos em ordem, pré-ordem e pós-ordem
#   - Merge Sort (divisão e conquista) nos relatórios
#   - Tabela Hash para buscar por ISBN rapidamente (otimização)
#   - Lista encadeada do TDE 1 mantida só pra medir o gargalo (benchmark)

import os
import time


# ===== ESTRUTURA: LISTA ENCADEADA (versão base do TDE 1) =====
# Mantida apenas para comparar o tempo de busca no benchmark.

class Node:
    def __init__(self, dado):
        self.dado = dado
        self.proximo = None


class ListaEncadeada:
    def __init__(self):
        self.cabeca = None

    def inserir(self, dado):
        novo_no = Node(dado)
        if self.cabeca is None:
            self.cabeca = novo_no
            return
        atual = self.cabeca
        while atual.proximo is not None:
            atual = atual.proximo
        atual.proximo = novo_no

    def buscar_por_isbn(self, isbn):
        atual = self.cabeca
        while atual is not None:
            if atual.dado["isbn"] == isbn:
                return atual.dado
            atual = atual.proximo
        return None


# ===== ESTRUTURA: ÁRVORE AVL =====
# Árvore binária de busca que se BALANCEIA sozinha.
# Regra: para todo nó, a diferença de altura entre a subárvore
# esquerda e a direita (fator de balanceamento) é no máximo 1.
# Se passar disso, fazemos ROTAÇÕES pra consertar.

class NoAVL:
    def __init__(self, dado):
        self.dado = dado       # dicionário do livro
        self.esq = None        # filho esquerdo (ISBNs menores)
        self.dir = None        # filho direito (ISBNs maiores)
        self.altura = 1        # altura do nó (folha = 1)


class ArvoreAVL:
    def __init__(self):
        self.raiz = None

    # ----- funções auxiliares de altura e balanceamento -----

    def _altura(self, no):
        if no is None:
            return 0
        return no.altura

    def _atualizar_altura(self, no):
        no.altura = 1 + max(self._altura(no.esq), self._altura(no.dir))

    def _fator(self, no):
        # positivo = pesado pra esquerda, negativo = pesado pra direita
        return self._altura(no.esq) - self._altura(no.dir)

    def _rotacao_direita(self, y):
        # Usada quando a esquerda está pesada demais.
        #     y            x
        #    / \          / \
        #   x   C   -->  A   y
        #  / \              / \
        # A   B            B   C
        x = y.esq
        y.esq = x.dir
        x.dir = y
        self._atualizar_altura(y)
        self._atualizar_altura(x)
        return x  # x é a nova raiz dessa subárvore

    def _rotacao_esquerda(self, x):
        # Espelho da rotação à direita (direita pesada demais).
        y = x.dir
        x.dir = y.esq
        y.esq = x
        self._atualizar_altura(x)
        self._atualizar_altura(y)
        return y

    def _balancear(self, no):
        self._atualizar_altura(no)
        fator = self._fator(no)

        if fator > 1:
            # Esquerda pesada. Se o filho esquerdo pende pra direita,
            # primeiro rotaciona ele (caso esquerda-direita).
            if self._fator(no.esq) < 0:
                no.esq = self._rotacao_esquerda(no.esq)
            return self._rotacao_direita(no)

        if fator < -1:
            # Direita pesada. Caso direita-esquerda se o filho pende pra esquerda.
            if self._fator(no.dir) > 0:
                no.dir = self._rotacao_direita(no.dir)
            return self._rotacao_esquerda(no)

        return no  # já estava balanceado

    # ----- inserir -----

    def inserir(self, dado):
        self.raiz = self._inserir(self.raiz, dado)

    def _inserir(self, no, dado):
        if no is None:
            return NoAVL(dado)

        if dado["isbn"] < no.dado["isbn"]:
            no.esq = self._inserir(no.esq, dado)
        else:
            no.dir = self._inserir(no.dir, dado)

        return self._balancear(no)  # reequilibra no caminho de volta

    # ----- remover -----

    def remover(self, isbn):
        self.raiz = self._remover(self.raiz, isbn)

    def _remover(self, no, isbn):
        if no is None:
            return None

        if isbn < no.dado["isbn"]:
            no.esq = self._remover(no.esq, isbn)
        elif isbn > no.dado["isbn"]:
            no.dir = self._remover(no.dir, isbn)
        else:
            # Achamos o nó a remover.
            if no.esq is None:
                return no.dir      # 0 ou 1 filho (direito)
            if no.dir is None:
                return no.esq      # 1 filho (esquerdo)

            # 2 filhos: pega o sucessor (menor ISBN da direita),
            # copia ele pra cá e remove o sucessor da subárvore direita.
            sucessor = no.dir
            while sucessor.esq is not None:
                sucessor = sucessor.esq
            no.dado = sucessor.dado
            no.dir = self._remover(no.dir, sucessor.dado["isbn"])

        return self._balancear(no)

    # ----- busca (feita direto na árvore, sem converter pra lista) -----

    def buscar(self, isbn):
        atual = self.raiz
        while atual is not None:
            if isbn == atual.dado["isbn"]:
                return atual.dado
            elif isbn < atual.dado["isbn"]:
                atual = atual.esq   # só pode estar na esquerda
            else:
                atual = atual.dir   # só pode estar na direita
        return None

    def buscar_por_titulo(self, termo):
        termo = termo.lower()
        encontrados = []
        self._buscar_titulo(self.raiz, termo, encontrados)
        return encontrados

    def _buscar_titulo(self, no, termo, encontrados):
        # Percorre a árvore em ordem, checando o título de cada nó.
        if no is None:
            return
        self._buscar_titulo(no.esq, termo, encontrados)
        if termo in no.dado["titulo"].lower():
            encontrados.append(no.dado)
        self._buscar_titulo(no.dir, termo, encontrados)

    # ----- travessias -----

    def em_ordem(self):
        # esquerda -> raiz -> direita (sai ordenado por ISBN)
        resultado = []
        self._em_ordem(self.raiz, resultado)
        return resultado

    def _em_ordem(self, no, resultado):
        if no is None:
            return
        self._em_ordem(no.esq, resultado)
        resultado.append(no.dado)
        self._em_ordem(no.dir, resultado)

    def pre_ordem(self):
        # raiz -> esquerda -> direita
        resultado = []
        self._pre_ordem(self.raiz, resultado)
        return resultado

    def _pre_ordem(self, no, resultado):
        if no is None:
            return
        resultado.append(no.dado)
        self._pre_ordem(no.esq, resultado)
        self._pre_ordem(no.dir, resultado)

    def pos_ordem(self):
        # esquerda -> direita -> raiz
        resultado = []
        self._pos_ordem(self.raiz, resultado)
        return resultado

    def _pos_ordem(self, no, resultado):
        if no is None:
            return
        self._pos_ordem(no.esq, resultado)
        self._pos_ordem(no.dir, resultado)
        resultado.append(no.dado)


# ===== ESTRUTURA: TABELA HASH (OTIMIZAÇÃO) =====
# Gargalo medido na versão base: buscar por ISBN na lista encadeada
# percorre nó por nó (O(n)). Na tabela hash, o ISBN vira um número
# (índice) e vamos direto no "balde" certo (O(1) na média).
# Colisões (ISBNs no mesmo balde) são tratadas com uma lista por balde.

class TabelaHash:
    def __init__(self, tamanho=1009):
        self.tamanho = tamanho
        self.baldes = [[] for _ in range(tamanho)]

    def _hash(self, isbn):
        # Função hash simples: mistura os códigos dos caracteres.
        valor = 0
        for letra in isbn:
            valor = (valor * 31 + ord(letra)) % self.tamanho
        return valor

    def inserir(self, livro):
        indice = self._hash(livro["isbn"])
        self.baldes[indice].append(livro)

    def buscar(self, isbn):
        indice = self._hash(isbn)
        for livro in self.baldes[indice]:
            if livro["isbn"] == isbn:
                return livro
        return None

    def remover(self, isbn):
        indice = self._hash(isbn)
        for livro in self.baldes[indice]:
            if livro["isbn"] == isbn:
                self.baldes[indice].remove(livro)
                return True
        return False


# ===== CATÁLOGO: junta a árvore e a hash =====
# Os dois guardam o MESMO dicionário do livro (referência), então
# alterar o livro por um lado reflete no outro.
# Mantive os nomes inserir/buscar_por_isbn/remover/percorrer do TDE 1,
# assim o resto do sistema quase não muda.

class Catalogo:
    def __init__(self):
        self.arvore = ArvoreAVL()
        self.tabela = TabelaHash()

    def inserir(self, livro):
        self.arvore.inserir(livro)
        self.tabela.inserir(livro)

    def buscar_por_isbn(self, isbn):
        return self.tabela.buscar(isbn)   # busca rápida pela hash

    def remover(self, isbn):
        if self.tabela.buscar(isbn) is None:
            return False
        self.arvore.remover(isbn)
        self.tabela.remover(isbn)
        return True

    def percorrer(self):
        return self.arvore.em_ordem()     # lista Python ordenada por ISBN


# ===== ESTRUTURA: PILHA (LIFO) =====

class Pilha:
    def __init__(self):
        self.itens = []

    def empilhar(self, movimentacao):
        self.itens.append(movimentacao)

    def desempilhar(self):
        if len(self.itens) == 0:
            return None
        return self.itens.pop()

    def esta_vazia(self):
        return len(self.itens) == 0


# ===== ESTRUTURA: FILA DE PRIORIDADE =====

class FilaPrioridade:
    def __init__(self):
        self.itens = []

    def inserir(self, item, prioridade):
        self.itens.append({"item": item, "prioridade": prioridade})
        self.itens.sort(key=lambda x: x["prioridade"], reverse=True)

    def proximo(self):
        if len(self.itens) == 0:
            return None
        return self.itens.pop(0)["item"]

    def esta_vazia(self):
        return len(self.itens) == 0


# ===== CRUD DE LIVROS =====

def cadastrar_livro(catalogo):
    isbn = input("ISBN: ").strip()
    titulo = input("Título: ").strip()
    autor = input("Autor: ").strip()

    if not isbn or not titulo or not autor:
        print("Erro: todos os campos são obrigatórios.")
        return

    if catalogo.buscar_por_isbn(isbn) is not None:
        print("Erro: já existe um livro com esse ISBN.")
        return

    try:
        preco = float(input("Preço: "))
        quantidade = int(input("Quantidade em estoque: "))
        estoque_minimo = int(input("Estoque mínimo: "))
    except ValueError:
        print("Erro: preço/quantidade devem ser números.")
        return

    if preco <= 0 or quantidade < 0 or estoque_minimo < 0:
        print("Erro: valores inválidos.")
        return

    livro = {
        "isbn": isbn,
        "titulo": titulo,
        "autor": autor,
        "preco": preco,
        "quantidade": quantidade,
        "estoque_minimo": estoque_minimo
    }

    catalogo.inserir(livro)
    print("Livro cadastrado com sucesso!")


def listar_livros(catalogo):
    livros = catalogo.percorrer()  # percurso em ordem (ordenado por ISBN)

    if len(livros) == 0:
        print("Nenhum livro cadastrado.")
        return

    for livro in livros:
        print(f"{livro['isbn']} - {livro['titulo']} - {livro['autor']} - "
              f"R$ {livro['preco']:.2f} - Qtd: {livro['quantidade']}")


def atualizar_livro(catalogo):
    isbn = input("ISBN do livro a atualizar: ").strip()
    livro = catalogo.buscar_por_isbn(isbn)

    if livro is None:
        print("Livro não encontrado.")
        return

    print("Deixe em branco para não alterar.")
    novo_titulo = input(f"Título ({livro['titulo']}): ").strip()
    novo_preco = input(f"Preço ({livro['preco']}): ").strip()

    if novo_titulo:
        livro["titulo"] = novo_titulo

    if novo_preco:
        try:
            livro["preco"] = float(novo_preco)
        except ValueError:
            print("Preço inválido, mantendo o anterior.")

    print("Livro atualizado com sucesso!")


def remover_livro(catalogo):
    isbn = input("ISBN do livro a remover: ").strip()

    if catalogo.remover(isbn):
        print("Livro removido com sucesso!")
    else:
        print("Livro não encontrado.")


# ===== BUSCA =====

def buscar_livro(catalogo):
    print("1 - Por ISBN (busca na árvore AVL)")
    print("2 - Por título (busca na árvore, percurso em ordem)")
    print("3 - Por ISBN (tabela hash)")
    opcao = input("Escolha: ").strip()

    if opcao == "1":
        isbn = input("ISBN: ").strip()
        resultado = catalogo.arvore.buscar(isbn)
        if resultado:
            print(resultado)
        else:
            print("Livro não encontrado.")

    elif opcao == "2":
        termo = input("Título (ou parte dele): ").strip()
        resultados = catalogo.arvore.buscar_por_titulo(termo)
        if resultados:
            for livro in resultados:
                print(livro)
        else:
            print("Nenhum livro encontrado.")

    elif opcao == "3":
        isbn = input("ISBN: ").strip()
        resultado = catalogo.buscar_por_isbn(isbn)
        if resultado:
            print(resultado)
        else:
            print("Livro não encontrado.")

    else:
        print("Opção inválida.")


# ===== PERCURSOS DA ÁRVORE =====

def mostrar_percursos(catalogo):
    if catalogo.arvore.raiz is None:
        print("Nenhum livro cadastrado.")
        return

    print("Em ordem:  ", [l["isbn"] for l in catalogo.arvore.em_ordem()])
    print("Pré-ordem: ", [l["isbn"] for l in catalogo.arvore.pre_ordem()])
    print("Pós-ordem: ", [l["isbn"] for l in catalogo.arvore.pos_ordem()])


# ===== MOVIMENTAÇÃO DE ESTOQUE =====

def entrada_estoque(catalogo, pilha):
    isbn = input("ISBN: ").strip()
    livro = catalogo.buscar_por_isbn(isbn)
    if livro is None:
        print("Livro não encontrado.")
        return

    try:
        quantidade = int(input("Quantidade a adicionar: "))
    except ValueError:
        print("Quantidade inválida.")
        return

    if quantidade <= 0:
        print("Quantidade deve ser positiva.")
        return

    livro["quantidade"] += quantidade
    pilha.empilhar({"tipo": "entrada", "isbn": isbn, "quantidade": quantidade})
    print("Entrada registrada com sucesso!")


def registrar_venda(catalogo, pilha):
    isbn = input("ISBN: ").strip()
    livro = catalogo.buscar_por_isbn(isbn)
    if livro is None:
        print("Livro não encontrado.")
        return

    try:
        quantidade = int(input("Quantidade vendida: "))
    except ValueError:
        print("Quantidade inválida.")
        return

    if quantidade <= 0:
        print("Quantidade deve ser positiva.")
        return

    if quantidade > livro["quantidade"]:
        print("Erro: estoque insuficiente.")
        return

    livro["quantidade"] -= quantidade
    pilha.empilhar({"tipo": "venda", "isbn": isbn, "quantidade": quantidade})
    print("Venda registrada com sucesso!")


def desfazer_ultima_movimentacao(catalogo, pilha):
    movimentacao = pilha.desempilhar()

    if movimentacao is None:
        print("Não há movimentações para desfazer.")
        return

    livro = catalogo.buscar_por_isbn(movimentacao["isbn"])

    if livro is None:
        print("Livro da movimentação não existe mais.")
        return

    if movimentacao["tipo"] == "entrada":
        livro["quantidade"] -= movimentacao["quantidade"]
    elif movimentacao["tipo"] == "venda":
        livro["quantidade"] += movimentacao["quantidade"]

    print(f"Movimentação desfeita: {movimentacao['tipo']} de {movimentacao['quantidade']} un.")


# ===== ORDENAÇÃO (Merge Sort - Divisão e Conquista) =====
# 1) DIVIDE a lista no meio
# 2) CONQUISTA: ordena cada metade (recursivamente)
# 3) COMBINA: junta as duas metades já ordenadas
# "chave" é uma função que diz por qual valor do livro ordenar.

def merge_sort(lista, chave):
    if len(lista) <= 1:
        return lista  # caso base: 0 ou 1 elemento já está ordenado

    meio = len(lista) // 2
    esquerda = merge_sort(lista[:meio], chave)
    direita = merge_sort(lista[meio:], chave)

    return juntar(esquerda, direita, chave)


def juntar(esquerda, direita, chave):
    resultado = []
    i = 0  # posição na esquerda
    j = 0  # posição na direita

    # Compara o primeiro de cada lado e pega o menor
    while i < len(esquerda) and j < len(direita):
        if chave(esquerda[i]) <= chave(direita[j]):
            resultado.append(esquerda[i])
            i += 1
        else:
            resultado.append(direita[j])
            j += 1

    # Sobrou elemento de um dos lados: já está ordenado, só copia
    while i < len(esquerda):
        resultado.append(esquerda[i])
        i += 1
    while j < len(direita):
        resultado.append(direita[j])
        j += 1

    return resultado


def ordenar_por_quantidade(livros):
    return merge_sort(livros, lambda livro: livro["quantidade"])


def ordenar_por_valor_total(livros):
    return merge_sort(livros, lambda livro: livro["preco"] * livro["quantidade"])


# ===== REPOSIÇÃO E RELATÓRIOS =====

def gerar_pedidos_reposicao(catalogo):
    livros = catalogo.percorrer()
    fila = FilaPrioridade()

    for livro in livros:
        prioridade = livro["estoque_minimo"] - livro["quantidade"]

        if prioridade > 0:
            fila.inserir(livro, prioridade)

    if fila.esta_vazia():
        print("Nenhum livro precisa de reposição.")
        return

    print("=== PEDIDOS DE REPOSIÇÃO (mais urgente primeiro) ===")
    while not fila.esta_vazia():
        livro = fila.proximo()
        print(f"{livro['titulo']} - faltam {livro['estoque_minimo'] - livro['quantidade']} unidades")


def relatorio_por_quantidade(catalogo):
    livros = catalogo.percorrer()

    if len(livros) == 0:
        print("Nenhum livro cadastrado para gerar relatório.")
        return

    ordenados = ordenar_por_quantidade(livros)  # Merge Sort

    print("=== RELATÓRIO POR QUANTIDADE ===")
    for livro in ordenados:
        print(f"{livro['titulo']} - Qtd: {livro['quantidade']}")


def relatorio_por_valor_total(catalogo):
    livros = catalogo.percorrer()

    if len(livros) == 0:
        print("Nenhum livro cadastrado para gerar relatório.")
        return

    print("=== RELATÓRIO POR VALOR TOTAL ===")
    for livro in ordenar_por_valor_total(livros):  # Merge Sort
        print(f"{livro['titulo']} - R$ {livro['preco'] * livro['quantidade']:.2f}")


# ===== BENCHMARK (mede o gargalo e o ganho da otimização) =====

def benchmark():
    quantidade = 3000   # quantidade de livros de teste
    buscas = 300        # quantas buscas repetir em cada estrutura

    lista = ListaEncadeada()
    catalogo = Catalogo()

    for i in range(quantidade):
        livro = {
            "isbn": str(i).zfill(7),
            "titulo": f"Livro {i}",
            "autor": "Autor",
            "preco": 10.0,
            "quantidade": 5,
            "estoque_minimo": 2
        }
        lista.inserir(livro)
        catalogo.inserir(livro)

    # Pior caso pra lista: buscar o ÚLTIMO livro inserido
    isbn_alvo = str(quantidade - 1).zfill(7)

    inicio = time.perf_counter()
    for _ in range(buscas):
        lista.buscar_por_isbn(isbn_alvo)
    tempo_lista = time.perf_counter() - inicio

    inicio = time.perf_counter()
    for _ in range(buscas):
        catalogo.arvore.buscar(isbn_alvo)
    tempo_arvore = time.perf_counter() - inicio

    inicio = time.perf_counter()
    for _ in range(buscas):
        catalogo.tabela.buscar(isbn_alvo)
    tempo_hash = time.perf_counter() - inicio

    print(f"=== BENCHMARK: {buscas} buscas em {quantidade} livros ===")
    print(f"Lista encadeada (versão base): {tempo_lista:.6f} s")
    print(f"Árvore AVL:                    {tempo_arvore:.6f} s")
    print(f"Tabela hash (otimização):      {tempo_hash:.6f} s")

    if tempo_hash > 0:
        print(f"A hash foi ~{tempo_lista / tempo_hash:.0f}x mais rápida que a lista encadeada.")


# ===== UTILIDADES =====

def limpar_tela():
    os.system("cls" if os.name == "nt" else "clear")


def pausar():
    input("\nPressione ENTER para continuar...")


# ===== PROGRAMA PRINCIPAL =====

def menu():
    catalogo = Catalogo()
    pilha = Pilha()

    while True:
        limpar_tela()

        print("\n  ---- LIVRARIA ----  ")
        print("-----------------------")
        print("1. Cadastrar livro")
        print("2. Listar livros")
        print("3. Buscar livro")
        print("4. Atualizar livro")
        print("5. Remover livro")
        print("6. Entrada de estoque")
        print("7. Venda")
        print("8. Desfazer última movimentação")
        print("9. Pedidos de reposição")
        print("10. Relatório por quantidade")
        print("11. Relatório por valor total")
        print("12. Percursos da árvore")
        print("13. Benchmark (lista x árvore x hash)")
        print("0. Sair")

        opcao = input("Escolha uma opção: ").strip()

        match opcao:
            case "1":
                cadastrar_livro(catalogo)
                pausar()
            case "2":
                listar_livros(catalogo)
                pausar()
            case "3":
                buscar_livro(catalogo)
                pausar()
            case "4":
                atualizar_livro(catalogo)
                pausar()
            case "5":
                remover_livro(catalogo)
                pausar()
            case "6":
                entrada_estoque(catalogo, pilha)
                pausar()
            case "7":
                registrar_venda(catalogo, pilha)
                pausar()
            case "8":
                desfazer_ultima_movimentacao(catalogo, pilha)
                pausar()
            case "9":
                gerar_pedidos_reposicao(catalogo)
                pausar()
            case "10":
                relatorio_por_quantidade(catalogo)
                pausar()
            case "11":
                relatorio_por_valor_total(catalogo)
                pausar()
            case "12":
                mostrar_percursos(catalogo)
                pausar()
            case "13":
                benchmark()
                pausar()
            case "0":
                print("Saindo...")
                break
            case _:
                print("Opção inválida.")
                pausar()


if __name__ == "__main__":
    menu()
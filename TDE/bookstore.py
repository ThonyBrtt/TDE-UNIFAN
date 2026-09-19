# ===== ESTRUTURA: NODE (NÓ) =====
# Um "Node" é a unidade básica da lista encadeada.
# Pense nele como uma caixa que guarda UM livro e sabe apontar pra próxima caixa.
import os


class Node:
    def __init__(self, dado):
        self.dado = dado       # Guarda o conteúdo real (o dicionário do livro)
        self.proximo = None    # Aponta pro próximo Node da lista. Começa em None
                                # porque, quando o nó é criado, ele ainda não está
                                # conectado a nenhum outro nó.


# ===== ESTRUTURA: LISTA ENCADEADA =====

class ListaEncadeada:
    def __init__(self):
        self.cabeca = None
        # "cabeca" é o ponteiro pro primeiro Node da lista.
        # Se cabeca == None, a lista está vazia — não existe nenhum nó ainda.

    def inserir(self, dado):
        novo_no = Node(dado)
        # Cria a caixinha nova, já com o livro dentro. Nesse momento,
        # novo_no.proximo ainda é None (não está ligado a nada).

        if self.cabeca is None:
            # CASO 1: a lista está vazia.
            # Não existe "fim" pra percorrer, então o novo nó vira
            # diretamente o primeiro (e único) nó da lista.
            self.cabeca = novo_no
            return

        # CASO 2: a lista já tem elementos.
        # Precisamos "andar" nó por nó até achar o ÚLTIMO,
        # porque é nele que vamos grudar o novo nó.
        atual = self.cabeca  # começamos a andar a partir do primeiro nó

        while atual.proximo is not None:
            # Enquanto o nó atual APONTAR pra outro nó (proximo != None),
            # significa que ele NÃO é o último. Então avançamos.
            atual = atual.proximo

        # Quando o loop para, "atual" é o ÚLTIMO nó da lista
        # (o único cujo .proximo é None).
        atual.proximo = novo_no
        # Conectamos o último nó ao novo nó. Agora o novo_no
        # passa a ser o novo último elemento da corrente.

    def buscar_por_isbn(self, isbn):
        atual = self.cabeca  # começa a busca pelo primeiro nó

        while atual is not None:
            # Continua enquanto ainda existir um nó pra checar.
            # Quando atual virar None, significa que chegamos ao
            # fim da lista sem achar o ISBN.

            if atual.dado["isbn"] == isbn:
                # Achou! O ISBN guardado nesse nó bate com o procurado.
                return atual.dado  # devolve o dicionário do livro inteiro

            atual = atual.proximo  # não era esse, avança pro próximo nó

        return None  # percorreu tudo e não achou nada

    def remover(self, isbn):
        atual = self.cabeca     # nó que estamos analisando agora
        anterior = None         # nó que veio ANTES do atual (começa None
                                 # porque o primeiro nó não tem "antes")

        while atual is not None:
            if atual.dado["isbn"] == isbn:
                # Achamos o nó que precisa ser removido.

                if anterior is None:
                    # Se não existe "anterior", o nó a remover é o
                    # PRIMEIRO da lista. Nesse caso, a cabeça da lista
                    # passa a apontar direto pro segundo nó.
                    self.cabeca = atual.proximo
                else:
                    # Se existe anterior, "pulamos" o nó atual:
                    # o anterior passa a apontar direto pro que vem
                    # depois do atual, cortando o atual da corrente.
                    anterior.proximo = atual.proximo

                return True  # remoção concluída com sucesso

            # Não era esse nó — antes de avançar, guardamos ele
            # como "anterior" pro próximo passo do loop.
            anterior = atual
            atual = atual.proximo

        return False  # percorreu tudo e não achou o ISBN

    def percorrer(self):
        # Essa função "tira uma foto" de tudo que está na lista encadeada
        # nesse exato momento e devolve como uma lista Python comum.
        # É útil porque andar na lista encadeada exige usar .proximo em loop,
        # mas outras partes do sistema (ordenação, listagem, relatórios)
        # trabalham melhor com uma lista Python indexável (lista[0], lista[1]...).

        resultado = []          # lista Python comum, vai virar o "retrato"
                                 # de todos os livros da lista encadeada
        atual = self.cabeca

        while atual is not None:
            resultado.append(atual.dado)
            # IMPORTANTE: aqui copiamos o dicionário do livro (atual.dado)
            # pra dentro da lista Python "resultado". Mas essa cópia é só
            # da REFERÊNCIA ao dicionário, não do conteúdo dele.
            #
            # Ou seja: "resultado" é uma lista NOVA, mas os livros que
            # estão dentro dela são os MESMOS objetos que continuam
            # ligados na lista encadeada. Se alguém alterar
            # resultado[0]["preco"], o preço muda pra todo mundo,
            # porque é o mesmo dicionário na memória — só está
            # "guardado" em dois lugares diferentes (no Node e na lista).
            #
            # Isso é ótimo pra nós: significa que atualizar_livro(),
            # entrada_estoque() e registrar_venda() conseguem editar
            # o livro direto (livro["quantidade"] += x) sem precisar
            # "salvar de volta" na lista encadeada depois.

            atual = atual.proximo

        return resultado
        # Resumindo: a LISTA em si é uma cópia temporária (se você
        # inserir um livro novo depois, esse "resultado" antigo não
        # atualiza sozinho — você precisa chamar percorrer() de novo).
        # Mas os DADOS de cada livro dentro dela são compartilhados
        # com a lista encadeada original.


# ===== ESTRUTURA: PILHA (LIFO) =====
# LIFO = Last In, First Out (o último que entra é o primeiro que sai).
# Pense numa pilha de pratos: você só consegue tirar o de cima,
# que foi o último a ser colocado.

class Pilha:
    def __init__(self):
        self.itens = []
        # Usamos uma lista Python só como "container" por baixo.
        # A REGRA de pilha está em COMO usamos essa lista:
        # só mexemos no final dela, nunca no meio ou no início.

    def empilhar(self, movimentacao):
        self.itens.append(movimentacao)
        # append() adiciona no FINAL da lista.
        # Isso representa "colocar um prato em cima da pilha".
        # "movimentacao" é um dicionário tipo:
        # {"tipo": "venda", "isbn": "123", "quantidade": 5}

    def desempilhar(self):
        if len(self.itens) == 0:
            # Pilha vazia — não tem o que desempilhar.
            return None

        return self.itens.pop()
        # pop() SEM argumento remove e devolve o ÚLTIMO elemento da lista.
        # Isso representa "tirar o prato do topo" — exatamente o
        # comportamento LIFO que a pilha precisa ter.

    def esta_vazia(self):
        return len(self.itens) == 0
        # Função auxiliar pra checar rapidamente se ainda tem
        # movimentações no histórico antes de tentar desempilhar.


# ===== ESTRUTURA: FILA DE PRIORIDADE =====
# Diferente de uma fila comum (que é FIFO - primeiro que entra,
# primeiro que sai), aqui quem sai primeiro é quem tem a
# MAIOR PRIORIDADE, não importa a ordem de chegada.

class FilaPrioridade:
    def __init__(self):
        self.itens = []
        # Lista Python usada como container. Cada item guardado
        # aqui é um dicionário: {"item": livro, "prioridade": numero}

    def inserir(self, item, prioridade):
        self.itens.append({"item": item, "prioridade": prioridade})
        # Adiciona o novo item no final, junto com sua prioridade.

        self.itens.sort(key=lambda x: x["prioridade"], reverse=True)
        # Reordena TODA a lista toda vez que um item novo entra.
        # key=lambda x: x["prioridade"]  → diz pro sort olhar
        #   só o campo "prioridade" de cada item pra comparar
        # reverse=True → do MAIOR pro menor, porque quanto maior
        #   a prioridade (mais crítico o estoque), mais urgente ele é

    def proximo(self):
        if len(self.itens) == 0:
            return None

        return self.itens.pop(0)["item"]
        # pop(0) remove e devolve o PRIMEIRO elemento da lista.
        # Como a lista está sempre ordenada (por causa do sort no
        # inserir), o primeiro elemento é sempre o de MAIOR prioridade.
        # Devolvemos só o "item" (o livro), não o dicionário inteiro
        # com a prioridade junto.

    def esta_vazia(self):
        return len(self.itens) == 0


# ===== CRUD DE LIVROS =====

def cadastrar_livro(catalogo):
    # "catalogo" é a ListaEncadeada que guarda todos os livros.
    # Ela chega aqui como parâmetro porque essa função só sabe
    # MEXER na lista, não sabe onde ela foi criada (isso é feito
    # lá no menu principal).

    isbn = input("ISBN: ").strip()
    titulo = input("Título: ").strip()
    autor = input("Autor: ").strip()
    # .strip() remove espaços em branco extras do início/fim.
    # Ex: se o usuário digitar "  123  ", vira "123".
    # Isso evita bugs bobos tipo "123" != "123 " na hora de comparar.

    if not isbn or not titulo or not autor:
        # Em Python, uma string vazia "" é considerada "False".
        # Então "not isbn" é True quando isbn == "".
        # Essa linha checa: se QUALQUER um dos três campos
        # estiver vazio, bloqueia o cadastro.
        print("Erro: todos os campos são obrigatórios.")
        return  # sai da função imediatamente, sem cadastrar nada

    if catalogo.buscar_por_isbn(isbn) is not None:
        # Aqui REUTILIZAMOS o método que já existe na ListaEncadeada.
        # Se ele encontrar um livro com esse ISBN, retorna o livro
        # (não é None) — ou seja, o ISBN já está em uso.
        print("Erro: já existe um livro com esse ISBN.")
        return

    try:
        preco = float(input("Preço: "))
        quantidade = int(input("Quantidade em estoque: "))
        estoque_minimo = int(input("Estoque mínimo: "))
    except ValueError:
        # Se o usuário digitar uma letra em vez de número
        # (ex: "abc" em vez de "19.90"), o Python tenta converter
        # com float()/int() e explode um erro chamado ValueError.
        # O "try/except" CAPTURA esse erro antes que o programa quebre,
        # e você trata ele mostrando uma mensagem amigável.
        print("Erro: preço/quantidade devem ser números.")
        return

    if preco <= 0 or quantidade < 0 or estoque_minimo < 0:
        # Mesmo que sejam números válidos, eles podem ser
        # ABSURDOS pro seu negócio: preço negativo ou zero não
        # faz sentido; quantidade negativa também não.
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
    # Só depois de passar por TODAS as validações acima,
    # montamos o dicionário do livro com os dados coletados.

    catalogo.inserir(livro)
    # Chama o método da ListaEncadeada que já explicamos antes:
    # ele cria um Node com esse dicionário dentro e gruda
    # no final da lista encadeada.

    print("Livro cadastrado com sucesso!")


def listar_livros(catalogo):
    livros = catalogo.percorrer()
    # percorrer() devolve uma lista Python comum com todos os
    # dicionários de livro, na ordem em que estão na lista encadeada.

    if len(livros) == 0:
        print("Nenhum livro cadastrado.")
        return
        # Evita imprimir um "quadro vazio" — se não tem livro
        # nenhum, avisa isso direto e sai da função.

    for livro in livros:
        print(f"{livro['isbn']} - {livro['titulo']} - {livro['autor']} - "
              f"R$ {livro['preco']:.2f} - Qtd: {livro['quantidade']}")
        # Percorre a lista Python (não a encadeada — já convertemos)
        # e imprime cada livro formatado numa linha.
        # :.2f formata o preço com 2 casas decimais (ex: 19.9 -> 19.90).


def atualizar_livro(catalogo):
    isbn = input("ISBN do livro a atualizar: ").strip()
    livro = catalogo.buscar_por_isbn(isbn)
    # Reutiliza a busca que já existe. "livro" aqui é uma REFERÊNCIA
    # direta ao dicionário que está dentro do Node na lista encadeada
    # — não é uma cópia!

    if livro is None:
        print("Livro não encontrado.")
        return

    print("Deixe em branco para não alterar.")
    novo_titulo = input(f"Título ({livro['titulo']}): ").strip()
    novo_preco = input(f"Preço ({livro['preco']}): ").strip()
    # Mostra o valor ATUAL entre parênteses, como referência,
    # e deixa o usuário decidir se quer mudar ou só apertar Enter.

    if novo_titulo:
        # Se o usuário digitou algo (string não-vazia é "True"),
        # atualiza o título.
        livro["titulo"] = novo_titulo
        # Se ele só apertou Enter (string vazia), essa condição é
        # False e o título antigo permanece intocado.

    if novo_preco:
        try:
            livro["preco"] = float(novo_preco)
        except ValueError:
            print("Preço inválido, mantendo o anterior.")
            # Aqui também protegemos contra o usuário digitar
            # texto no lugar de número, sem travar o programa.

    print("Livro atualizado com sucesso!")


def remover_livro(catalogo):
    isbn = input("ISBN do livro a remover: ").strip()

    if catalogo.remover(isbn):
        # catalogo.remover() retorna True se achou e removeu,
        # False se não achou o ISBN (lembra do bloco 1?).
        # Aqui usamos o retorno direto dentro do "if".
        print("Livro removido com sucesso!")
    else:
        print("Livro não encontrado.")


# ===== BUSCA =====

def busca_sequencial_por_titulo(livros, termo):
    termo = termo.lower()
    encontrados = []
    for livro in livros:
        if termo in livro["titulo"].lower():
            encontrados.append(livro)
    return encontrados


def busca_binaria_por_isbn(livros_ordenados, isbn):
    inicio = 0
    fim = len(livros_ordenados) - 1

    while inicio <= fim:
        meio = (inicio + fim) // 2
        if livros_ordenados[meio]["isbn"] == isbn:
            return livros_ordenados[meio]
        elif livros_ordenados[meio]["isbn"] < isbn:
            inicio = meio + 1
        else:
            fim = meio - 1

    return None


def buscar_livro(catalogo):
    print("1 - Por ISBN (busca binária)")
    print("2 - Por título (busca sequencial)")
    opcao = input("Escolha: ")

    livros = catalogo.percorrer()

    if opcao == "1":
        isbn = input("ISBN: ").strip()
        livros_ordenados = ordenar_por_isbn(livros)  # função definida no bloco de ordenação
        resultado = busca_binaria_por_isbn(livros_ordenados, isbn)
        if resultado:
            print(resultado)
        else:
            print("Livro não encontrado.")
    elif opcao == "2":
        termo = input("Título (ou parte dele): ").strip()
        resultados = busca_sequencial_por_titulo(livros, termo)
        if resultados:
            for livro in resultados:
                print(livro)
        else:
            print("Nenhum livro encontrado.")
    else:
        print("Opção inválida.")


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


# ===== ORDENAÇÃO (Insertion Sort) =====

def ordenar_por_isbn(livros):
    lista = livros.copy()
    for i in range(1, len(lista)):
        atual = lista[i]
        j = i - 1
        while j >= 0 and lista[j]["isbn"] > atual["isbn"]:
            lista[j + 1] = lista[j]
            j -= 1
        lista[j + 1] = atual
    return lista


def ordenar_por_quantidade(livros):
    lista = livros.copy()
    for i in range(1, len(lista)):
        atual = lista[i]
        j = i - 1
        while j >= 0 and lista[j]["quantidade"] > atual["quantidade"]:
            lista[j + 1] = lista[j]
            j -= 1
        lista[j + 1] = atual
    return lista


def ordenar_por_valor_total(livros):
    lista = livros.copy()
    for i in range(1, len(lista)):
        atual = lista[i]
        valor_atual = atual["preco"] * atual["quantidade"]
        j = i - 1
        while j >= 0 and (lista[j]["preco"] * lista[j]["quantidade"]) > valor_atual:
            lista[j + 1] = lista[j]
            j -= 1
        lista[j + 1] = atual
    return lista


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
        # Sem essa checagem, o cabeçalho aparecia sozinho e o "for"
        # abaixo não imprimia nada, dando a impressão de relatório quebrado.
        print("Nenhum livro cadastrado para gerar relatório.")
        return

    ordenados = ordenar_por_quantidade(livros)
    print("=== RELATÓRIO POR QUANTIDADE ===")
    for livro in ordenados:
        print(f"{livro['titulo']} - Qtd: {livro['quantidade']}")


def relatorio_por_valor_total(catalogo):
    livros = catalogo.percorrer()

    if len(livros) == 0:
        # Mesma lógica da função acima: sem livro cadastrado, avisa
        # e sai, em vez de mostrar só o cabeçalho vazio.
        print("Nenhum livro cadastrado para gerar relatório.")
        return

    ordenados = ordenar_por_valor_total(livros)
    print("=== RELATÓRIO POR VALOR TOTAL ===")
    for livro in ordenados:
        valor = livro["preco"] * livro["quantidade"]
        print(f"{livro['titulo']} - Valor total: R$ {valor:.2f}")


def limpar_tela():
    os.system("cls" if os.name == "nt" else "clear")
    # os.name == "nt" → é Windows, então usa o comando "cls"
    # qualquer outro valor (Linux/Mac) → usa o comando "clear"


def pausar():
    input("\nPressione ENTER para continuar...")
    # Trava a execução até o usuário apertar Enter, dando tempo
    # de ler o resultado antes da tela ser limpa no próximo loop.


# ===== PROGRAMA PRINCIPAL =====

def menu():
    catalogo = ListaEncadeada()
    pilha = Pilha()

    while True:
        limpar_tela()  # limpa ANTES de mostrar o menu de novo

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
            case "0":
                print("Saindo...")
                break
            case _:
                print("Opção inválida.")
                pausar()


if __name__ == "__main__":
    menu()
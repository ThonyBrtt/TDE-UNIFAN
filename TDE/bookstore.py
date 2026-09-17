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
        resultado = []          # lista Python comum, vai virar o "retrato"
                                 # de todos os livros da lista encadeada
        atual = self.cabeca

        while atual is not None:
            resultado.append(atual.dado)  # copia o livro pra lista Python
            atual = atual.proximo

        return resultado
        # Essa lista Python é só uma CÓPIA temporária dos dados,
        # útil pra imprimir tudo de uma vez ou pra passar pras
        # funções de ordenação (que preferem trabalhar com listas comuns).

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

def menu():
    catalogo = ListaEncadeada()
    pilha = Pilha()

    while True:
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
                #listar_livros(catalogo)
            case "3":
                #buscar_livro(catalogo)
            case "4":
                #atualizar_livro(catalogo)
            case "5":
                #remover_livro(catalogo)
            case "6":
               # entrada_estoque(catalogo, pilha)
            case "7":
               # registrar_venda(catalogo, pilha)
            case "8":
                #desfazer_ultima_movimentacao(catalogo, pilha)
            case "9":
               # gerar_pedidos_reposicao(catalogo)
            case "10":
               # relatorio_por_quantidade(catalogo)
            case "11":
                # relatorio_por_valor_total(catalogo)
            case "0":
                print("Saindo...")
                break
            case _:
                print("Opção inválida.")


if __name__ == "__main__":
    menu()
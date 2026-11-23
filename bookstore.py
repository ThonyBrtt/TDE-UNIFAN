# ESCOLHER A OPÇÃO DESEJADA 

print("  ---- LIVRARIA ----  ")
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

opcao = int(input("\nDigite uma opção: "))

match opcao:
    case 1 :
        print(" -- CADASTRO DE LIVROS -- ")
    case 2 :
        print(" -- LISTA DE LIVROS -- ")
    case 3 :
        print(" -- BUSCAR LIVRO -- ")
    case 4 :
        print(" -- ATUALIZAR LIVRO -- ")
    case 5 :
        print(" -- REMOVER LIVRO -- ")
    case 6 :
        print(" -- ENTRADA DE ESTOQUE -- ")
    case 7 :
        print(" -- VENDA -- ")
    case 8 : 
        print(" -- DESFAZER ÚLTIMA MOVIMENTAÇÃO -- ")
    case 9 : 
        print(" -- PEDIDOS DE REPOSIÇÃO -- ")
    case 10 : 
        print(" -- RELATORIOS POR QUANTIDADE -- ")
    case 11 : 
        print(" -- RELATORIOS POR VALOR TOTAL -- ")
    case 0 :
        print(" Saindo do sitema... ")
    case _ :
        print("OPÇÃO INVALIDA")


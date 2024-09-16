finalizacoes = [('Dinheiro',1),('Crédito',2),('Débito',3),('Pix',4)]
listaProdutos = {1234:[5.29,'Item 1'],1235:[3.99,'Item 2'],1236:[23.99,'Item 3']}

def ConsultarProduto(id):
    if id in listaProdutos.keys():
        produtoInfo = [listaProdutos[id][1],listaProdutos[id][0]]
        return produtoInfo
    return 'não cadastrado!'

def ConsultaFinalizacao(i):
    i = int(i)
    for x in finalizacoes:
        if x[1] == i:
            return x[0]
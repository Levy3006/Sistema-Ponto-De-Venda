from PyQt5 import uic, QtWidgets
from PyQt5.QtWidgets import QMessageBox
import bancoProdutos
from collections import defaultdict
from PyQt5.QtGui import QKeyEvent
from pynput.keyboard import Listener, Key
from PyQt5.QtGui import QKeySequence
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QShortcut

from PyQt5.QtGui import QActionEvent
    

total = 0.0
linhas = 0
dicPag = defaultdict(list) 
pagamento = 0
nota = '=====NOTA FISCAL===== \n'

def adicionar():

    global total
    global linhas
    global nota

    if sistema.Codigo.text() != '':
        try:
            produtoCodigo = int(sistema.Codigo.text())
            r = bancoProdutos.ConsultarProduto(produtoCodigo)
            
            if r != 'não cadastrado!':
                linhas+=1
                sistema.TelaCompras.addItem(f'{linhas} - {str(r)}')
                sistema.Codigo.setText('')
                total = round(total +r[1],2)
                sistema.TotalLabel.setText(str(total))
            else:
                QMessageBox.about(sistema,'Alerta','PRODUTO NÃO CADASTRADO!')
        except ValueError:
            QMessageBox.about(sistema,'Atenção','CÓDIGO INVÁLIDO!')
    else:
        QMessageBox.about(sistema,"Alerta",'Sem Produtos Para Adicionar!')
    
def remover():
    global linhas
    global total
    try:
        if sistema.TelaCompras.count() == 0:
            return QMessageBox.about(sistema,'Alerta','Lista Vazia!')
        currentIndex = sistema.TelaCompras.currentRow()
        itemText = sistema.TelaCompras.currentItem().text()
        valoritemText = float(str(itemText[5:-1]).split(',')[1])
        if (total-valoritemText)<0:
            return QMessageBox.about(sistema,'ERRO','Não é possível remover itens com o valor total maior que a diferença a ser paga. Estorne algum pagamento e tente novamente')
        item = sistema.TelaCompras.takeItem(currentIndex)
        del item
        
        total = total - float(valoritemText)
        total = round(total,2)
        sistema.TotalLabel.setText(str(total))
    except AttributeError:
        QMessageBox.about(sistema,'Atenção','SEM ITENS SELECIONADOS!')
    
formasPagamento = ''
# dicPag é a lista que contém pagamentos feitos pelo cliente

def pagar():
    global total
    global pagamento
    global nota
    global formasPagamento
    def trocoEnota():
        global total
        global pagamento
        global nota
        global formasPagamento
        if total <= 0.0:
            telaPagamento.Total.setText(str(total))
            itemsTextList =  [str(sistema.TelaCompras.item(i).text()) for i in range(sistema.TelaCompras.count())]
            for x in itemsTextList:
                nota = nota + x +'\n'
            total = round(total,2)
            
            for x,y in dicPag.items():
                formasPagamento += f'{x}: R${y} | '
            nota = nota + '\n'+ formasPagamento
            val = []
            troco = 1
            if total <0:
                troco = -(total)
            elif total == 0:
                troco = 0
            for x in dicPag.values():
                val +=x
            for x in val:
                total+=float(x)
            
            nota = nota + '\n' + f'Total: R${round(total,2)} \nTroco: R${troco}'
            print(nota)
            QMessageBox.about(telaPagamento,'Obrigado!',f'Troco: R$: {troco}')
            telaBoasVindas.show()
            telaPagamento.close()
            
    if total<0:
        trocoEnota()
    try:
        if total>=0:
            
            telaPagamento.Total.setText(str(total))
            retorno = 'Finalizadora Não Cadastrada!'
            entradaPag = telaPagamento.EntradaPagamento.text()
            retorno = bancoProdutos.ConsultaFinalizacao(int(entradaPag))
            while(retorno == None):
                telaPagamento.EntradaPagamento.clear()
                telaPagamento.EntradaValor.clear()
                entradaPag = telaPagamento.EntradaPagamento.text()
                retorno = bancoProdutos.ConsultaFinalizacao(int(entradaPag))
            entradaVal = str(telaPagamento.EntradaValor.text()).strip()
            pagamento = f'{retorno} : R${entradaVal}'
            total = round(total - float(entradaVal),2)
            telaPagamento.Total.setText(str(total))
            telaPagamento.listaPagamentos.addItem(pagamento)
            dicPag[retorno].append(entradaVal)
    except ValueError:
        QMessageBox.about(telaPagamento,'Atenção','==== Finalização inválida ====')
        telaPagamento.EntradaPagamento.clear()
        telaPagamento.EntradaValor.clear()
        
    trocoEnota()
    
def voltar():
    return telaPagamento.close()
def removerPagamento():
    global total
    if telaPagamento.listaPagamentos.count() == 0:
        return QMessageBox.about(telaPagamento,'Alerta','Sem Pagamentos para Remover!')
    try:
        currentIndex = telaPagamento.listaPagamentos.currentRow()
        itemText = telaPagamento.listaPagamentos.currentItem().text()
        IndexValorPag = str(itemText).find('$')
        valorPag = float(str(itemText[IndexValorPag + 1:]).strip())
        item = telaPagamento.listaPagamentos.takeItem(currentIndex)
        del item
        itemText = str(itemText.replace('R$','')).replace(' : ',',').split(',')
        dicPag[itemText[0]].remove(itemText[1])
        total = round(total + valorPag,2)
        telaPagamento.Total.setText(str(total))
    except AttributeError:
        QMessageBox.about(telaPagamento,'Atenção','=== Selecione Finalização a Remover ===')

def finalizar():
    
    if sistema.TelaCompras.count() == 0:
        return QMessageBox.about(sistema,'Alerta','Sem Items para finalizar!')
    telaPagamento.Total.setText(str(total))
    return telaPagamento.show()

def consulta():
    telaConsulta.show()
    
def verificarEntrada(entrada):
    try:
        entrada = int(telaConsulta.ConsultaEntrada.text())
        retorno = str(bancoProdutos.ConsultarProduto(entrada))
        nome_Preco = retorno.replace('[','').replace(']','').replace("'",'')
        indexVirgula = nome_Preco.find(',')
        nome = nome_Preco[0:indexVirgula]
        preco = nome_Preco[indexVirgula+1:].strip()
        telaConsulta.ValorNome.setText(nome)
        telaConsulta.ValorPreco.setText(preco)
        
    except ValueError:
        QMessageBox.about(telaConsulta,'Erro','Código Inválido!')

app = QtWidgets.QApplication([])
telaPagamento = uic.loadUi('TelaPagamento.ui')
sistema = uic.loadUi('sistema_compras.ui')
telaConsulta = uic.loadUi('TelaConsulta.ui')
telaBoasVindas = uic.loadUi('TelaBoasVindas.ui')

def TelaVendas():
    telaBoasVindas.close()
    return sistema.show()

def boasVindas():
    return telaBoasVindas.show()
def fecharConsulta():
    return telaConsulta.close()

# botões
sistema.botaoAdd.clicked.connect(adicionar)
sistema.botaoRem.clicked.connect(remover)
sistema.botaoFin.clicked.connect(finalizar)
sistema.btnIniciarConsulta.clicked.connect(consulta)
telaBoasVindas.btnConsulta.clicked.connect(consulta)
telaConsulta.btnVoltar.clicked.connect(fecharConsulta)
telaConsulta.btnPesq.clicked.connect(verificarEntrada)
telaBoasVindas.btnIniciarVenda.clicked.connect(TelaVendas)
telaPagamento.btnPagar.clicked.connect(pagar)
telaPagamento.btnVoltar.clicked.connect(voltar)
telaPagamento.btnRemover.clicked.connect(removerPagamento)


telaBoasVindas.show()
app.exec()
 


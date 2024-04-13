import sqlite3
from pathlib import Path

database = Path("estoque.db")


class Gestão:        
    def __init__(self, banco):
        self.conn = sqlite3.connect(banco)
        self.criar_tabela_estoque()

    def criar_tabela_estoque(self):
        cursor = self.conn.cursor()
        cursor.execute("""
                CREATE TABLE IF NOT EXISTS estoque (
                    id INTEGER PRIMARY KEY,
                    produto TEXT,
                    quantidade INTEGER
                )""")
            #save database
        self.conn.commit()


    def adicionar_produto(self, produto, quantidade):
        cursor = self.conn.cursor()
        #Is in acording with your tables above.
        cursor.execute(
            "INSERT INTO estoque (produto, quantidade) VALUES (?, ?)", (produto, quantidade))
        self.conn.commit()

    def remover_produto(self,produto, quantidade):
        cursor = self.conn.cursor()
        cursor.execute(
            "SELECT quantidade FROM estoque WHERE produto=?", (produto,))
        resultado = cursor.fetchone()
        #checking if product exist or not
        if resultado:
            estoque_atual = resultado[0]
            if estoque_atual >= quantidade:
                cursor.execute("UPDATE estoque SET quantidade=? WHERE produto=?",
                            (estoque_atual - quantidade, produto))
                self.conn.commit()
            else:
                print(f"Quantidade insuficiente de {produto} em estoque.")
        else:
            print(f"{produto} não encontrado em estoque")

    def consultar_estoque(self, produto):
        cursor = self.conn.cursor()
        cursor.execute(
            "SELECT  quantidade FROM  estoque WHERE  produto=?", (produto,))
        resultado = cursor.fetchone()
        if resultado:
            return resultado[0]
        else:
            return 0

    def listar_produtos(self):
        cursor = self.conn.cursor()
        cursor.execute("SELECT produto FROM estoque")
        produtos = cursor.fetchall()
        #Bring the first product "[0]"
        return [produto[0] for produto in produtos]
    
    def excluir_produto(self, produto):
        cursor = self.conn.cursor()
        cursor.execute("DELETE FROM estoque WHERE produto = ?", (produto,))
        self.conn.commit()

sistema = Gestão("estoque.db")

#excluir = sistema.excluir_produto("Camisas")
#sistema.adicionar_produto("Quantos planetas do sistema solar têm anéis visíveis a partir da Terra?\na)1\nb)2\nc)3\nd)4\n", 4)
#estoque_camiseta = sistema.consultar_estoque("Camiseta")
#sistema.remover_produto("Tênis", 20)

produtos_em_estoque = sistema.listar_produtos()

for produto in produtos_em_estoque:
    quantidade = sistema.consultar_estoque(produto)
    print(f"{produto} - {quantidade}")




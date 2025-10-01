from pathlib import Path
import sqlite3

base_path = Path(__file__).parent
db_path = base_path / "ytupload.db"

def conectar():
    dbselected = sqlite3.connect(db_path)
    return dbselected

def createTable():
    try:
        dbselected = conectar()
        cursor = dbselected.cursor()

        # O comando SQL para criar a tabela
        cursor.execute(f"""
        CREATE TABLE IF NOT EXISTS configs (
            user_id INTEGER,
            ytstudio_link TEXT,
            user_ntfy TEXT,
            FOREIGN KEY (user_id) REFERENCES users (user_id)
        );
        """)
            
        dbselected.close()
    except Exception as e:
        print(f"Erro ao criar a tabela: {e}")

def inserir_dados():
    try:
        dbselected = conectar()
        cursor = dbselected.cursor()

        # Usamos '?' para evitar injeção de SQL. É a forma mais segura!
        cursor.execute("INSERT INTO users (user_name, user_pw) VALUES (?, ?)", ("berlotti", "123"))
        cursor.execute("INSERT INTO users (user_name, user_pw) VALUES (?, ?)", ("fabio", "123"))

        dbselected.commit()  # ESSENCIAL! Confirma e salva a transação.
        dbselected.close()
    except Exception as e:
        print(f"Erro ao inserir livro: {e}")

def consultar():
    """Consulta e exibe todos os livros da tabela."""
    try:
        dbselected = conectar()
        cursor = dbselected.cursor()

        cursor.execute("SELECT * FROM livros")  # O '*' significa "todas as colunas"

        livros = cursor.fetchall()  # Pega todos os resultados da consulta
        dbselected.close()

        if not livros:
            print("Nenhum livro cadastrado.")
        else:
            print("\n--- Lista de Livros ---")
            for livro in livros:
                # livro[0] é o id, livro[1] o título, livro[2] o autor
                print(f"ID: {livro[0]}, Título: {livro[1]}, Autor: {livro[2]}")
            print("-----------------------\n")
        return livros # Retornar a lista pode ser útil
    except Exception as e:
        print(f"Erro ao listar livros: {e}")
        return []
    
def atualizar_livro(id_livro, novo_titulo, novo_autor):
    """Atualiza o título e/ou autor de um livro específico pelo seu ID."""
    try:
        dbselected = conectar()
        cursor = dbselected.cursor()

        cursor.execute("""
        UPDATE livros
        SET titulo = ?, autor = ?
        WHERE id = ?
        """, (novo_titulo, novo_autor, id_livro))

        dbselected.commit() # Não se esqueça do commit ao modificar dados!
        dbselected.close()
        print(f"Livro com ID {id_livro} foi atualizado.")
    except Exception as e:
        print(f"Erro ao atualizar livro: {e}")

def deletar_livro(id_livro):
    """Deleta um livro específico pelo seu ID."""
    try:
        dbselected = conectar()
        cursor = dbselected.cursor()

        cursor.execute("DELETE FROM livros WHERE id = ?", (id_livro,)) # A vírgula é importante!

        dbselected.commit() # Commit também é necessário para deleções.
        dbselected.close()
        print(f"Livro com ID {id_livro} foi deletado.")
    except Exception as e:
        print(f"Erro ao deletar livro: {e}")

def adicionarColuna():
    """Conecta ao banco 'ytupload.db' e adiciona novas colunas à tabela 'users'."""
    try:
        # 1. Conecta ao seu banco de dados
        dbselected = sqlite3.connect('ytupload.db')
        cursor = dbselected.cursor()

        #"Adiciona uma coluna"
        cursor.execute("ALTER TABLE users ADD COLUMN user_name TEXT NOT NULL UNIQUE DEFAULT 'Nome não informado'")
        cursor.execute("ALTER TABLE users ADD COLUMN user_pw TEXT NOT NULL DEFAULT 'senha_padrao'")

        dbselected.commit()

    except sqlite3.OperationalError as e:
        # Este erro acontece se você tentar adicionar uma coluna que já existe.
        print(f"Erro: {e}. É possível que uma das colunas já exista na tabela.")
    except Exception as e:
        print(f"Ocorreu um erro inesperado: {e}")
    finally:
        # 6. Fecha a conexão
        if dbselected:
            dbselected.close()



# createTable("nome da tabela", "nome do id primario da tabela") - CRIAR TABELA


# Código principal para testarmos nossas funções
if __name__ == "__main__":
    # 1. Cria tabela
    #createTable()
    inserir_dados()
    #adicionarColuna() 
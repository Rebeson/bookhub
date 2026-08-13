import sqlite3 as sql

banco = sql.connect("files/dados.db")

def inserir_livro(titulo, autor, editora, ano_publicacao, isbn):
    banco.execute("""INSERT INTO livros(titulo, autor, editora, ano_publicacao, isbn)\
        VALUES (?, ?, ?, ?, ?)""", (titulo, autor, editora, ano_publicacao, isbn))
    banco.commit()
    banco.close()

def inserir_usuario(nome, sobrenome, endereco, e_mail, telefone):
    banco.execute("""INSERT INTO usuarios(nome, sobrenome, endereço, e_mail, telefone)\
         VALUES (?, ?, ?, ?, ?)""", (nome, sobrenome, endereco, e_mail, telefone))
    banco.commit()
    banco.close()

# Exemplo
inserir_livro("Ensaio sobre a cegueira", "José Saramago", "Companhia das Letras", 1998, "12547965")

banco = sql.connect("files/dados.db")
def exibir_livros():
    livros = banco.execute("""SELECT * FROM livros """).fetchall()

    if not livros:
        print("Nenhum livros encontrado na biblioteca.")
        return

    print("Livros na biblioteca:")
    for livros in livros:
        print(f"ID: {livros[0]}")
        print(f"Titulo: {livros[1]}")
        print(f"Autor: {livros[2]}")
        print(f"Editora: {livros[3]}")
        print(f"Ano de publicacao: {livros[4]}")
        print(f"ISBN: {livros[5]}")

exibir_livros()
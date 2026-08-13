import sqlite3 as sql
import os

os.makedirs("files", exist_ok=True)
banco = sql.connect("files/dados.db")

banco.execute("""CREATE TABLE IF NOT EXISTS livros(
              id INTEGER PRIMARY KEY AUTOINCREMENT,
              titulo TEXT NOT NULL,
              autor TEXT NOT NULL,
              editora TEXT NOT NULL,
              ano_publicacao INTEGER NOT NULL,
              isbn TEXT)""")

banco.execute("""CREATE TABLE IF NOT EXISTS usuarios(
              id INTEGER PRIMARY KEY AUTOINCREMENT,
              nome TEXT NOT NULL,
              sobrenome TEXT NOT NULL,
              endereco TEXT NOT NULL,
              e_mail TEXT NOT NULL,
              telefone INTEGER)""")

banco.execute("""CREATE TABLE IF NOT EXISTS emprestimos(
              id INTEGER PRIMARY KEY AUTOINCREMENT,
              id_livro INTEGER NOT NULL,
              id_usuario INTEGER NOT NULL,
              data_emprestimo TEXT NOT NULL,
              data_devolucao TEXT,
              FOREIGN KEY(id_livro) REFERENCES livros(id),
              FOREIGN KEY(id_usuario) REFERENCES usuarios(id))""")
print('tabela criada com sucesso!')
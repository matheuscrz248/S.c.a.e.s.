import sqlite3
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from model.user import User


class Database:
    def __init__(self, nome_banco="auth_db.sqlite"):
        self.nome_banco = os.path.join(os.path.dirname(__file__), nome_banco)
        self.conn = None
        self.conectar()
        self.criar_tabelas()

    def conectar(self):
        """Conecta ao banco de dados SQLite"""
        try:
            self.conn = sqlite3.connect(self.nome_banco)
        except sqlite3.Error as e:
            print(f"Erro ao conectar ao banco de dados: {e}")

    def criar_tabelas(self):
        """Cria as tabelas necessárias no banco de dados"""
        if self.conn:
            try:
                cursor = self.conn.cursor()
                cursor.execute(
                    """CREATE TABLE IF NOT EXISTS usuarios (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        nomeusuario TEXT UNIQUE NOT NULL,
                        nome TEXT NOT NULL,
                        senha TEXT NOT NULL
                    )"""
                )
                self.conn.commit()
            except sqlite3.Error as e:
                print(f"Erro ao criar tabela usuarios: {e}")

    def inserir_usuario(self, user: User):
        """Insere um novo usuário na tabela"""
        if self.conn:
            try:
                cursor = self.conn.cursor()
                cursor.execute(
                    "INSERT INTO usuarios (nomeusuario, nome, senha) VALUES (?, ?, ?)",
                    (user.nomeusuario, user.nome, user.senha),
                )
                self.conn.commit()
            except sqlite3.Error as e:
                print(f"Erro ao inserir usuário: {e}")

    def buscar_usuario_por_nomeusuario(self, nomeusuario):
        """Busca um usuário pelo nome de usuário"""
        cursor = self.conn.cursor()
        cursor.execute("SELECT id, nome, nomeusuario, senha FROM usuarios WHERE nomeusuario = ?", (nomeusuario,))
        row = cursor.fetchone()
        if row:
            return User(id=row[0], nome=row[1], nomeusuario=row[2], senha=row[3])
        return None

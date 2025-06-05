from db.database import Database
from model.user import User


class AuthController:
    def __init__(self):
        self.db = Database()

    def login(self, nomeusuario, senha):
        """Verifica se as credenciais são válidas no banco de dados"""
        user = self.db.buscar_usuario_por_nomeusuario(nomeusuario)
        if user and user.senha == senha:
            return True, user, "Login realizado com sucesso!"
        return False, None, "Nome de usuário ou senha incorretos!"

    def register(self, nome, nomeusuario, senha):
        """Registra um novo usuário no banco de dados"""
        user_existente = self.db.buscar_usuario_por_nomeusuario(nomeusuario)
        if user_existente:
            return False, "Nome de usuário já registrado!"
        novo_usuario = User(nome=nome, nomeusuario=nomeusuario, senha=senha)
        self.db.inserir_usuario(novo_usuario)
        return True, "Usuário registrado com sucesso!"

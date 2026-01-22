# Sistema de Controle de Aluguéis de Equipamentos de Som 🎧

Este projeto é um sistema de controle de aluguéis de equipamentos de som, com suporte a múltiplos usuários, interface gráfica e banco de dados local.


## Funcionalidades

- Registro e login de usuário
- Cadastro, edição e remoção de aluguéis por usuário
- Geração de relatórios individuais por usuário
- Interface gráfica com Tkinter
- Banco de dados SQLite


## Tecnologias utilizadas na criação

- Python 3.13.3
- Tkinter (já incluso no Python)
- SQLite (biblioteca padrão do Python)
- VS Code


## Como executar o projeto

1. Baixe o código ou clone o repositório:

```plaintext
git clone https://github.com/matheuscrz248/S.c.a.e.s..git
```

2. Instale o Python 3, se ainda não tiver.

3. Execute o arquivo chamado "login_view.py" dentro da pasta SCAES/login/view.


## Estrutura do projeto

```plaintext
login/
├── controller/            # Lógica de autenticação
│   └── auth_controller.py
├── db/                    # Banco de dados SQLite
│   └── database.py
├── model/                 # Usuário
│   └── user.py
├── view/                  # Telas e interface gráfica
│   ├── login_view.py      # Arquivo que deverá ser executado
│   ├── main_view.py
│   └── register_view.py
└── README.md
```

## Adendos

O projeto NÃO POSSUI criptografia pra senhas.


## Autor

- [matheuscrz248 - Matheus Cruz de Oliveira](https://github.com/matheuscrz248)

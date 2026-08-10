# Chat em Tempo Real

Aplicação web de mensagens em tempo real desenvolvida para estudo de desenvolvimento full stack, autenticação e comunicação via WebSockets.

O projeto permite que usuários realizem cadastro, autenticação e troquem mensagens em tempo real através de uma comunicação persistente entre frontend e backend.

## Funcionalidades

- Cadastro e autenticação de usuários
- Login utilizando JWT
- Envio e recebimento de mensagens em tempo real utilizando WebSockets
- Gerenciamento de usuários
- Persistência de mensagens em banco de dados

## Tecnologias

### Backend
- Python
- FastAPI
- SQLAlchemy
- SQLite
- JWT
- WebSockets

### Frontend
- React
- TypeScript
- HTML
- CSS

## Como executar

### Backend

```bash
cd backend

python -m venv venv
source venv/bin/activate

pip install -r requirements.txt

uvicorn main:app --reload
```

### Frontend

```bash
cd frontend

npm install

npm run dev
```

## Próximas melhorias

- Melhorar a implementação do refresh no websocket
- Adicionar e remover usuários em grupos já criados
- Melhorias na interface do usuário
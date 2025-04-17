from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from .auth import create_access_token, verify_password, get_password_hash

router = APIRouter()

# Usuário fake para demonstração
fake_user_db = {
    "victor@123": {
        "email": "victor@123",
        "hashed_password": get_password_hash("123"),
    }
}

# Modelo para a solicitação de login
class LoginRequest(BaseModel):
    email: str
    password: str

# Modelo para a resposta com o token
class TokenResponse(BaseModel):
    access_token: str
    token_type: str

@router.post("/login", response_model=TokenResponse)
def login(request: LoginRequest):
    user = fake_user_db.get(request.email)
    if not user or not verify_password(request.password, user["hashed_password"]):
        raise HTTPException(status_code=401, detail="e-mail ou senha inválidos")
    
    # Dados para o token
    token_data = {"sub": request.email}
    access_token = create_access_token(data=token_data)
    return {"access_token": access_token, "token_type": "bearer"}

@router.get("/", response_class=HTMLResponse)
def welcome_page():
    return """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Welcome</title>
        <style>
            body {
                font-family: Arial, sans-serif;
                background-color: #f9f9f9;
                color: #444;
                text-align: center;
                margin: 0;
                padding: 0;
                display: flex;
                flex-direction: column;
                justify-content: center;
                height: 100vh;
            }
            h1 {
                color: #4caf50;
                font-size: 2.5rem;
            }
            p {
                font-size: 1.2rem;
                color: #666;
            }
            footer {
                margin-top: 20px;
                font-size: 0.9rem;
                color: #aaa;
            }
        </style>
    </head>
    <body>
        <h1>Bem-vindo à nossa API!</h1>
        <p>Explore os recursos disponíveis acessando a documentação ou outros endpoints.</p>
        <footer>
            <p>&copy; 2025 - Nossa Empresa</p>
        </footer>
    </body>
    </html>
    """

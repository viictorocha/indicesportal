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

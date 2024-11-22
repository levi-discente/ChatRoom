from datetime import datetime, timedelta
from fastapi import Depends, HTTPException
from fastapi.security.oauth2 import OAuth2PasswordBearer
import jwt

SECRET_KEY = "your_secret_key"  # Substitua por uma chave forte e secreta
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# Dependência para autenticação
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")


# Utilidades
def create_access_token(data: dict, expires_delta: timedelta):
    """
    Cria um token JWT com um tempo de expiração.
    """
    to_encode = data.copy()
    expire = datetime.utcnow() + expires_delta
    to_encode.update({"exp": expire})
    # PyJWT usa diretamente a função jwt.encode
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


def verify_token(token: str):
    """
    Decodifica e valida um token JWT.
    """
    try:
        # PyJWT usa diretamente a função jwt.decode
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token expirado")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Token inválido")


def get_current_user(token: str = Depends(oauth2_scheme)):
    """
    Decodifica o token JWT e retorna o nome do usuário.
    """
    payload = verify_token(token)
    username = payload.get("sub")
    if not username:
        raise HTTPException(status_code=401, detail="Usuário não autenticado")
    return username

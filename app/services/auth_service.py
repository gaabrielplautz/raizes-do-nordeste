from sqlalchemy.orm import Session
from app.models.models import Usuario, TipoUsuarioEnum
from app.schemas.schemas import UsuarioCreate
from app.core.security import get_password_hash, verify_password, create_access_token
from fastapi import HTTPException, status
from datetime import timedelta
from app.core.config import settings


def criar_usuario(db: Session, usuario_data: UsuarioCreate):
    # Verifica se o e-mail já está cadastrado (Conformidade com regras de negócio e LGPD)
    db_usuario = db.query(Usuario).filter(Usuario.email == usuario_data.email).first()
    if db_usuario:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="O e-mail informado já está cadastrado no sistema."
        )

    # Cria o hash seguro da senha usando Bcrypt (requisito de segurança)
    senha_hash = get_password_hash(usuario_data.senha)

    novo_usuario = Usuario(
        nome=usuario_data.nome,
        email=usuario_data.email,
        senha_hash=senha_hash,
        tipo=usuario_data.tipo or TipoUsuarioEnum.CLIENTE
    )

    db.add(novo_usuario)
    db.commit()
    db.refresh(novo_usuario)
    return novo_usuario


def autenticar_usuario(db: Session, email: str, senha: str):
    usuario = db.query(Usuario).filter(Usuario.email == email).first()
    if not usuario or not verify_password(senha, usuario.senha_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="E-mail ou palavra-passe incorretos",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # Gera o token JWT de acesso (HS256)
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": usuario.email, "tipo": usuario.tipo}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}
from pydantic import BaseModel, Field

class FidelidadeResponse(BaseModel):
    id: int
    usuario_id: int = Field(..., validation_alias="usuario_id")
    pontos: int
    consentimento_lgpd: bool = Field(..., validation_alias="consentimento_lgpd")

    class Config:
        from_attributes = True
        populate_by_name = True

class ResgatePontosRequest(BaseModel):
    quantidade: int
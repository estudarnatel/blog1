from pydantic import BaseModel
from typing import Optional


# =========================
# Aprovado (CSV)
# =========================
class Aprovado(BaseModel):
    Curso: str
    Nome: str        
    Posicao: str
    Nota: str
    Categoria: str
    Semestre: str
    Chamada: str


# # # # # # # # # # # # # # # # # # # # # FIM DAS ROTAS PARA O BLOG DA ATIVIDADE EM CLASSE (EXCLUIR DEPOIS) # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
class Blog (BaseModel):
    Action: str
    Message: str        
    Author: str
    
# # # # # # # # # # # # # # # # # # # # # FIM DAS ROTAS PARA O BLOG DA ATIVIDADE EM CLASSE (EXCLUIR DEPOIS) # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
    
# =========================
# SETTINGS
# =========================
class SettingSchema(BaseModel):
    varName: str
    varValue: Optional[str] = None
    boolean: Optional[bool] = None

    class Config:
        from_attributes = True


class SettingUpdate(BaseModel):
    varValue: Optional[str] = None
    boolean: Optional[bool] = None


# =========================
# CANAIS
# =========================
class Canal(BaseModel):
    cId: int | None = None
    channelId: str
    channelName: str
    channelProfilePicUrl: str


class CanalResponse2(BaseModel):
    cId: int | None = None
    channelId: str


class CanalResponse3(BaseModel):
    channelId: str
    channelName: str
    channelProfilePicUrl: str

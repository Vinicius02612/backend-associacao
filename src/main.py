import uvicorn
from fastapi import FastAPI
from routers import router_login, router_user_associate,router_solictacoes, router_projetos, router_despesas, router_receitas, router_mensalidade
from connection.database import Base, engine



#Base.metadata.drop_all(bind=engine)
Base.metadata.create_all(bind=engine)

app = FastAPI()


app.include_router(router_login.router)
app.include_router(router_user_associate.router)
app.include_router(router_projetos.router)
app.include_router(router_solictacoes.router)
app.include_router(router_despesas.router)
app.include_router(router_receitas.router)
app.include_router(router_mensalidade.router)

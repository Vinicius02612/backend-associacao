import uvicorn
from fastapi import FastAPI, HTTPException,status
from routers import router_user_associate, router_solictacoes, router_projetos, router_despesas
from connection.database import Base, engine



#Base.metadata.drop_all(bind=engine)
Base.metadata.create_all(bind=engine)

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Hello World"}

app.include_router(router_user_associate.router)
app.include_router(router_projetos.router)
app.include_router(router_solictacoes.router)
app.include_router(router_despesas.router)


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
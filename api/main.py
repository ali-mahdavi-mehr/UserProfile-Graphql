
from typing import Union
from fastapi import FastAPI
import uvicorn
from . import v1
from strawberry.asgi import GraphQL
from schemas import graph

app = FastAPI()
app.include_router(v1.users.router)
app.include_router(v1.profile.router)



graphql_app = GraphQL(graph.query.schema, graphiql=True)

app.add_route("/graphql", graphql_app)

if __name__ == "__main__":
    uvicorn.run(app=app)

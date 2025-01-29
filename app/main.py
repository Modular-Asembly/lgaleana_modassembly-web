from dotenv import load_dotenv
from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware


load_dotenv()


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Models

from app.models.User import User
from app.models.Conversation import Conversation
from app.models.Message import Message
from app.models.Repository import Repository

# Endpoints

from app.api.repository.create_repository_endpoint import router
app.include_router(router)
from app.api.auth.login_user_endpoint import router
app.include_router(router)
from app.api.user.create_user_endpoint import router
app.include_router(router)
from app.api.conversation.create_conversation_endpoint import router
app.include_router(router)
from app.api.repository.delete_repository_endpoint import router
app.include_router(router)

# Database

from app.modassembly.database.sql.get_sql_session import Base, engine
Base.metadata.create_all(engine)

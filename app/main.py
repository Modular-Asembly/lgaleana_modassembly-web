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

from app.modassembly.models.repository.Repository import Repository
from app.modassembly.models.message.Message import Message
from app.modassembly.models.user.User import User
from app.modassembly.models.conversation.Conversation import Conversation

# Endpoints

from app.modassembly.users.endpoints.create_user_endpoint import router
app.include_router(router)
from app.modassembly.users.endpoints.login_user_endpoint import router
app.include_router(router)
from app.modassembly.repositories.endpoints.create_repository_endpoint import router
app.include_router(router)
from app.modassembly.repositories.endpoints.delete_repository_endpoint import router
app.include_router(router)
from app.modassembly.conversations.endpoints.list_conversations_endpoint import router
app.include_router(router)

# Database

from app.modassembly.database.sql.get_sql_session import Base, engine
Base.metadata.create_all(engine)

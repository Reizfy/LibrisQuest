from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from slowapi.errors import RateLimitExceeded
from slowapi.middleware import SlowAPIMiddleware
from app.core.limiter import limiter
from app.core.database import database
from app.core.exception import CustomException
from app.middlewares.main import middleware
from app.core.config import config
from app.api.routes import main

app = FastAPI(
    title="LibrisQuest REST API",
    description="RESTful API for LibrisQuest - Gamified Digital Reader for University Students",
    version="1.0.0",
)

# rate limiter
app.state.limiter = limiter

# event handler
app.add_event_handler("startup", database.open_db_connection)
app.add_event_handler("shutdown", database.close_db_connection)

# middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=config.ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.add_middleware(SlowAPIMiddleware)

# exception handler
app.add_exception_handler(CustomException, middleware.custom_exception_handler)
app.add_exception_handler(RateLimitExceeded, middleware.rate_limit_exception_handler)
app.add_exception_handler(Exception, middleware.unhandled_exception_handler)


# router
app.include_router(main.router)


@app.get("/")
async def root():
    return {
        "name": "LibrisQuest REST API",
        "version": "1.0.0",
        "status": "online",
    }

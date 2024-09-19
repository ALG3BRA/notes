from api.notes import router as doc_router
from api.auth import router as auth_router

all_routers = [
    doc_router,
    auth_router
]

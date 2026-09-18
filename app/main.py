from fastapi import Depends, FastAPI, File, Request, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import Response
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded
from slowapi.util import get_remote_address

from app.auth import verify_api_key
from app.config import settings
from app.models import ApiResponse
from app.remover import remove_background
from app.remover import get_session
get_session()  # 起動時にモデルをロード

limiter = Limiter(key_func=get_remote_address)

app = FastAPI(title=settings.app_name, version="0.1.0")
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
@app.head("/")
def root():
    return {"name": settings.app_name, "status": "ok"}


@app.get("/health")
def health():
    return {"status": "healthy"}


@app.post("/v1/remove-bg")
@limiter.limit("30/minute")
async def remove_bg(
    request: Request,
    file: UploadFile = File(...),
    _: str = Depends(verify_api_key),
):
    image_bytes = await file.read()
    result_bytes = remove_background(image_bytes)
    return Response(content=result_bytes, media_type="image/png")
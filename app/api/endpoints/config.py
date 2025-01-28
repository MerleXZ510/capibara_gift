from fastapi import APIRouter
from loguru import logger
import os

router = APIRouter()

@router.get("/config")
async def get_config():
    """獲取前端所需的配置"""
    return {
        "captcha_api_url": os.getenv("CAPTCHA_GENERATE_URL"),
        "claim_api_url": os.getenv("CLAIM_API_URL"),
        "default_user_ids": os.getenv("DEFAULT_USER_IDS", "").split(",")
    } 
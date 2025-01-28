from fastapi import APIRouter, UploadFile, File, Form, HTTPException
from loguru import logger
from typing import Optional
from app.services.captcha_service import CaptchaService
import httpx
import os

router = APIRouter()
captcha_service = CaptchaService()

@router.post("/captcha", status_code=200)
async def recognize_captcha(
    game_id: str = Form(...),
    serial_number: str = Form(...),
    captcha_id: str = Form(...)
):
    try:
        logger.info(f"接收到辨識請求: game_id={game_id}, serial_number={serial_number}, captcha_id={captcha_id}")
        
        # 從遠程服務器獲取驗證碼圖片
        base_url = os.getenv('CAPTCHA_BASE_URL')
        image_url = f"{base_url}/image/{captcha_id}"
            
        logger.info(f"獲取驗證碼圖片: {image_url}")
        
        async with httpx.AsyncClient() as client:
            response = await client.get(image_url)
            if response.status_code != 200:
                logger.error(f"獲取驗證碼圖片失敗: status={response.status_code}, response={response.text}")
                raise HTTPException(status_code=400, detail=f"無法獲取驗證碼圖片: {response.text}")
            
            image_content = response.content
            logger.info("成功獲取驗證碼圖片")

        # 調用驗證碼辨識服務
        try:
            result = await captcha_service.recognize(image_content)
            logger.info(f"驗證碼辨識結果: {result}")
            
            response_data = {
                "success": True,
                "result": result,
                "message": "辨識成功"
            }
            logger.info(f"返回結果: {response_data}")
            return response_data

        except ValueError as ve:
            logger.warning(f"驗證碼辨識值錯誤: {str(ve)}")
            return {
                "success": False,
                "result": None,
                "message": str(ve)
            }
        except Exception as e:
            logger.error(f"驗證碼辨識失敗: {str(e)}")
            return {
                "success": False,
                "result": None,
                "message": f"辨識失敗: {str(e)}"
            }
            
    except HTTPException as he:
        raise he
    except Exception as e:
        logger.error(f"處理請求失敗: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e)) 
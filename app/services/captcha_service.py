import ddddocr
from loguru import logger

class CaptchaService:
    def __init__(self):
        try:
            # 初始化 ddddocr
            self.dddd_reader = ddddocr.DdddOcr(show_ad=False)
            logger.info("ddddocr 初始化成功")
        except Exception as e:
            logger.error(f"ddddocr 初始化失敗: {str(e)}")
            raise

    async def recognize(self, image_content: bytes) -> str:
        try:
            if not image_content:
                raise ValueError("圖片內容為空")

            # 進行辨識
            result = self.dddd_reader.classification(image_content)
            logger.info(f"原始辨識結果: {result}")
            
            if not result:
                raise ValueError("無法辨識驗證碼")

            # 清理結果，只保留數字
            cleaned_result = ''.join(filter(str.isdigit, result))
            logger.info(f"清理後結果: {cleaned_result}")
            
            # 驗證結果長度
            if len(cleaned_result) != 4:
                logger.warning(f"辨識結果長度不正確: {cleaned_result} (長度: {len(cleaned_result)})")
                # 如果長度不足4位，嘗試補0
                if len(cleaned_result) < 4:
                    cleaned_result = cleaned_result.zfill(4)
                    logger.info(f"補0後結果: {cleaned_result}")
                else:
                    raise ValueError("驗證碼格式不正確")

            logger.info(f"最終驗證碼結果: {cleaned_result}")
            return cleaned_result

        except ValueError as ve:
            logger.error(f"驗證碼辨識錯誤: {str(ve)}")
            raise
        except Exception as e:
            logger.error(f"驗證碼辨識處理錯誤: {str(e)}")
            raise 
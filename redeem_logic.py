# redeem_logic.py
import httpx
import os

async def redeem_code_for_user(user_id, gift_code):
    captcha_generate_url = os.getenv("CAPTCHA_GENERATE_URL")
    captcha_api_url = os.getenv("CAPTCHA_API_URL")
    claim_api_url = os.getenv("CLAIM_API_URL")

    async with httpx.AsyncClient() as client:
        try:
            # Step 1: 產生 Captcha
            captcha_res = await client.post(captcha_generate_url)
            captcha_data = captcha_res.json()
            captcha_id = captcha_data["data"]["captchaId"]

            # Step 2: 辨識 Captcha
            form_data = {
                "game_id": user_id,
                "serial_number": gift_code,
                "captcha_id": captcha_id
            }
            captcha_res = await client.post(captcha_api_url, data=form_data)
            captcha_result = captcha_res.json()

            if not captcha_result["success"]:
                return f"[{user_id}] ❌ 驗證碼失敗: {captcha_result['message']}"

            # Step 3: 提交兌換
            payload = {
                "userId": user_id,
                "giftCode": gift_code,
                "captcha": captcha_result["result"],
                "captchaId": captcha_id
            }
            claim_res = await client.post(claim_api_url, json=payload)
            claim_data = claim_res.json()

            if claim_data.get("code") == 0:
                return f"[{user_id}] ✅ 兌換成功"
            elif claim_data.get("code") == 20407:
                return f"[{user_id}] ⚠️ 已經兌換過"
            else:
                return f"[{user_id}] ❌ 兌換失敗: {claim_data.get('message', '未知錯誤')}"

        except Exception as e:
            return f"[{user_id}] ⚠️ 發生錯誤: {str(e)}"

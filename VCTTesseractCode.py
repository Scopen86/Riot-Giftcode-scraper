import keyboard
import pytesseract
from PIL import ImageGrab, Image
import requests
import json

def request(code):
    authToken = "eyJraWQiOiIxIiwiYWxnIjoiUlMyNTYifQ.eyJwcCI6eyJjIjoiYXMifSwic3ViIjoiOGQ3ZjY3Y2YtNDA4NS01NDExLWIwOWEtNjJjODNjNmVkMTZlIiwic2NwIjpbImFjY291bnQiLCJvcGVuaWQiLCJsb2wiXSwiY2xtIjpbImVtYWlsX3ZlcmlmaWVkIiwib3BlbmlkIiwicHciLCJsb2wiLCJwaG9uZV9udW1iZXJfdmVyaWZpZWQiLCJsb2NhbGUiLCJhY2NvdW50X3ZlcmlmaWVkIiwiZmVkZXJhdGVkX2lkZW50aXR5X2RldGFpbHMiLCJyZ25fVk4yIiwiZmVkZXJhdGVkX2lkZW50aXR5X3Byb3ZpZGVycyIsImFjY3RfZ250IiwiYWNjdCIsImFnZSIsImFmZmluaXR5Il0sImRhdCI6eyJwIjpudWxsLCJyIjoiVk4yIiwiYyI6ImFzMSIsInUiOjMxNDg1MzE4NTA5NzA0NjQsImxpZCI6Im5WQldTRnZlQXptNXkwWGpIdDJtWGcifSwiaXNzIjoiaHR0cHM6Ly9hdXRoLnJpb3RnYW1lcy5jb20iLCJwbHQiOnsiZGV2IjoidW5rbm93biIsImlkIjoid2ViIn0sImV4cCI6MTcyMzcyMDIwOCwiaWF0IjoxNzIzNzE2NjA4LCJqdGkiOiJsVS1RWExWT0drQSIsImNpZCI6ImRpcmVjdGJ1eS1wcm9kIn0.JipIxw-SQf2xZzFfNNyaJYHL923aLntGts0qEwwZ6BEPD1grNXw8RABLMEZIxN8WeUEV9dwrRbFxeNZy8gdF_BBlbAIt5YUa4vJg78GHXQha8Dwg-yn3pWYXxbMLudEdRuodOST9QtYoRut2GcUik8MroI3Ef6Li8-L0ip-_p5fI3lgRl9Zy3f9hIWvXLwhiCFQTGTFMkZslpB9MnWLmk5Z-Uqz6tQR--fhgapiiA-JQGkCX6iqFGKvGcDE5nsi4mnwqDOjAFbjL5pw5Epb2bKPYUOcMH9k3O40kTEpkmMV-MyLtjDI3cB9uTbXNNfbMaFMx73hJXqHHcFxcewoXCA"
    url = "https://usw2-red.pp.sgp.pvp.net/contentcodes/v1/validate"

    payload = json.dumps({
    "code": code,
    "locale": "vi_VN"
    })
    headers = {
    'accept': 'application/json, text/plain, */*',
    'accept-language': 'en-US,en;q=0.9,vi;q=0.8',
    'authorization': f'Bearer {authToken}',
    'content-type': 'application/json',
    'origin': 'https://shop.riotgames.com',
    'priority': 'u=1, i',
    'referer': 'https://shop.riotgames.com/vi-vn/redeem/',
    'sec-ch-ua': '"Not)A;Brand";v="99", "Microsoft Edge";v="127", "Chromium";v="127"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'cross-site',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36 Edg/127.0.0.0',
    'Cookie': '__cf_bm=OyfXIwem2n5EZZI6WXHpSpmDwAgRybIbPVHFLPM.bvI-1723658916-1.0.1.1-F2GVvWEy99icWlrAnc7iLLXS0bIRv4dn1XzpK34pKOWsc5Q6dZlaXst_sqIe.ietihuMFVBBqPTdjxjmJALWBA'
    }

    response = requests.request("POST", url, headers=headers, data=payload)

    print(response.text)

pytesseract.pytesseract.tesseract_cmd = 'C:\\Program Files\\Tesseract-OCR\\tesseract.exe'

def capture_and_extract_text():
    # Coordinates for the region to capture
    x1, y1, x2, y2 = 460, 780, 1100, 850

    # Capture the specific region of the screen using ImageGrab
    screenshot = ImageGrab.grab(bbox=(x1, y1, x2, y2))

    # Show the captured image for debugging purposes (optional)
    #screenshot.show()

    # Convert the screenshot to a format suitable for pytesseract (PIL Image)
    screenshot_pil = screenshot.convert('RGB')

    custom_oem_psm_config = r'--tessdata-dir "C:\\Users\\Scopen\\Desktop" --psm 6'

    # Use pytesseract to read the text from the captured image with the custom model
    extracted_text = pytesseract.image_to_string(screenshot_pil, config=custom_oem_psm_config, lang='VCT')


    # Output the extracted text
    print("Extracted Text:")
    print(extracted_text)
    return extracted_text

def on_key_press():
    extracted_text = capture_and_extract_text()
    response = request(extracted_text)

# Listen for the Alt+C key combination
keyboard.add_hotkey('alt+c', on_key_press)

# Keep the program running
print("Listening for Alt+C...")

keyboard.wait('esc')  # Press 'esc' to exit the program
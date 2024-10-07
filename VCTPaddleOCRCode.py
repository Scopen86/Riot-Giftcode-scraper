import keyboard
from PIL import ImageGrab, ImageOps
import requests
import json
from paddleocr import PaddleOCR
import numpy as np
import re
import time
from concurrent.futures import ThreadPoolExecutor, as_completed


authToken = "eyJraWQiOiIxIiwiYWxnIjoiUlMyNTYifQ.eyJwcCI6eyJjIjoiYXMifSwic3ViIjoiOGQ3ZjY3Y2YtNDA4NS01NDExLWIwOWEtNjJjODNjNmVkMTZlIiwic2NwIjpbImFjY291bnQiLCJvcGVuaWQiLCJsb2wiXSwiY2xtIjpbImVtYWlsX3ZlcmlmaWVkIiwib3BlbmlkIiwicHciLCJsb2wiLCJwaG9uZV9udW1iZXJfdmVyaWZpZWQiLCJsb2NhbGUiLCJhY2NvdW50X3ZlcmlmaWVkIiwiZmVkZXJhdGVkX2lkZW50aXR5X2RldGFpbHMiLCJyZ25fVk4yIiwiZmVkZXJhdGVkX2lkZW50aXR5X3Byb3ZpZGVycyIsImFjY3RfZ250IiwiYWNjdCIsImFnZSIsImFmZmluaXR5Il0sImRhdCI6eyJwIjpudWxsLCJyIjoiVk4yIiwiYyI6ImFzMSIsInUiOjMxNDg1MzE4NTA5NzA0NjQsImxpZCI6IjBQbTVjYkxQNkxHbGh6emNrN2lKcHcifSwiaXNzIjoiaHR0cHM6Ly9hdXRoLnJpb3RnYW1lcy5jb20iLCJwbHQiOnsiZGV2IjoidW5rbm93biIsImlkIjoid2ViIn0sImV4cCI6MTcyNDU5MDc1OSwiaWF0IjoxNzI0NTg3MTU5LCJqdGkiOiJJVnUwNVZwczZSNCIsImNpZCI6ImRpcmVjdGJ1eS1wcm9kIn0.OzZJ5HRPccsFT5i1h_zqvnNKcHTcfux-AdWU7X6IOIXU9lw0WQGemrWC6nd5kuvEMpvyBR1fX2TBaT12NhNUAgyVz-IDXZWA9PNIwHJpHFsL-M8AH6T0E4cKwQpB7ULC_Vt35Y43cI7WYY61mP2vj4V1i4MPhtdFSfds1FsOJSRSr7mep2YRzPjSvkNfAf_5yORNRdakCRXbtf9uneCWcHBkZUAjizgLkov2N9erRcvJK1tTFvWq5GixYzOr6HE5cKHUeulrIcsJDEktemOdQwVz-EA-TWQHsCh26r85us7n-u_AKEFsZ9IFockJxd_glihx-g1AhLvmw_cDW_4qTQ"


def request(code):
    url = "https://usw2-red.pp.sgp.pvp.net/contentcodes/v1/claim"

    payload = json.dumps({
    "code": code,
    "locale": "en_US"
    })
    headers = {
        'accept': 'application/json, text/plain, */*',
        'authorization': f'Bearer {authToken}',
        'content-type': 'application/json',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36 Edg/127.0.0.0'
    }

    response = requests.request("POST", url, headers=headers, data=payload)

    print(response.text)


def capture_and_extract_text():
    # Get the screen size using PIL
    #screen_width, screen_height = ImageGrab.grab().size

    # Coordinates for the region to capture
    #x1, y1, x2, y2 = 0, 0, screen_width, screen_height # screen_width, screen_height

    # Capture the specific region of the screen using ImageGrab
    #screenshot = ImageGrab.grab(bbox=(x1, y1, x2, y2))
    screenshot = ImageGrab.grab()
    # Show the captured image for debugging purposes (optional)
    #screenshot.show()

    # Convert the image to grayscale
    grayscale_screenshot = ImageOps.grayscale(screenshot)
    
    # Convert the grayscale screenshot to a numpy array (format suitable for PaddleOCR)
    screenshot_np = np.array(grayscale_screenshot)

    # Initialize the PaddleOCR model (set language model directory if needed)
    ocr = PaddleOCR(use_angle_cls=False, lang='en', use_gpu=False, enable_mkldnn=True)  # you can specify 'ch', 'en', or other languages 

    # Perform OCR on the captured region
    result = ocr.ocr(screenshot_np)

    # Extract and print the text from the OCR result
    extracted_text = ''.join([line[1][0] for line in result[0]])

    #print(f"Extracted Text: {extracted_text}")

    return extracted_text


def filter_codes(text):

    # Adjust the regex pattern to capture full strings, limited to 21 characters
    matches = re.findall(r'CC-[A-Za-z0-9-]{0,17}', text)

    # Print the matches
    return matches


def validate_request(code):
    url = "https://usw2-red.pp.sgp.pvp.net/contentcodes/v1/validate"

    payload = json.dumps({
    "code": code,
    "locale": "en_US"
    })
    headers = {
        'accept': 'application/json, text/plain, */*',
        'authorization': f'Bearer {authToken}',
        'content-type': 'application/json',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36 Edg/127.0.0.0'
    }

    response = requests.request("POST", url, headers=headers, data=payload)

    print(response.text)


# Function to send requests in parallel
def send_requests_parallel(codes):
    with ThreadPoolExecutor(max_workers=4) as executor:
        # Submit all the requests to the thread pool
        future_to_code = {executor.submit(request, code): code for code in codes}

        # Process results as they complete
        for future in as_completed(future_to_code):
            code = future_to_code[future]
            try:
                future.result()  # Get the result of the request
            except Exception as exc:
                print(f"Code {code} generated an exception: {exc}")


def send_validate_requests_parallel(codes):
    with ThreadPoolExecutor(max_workers=4) as executor:
        # Submit all the requests to the thread pool
        future_to_code = {executor.submit(validate_request, code): code for code in codes}

        # Process results as they complete
        for future in as_completed(future_to_code):
            code = future_to_code[future]
            try:
                future.result()  # Get the result of the request
            except Exception as exc:
                print(f"Code {code} generated an exception: {exc}")


def on_key_press():
    start_time = time.time()
    extracted_text = capture_and_extract_text()
    codes_list = filter_codes(extracted_text)
    # Call the function to send requests in parallel
    send_validate_requests_parallel(codes_list)
    send_requests_parallel(codes_list)

    print("--- %s seconds ---" % (time.time() - start_time))
    

# Listen for the Alt+C key combination
keyboard.add_hotkey('alt+c', on_key_press)

# Keep the program running
print("Listening for Alt+C...")

keyboard.wait('esc')  # Press 'esc' to exit the program



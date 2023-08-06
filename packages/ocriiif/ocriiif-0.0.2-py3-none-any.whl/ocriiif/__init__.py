import pytesseract
from pytesseract.pytesseract import TesseractNotFoundError, TesseractError
import os
from PIL import Image
import requests
import io


def url_to_image(image_url):
    if image_url:
        r = requests.get(image_url)
        if r.status_code == requests.codes.ok:
            image_bytes = io.BytesIO(r.content)
            image_obect = Image.open(image_bytes)
            return image_obect, {"status": "success", "reason": None}
        return None, {"status": "failure", "reason": r.status_code}
    return None, {"status": "failure", "reason": "No URL provided for image"}


def filepath_to_image(img_path):
    if img_path:
        if os.path.isfile(img_path):
            with open(img_path, "rb") as image_file:
                image_object = Image.open(image_file)
                image_object.load()
            return image_object
    return


def image_to_data(img, data_format="hocr", tesseract_binary=None):
    if tesseract_binary:
        binary_path = os.path.abspath(tesseract_binary)
        pytesseract.pytesseract.tesseract_cmd = binary_path
    if img:
        try:
            return pytesseract.image_to_pdf_or_hocr(image=img, extension=data_format), {
                "status": "success",
                "reason": None,
            }
        except TesseractNotFoundError or TesseractError as e:
            return None, {"status": "failure", "reason": e}
    return


if __name__ == "__main__":
    image_path = "/Users/matt.mcgrattan/Documents/Github/ocriiif/tests/images/yv1ZE.png"
    foo, bar = image_to_data(
        img=filepath_to_image(img_path=image_path), tesseract_binary="/usr/local/bin/tesseract"
    )
    u = "https://i.stack.imgur.com/yv1ZE.png"
    image_object, image_status = url_to_image(u)
    foo2, bar2 = image_to_data(img=url_to_image(u)[0])


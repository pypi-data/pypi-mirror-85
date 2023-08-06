import pytesseract
from pytesseract.pytesseract import TesseractNotFoundError, TesseractError
import os
from PIL import Image
import requests
import io


def parse_info_json(info_json, request_width=None, request_height=None, info_json_uri=None):
    if info_json:
        info_height = info_json.get("height")
        info_width = info_json.get("width")
        if not info_json_uri:
            info_json_uri = info_json.get("@id")
        if not info_json_uri:
            return None, None, None
        image_url = info_json_uri + "/full/"
        size = None
        if request_width:
            size = f"{request_width},"
        if request_height:
            if size:
                size += f"{request_height}"
            else:
                size = f",{request_height}"
        if size:
            image_url += f"{size}"
        else:
            image_url += "full"
        image_url += "/0/default.jpg"
        return image_url, info_width, info_height
    return None, None, None


def iiif_canvas_to_image(canvas_json, return_url=True, request_width=None, request_height=None):
    if canvas_json:
        if canvas_json:
            if (image_resources := canvas_json.get("images")) is not None:
                if (image_resource := image_resources[0].get("resource")) is not None:
                    if (service := image_resource.get("service")) is not None:
                        info_json_uri = service["@id"]
                        r = requests.get(info_json_uri)
                        if r.status_code == requests.codes.ok:
                            info_json = r.json()
                            image_url, info_width, info_height = parse_info_json(
                                info_json=info_json,
                                info_json_uri=info_json_uri,
                                request_width=request_width,
                                request_height=request_height,
                            )
                            if return_url:
                                return (
                                    image_url,
                                    info_width,
                                    info_height,
                                    {"status": "success", "reason": r.status_code},
                                )
                            else:
                                iiif_image_obj, iiif_image_status = url_to_image(image_url)
                                return (
                                    iiif_image_obj,
                                    info_width,
                                    info_height,
                                    {"status": "success", "reason": iiif_image_status},
                                )
                        else:
                            return None, None, None, {"status": "failure", "reason": r.status_code}
    return None, None, None, {"status": "failure", "reason": "No canvas JSON was provided"}


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
            if data_format in ["pdf", "hocr"]:
                return pytesseract.image_to_pdf_or_hocr(image=img, extension=data_format), {
                    "status": "success",
                    "reason": None,
                }
            elif data_format == "alto":
                return pytesseract.image_to_alto_xml(image=img), {
                    "status": "success",
                    "reason": None,
                }
        except TesseractNotFoundError or TesseractError as e:
            return None, {"status": "failure", "reason": e}
    return


def canvas_to_data(canvas, width=None, height=None, format="hocr"):
    iiif_image_url, info_width, info_height, info_status = iiif_canvas_to_image(canvas_json=canvas, request_height=height,
                                                                                request_width=width)
    if iiif_image_url:
        iiif_image_object, iiif_image_status = url_to_image(iiif_image_url)
        if iiif_image_object:
            iiif_data, iiif_data_status = image_to_data(img=iiif_image_object,
                                                        data_format=format)
            return iiif_data, iiif_data_status
        else:
            return None, iiif_image_status
    else:
        return None, info_status


if __name__ == "__main__":
    image_path = "/Users/matt.mcgrattan/Documents/Github/ocriiif/tests/images/yv1ZE.png"
    foo, bar = image_to_data(
        img=filepath_to_image(img_path=image_path), tesseract_binary="/usr/local/bin/tesseract"
    )
    u = "https://i.stack.imgur.com/yv1ZE.png"
    image_object, image_status = url_to_image(u)
    c = {
        "@id": "https://wellcomelibrary.org/iiif/b18031900-18/canvas/c0",
        "@type": "sc:Canvas",
        "label": " - ",
        "thumbnail": {
            "@id": "https://dlcs.io/thumbs/wellcome/5/b18031900_vol_5_part_3_0001.JP2/full/81,100/0/default.jpg",
            "@type": "dctypes:Image",
            "service": {
                "@context": "http://iiif.io/api/image/2/context.json",
                "@id": "https://dlcs.io/thumbs/wellcome/5/b18031900_vol_5_part_3_0001.JP2",
                "protocol": "http://iiif.io/api/image",
                "height": 1024,
                "width": 830,
                "sizes": [
                    {"width": 81, "height": 100},
                    {"width": 162, "height": 200},
                    {"width": 324, "height": 400},
                    {"width": 830, "height": 1024},
                ],
                "profile": ["http://iiif.io/api/image/2/level0.json"],
            },
        },
        "seeAlso": {
            "@id": "https://wellcomelibrary.org/service/alto/b18031900/18?image=0",
            "format": "text/xml",
            "profile": "http://www.loc.gov/standards/alto/v3/alto.xsd",
            "label": "METS-ALTO XML",
        },
        "height": 3318,
        "width": 2688,
        "images": [
            {
                "@id": "https://wellcomelibrary.org/iiif/b18031900-18/imageanno/b18031900_vol_5_part_3_0001.JP2",
                "@type": "oa:Annotation",
                "motivation": "sc:painting",
                "resource": {
                    "@id": "https://dlcs.io/iiif-img/wellcome/5/b18031900_vol_5_part_3_0001.JP2/full/!1024,1024/0/default.jpg",
                    "@type": "dctypes:Image",
                    "format": "image/jpeg",
                    "height": 1024,
                    "width": 830,
                    "service": {
                        "@context": "http://iiif.io/api/image/2/context.json",
                        "@id": "https://dlcs.io/iiif-img/wellcome/5/b18031900_vol_5_part_3_0001.JP2",
                        "profile": "http://iiif.io/api/image/2/level1.json",
                    },
                },
                "on": "https://wellcomelibrary.org/iiif/b18031900-18/canvas/c0",
            }
        ],
        "otherContent": [
            {
                "@id": "https://wellcomelibrary.org/iiif/b18031900-18/contentAsText/0",
                "@type": "sc:AnnotationList",
                "label": "Text of this page",
            }
        ],
    }
    # foo2, bar2 = image_to_data(img=url_to_image(u)[0])
    manifest = requests.get("https://wellcomelibrary.org/iiif/b18031900-18/manifest").json()
    canvas_j = manifest["sequences"][0]["canvases"][3]
    hocr, status = canvas_to_data(canvas=canvas_j, height=1800, format="hocr")
    print(hocr)
    # url, width, height, status = iiif_canvas_to_image(canvas_json=c, request_height=1800)
    # if url:
    #     image_object, image_status = url_to_image(url)
    #     if image_object:
    #         hocr, _ = image_to_data(img=image_object)
    #         print(hocr)


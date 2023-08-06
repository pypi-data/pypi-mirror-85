import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFont

def cv2pil(img_cv) -> Image:
    img_cv_rgb = img_cv[:, :, ::-1] # RGB
    img_pil = Image.fromarray(img_cv_rgb)
    return img_pil

def pil2cv(img_pil) -> np.ndarray:
    img_cv_rgb = np.array(img_pil, dtype=np.uint8)
    img_cv = np.array(img_cv_rgb[:, :, ::-1])
    return img_cv

def cvPutText(
    img: np.ndarray,
    text: str,
    org,
    fontFace='ipag.ttf',
    fontScale=20,
    color=(255, 0, 255),
    # thickness=1,
    # lineType=cv2.LINE_AA
):
    img = cv2pil(img)
    draw = ImageDraw.Draw(img)
    font = ImageFont.truetype(font=fontFace, size=fontScale)

    x, y = org
    b, g, r = color

    draw.text(
        xy=(x, y),
        text=text,
        fill=(r, g, b),
        font=font,
    )

    img = pil2cv(img)
    return img

import numpy as np # type: ignore
import aoirint_cv2videotools as cv2tools

def test_put_text():
    img = np.full(shape=(224, 224, 3), fill_value=255, dtype=np.uint8)
    text = 'あああ'

    cv2tools.util.cvPutText(img=img, text=text, org=(100, 100))

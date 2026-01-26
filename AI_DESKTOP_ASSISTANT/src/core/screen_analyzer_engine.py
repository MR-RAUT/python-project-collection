# ==========================================================
# SCREEN ANALYZER ENGINE (BUTTON-CLICK MODE)
# ==========================================================

# import pytesseract
from PIL import Image
import mss
import numpy as np

import pytesseract

pytesseract.pytesseract.tesseract_cmd = (
    r"C:\Program Files\Tesseract-OCR\tesseract.exe"
)



class ScreenAnalyzerEngine:
    def capture_text(self) -> str:
        """
        Capture screen ONCE and extract text using OCR
        """
        with mss.mss() as sct:
            monitor = sct.monitors[1]  # primary screen
            screenshot = sct.grab(monitor)
            img = Image.frombytes(
                "RGB",
                screenshot.size,
                screenshot.rgb
            )

        text = pytesseract.image_to_string(img)
        return text.strip()

    def build_prompt(self, extracted_text: str) -> str:
        return (
            "Analyze the following screen text.\n\n"
            "If it is a coding question, solve it.\n"
            "If it is MCQ, select correct option.\n"
            "If it is theory, answer concisely.\n\n"
            f"SCREEN TEXT:\n{extracted_text}"
        )

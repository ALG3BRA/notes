from abc import ABC, abstractmethod
from config import YANDEX_SPELLER_URL as URL
import requests


class AbstractTextCorrectorRepository(ABC):
    @staticmethod
    @abstractmethod
    async def correct_text(text: str) -> str:
        pass


class TextCorrectorRepo(AbstractTextCorrectorRepository):
    @staticmethod
    async def _get_spelling_suggestions(text: str) -> list:
        params = {"text": text, "lang": "ru,en", "options": 6}
        response = requests.get(URL, params=params)
        return response.json()

    @staticmethod
    async def correct_text(text: str) -> str:
        corrections = await TextCorrectorRepo._get_spelling_suggestions(text)
        corrected_text = list(text)

        for correction in sorted(corrections, key=lambda x: x["pos"], reverse=True):
            start_pos = correction["pos"]
            end_pos = start_pos + correction["len"]
            suggestion = correction["s"][0]
            corrected_text[start_pos:end_pos] = suggestion

        return "".join(corrected_text)

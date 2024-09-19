from repositories.yandex_speller_repo import AbstractTextCorrectorRepository, TextCorrectorRepo


class TextCorrectorService:
    _repo: AbstractTextCorrectorRepository = TextCorrectorRepo()

    @classmethod
    async def correct(cls, text: str) -> str:
        return await cls._repo.correct_text(text)

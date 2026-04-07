from pathlib import Path


class HighScoreStore:
    def __init__(self, file_path: str | None = None):
        default_path = Path(__file__).resolve().with_name("data.txt")
        self.file_path = Path(file_path) if file_path else default_path

    def load(self) -> int:
        try:
            value = self.file_path.read_text(encoding="utf-8").strip()
            score = int(value)
            if score < 0:
                raise ValueError("negative score")
            return score
        except (FileNotFoundError, ValueError, OSError):
            self.save(0)
            return 0

    def save(self, score: int) -> None:
        safe_score = max(0, int(score))
        self.file_path.write_text(str(safe_score), encoding="utf-8")

from questions import QUESTIONS


class Quiz:
    def __init__(self) -> None:
        self.questions = QUESTIONS
        self.question_idx = 0
        self.text: str | None = None
        self.options: list[str] | None = None
        self.answer: str | None = None
        self.image: str | None = None
        self.correct_answers = 0
        self.incorrect_answers = 0
        self.total_time = 0.0
        self.load_question()

    def load_question(self) -> None:
        question = self.questions[self.question_idx]
        self.text = question["text"]
        self.options = question["options"]
        self.answer = question["answer"]
        self.image = question["image"]

    def next_question(self) -> bool:
        if self.question_idx + 1 >= len(self.questions):
            return False
        self.question_idx += 1
        self.load_question()
        return True


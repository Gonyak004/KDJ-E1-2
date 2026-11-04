"""개별 객관식 문제와 JSON 변환."""


class Quiz:
    def __init__(self, question, choices, answer, explanation=""):
        if not isinstance(question, str) or not question.strip():
            raise ValueError("문제는 비어 있지 않은 문자열이어야 합니다.")
        if (not isinstance(choices, list) or len(choices) != 4
                or any(not isinstance(c, str) or not c.strip() for c in choices)):
            raise ValueError("선택지는 비어 있지 않은 문자열 4개여야 합니다.")
        if type(answer) is not int or not 1 <= answer <= 4:
            raise ValueError("정답은 1~4 정수여야 합니다.")
        self.question = question.strip()
        self.choices = [c.strip() for c in choices]
        self.answer = answer
        if not isinstance(explanation, str):
            raise ValueError("해설은 문자열이어야 합니다.")
        self.explanation = explanation.strip()

    def display(self):
        print(self.question)
        for number, choice in enumerate(self.choices, 1):
            print(f"  [{number}] {choice}")

    def check_answer(self, answer):
        return self.answer == answer

    def to_dict(self):
        return dict(question=self.question, choices=self.choices, answer=self.answer,
                    explanation=self.explanation)

    @classmethod
    def from_dict(cls, data):
        if not isinstance(data, dict):
            raise ValueError("문제 데이터는 객체여야 합니다.")
        return cls(data["question"], data["choices"], data["answer"], data.get("explanation", ""))

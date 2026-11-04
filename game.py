"""퀴즈 게임의 메뉴와 실행 흐름."""

from inputs import read_number, read_text
from defaults import default_quizzes
from quiz import Quiz


class QuizGame:
    def __init__(self):
        self.quizzes = default_quizzes()
        self.best_score = 0
        self.games_played = 0

    def show_menu(self):
        print("\n=== Python 기초 퀴즈 ===")
        print("1. 퀴즈 풀기  2. 퀴즈 추가  3. 퀴즈 목록  4. 점수 확인  5. 종료")

    def play(self):
        if not self.quizzes:
            print("등록된 퀴즈가 없습니다. 먼저 퀴즈를 추가해주세요.")
            return
        score = 0
        for index, quiz in enumerate(self.quizzes, 1):
            print(f"\n[{index}/{len(self.quizzes)}]")
            quiz.display()
            answer = read_number("정답 번호 > ", 1, 4)
            if quiz.check_answer(answer):
                score += 1
                print("정답입니다!")
            else:
                print(f"오답입니다. 정답: {quiz.answer}. {quiz.choices[quiz.answer - 1]}")
        print(f"\n결과: {len(self.quizzes)}문제 중 {score}문제 정답")
        self.record_score(score)

    def record_score(self, score):
        self.games_played += 1
        self.best_score = max(self.best_score, score)

    def add_quiz(self):
        print("\n=== 퀴즈 추가 ===")
        question = read_text("문제 > ")
        choices = [read_text(f"선택지 {i} > ") for i in range(1, 5)]
        answer = read_number("정답 번호 > ", 1, 4)
        self.quizzes.append(Quiz(question, choices, answer))
        self.save()
        print("퀴즈가 등록되었습니다.")

    def save(self):
        pass

    def list_quizzes(self):
        print(f"\n=== 퀴즈 목록 ({len(self.quizzes)}개) ===")
        if not self.quizzes:
            print("등록된 퀴즈가 없습니다.")
        for index, quiz in enumerate(self.quizzes, 1):
            print(f"\n[{index}]")
            quiz.display()

    def run(self):
        try:
            while True:
                self.show_menu()
                choice = read_number("메뉴 선택 > ", 1, 5)
                if choice == 5:
                    break
                if choice == 1:
                    self.play()
                elif choice == 2:
                    self.add_quiz()
                elif choice == 3:
                    self.list_quizzes()
                else:
                    print("기능 준비 중입니다.")
        except (KeyboardInterrupt, EOFError):
            print("\n입력이 중단되었습니다. 안전하게 종료합니다.")
        print("게임을 종료합니다.")

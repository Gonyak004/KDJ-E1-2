"""퀴즈 게임의 메뉴와 실행 흐름."""

from inputs import read_number, read_text
from quiz import Quiz
from storage import StateStore


class QuizGame:
    def __init__(self, state_path=None):
        self.store = StateStore() if state_path is None else StateStore(state_path)
        self.quizzes, self.best_score, self.games_played = self.store.load()

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
        if score > self.best_score:
            print("최고 점수를 갱신했습니다!")
        self.best_score = max(self.best_score, score)
        self.save()

    def show_score(self):
        print("\n=== 점수 확인 ===")
        if self.games_played == 0:
            print("아직 퀴즈를 풀지 않았습니다.")
        else:
            print(f"최고 점수: {self.best_score}문제 정답 / 완료한 게임: {self.games_played}회")

    def add_quiz(self):
        print("\n=== 퀴즈 추가 ===")
        question = read_text("문제 > ")
        choices = [read_text(f"선택지 {i} > ") for i in range(1, 5)]
        answer = read_number("정답 번호 > ", 1, 4)
        self.quizzes.append(Quiz(question, choices, answer))
        if self.save():
            print("퀴즈가 등록되고 파일에 저장되었습니다.")
        else:
            print("퀴즈가 등록되었지만 파일 저장은 실패했습니다.")

    def save(self):
        return self.store.save(self.quizzes, self.best_score, self.games_played)

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
                elif choice == 4:
                    self.show_score()
        except (KeyboardInterrupt, EOFError):
            print("\n입력이 중단되었습니다. 안전하게 종료합니다.")
        finally:
            self.save()
        print("게임을 종료합니다.")

"""퀴즈 게임의 메뉴와 실행 흐름."""

from inputs import read_number
from defaults import default_quizzes


class QuizGame:
    def __init__(self):
        self.quizzes = default_quizzes()
        self.best_score = 0
        self.games_played = 0

    def show_menu(self):
        print("\n=== Python 기초 퀴즈 ===")
        print("1. 퀴즈 풀기  2. 퀴즈 추가  3. 퀴즈 목록  4. 점수 확인  5. 종료")

    def run(self):
        try:
            while True:
                self.show_menu()
                choice = read_number("메뉴 선택 > ", 1, 5)
                if choice == 5:
                    break
                print("기능 준비 중입니다.")
        except (KeyboardInterrupt, EOFError):
            print("\n입력이 중단되었습니다. 안전하게 종료합니다.")
        print("게임을 종료합니다.")

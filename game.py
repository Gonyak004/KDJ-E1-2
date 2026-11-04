"""퀴즈 게임의 메뉴와 실행 흐름."""

from inputs import read_number, read_text
from quiz import Quiz
from storage import StateStore
from ui import Console


class QuizGame:
    def __init__(self, state_path=None):
        self.store = StateStore() if state_path is None else StateStore(state_path)
        self.quizzes, self.best_score, self.games_played = self.store.load()
        self.console = Console()

    def show_menu(self):
        self.console.card("H I S T O R Y   Q U E S T  /  세계사 타임투어", [
            "피라미드에서 혁명의 거리까지, 한 문제씩 시간 여행.",
            f"대기 중인 퀴즈 {len(self.quizzes)}개   /   최고 기록 {self.best_score}개 정답",
            "",
            "[1] 여행 시작      세계사를 따라가는 퀴즈 여정",
            "[2] 문제 만들기    나만의 역사 문제를 등록",
            "[3] 여행 지도      어떤 시대가 기다릴까?",
            "[4] 나의 기록      최고 점수와 도전 횟수",
            "[5] 여행 마치기    다음 시간 여행을 기약하며",
        ])
        print("  번호를 고르고 Enter를 눌러주세요.")

    def play(self):
        if not self.quizzes:
            print("등록된 퀴즈가 없습니다. 먼저 퀴즈를 추가해주세요.")
            return
        score = 0
        streak = 0
        best_streak = 0
        self.console.card("READY?  /  시간 여행 출발", [
            f"총 {len(self.quizzes)}문제 / 정답 하나에 1점",
            "보기 1~4 중 하나를 고르세요. 해설로 시대의 맥락도 확인!",
        ], "95")
        for index, quiz in enumerate(self.quizzes, 1):
            self.console.card(f"ROUND {index:02}  /  {self.console.progress(index, len(self.quizzes))}", [
                f"현재 {score}점   |   연속 정답 {streak}개", "", quiz.question, "",
                *[f"[{i}] {choice}" for i, choice in enumerate(quiz.choices, 1)],
            ])
            answer = read_number("  나의 선택 > ", 1, 4)
            if quiz.check_answer(answer):
                score += 1
                streak += 1
                best_streak = max(best_streak, streak)
                print(self.console.tint("  정답입니다! 역사의 한 장면을 찾았습니다.", "92"))
                if streak >= 2:
                    print(f"  COMBO x{streak}  /  시간 여행이 순조롭습니다!")
            else:
                streak = 0
                print(self.console.tint(f"  오답입니다. 정답: [{quiz.answer}] {quiz.choices[quiz.answer - 1]}", "93"))
                print("  잠깐 다른 시대로 갔네요. 해설을 읽고 다시 출발해요!")
            if quiz.explanation:
                print(f"  해설 > {quiz.explanation}")
        percentage = round(score / len(self.quizzes) * 100)
        if percentage == 100:
            rank, comment = "역사의 길잡이", "완벽한 여정! 모든 시대의 단서를 찾아냈습니다."
        elif percentage >= 70:
            rank, comment = "베테랑 탐험가", "역사의 흐름이 보이네요. 다음 여행은 만점에 도전!"
        elif percentage >= 40:
            rank, comment = "호기심 많은 여행자", "지도가 조금씩 채워지고 있어요. 한 번 더 떠나볼까요?"
        else:
            rank, comment = "첫 시간 여행자", "첫걸음이 가장 중요하죠. 오늘의 해설이 다음 여행의 힌트!"
        self.console.card("TRAVEL REPORT  /  시간 여행 성적표", [
            f"결과: {len(self.quizzes)}문제 중 {score}문제 정답",
            f"정답률 {percentage}%   /   최다 연속 정답 {best_streak}개",
            "", f"나의 등급: {rank}", comment,
        ], "95")
        self.record_score(score)

    def record_score(self, score):
        self.games_played += 1
        if score > self.best_score:
            print(self.console.tint("  NEW RECORD! 최고 점수를 갱신했습니다!", "93"))
        self.best_score = max(self.best_score, score)
        self.save()

    def show_score(self):
        if self.games_played == 0:
            lines = ["아직 퀴즈를 풀지 않았습니다.", "첫 도전의 주인공이 되어주세요. 메뉴 [1]에서 시작!"]
        else:
            lines = [f"최고 점수: {self.best_score}문제 정답",
                     f"완료한 게임: {self.games_played}회", "", "기록은 정답 개수 기준입니다. 다음 도전에서 갱신해봐요!"]
        self.console.card("MY RECORD  /  나의 기록", lines, "93")

    def add_quiz(self):
        self.console.card("QUIZ STUDIO  /  나도 출제자", [
            "역사 문제 하나, 보기 네 개, 정답 번호를 입력하세요.",
            "모든 입력을 마치면 바로 저장됩니다.",
        ], "95")
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
        self.console.card(f"QUIZ COLLECTION  /  퀴즈 목록 ({len(self.quizzes)}개)", [
            "정답은 도전하기에서 공개! 마음에 드는 문제를 찾아보세요.",
        ])
        if not self.quizzes:
            print("등록된 퀴즈가 없습니다.")
        for index, quiz in enumerate(self.quizzes, 1):
            self.console.card(f"NO. {index:02}", [quiz.question,
                *[f"[{i}] {choice}" for i, choice in enumerate(quiz.choices, 1)]])

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
        self.console.card("SEE YOU!  /  이번 여행은 여기까지", ["게임을 종료합니다. 다음에는 또 다른 시대에서 만나요!"])

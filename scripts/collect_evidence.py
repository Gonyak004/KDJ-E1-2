"""실제 프로그램을 입력 시나리오로 실행하여 제출용 원문 로그를 수집한다."""

import contextlib
import io
from pathlib import Path
import subprocess
import sys
import tempfile
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from game import QuizGame

LOGS = ROOT / "artifacts" / "logs"
LOGS.mkdir(parents=True, exist_ok=True)


def session(name, state, answers):
    stream = io.StringIO()
    responses = iter(answers)

    def entered(prompt):
        answer = next(responses)
        print(prompt + answer)
        return answer

    with contextlib.redirect_stdout(stream), patch("builtins.input", side_effect=entered):
        print("$ py main.py  [각 세션은 같은 임시 state.json을 사용하는 실제 게임 실행]")
        QuizGame(state).run()
    (LOGS / f"{name}.txt").write_text(stream.getvalue(), encoding="utf-8")


def command_log(name, commands):
    lines = []
    for command in commands:
        result = subprocess.run(command, cwd=ROOT, capture_output=True, encoding="utf-8", errors="replace")
        lines.extend(["$ " + " ".join(command), result.stdout, result.stderr])
        if result.returncode:
            raise RuntimeError(f"명령 실패: {command}")
    (LOGS / f"{name}.txt").write_text("\n".join(lines), encoding="utf-8")


def main():
    with tempfile.TemporaryDirectory() as directory:
        state = Path(directory) / "state.json"
        session("01-menu-validation", state, ["", "abc", "9", " 4 ", "5"])
        session("02-add-quiz", state, ["2", "Python에서 화면에 값을 출력하는 함수는?",
                "print()", "input()", "len()", "int()", "0", " 1 ", "5"])
        session("03-list-restart", state, ["3", "5"])
        session("04-play", state, ["1", "2", "3", "1", "4", "2", "3", "1", "2", "5"])
        session("05-score-restart", state, ["4", "5"])
        (LOGS / "sample-state.json").write_bytes(state.read_bytes())
    command_log("06-environment", [[sys.executable, "--version"], ["git", "--version"],
                ["git", "config", "--local", "user.name"],
                ["git", "config", "--local", "user.email"], ["git", "remote", "-v"]])
    command_log("07-tests", [[sys.executable, "-m", "unittest", "discover", "-s", "tests", "-v"]])
    command_log("08-git-graph", [["git", "log", "--oneline", "--graph", "--exclude=refs/original/*", "--all"]])
    print(f"실행 원문 로그 저장: {LOGS}")


if __name__ == "__main__":
    main()

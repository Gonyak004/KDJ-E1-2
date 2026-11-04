"""UTF-8 JSON 읽기 및 원자적 저장. 손상된 원본은 별도 보존한다."""

import json
import shutil
from datetime import datetime
from pathlib import Path

from defaults import default_quizzes, legacy_default_quizzes, party_default_quizzes
from quiz import Quiz

STATE_PATH = Path(__file__).resolve().parent / "state.json"


class StateStore:
    def __init__(self, path=STATE_PATH):
        self.path = Path(path)

    def load(self):
        try:
            data = json.loads(self.path.read_text(encoding="utf-8"))
            if not isinstance(data, dict) or not isinstance(data["quizzes"], list):
                raise ValueError("잘못된 데이터 구조")
            quizzes = [Quiz.from_dict(item) for item in data["quizzes"]]
            best = data["best_score"]
            played = data["games_played"]
            if (type(best) is not int or type(played) is not int
                    or best < 0 or played < 0 or best > len(quizzes)
                    or (played == 0 and best != 0)):
                raise ValueError("잘못된 점수 데이터")
            previous_sets = [legacy_default_quizzes(), party_default_quizzes()]
            legacy = next((items for items in previous_sets
                           if [q.to_dict() for q in quizzes[:len(items)]] == [q.to_dict() for q in items]), None)
            if legacy is not None:
                backup = self.path.with_name(f"state.before-theme-{datetime.now():%Y%m%d-%H%M%S-%f}.json")
                try:
                    shutil.copy2(self.path, backup)
                except OSError as error:
                    print(f"이전 기록을 백업하지 못해 기존 문제를 유지합니다: {error}")
                else:
                    print("세계사 타임투어로 새 단장! 직접 추가한 문제는 그대로 유지합니다.")
                    print(f"이전 문제와 점수 백업: {backup.name}")
                    print("새 테마의 최고 점수는 0부터 시작합니다.")
                    return default_quizzes() + quizzes[len(legacy):], 0, 0
            return quizzes, best, played
        except FileNotFoundError:
            print("저장 파일이 없어 기본 퀴즈로 시작합니다.")
        except (ValueError, KeyError, TypeError, UnicodeError):
            print("저장 파일이 손상되었습니다. 기본 퀴즈로 복구합니다.")
            self.backup_corrupt()
        except OSError as error:
            print(f"저장 파일을 읽을 수 없습니다. 기본 퀴즈로 시작합니다: {error}")
        return default_quizzes(), 0, 0

    def backup_corrupt(self):
        backup = self.path.with_name(f"state.corrupt-{datetime.now():%Y%m%d-%H%M%S-%f}.json")
        try:
            self.path.replace(backup)
            print(f"손상된 원본 보관: {backup.name}")
        except OSError as error:
            print(f"손상 파일을 보관하지 못했습니다: {error}")

    def save(self, quizzes, best_score, games_played):
        temporary = self.path.with_name(self.path.name + ".tmp")
        data = {"quizzes": [q.to_dict() for q in quizzes],
                "best_score": best_score, "games_played": games_played}
        try:
            temporary.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
            temporary.replace(self.path)
            return True
        except OSError as error:
            print(f"저장 실패: {error}\n현재 내용은 메모리에 유지됩니다. 종료 시 다시 저장합니다.")
            return False

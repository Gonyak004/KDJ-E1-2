import contextlib
import io
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

from game import QuizGame
from inputs import read_number
from quiz import Quiz
from storage import StateStore
from defaults import default_quizzes, legacy_default_quizzes, party_default_quizzes
from ui import Console, text_width


class GameTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.path = Path(self.temp.name) / "state.json"
        self.output = io.StringIO()
        self.redirect = contextlib.redirect_stdout(self.output)
        self.redirect.__enter__()
        self.addCleanup(self.redirect.__exit__, None, None, None)

    def game(self):
        return QuizGame(self.path)

    def test_default_questions(self):
        game = self.game()
        self.assertGreaterEqual(len(game.quizzes), 5)
        self.assertTrue(all(len(q.choices) == 4 for q in game.quizzes))

    def test_number_retries_and_trims(self):
        with patch("builtins.input", side_effect=["", "abc", "9", " 2 "]):
            self.assertEqual(read_number("> ", 1, 4), 2)
        for message in ["빈 입력", "숫자로", "1~4"]:
            self.assertIn(message, self.output.getvalue())

    def test_add_and_restart(self):
        game = self.game()
        with patch("builtins.input", side_effect=["", "새 문제", "A", "B", "C", "D", "0", " 3 "]):
            game.add_quiz()
        restored = self.game()
        self.assertEqual(len(restored.quizzes), 8)
        self.assertEqual(restored.quizzes[-1].question, "새 문제")
        self.assertEqual(restored.quizzes[-1].answer, 3)
        self.assertIn("새 문제", self.path.read_text(encoding="utf-8"))

    def test_score_persistence_and_lower_score(self):
        game = self.game()
        with patch("builtins.input", side_effect=[str(q.answer) for q in game.quizzes]):
            game.play()
        restored = self.game()
        self.assertEqual(restored.best_score, 7)
        restored.record_score(0)
        self.assertEqual(self.game().best_score, 7)
        self.assertEqual(self.game().games_played, 2)

    def test_wrong_answers(self):
        game = self.game()
        with patch("builtins.input", side_effect=[str(q.answer % 4 + 1) for q in game.quizzes]):
            game.play()
        self.assertEqual(game.best_score, 0)
        self.assertEqual(game.games_played, 1)
        self.assertIn("오답입니다", self.output.getvalue())

    def test_empty_quizzes(self):
        game = self.game()
        game.quizzes = []
        game.list_quizzes()
        game.play()
        game.save()
        self.assertEqual(self.game().quizzes, [])
        self.assertIn("등록된 퀴즈가 없습니다", self.output.getvalue())

    def test_score_before_playing(self):
        self.game().show_score()
        self.assertIn("아직 퀴즈를 풀지 않았습니다", self.output.getvalue())

    def test_interrupted_inputs_save(self):
        for exception in [EOFError, KeyboardInterrupt]:
            with self.subTest(exception=exception):
                game = self.game()
                with patch("builtins.input", side_effect=exception):
                    game.run()
                self.assertTrue(self.path.exists())

    def test_partial_registration_is_not_added(self):
        game = self.game()
        with patch("builtins.input", side_effect=["2", "미완성", KeyboardInterrupt]):
            game.run()
        self.assertEqual(len(self.game().quizzes), 7)

    def test_corrupt_and_invalid_state(self):
        invalid = ["{", "[]", '{"quizzes":[],"best_score":true,"games_played":0}',
                   '{"quizzes":[],"best_score":-1,"games_played":1}',
                   '{"quizzes":[{}],"best_score":0,"games_played":0}']
        for content in invalid:
            with self.subTest(content=content):
                self.path.write_text(content, encoding="utf-8")
                self.assertEqual(len(self.game().quizzes), 7)
        self.assertEqual(len(list(self.path.parent.glob("state.corrupt-*.json"))), len(invalid))

    def test_invalid_encoding(self):
        self.path.write_bytes(b"\xff\xfe")
        self.assertEqual(len(self.game().quizzes), 7)

    def test_read_and_write_errors(self):
        self.path.mkdir()
        game = self.game()
        self.assertFalse(game.save())
        self.assertIn("저장 실패", self.output.getvalue())

    def test_atomic_write_keeps_previous_data_on_failure(self):
        game = self.game()
        game.save()
        before = self.path.read_bytes()
        with patch.object(Path, "replace", side_effect=OSError("쓰기 거부")):
            self.assertFalse(game.save())
        self.assertEqual(self.path.read_bytes(), before)

    def test_quiz_validation(self):
        for answer in [True, 0, 5, "1"]:
            with self.assertRaises(ValueError):
                Quiz("문제", ["a", "b", "c", "d"], answer)
        with self.assertRaises(ValueError):
            Quiz("", ["a"] * 4, 1)

    def test_legacy_theme_migration_preserves_custom_quiz_and_backup(self):
        custom = Quiz("내가 만든 문제", ["a", "b", "c", "d"], 2)
        StateStore(self.path).save(legacy_default_quizzes() + [custom], 5, 3)
        original = self.path.read_bytes()
        game = self.game()
        self.assertEqual(game.quizzes[0].question, default_quizzes()[0].question)
        self.assertEqual(game.quizzes[-1].to_dict(), custom.to_dict())
        self.assertEqual((game.best_score, game.games_played), (0, 0))
        backups = list(self.path.parent.glob("state.before-theme-*.json"))
        self.assertEqual(len(backups), 1)
        self.assertEqual(backups[0].read_bytes(), original)
        game.save()
        self.game()
        self.assertEqual(len(list(self.path.parent.glob("state.before-theme-*.json"))), 1)

    def test_failed_migration_backup_keeps_previous_game(self):
        StateStore(self.path).save(legacy_default_quizzes(), 5, 3)
        with patch("storage.shutil.copy2", side_effect=OSError("쓰기 거부")):
            game = self.game()
        self.assertEqual(game.quizzes[0].question, legacy_default_quizzes()[0].question)
        self.assertEqual((game.best_score, game.games_played), (5, 3))

    def test_history_theme_keeps_existing_history_score(self):
        StateStore(self.path).save(default_quizzes(), 6, 2)
        game = self.game()
        self.assertEqual((game.best_score, game.games_played), (6, 2))
        self.assertTrue(all(q.explanation for q in game.quizzes))

    def test_party_quizzes_migrate_to_history(self):
        StateStore(self.path).save(party_default_quizzes(), 4, 2)
        game = self.game()
        self.assertEqual(game.quizzes[0].question, default_quizzes()[0].question)
        self.assertEqual((game.best_score, game.games_played), (0, 0))

    def test_card_wraps_long_korean_text(self):
        console = Console()
        console.color = False
        console.card("긴 문제", ["가나다라마바사" * 30, "한글과 English 함께"])
        lines = self.output.getvalue().strip().splitlines()
        self.assertTrue(all(text_width(line) == 64 for line in lines))

    def test_delete_persists_and_preserves_historical_score(self):
        game = self.game()
        game.record_score(7)
        removed = game.quizzes[0].question
        with patch("builtins.input", side_effect=["abc", "9", " 1 ", "0", "1"]):
            game.delete_quiz()
        restored = self.game()
        self.assertEqual(len(restored.quizzes), 6)
        self.assertNotIn(removed, [q.question for q in restored.quizzes])
        self.assertEqual(restored.best_score, 7)

    def test_delete_can_cancel_at_both_steps(self):
        game = self.game()
        for answers in [["0"], ["1", "2"]]:
            with patch("builtins.input", side_effect=answers):
                game.delete_quiz()
            self.assertEqual(len(game.quizzes), 7)

    def test_delete_last_question_and_empty_list(self):
        game = self.game()
        game.quizzes = game.quizzes[:1]
        game.record_score(1)
        with patch("builtins.input", side_effect=["6", "1", "1", "6", "5"]):
            game.run()
        restored = self.game()
        self.assertEqual(restored.quizzes, [])
        self.assertEqual(restored.best_score, 1)

    def test_interrupt_delete_confirmation_keeps_question(self):
        game = self.game()
        with patch("builtins.input", side_effect=["6", "1", KeyboardInterrupt]):
            game.run()
        self.assertEqual(len(self.game().quizzes), 7)


if __name__ == "__main__":
    unittest.main()

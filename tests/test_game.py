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
                   '{"quizzes":[],"best_score":1,"games_played":1}',
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


if __name__ == "__main__":
    unittest.main()

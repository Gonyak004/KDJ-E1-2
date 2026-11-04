"""첫 실행과 데이터 복구에 사용하는 Python 기초 문제."""

from quiz import Quiz


def default_quizzes():
    return [
        Quiz("Python에서 정수를 나타내는 자료형은?", ["str", "int", "list", "dict"], 2),
        Quiz("순서가 있는 여러 값을 저장하는 자료형은?", ["bool", "int", "list", "float"], 3),
        Quiz("조건에 따라 실행할 코드를 나누는 키워드는?", ["if", "import", "return", "class"], 1),
        Quiz("함수를 정의할 때 사용하는 키워드는?", ["for", "while", "try", "def"], 4),
        Quiz("클래스에서 인스턴스 자신을 가리키는 관례적인 이름은?", ["this", "self", "main", "super"], 2),
        Quiz("키와 값의 쌍을 저장하는 자료형은?", ["tuple", "str", "dict", "bool"], 3),
        Quiz("예외를 처리할 때 try와 함께 사용하는 키워드는?", ["except", "elsewhere", "catch", "error"], 1),
    ]

"""메뉴와 퀴즈 등록에서 공유하는 입력 검증."""


def read_text(prompt):
    while True:
        value = input(prompt).strip()
        if value:
            return value
        print("빈 입력은 사용할 수 없습니다. 다시 입력해주세요.")


def read_number(prompt, minimum, maximum):
    while True:
        value = read_text(prompt)
        try:
            number = int(value)
        except ValueError:
            print("숫자로 입력해주세요.")
            continue
        if minimum <= number <= maximum:
            return number
        print(f"{minimum}~{maximum} 사이의 번호를 입력해주세요.")

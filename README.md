# KDJ-E1-2

### 세계사 타임투어 — 한 문제씩 떠나는 시간 여행

Python 콘솔 퀴즈 게임 만들기: 클래스, 입력 처리, JSON 파일 저장 및 Git/GitHub 실습

목차

- [1. 프로젝트 소개](#1-프로젝트-소개)
- [2. 기술 스택 및 개발 환경](#2-기술-스택-및-개발-환경)
- [3. 실습 및 실행 방법](#3-실습-및-실행-방법)
- [4. 프로젝트 구조](#4-프로젝트-구조)
- [5. 트러블슈팅](#5-트러블슈팅)
- [6. 로그 및 증빙 자료](#6-로그-및-증빙-자료)
- [7. 실습 확인 결과](#7-실습-확인-결과)

---

### 1. 프로젝트 소개

> Python으로 터미널에서 동작하는 세계사 퀴즈 게임을 만드는 실습입니다. 문제를 풀고 직접 등록하거나 삭제할 수 있으며, 프로그램을 종료해도 문제와 최고 점수가 유지되도록 JSON 파일 저장 기능을 구현했습니다. 기능별 커밋, 브랜치 생성과 병합, 원격 저장소 복제 및 동기화 과정도 함께 기록했습니다.

#### 퀴즈 주제 선정 이유

세계사를 주제로 선정했습니다. 고대 이집트, 로마 제국, 실크로드, 마그나 카르타, 르네상스, 프랑스 혁명, 로제타석을 다루는 기본 문제 7개를 구성했습니다. 정답만 확인하는 데서 끝나지 않고, 짧은 해설로 사건과 문화의 배경도 같이 알아볼 수 있도록 만들었습니다.

화면은 시간 여행이라는 주제에 맞춰 카드형 메뉴, 진행 막대, 연속 정답 표시와 마지막 여행 성적표로 구성했습니다.

주요 실습 내용

- `Quiz`, `QuizGame`, `StateStore` 클래스로 문제·게임 진행·파일 저장 역할 분리
- 조건문과 반복문을 이용한 메뉴 및 객관식 문제 풀이
- 빈 입력, 숫자가 아닌 입력, 범위 밖 번호에 대한 재입력 처리
- UTF-8 JSON 저장과 재실행 후 데이터 유지 확인
- 손상 파일 복구, 읽기·쓰기 오류, Ctrl+C 및 EOF 처리
- Git 기능별 커밋, 브랜치 병합, GitHub push 및 clone/pull 실습
- 선택 기능인 문제 삭제와 삭제 확인·취소 구현

저장소: [Gonyak004/KDJ-E1-2](https://github.com/Gonyak004/KDJ-E1-2)

이 문서는 현재 코드, 실제 실행 로그 및 세계사 퀴즈로 갱신한 스크린샷을 기준으로 작성했습니다. 실행 화면 증빙은 실제 게임에 입력 시나리오를 자동 재현하고, 그 원문을 Windows 실행 기록 뷰어에 표시해 캡처한 자료입니다. 아래 명령어는 재현·확인용으로 참고 부탁드립니다.

---

### 2. 기술 스택 및 개발 환경

| 구분 | 사용 환경 및 역할 |
| --- | --- |
| 운영체제 | Windows |
| 터미널 | PowerShell |
| 개발 도구 | Visual Studio Code |
| 언어 | Python 3.10 이상 / 실행 확인 환경 Python 3.15.2 |
| 라이브러리 | Python 표준 라이브러리만 사용, 별도 설치 없음 |
| 데이터 저장 | 프로젝트 루트의 `state.json` / UTF-8 JSON |
| 버전 관리 | Git 2.56.0.windows.4 / GitHub |
| 테스트 | 표준 라이브러리 `unittest` / 23개 테스트 통과 |

Windows 작업 경로는 `C:\Users\User\OneDrive\Desktop\KDJ-E1-2`입니다. 다른 위치에 복제하셨다면 실제 프로젝트 폴더로 이동하시면 됩니다.

```powershell
py --version
git --version
git config --local user.name
git remote -v
```

Python 버전과 Git 설정의 실행 출력은 [개발 환경 로그](artifacts/logs/06-environment.txt)에 저장했습니다.

---

### 3. 실습 및 실행 방법

#### 저장소 복제 및 게임 실행

```powershell
git clone https://github.com/Gonyak004/KDJ-E1-2
cd KDJ-E1-2
py main.py
```

`py` 명령이 없는 환경에서는 Python 3.10 이상으로 연결된 `python main.py` 또는 `python3 main.py`를 사용합니다. 외부 라이브러리를 사용하지 않아 `pip install` 과정은 필요하지 않습니다.

처음 실행하면 기본 퀴즈 7개를 불러옵니다. 문제 등록·삭제, 게임 완료 및 종료 시 저장하며, 다음 실행부터 기존 저장 파일을 읽습니다.

#### 메뉴 및 기능 목록

| 번호 | 화면 이름 | 기능 |
| --- | --- | --- |
| 1 | 여행 시작 | 저장된 모든 문제를 순서대로 출제하고 정답·오답, 기본 문제 해설 및 결과 표시 |
| 2 | 문제 만들기 | 문제, 선택지 4개, 정답 번호 1~4 입력 후 저장 |
| 3 | 여행 지도 | 등록된 문제와 선택지 목록 확인. 실제 지도가 아닌 퀴즈 목록 기능 |
| 4 | 나의 기록 | 최고 정답 수와 완료한 게임 횟수 확인 |
| 5 | 여행 마치기 | 현재 데이터를 저장하고 종료 |
| 6 | 문제 삭제 | 문제 번호 선택 → 삭제 확인 → 파일 반영. 선택 단계에서 0, 확인 단계에서 2로 취소 |

문제마다 정답을 맞히면 1점이며, 연속 정답 횟수도 화면에 표시합니다. 모든 문제를 풀면 정답률, 최다 연속 정답과 결과 등급을 확인할 수 있습니다. 등급은 정답률 기준으로 100% ‘역사의 길잡이’, 70% 이상 ‘베테랑 탐험가’, 40% 이상 ‘호기심 많은 여행자’, 그 미만 ‘첫 시간 여행자’입니다.

최고 점수는 **지금까지 한 게임에서 맞힌 문제 수의 최댓값**입니다. 문제를 삭제해도 과거 기록은 유지하므로 현재 등록된 문제 수보다 최고 점수가 클 수 있습니다. 완료하지 않고 중단한 게임은 점수 기록에 포함하지 않습니다.

#### 입력 및 예외 처리

- 입력 앞뒤 공백을 제거하고 번호를 확인합니다.
- 빈 입력, `abc`와 같은 문자, 허용 범위 밖 숫자는 안내 후 다시 입력받습니다.
- 문제가 없는 경우 풀이·목록·삭제 화면에서 안내합니다.
- Ctrl+C 또는 입력 스트림 종료가 발생하면 안내 후 저장을 시도하고 종료합니다.
- 문제 등록은 모든 입력이 끝난 뒤, 삭제는 확인이 끝난 뒤 반영하므로 중간 취소로 미완성 변경이 생기지 않습니다.

#### 자동 테스트

프로젝트 루트에서 실행합니다.

```powershell
py -m unittest discover -s tests -v
```

입력 검증, 정답·오답, 저장 후 재실행, 파일 손상과 쓰기 실패, 삭제 취소 및 빈 목록 등을 확인합니다. 테스트는 임시 폴더를 사용하므로 실제 플레이 기록에 영향을 주지 않습니다. [테스트 로그](artifacts/logs/07-tests.txt)에서 `Ran 23 tests`와 `OK`를 확인했습니다.

#### Git 브랜치 및 원격 동기화 실습

퀴즈 풀이 기능은 `feature/quiz-play` 브랜치에서 작업한 뒤 `main`으로 병합했습니다. 다음 명령은 해당 작업에서 사용한 흐름입니다.

```powershell
git checkout -b feature/quiz-play
# 기능 구현 후 add / commit
git checkout main
git merge --no-ff feature/quiz-play -m "Merge: 퀴즈 풀이 기능 브랜치 병합"
```

이미 존재하는 브랜치이므로 현재 저장소에서 전환만 하려면 `git checkout feature/quiz-play`를 사용합니다. 병합 커밋은 `d2b5368`이며, [Git 그래프 로그](artifacts/logs/08-git-graph.txt)에 기록되어 있습니다.

clone/pull 실습은 기존 작업 폴더 안의 별도 복제본 `practice-clone/`에서 진행했습니다.

```powershell
git clone https://github.com/Gonyak004/KDJ-E1-2 practice-clone
# 복제본에 docs/git-practice.txt 추가
git -C practice-clone add docs/git-practice.txt
git -C practice-clone commit -m "Docs: 복제한 저장소에서 Git 동기화 실습 기록 추가"
git -C practice-clone push origin main
git pull --ff-only origin main
git rev-parse HEAD
git -C practice-clone rev-parse HEAD
```

실습 당시 두 폴더의 HEAD가 `271557b2a773e78c26f8ba1eebd6d9c2922fe93d`로 같은 것을 확인했습니다. 이후 개발이 계속되어 현재 HEAD는 달라질 수 있습니다. 실제 실행 기록은 [clone/pull 로그](artifacts/logs/09-clone-pull.txt), 실습에서 추가한 파일은 [Git 실습 기록](docs/git-practice.txt)에서 확인할 수 있습니다.

---

### 4. 프로젝트 구조

```text
KDJ-E1-2/
├── main.py                     # 실행 진입점
├── game.py                     # QuizGame: 메뉴, 풀이, 등록, 목록, 점수, 삭제
├── quiz.py                     # Quiz: 문제, 선택지, 정답, 해설, JSON 변환
├── defaults.py                 # 세계사 기본 7문제 및 이전 기본 문제 식별
├── inputs.py                   # 문자열·숫자 입력 검증
├── storage.py                  # StateStore: JSON 저장, 불러오기, 백업·복구
├── ui.py                       # 카드형 화면, 색상, 진행 막대
├── state.json                  # 실행 시 생성되는 개인 데이터 / Git 제외
├── .gitignore
├── README.md
├── tests/
│   └── test_game.py             # 자동 테스트 23개
├── scripts/
│   ├── collect_evidence.py      # 실제 실행 로그 수집
│   └── capture_evidence.ps1     # 로그를 표시한 Windows 화면 캡처
├── docs/
│   └── git-practice.txt         # 복제본에서 추가 후 pull한 실습 기록
├── artifacts/
│   ├── logs/                   # 실행·환경·테스트·Git 로그, 저장 데이터 예시
│   ├── screenshots/            # 세계사 퀴즈 실행 증빙 PNG
│   └── submission-checklist.txt
└── practice-clone/             # 로컬 Git 실습 복제본 / Git 제외
```

#### 데이터 파일 설명 — state.json

저장 위치는 실행한 터미널의 현재 폴더가 아닌 **프로젝트 루트의 `state.json`**입니다. `storage.py`의 위치를 기준으로 경로를 정하므로 다른 폴더에서 실행해도 같은 파일을 사용합니다.

다음은 스키마 설명용 축약 예시입니다. 실제 저장 파일에는 등록된 모든 문제가 포함됩니다.

```json
{
  "quizzes": [
    {
      "question": "로마 제국의 초대 황제는 누구일까요?",
      "choices": ["네로", "율리우스 카이사르", "아우구스투스", "콘스탄티누스"],
      "answer": 3,
      "explanation": "옥타비아누스는 기원전 27년 아우구스투스라는 칭호를 받았습니다."
    }
  ],
  "best_score": 1,
  "games_played": 1
}
```

| 키 | 역할 |
| --- | --- |
| `quizzes` | 등록된 퀴즈 목록. 빈 목록도 정상 데이터로 유지 |
| `question` | 비어 있지 않은 문제 문자열 |
| `choices` | 비어 있지 않은 선택지 문자열 4개 |
| `answer` | 1~4 정수 정답 번호 |
| `explanation` | 해설 문자열. 기본 문제는 해설 포함, 직접 등록한 문제는 빈 문자열 |
| `best_score` | 과거 최고 정답 수 / 초기값 0 |
| `games_played` | 끝까지 완료한 게임 횟수 / 초기값 0 |

UTF-8로 한글을 그대로 저장합니다. 먼저 `state.json.tmp`에 쓴 뒤 기존 파일을 교체합니다. 손상된 파일은 `state.corrupt-날짜-시간.json`으로 보관하고 기본 문제로 복구합니다.

이전 Python·아재개그 기본 문제를 그대로 사용하던 저장 파일은 백업 후 세계사 문제로 전환합니다. 직접 추가한 문제는 유지하고, 기존 문제와 점수는 `state.before-theme-날짜-시간.json`으로 보관한 뒤 새 테마 점수를 0부터 시작합니다. 백업에 실패하면 기존 상태를 유지합니다.

개인 진행 파일과 백업은 `.gitignore`에서 제외했습니다. 저장 형식의 실제 실행 예시는 [sample-state.json](artifacts/logs/sample-state.json)에 포함했습니다.

---

### 5. 트러블슈팅

#### 1. 다른 GitHub 계정 인증으로 인한 403 오류

- 문제: 본인 저장소에 push할 때 권한 오류가 발생했습니다.
- 원인: 저장소 주소는 본인 계정이었지만 PC에 저장된 GitHub 인증이 다른 사용자 계정이었습니다. 커밋 작성자 설정과 원격 인증 계정은 별도로 관리되는 것을 확인했습니다.
- 조치: 이전 인증을 제거하고 `Gonyak004`로 다시 인증했습니다. Git 작성자도 본인 계정으로 설정했습니다.
- 현재 확인: `origin`은 `Gonyak004/KDJ-E1-2`이며 본인 계정으로 push를 완료했습니다.

> 공용 PC에서는 커밋 작성자 설정뿐 아니라 실제 인증 계정도 함께 확인해야 할 듯 싶습니다.

#### 2. 빈 입력이나 문자 입력 시 숫자 변환 문제

- 문제: 메뉴와 정답 입력에서 숫자로 바꿀 수 없는 값이나 범위 밖 번호가 들어올 수 있습니다.
- 조치: 공통 입력 함수를 분리하고 `strip()`, `int()` 변환 및 `try/except`를 적용했습니다.
- 현재 확인: 빈 입력, `abc`, 메뉴 `9`, 정답 `0`에 대해 안내 후 재입력되는 것을 로그와 테스트에서 확인했습니다.

#### 3. 문제 삭제 후 기존 최고 점수가 손상 데이터로 판단되는 문제

- 문제: 기존에는 최고 점수가 현재 문제 수보다 크면 잘못된 데이터로 판단했습니다. 문제를 삭제하면 정상적인 과거 기록도 이 조건에 걸릴 수 있었습니다.
- 조치: 최고 점수와 현재 문제 수를 비교하는 제한을 제거하고, 정수 여부·음수·미플레이 기록과의 일관성을 확인하도록 변경했습니다.
- 현재 확인: 7점 기록에서 문제 수가 6개가 되거나, 마지막 문제를 삭제한 뒤 재실행해도 최고 점수가 유지되는 테스트를 통과했습니다.

#### 4. 한글과 테두리의 콘솔 정렬 문제

- 문제: 한글과 영문은 화면에서 차지하는 폭이 다르고, 글꼴에 따라 테두리 문자의 폭도 달라질 수 있었습니다.
- 조치: 한글 표시 폭을 계산해 줄바꿈과 여백을 처리하고 ASCII 테두리를 사용했습니다. 캡처 뷰어에는 한글 고정폭 글꼴을 적용했습니다.
- 현재 확인: 긴 한글 문장의 카드 폭 테스트와 갱신한 실행 캡처에서 정렬을 확인했습니다. 색상을 지원하지 않는 출력에서는 색상 코드를 넣지 않습니다.

---

### 6. 로그 및 증빙 자료

| 자료 | 확인 내용 |
| --- | --- |
| [메뉴·입력 검증](artifacts/logs/01-menu-validation.txt) | 메뉴, 빈 입력·문자·범위 오류 및 미플레이 점수 |
| [퀴즈 추가](artifacts/logs/02-add-quiz.txt) | 올림픽 문제 등록, 정답 번호 검증, 파일 저장 |
| [재실행 후 목록](artifacts/logs/03-list-restart.txt) | 기본 7개에 새 문제가 추가된 8개 목록 |
| [퀴즈 풀이](artifacts/logs/04-play.txt) | 정답·오답, 해설, 연속 정답 및 최종 결과 |
| [재실행 후 점수](artifacts/logs/05-score-restart.txt) | 최고 점수 7개 정답, 완료 게임 1회 유지 |
| [개발 환경](artifacts/logs/06-environment.txt) | Python·Git 버전, 작성자 및 원격 주소 |
| [테스트 결과](artifacts/logs/07-tests.txt) | 자동 테스트 23개 통과 |
| [Git 그래프](artifacts/logs/08-git-graph.txt) | 기능별 커밋과 별도 브랜치 병합 |
| [clone/pull 실습](artifacts/logs/09-clone-pull.txt) | 복제본 변경·push, 원본 pull 및 실습 당시 HEAD 일치 |
| [문제 삭제](artifacts/logs/10-delete-quiz.txt) | 추가한 8번 문제 선택, 확인 및 저장 |
| [삭제 후 재실행](artifacts/logs/11-list-after-delete.txt) | 7개 목록과 기존 최고 점수 유지 |

#### 실습 화면 증빙

화면에서 확인되는 내용을 기준으로 대표 이미지를 첨부했습니다. 연속된 전체 화면은 [스크린샷 폴더](artifacts/screenshots)에서 확인하실 수 있습니다.

##### 개발 환경 확인

> Python 3.15.2, Git 버전, 작성자 Gonyak004와 본인 저장소의 fetch/push 주소를 확인했습니다.

![개발 환경 확인](artifacts/screenshots/06-environment-01.png)

##### 메뉴 및 잘못된 입력 처리

> 메뉴 1~6과 빈 입력, abc, 범위 밖 번호 9에 대한 안내를 확인했습니다.

![메뉴 및 입력 검증](artifacts/screenshots/01-menu-validation-01.png)

##### 퀴즈 등록 및 저장

> 고대 올림픽 문제와 선택지를 입력하고, 정답 번호를 검증한 뒤 파일에 저장했습니다. 등록 후 문제 수가 8개로 바뀌었습니다.

![퀴즈 등록 입력](artifacts/screenshots/02-add-quiz-01.png)

![퀴즈 등록 저장 결과](artifacts/screenshots/02-add-quiz-02.png)

##### 재실행 후 퀴즈 목록

> 프로그램을 다시 실행해 목록 8개를 확인했습니다. 기본 문제에 더해 직접 등록한 올림픽 문제가 8번으로 남아 있습니다.

![재실행 후 퀴즈 목록](artifacts/screenshots/03-list-restart-01.png)

![추가한 문제 유지 확인](artifacts/screenshots/03-list-restart-04.png)

##### 문제 풀이와 해설

> 카드형 문제, 정답 안내, 해설 및 연속 정답 표시를 확인했습니다.

![퀴즈 풀이 및 해설](artifacts/screenshots/04-play-02.png)

##### 오답 및 최종 결과

> 마지막 문제는 오답으로 입력했습니다. 총 8문제 중 7문제 정답, 정답률 88%, 최다 연속 정답 7개와 ‘베테랑 탐험가’ 등급을 확인했습니다.

![퀴즈 풀이 결과](artifacts/screenshots/04-play-06.png)

##### 재실행 후 최고 점수

> 새 실행에서도 최고 점수 7문제 정답, 완료한 게임 1회가 유지되었습니다.

![재실행 후 점수 확인](artifacts/screenshots/05-score-restart-01.png)

##### 문제 삭제 및 재실행 확인

> 등록한 8번 올림픽 문제를 선택하고 삭제를 확인했습니다. 삭제 후 문제 수가 7개가 되었으며, 다시 실행해도 7개 목록과 최고 점수 7개 정답이 유지되었습니다.

![문제 삭제 확인 및 저장](artifacts/screenshots/10-delete-quiz-02.png)

![삭제 후 재실행 목록](artifacts/screenshots/11-list-after-delete-01.png)

![삭제 후 최고 점수 유지](artifacts/screenshots/11-list-after-delete-04.png)

##### Git 커밋 및 브랜치 병합

> 기능별 커밋과 퀴즈 풀이 브랜치의 병합 그래프를 확인했습니다. 이 화면은 증빙 수집 당시 기록이며, README 등 이후 커밋은 현재 Git 이력에서 확인합니다.

![Git 커밋 그래프](artifacts/screenshots/08-git-graph-01.png)

##### 저장소 복제와 동기화

> 복제본에서 실습 기록을 추가하고 push한 뒤, 기존 작업 폴더에서 pull해 같은 커밋이 반영된 기록입니다.

![Git clone 및 pull 실습](artifacts/screenshots/09-clone-pull-01.png)

##### 자동 테스트

> 테스트 결과의 `Ran 23 tests`와 `OK`를 확인했습니다.

![자동 테스트 결과](artifacts/screenshots/07-tests-01.png)

#### 증빙 재수집

프로젝트 루트에서 다음 명령으로 로그와 캡처를 갱신할 수 있습니다. 캡처 스크립트는 Windows 전용이며 실행 시 기록 뷰어 창이 잠시 표시됩니다.

```powershell
py scripts/collect_evidence.py
powershell -NoProfile -ExecutionPolicy Bypass -File scripts/capture_evidence.ps1
```

게임 시나리오는 임시 폴더의 `state.json`을 사용합니다. 실제 플레이 기록은 변경하지 않지만 `artifacts/logs/`와 같은 이름의 PNG는 갱신됩니다. clone/pull 로그는 앞서 실제 수행한 기록을 보관한 것이므로 위 명령으로 원격 실습을 다시 수행하지는 않습니다.

---

### 7. 실습 확인 결과

| 확인 항목 | 실행 결과 |
| --- | --- |
| 기본 퀴즈 | 세계사 주제 7개, 선택지 각 4개 및 해설 포함 |
| 코드 구조 | Quiz·QuizGame·StateStore로 역할 분리, 입력·출력 모듈 분리 |
| 메뉴 및 입력 | 기능 선택·종료, 공백 제거, 빈 입력·문자·범위 오류 처리 |
| 퀴즈 추가 | 올림픽 문제 등록 후 8개, 재실행 목록에서 유지 |
| 퀴즈 풀이 | 8문제 중 7문제 정답, 해설·결과 등급 표시 |
| 최고 점수 | 재실행 후 최고 정답 수 7개와 완료 게임 1회 유지 |
| 문제 삭제 | 삭제 확인·취소, 삭제 후 재실행 목록과 과거 점수 유지 |
| 파일 처리 | UTF-8 JSON 저장, 파일 없음·손상·읽기·쓰기 오류 테스트 통과 |
| 안전 종료 | Ctrl+C 및 EOF 발생 시 저장과 종료 테스트 통과 |
| 자동 테스트 | unittest 23개 통과 |
| Git 이력 | 10개 이상의 기능별 커밋과 feature/quiz-play 병합 |
| clone / pull | 복제본 commit·push → 기존 폴더 pull → 실습 당시 HEAD 일치 |

실제 실행 결과는 [원문 로그](artifacts/logs)와 [스크린샷](artifacts/screenshots)에서 확인할 수 있습니다. 개인 데이터인 루트 `state.json`은 제출 코드에 포함하지 않으며, 처음 실행할 때 자동 생성됩니다.

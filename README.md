# Book_Publishing: 실용서 쓰기 스킬

> Claude Code의 슬래시 커맨드 4개로 한국어 실용서 한 권을 처음부터 끝까지 완성하는 하네스입니다.
> `user-book-toc.md` 한 파일만 교체하면 다른 책에도 그대로 재사용할 수 있습니다.

**버전** 1.2.0 · **언어** 한국어 · **산출물** Word(`.docx`) + 출판 메타데이터

## 무엇을 하는가

```
/research   웹 조사 (Tier 1/2/3 출처 분류)
/write      구조 설계 + 초안 (첫 호출에 청크 단위 1회 질의)
/review     내부 리뷰 6단계 + 외부 리뷰 3단계 + 최종 수정
/publish    자동 검증 + Word 변환 + 출판 메타데이터
```

핵심 커맨드 4개를 순서대로 실행하면 약 240페이지 분량의 책 한 권이 완성됩니다.

## 시작하기

```bash
# 1. 클론
git clone https://github.com/airoasting/book_publishing.git my-book
cd my-book

# 2. 의존성
pip install python-docx matplotlib
npm install -g @anthropic-ai/claude-code

# 3. (선택) 검증기 동작 확인
bash tests/run-smoke.sh   # → PASS=2, FAIL=0

# 4. user-book-toc.md를 자기 책에 맞게 편집

# 5. 실행
claude
> /research
> /write     # 첫 호출에서 청크 단위를 한 번 묻습니다
> /review
> /publish
```

`user-book-toc.md`는 6개 섹션(기본 정보, 페르소나, 목차, 활용법 가이드, 작성 스타일, 퍼블리싱 사양)으로 구성되어 있습니다. 현재 들어 있는 "노트북LM으로 다 됨" 사양을 예시 삼아 자기 책에 맞게 통째로 교체하시면 됩니다.

## 어떻게 작동하나

### 9명의 리뷰어가 단계별로 검수합니다

리뷰어 9명은 두 그룹으로 나뉘어 있습니다.

**내부 리뷰어 7명** (원고를 출판 가능한 수준까지 끌어올리는 역할)

| 리뷰어 | 무엇을 보는가 |
|--------|--------------|
| 비평가 | 근거 없는 주장과 논리 비약을 잡아냅니다 |
| 독자 | 따라 하기 어렵거나 흥미가 끊기는 부분을 짚어냅니다 |
| 사실 검증가 | 통계와 인용의 출처를 확인합니다 |
| 구조 검증가 | 목차와 글의 흐름이 일관된지 점검합니다 |
| 논리 검증가 | 전제와 결론이 매끄럽게 이어지는지 확인합니다 |
| 독자 검증가 | 전문 용어 설명과 전반적인 이해도를 점검합니다 |
| 서식 검증가 | 표기 규칙과 부호가 통일되어 있는지 검사합니다 |

뒤의 다섯 명(사실·구조·논리·독자·서식 검증가)은 합평 5인으로 묶여 두 라운드에 걸쳐 함께 검수합니다.

**외부 리뷰어 2명** (출판 직전 마지막 점검)

| 리뷰어 | 무엇을 보는가 |
|--------|--------------|
| 편집자 | 구성·서사·톤·완성도를 평가합니다 |
| 프루프리더 | 맞춤법·비문·부호 오류를 잡아냅니다 |

마케터도 별도로 의견을 주지만 점수는 매기지 않으며, 출판 메타데이터(부제·소개·키워드)에만 참고용으로 반영합니다.

### 9개 단계로 진행됩니다

| 단계 | 작업 | 산출물 |
|------|------|--------|
| 1 | 비평가 리뷰 | `04_review-red.md` |
| 2 | 비평 반영 수정 | `05_draft-v2.md` |
| 3 | 독자 리뷰 | `06_review-pink.md` |
| 4 | 독자 반영 수정 | `07_draft-v3.md` |
| 5 | 합평 1라운드 (5인) | `08_ensemble-review-1.md` |
| 6 | 합평 2라운드 (5인) | `10_ensemble-review-2.md` |
| 7 | 편집자 리뷰 | `12_review-editor.md` |
| 8 | 마케터·프루프리더 리뷰 | `13_review-marketer.md`, `14_review-proofreader.md` |
| 9 | 최종 수정 | `11_draft-final.md` |

모든 리뷰어가 동일한 10점 만점 기준으로 채점합니다. 합평을 통과하려면 **🔴이 0건이고 평균 9점 이상**이어야 하며, 기준에 도달할 때까지 최대 3라운드를 자동으로 반복합니다.

**자동 검증기 (`tests/verify.py`)**

`/publish`의 1단계에서 12가지 항목을 자동으로 검사합니다. 검사 항목에는 em dash 잔존, `**` 마크다운 잔존, 목차 헤딩 누락, 상태 마커 누락, 분량 미달, 용어 위반, 합쇼체 혼용 등이 포함됩니다. 🔴 등급의 결함이 한 건이라도 발견되면 종료 코드 1을 반환하여 Word 변환을 막습니다.

**상태 마커**

각 산출물의 마지막 줄에 들어가는 `<!-- STAGE_COMPLETE: ... -->` 마커로 단계의 완료 여부를 판정합니다. 대화가 중간에 끊기더라도 활성 폴더와 마커를 자동으로 감지하여 미완료 단계부터 이어쓰기로 재개합니다.

## 레포 구조

클론 직후의 상태입니다. 사용자가 직접 편집해야 하는 파일은 `user-book-toc.md` 하나뿐입니다.

```
프로젝트 루트/
├── CLAUDE.md                       프로세스 + 범용 규칙 (수정 불필요)
├── user-book-toc.md                ★ 유일한 교체 대상
├── README.md
├── CHANGELOG.md
├── LICENSE                         Apache License 2.0
├── .gitignore
├── .claude-plugin/
│   └── plugin.json                 플러그인 매니페스트
├── .claude/
│   ├── book-toc.md                 (구버전 호환용 redirect stub)
│   └── skills/
│       ├── research.md             /research
│       ├── write.md                /write
│       ├── review.md               /review
│       └── publish.md              /publish
└── tests/
    ├── verify.py                   원고 자동 검증기 (12개 검사)
    ├── run-smoke.sh                스모크 테스트 러너
    └── fixtures/
        ├── mini-user-book-toc.md
        ├── pass-draft-final.md
        └── fail-draft-final.md
```

## 스킬을 돌리면 생기는 파일들

스킬을 실행하면 두 개의 날짜 폴더가 자동으로 만들어집니다. 작업 중인 원고는 `draft/YYYYMMDD/`에 쌓이고, 출판용 최종 산출물은 `output/YYYYMMDD/`에 저장됩니다. 두 폴더는 모두 `.gitignore`에 등록되어 있어 레포에 커밋되지 않습니다.

```
draft/
└── 20260504/                       ← 한 권 = 하나의 날짜 폴더
    │
    │  /research 산출물
    ├── 01_research-notes.md        웹 조사 노트
    ├── 01_citations.json           인용 추적 (Tier 1/2/3 등급)
    │
    │  /write 산출물
    ├── 02_outline.md               구조 설계
    ├── 03_draft-v1_part1.md        Part별 청크 (병합 전)
    ├── 03_draft-v1_part2.md
    ├── ...
    ├── 03_draft-v1.md              초안 (병합 결과)
    ├── _session-config.json        /write 청크 단위 설정
    │
    │  /review 산출물 (내부 리뷰 6단계 + 외부 리뷰 3단계 + 최종 수정)
    ├── 04_review-red.md            비평가 리뷰
    ├── 05_draft-v2.md              비평 반영본
    ├── 06_review-pink.md           독자 리뷰
    ├── 07_draft-v3.md              독자 반영본
    ├── 08_ensemble-review-1.md     합평 1라운드 (5인)
    ├── 09_draft-v4.md              합평1 반영본
    ├── 10_ensemble-review-2.md     합평 2라운드 (5인, 통과 게이트)
    ├── 11_draft-final.md           최종 원고 (이후 9단계에서 덮어쓰기 갱신)
    ├── 12_review-editor.md         편집자 리뷰
    ├── 13_review-marketer.md       마케터 리뷰 (참고용)
    ├── 14_review-proofreader.md    프루프리더 리뷰
    │
    └── _backup/                    자동 백업 (gitignore)

output/
└── 20260504/                       ← 같은 날짜의 출판 산출물
    │
    │  /publish 산출물
    ├── final.docx                  ★ Word 최종본
    ├── metadata.md                 출판 메타데이터 (제목·부제·소개·키워드)
    ├── verify-report.md            검증 리포트 + 자가 채점 (10점 만점)
    └── images/                     본문 다이어그램 (matplotlib 생성)
        ├── fig01.png
        ├── fig02.png
        └── ...
```

같은 날 새 책을 시작하면 `draft/20260504_01/`처럼 접미가 붙어 여러 책을 동시에 작업해도 서로 섞이지 않습니다.

## 다른 책에 재사용

`user-book-toc.md` **한 파일만** 교체하시면 됩니다. `CLAUDE.md`, 스킬 4개, `verify.py`는 손대지 않아도 동일하게 작동합니다. 다른 언어로 책을 쓰실 때에도 작성 스타일과 퍼블리싱 사양(폰트 등)만 해당 언어에 맞게 수정하시면 됩니다.

## 트러블슈팅

| 상황 | 처리 방법 |
|------|----------|
| 대화가 중간에 끊겼을 때 | `/write 이어서 작성해줘` 또는 `/review 이어서 진행해줘`라고 입력하시면 활성 폴더와 마커를 기준으로 자동 재개합니다 |
| 합평이 9점을 넘지 못할 때 | 최대 3라운드까지 자동으로 반복합니다. 그래도 통과하지 못하면 미통과 사유가 `10_ensemble-review-2.md`에 기록됩니다 |
| 검증에서 🔴이 나왔을 때 | `output/{ACTIVE}/verify-report.md`를 확인한 뒤 본문을 직접 수정하시거나 `/review`의 9단계를 다시 실행하시면 됩니다. 🔴이 0이 될 때까지 Word 변환은 진행되지 않습니다 |
| 청크 단위를 바꾸고 싶을 때 | `draft/{ACTIVE}/_session-config.json` 파일을 직접 편집하시거나 삭제하시면 됩니다 |

## 라이선스

이 하네스(`CLAUDE.md`, 스킬, `verify.py`, fixture 등 구조 자체)는 **Apache License 2.0**으로 배포됩니다. 자세한 내용은 [LICENSE](LICENSE) 파일을 참조해 주세요.

콘텐츠 산출물(원고와 이미지처럼 사용자가 이 하네스로 만든 결과물)의 저작권은 작성자 본인에게 있습니다.

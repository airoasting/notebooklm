# Book_Publishing — 실용서 쓰기 스킬

> Claude Code 슬래시 커맨드 4개로 한국어 실용서 한 권을 처음부터 끝까지 쓰는 하네스.
> `user-book-toc.md` 한 파일만 교체하면 다른 책으로 재사용된다.

**버전** 1.2.0 · **언어** 한국어 · **산출물** Word(`.docx`) + 출판 메타데이터

## 무엇을 하는가

```
/research   웹 조사 (Tier 1/2/3 출처 분류)
/write      구조 설계 + 초안 (첫 호출에 청크 단위 1회 질의)
/review     내부 리뷰 6단계 + 외부 리뷰 3단계 + 최종 수정
/publish    자동 검증 + Word 변환 + 출판 메타데이터
```

핵심 4개 커맨드를 순서대로 실행하면 약 240페이지 분량의 책이 완성된다. 표지는 다루지 않으며 외부 도구나 디자이너에 위임한다.

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
> /write     # 첫 호출에서 청크 단위를 한 번 묻는다
> /review
> /publish
```

`user-book-toc.md`는 6개 섹션(기본 정보, 페르소나, 목차, 활용법 가이드, 작성 스타일, 퍼블리싱 사양)으로 구성된다. 현재 들어 있는 "노트북LM으로 다 됨" 사양을 예시로 보고 자기 책에 맞게 통째로 교체하면 된다.

## 어떻게 작동하나

**9명의 리뷰어가 9단계로 검수**

| 단계 | 리뷰어 | 산출물 |
|------|--------|--------|
| 1 | 비평가 | `04_review-red.md` |
| 3 | 독자 | `06_review-pink.md` |
| 5 | 합평 1라운드 (5인) | `08_ensemble-review-1.md` |
| 6 | 합평 2라운드 (5인) | `10_ensemble-review-2.md` |
| 7 | 편집자 | `12_review-editor.md` |
| 8 | 마케터 / 프루프리더 | `13_review-marketer.md`, `14_review-proofreader.md` |
| 9 | 최종 수정 | `11_draft-final.md` |

모든 리뷰어가 같은 10점 anchor로 채점한다. 합평 통과 게이트는 **🔴 0건 + 평균 9점 이상**이며 최대 3라운드까지 자동 진행한다.

**자동 검증기 (`tests/verify.py`)**

`/publish` 1단계에서 12가지를 자동 검사한다 — em dash 잔존, `**` 마크다운 잔존, 목차 헤딩 누락, 상태 마커 누락, 분량 미달, 용어 위반, 합쇼체 혼용 등. 🔴이 1건이라도 있으면 종료 코드 1로 Word 변환을 막는다.

**상태 마커**

각 산출물 끝의 `<!-- STAGE_COMPLETE: ... -->` 마커로 단계 완료를 판정한다. 대화가 끊겨도 활성 폴더와 마커를 자동 감지해 미완료 단계부터 append로 재개한다.

## 폴더 구조

```
프로젝트 루트/
├── CLAUDE.md                       프로세스 + 범용 규칙 (수정 불필요)
├── user-book-toc.md                ★ 유일한 교체 대상
├── .claude-plugin/plugin.json      플러그인 매니페스트
├── .claude/skills/
│   ├── research.md                 /research
│   ├── write.md                    /write
│   ├── review.md                   /review
│   └── publish.md                  /publish
├── tests/
│   ├── verify.py                   원고 자동 검증기 (12개 검사)
│   ├── run-smoke.sh                스모크 테스트 러너
│   └── fixtures/                   pass/fail fixture 3개
├── draft/YYYYMMDD/                 ← 한 권 = 하나의 날짜 폴더 (gitignore)
│   └── 01_research-notes.md ~ 14_review-proofreader.md
└── output/YYYYMMDD/                ← 같은 날짜의 출판 산출물 (gitignore)
    ├── final.docx
    ├── metadata.md
    └── images/
```

같은 날 새 책을 시작하면 `draft/YYYYMMDD_01/`처럼 접미가 붙는다.

## 다른 책에 재사용

`user-book-toc.md` **한 파일만** 교체한다. `CLAUDE.md`, 스킬 4개, `verify.py`는 손대지 않는다. 다른 언어로 쓸 때도 작성 스타일·퍼블리싱 사양(폰트)만 해당 언어에 맞게 수정하면 된다.

## 트러블슈팅

| 상황 | 처리 |
|------|------|
| 대화가 중간에 끊겼다 | `/write 이어서 작성해줘` 또는 `/review 이어서 진행해줘`. 활성 폴더와 마커로 재개한다 |
| 합평이 9점을 못 넘긴다 | 최대 3라운드까지 자동. 미통과 시 사유가 `10_ensemble-review-2.md`에 기록된다 |
| 검증에서 🔴이 나왔다 | `output/{ACTIVE}/verify-report.md` 확인 → 본문 직접 수정 또는 `/review` 9단계 재실행. 🔴 0이 될 때까지 Word 변환은 막힌다 |
| 청크 단위를 바꾸고 싶다 | `draft/{ACTIVE}/_session-config.json`을 편집하거나 삭제 |

## 라이선스

- 콘텐츠 산출물(원고·이미지)의 저작권은 작성자에게 있다
- 하네스 구조(`CLAUDE.md`, 스킬, `verify.py`, fixture)는 자유롭게 참고·변형해 사용할 수 있다

## 변경 이력

상세 내용은 [CHANGELOG.md](CHANGELOG.md)를 참조한다.

- **1.2.0** (2026-05-04) — `user-book-toc.md` 이름·위치 변경 (루트로)
- **1.1.0** (2026-05-04) — `/write` 청크 단위 1회 질의, `/cover` 스킬 제거
- **1.0.0** (2026-05-04) — 플러그인 매니페스트, 스모크 테스트, 자동 검증기, 출처 신뢰도 등급, 자가 채점

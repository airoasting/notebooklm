---
name: publish
description: "리뷰 완료된 최종 원고를 검증·Word 변환·메타데이터 생성한다. /review 다음에 실행. Use after /review completes — runs an automated verifier first to catch style violations and placeholder leaks, then produces final.docx and metadata.md in output/{ACTIVE}/."
allowed-tools: Read, Write, Edit, Bash
user_invocable: true
---

# 퍼블리싱 + 검증 + 메타데이터

이 스킬은 3단계를 순서대로 수행한다. 검증을 통과해야 Word 변환으로 넘어간다.

## 시작 전 준비

`user-book-toc.md`를 읽고 다음을 파악한다:
- 기본 정보: 제목, 필명, 판형
- 목차: 부 제목, 부 부제, 장 제목 (헤딩 구조에 사용)
- 퍼블리싱 사양: 폰트, 색상, 여백, 문서 구성 요소, 시각 자료, 이미지 생성 규칙

## 활성 폴더 결정

`draft/` 하위 폴더 중 사전순 가장 최신 폴더를 활성으로 선택한다. 동일 이름의 `output/` 폴더에 산출물을 생성한다.

```bash
ACTIVE=$(ls -1d draft/*/ 2>/dev/null | sort | tail -n 1)
ACTIVE="${ACTIVE%/}"
[ -z "${ACTIVE}" ] && { echo "활성 폴더 없음. /research를 먼저 실행하세요."; exit 1; }
OUT="output/${ACTIVE#draft/}"
mkdir -p "${OUT}/images"
echo "활성 프로젝트 폴더: ${ACTIVE}"
echo "출판 출력 폴더: ${OUT}"
```

---

## 1단계: 검증 (verify.py)

원고를 Word로 변환하기 **전에** 자동 검사를 돌려 스타일·서식 위반을 잡아낸다. `/review` 사이클이 끝나도 LLM이 놓친 위반이 남아 있을 수 있다.

### 1.1 검증 스크립트 준비

이 하네스의 표준 검증기는 `tests/verify.py`다. `/publish`는 이 파일을 그대로 사용한다 (단일 진실 원칙: 책마다 verifier가 따로 생기지 않는다).

```bash
# verify.py가 정상 작동하는지 사전 체크 (옵션)
bash tests/run-smoke.sh
```

검증기가 검사하는 항목 (자가 채점 anchor와 함께):

| # | 검사 | 심각도 |
|---|------|--------|
| 1 | em dash(—, –) 잔존 | 🔴 |
| 2 | `**` 마크다운 잔존 | 🔴 |
| 3 | [그림 N] 참조 수 (정보) | ℹ️ |
| 4 | 합쇼체 혼용 비율 (>5%) | 🟡 |
| 5 | 분량 vs user-book-toc.md 목표 (미달이면 🔴) | 🔴 / ℹ️ |
| 6 | user-book-toc.md 목차 헤딩 누락 | 🔴 |
| 7 | `<!-- STAGE_COMPLETE: 11_draft-final -->` 마커 | 🔴 |
| 8 | "N부를 마치며" 브릿지 누락 | 🟡 |
| 9 | 용어 위반 ("커스텀 지시" 등 book-toc 위반) | 🔴 |
| 10 | 불릿 부호 통일 (●, ▪ 검출) | 🟡 |
| 11 | 영어 단독 표현 ("Before/After" 등) | 🟡 |
| 12 | 자가 채점 (10점 만점) | 정보 |

자가 채점은 CLAUDE.md "자가 채점" 표 anchor를 그대로 따른다.

### 1.2 검증 실행

```bash
python3 tests/verify.py \
  "${ACTIVE}/11_draft-final.md" \
  "user-book-toc.md" \
  "${OUT}/verify-report.md"
```

- 종료 코드 0 → 다음 단계
- 종료 코드 1 → `{OUT}/verify-report.md`를 읽고 🔴 항목을 사용자에게 보고. 🔴이 0건이 될 때까지 본문을 직접 수정하거나 `/review` 9단계 최종 수정을 다시 한 번 돌린다

검증 보고서는 항상 `{OUT}/verify-report.md`로 저장된다. 통과해도 ℹ️·🟡 항목은 사용자에게 한 줄 요약으로 알린다.

### 1.3 자가 채점 보고

`{OUT}/verify-report.md` 상단에 박힌 자가 채점(10점 만점)을 사용자에게 그대로 한 줄로 알린다.

```
verify 통과: 자가 채점 9 / 10 (🔴 0, 🟡 1)
```

9점 미만이면 출판을 보류하고 🟡 항목을 한 번 더 다듬을 것을 권장한다.

### 1.4 백업

검증 통과 시점의 `{ACTIVE}/11_draft-final.md`를 `{ACTIVE}/_backup/11_draft-final_published_$(date +%Y%m%d_%H%M).md`로 복사한다 (CLAUDE.md "백업 정책"의 세 번째 트리거).

---

## 2단계: Word 문서 생성

입력: `{ACTIVE}/11_draft-final.md`

`user-book-toc.md`의 "퍼블리싱 사양" 섹션에 정의된 모든 서식 규칙을 적용하여 Word 문서를 생성한다.

생성 스크립트:
- `{OUT}/generate_images.py` — matplotlib으로 [그림 N] 위치에 들어갈 이미지 생성. `{OUT}/images/fig01.png`부터 순번 저장
- `{OUT}/generate_docx.py` — python-docx로 final.docx 생성. [그림 N] 패턴을 감지해 자동 삽입

산출물:
- `{OUT}/final.docx`
- 문서 작성자(author) 속성은 `user-book-toc.md`의 필명으로 설정

## 3단계: 출판 메타데이터 생성

최종 원고와 `13_review-marketer.md`(참고용)를 기반으로 출판 메타데이터를 생성한다.

### 마케터 리뷰 → 메타데이터 매핑

마케터 리뷰가 본문에는 반영되지 않지만, 메타데이터에서는 1차 입력으로 쓴다.

| 마케터 리뷰 항목 | 메타데이터 필드 |
|------------------|-----------------|
| 한 줄 소개 후보 3개 | 도서 설명문 첫 문장 (후킹) |
| 타겟 명확성 평가 | 검색 키워드 후보 |
| 제목 파워 평가 | 부제·띠지 카피 보강 |
| 시의성 평가 | 가격 전략·시즌 캠페인 |

### 생성 항목

- 도서 분류: BISAC(국제) 및 KDC(한국) 분류 코드
- 판매 카피: "후킹 → 가치 → 독자가 얻을 것 → 행동 유도" 구조의 도서 설명문 (내용 요약이 아닌 판매 목적)
- 검색 키워드: 독자가 실제로 검색하는 단어 기준 7~10개
- 가격 전략: 경쟁 도서 분석 기반 권장 가격대
- 플랫폼별 배포 설정: 교보문고, 리디북스, 예스24, 밀리의 서재, 아마존 KDP

출력: `{OUT}/metadata.md`

## 완료 처리

완료되면 사용자에게 안내한다:
```
퍼블리싱 완료.
- ${OUT}/final.docx (최종 문서)
- ${OUT}/metadata.md (출판 메타데이터)
- ${OUT}/verify-report.md (검증 보고서)
```

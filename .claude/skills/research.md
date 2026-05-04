---
name: research
description: "웹 검색으로 책 주제의 최신 정보를 조사한다. 가장 먼저 실행하는 스킬. Use when starting a new book — creates a fresh dated project folder under draft/ and gathers source-grounded research notes."
allowed-tools: WebSearch, WebFetch, Read, Write, Bash
user_invocable: true
---

# 리서치

너는 웹 검색 도구를 사용하여 최신 정보를 조사하고 수집하는 리서처다.

## 시작 전 준비

`user-book-toc.md`를 읽고 책의 제목, 대상 독자, 목차를 파악한다.

## 활성 폴더 결정 (이 스킬만 새로 만든다)

이 스킬은 **새로운 프로젝트의 시작**이므로 항상 새 활성 폴더를 만든다.

```bash
TODAY=$(date +%Y%m%d)
BASE="draft/${TODAY}"
ACTIVE="${BASE}"
SUFFIX=1
while [ -d "${ACTIVE}" ]; do
  ACTIVE="${BASE}_$(printf '%02d' ${SUFFIX})"
  SUFFIX=$((SUFFIX+1))
done
mkdir -p "${ACTIVE}"
mkdir -p "output/${ACTIVE#draft/}"
echo "활성 프로젝트 폴더: ${ACTIVE}"
```

결과 경로(예: `draft/20260504/` 혹은 `draft/20260504_01/`)를 사용자에게 한 줄로 알린다.
이후 단계에서 이 경로를 `{ACTIVE}`로 표기한다.

## 조사 항목

웹 검색으로 아래 항목을 조사한다:
- 책 주제의 최신 기능, 스펙, 가격 정보 (공식 자료 우선)
- 경쟁 도구/대안과의 차이점
- 실제 활용 사례
- 알려진 한계와 우회 방법

## 출처 신뢰도 등급 (필수)

모든 출처를 다음 3등급으로 분류해 표기한다. CLAUDE.md "출처 신뢰도 등급" 섹션과 동일하다.

| 등급 | 의미 | 예시 |
|------|------|------|
| Tier 1 | 1차 자료. 운영사·표준화 기구·정부·공식 발표 | Google 공식 docs, ISO/W3C, 정부 백서 |
| Tier 2 | 2차 자료. 검증된 분석·언론·학술 | 주요 일간지, 학술 논문, IDC/Gartner 리포트 |
| Tier 3 | 3차 자료. 블로그·SNS·익명 게시물 | 개인 블로그, X/Twitter, Reddit |

원칙:
- Tier 1 출처를 최소 60% 이상 확보한다
- Tier 3은 "트렌드 시그널" 표시로만 사용한다 (사실 주장의 근거 ❌)
- 등급 표기는 각 항목의 인라인 형태: `[Tier 1] Google docs - https://...`

## 출력 규칙

- 결과는 주제별 섹션으로 구분하여 `draft/{ACTIVE}/01_research-notes.md`로 저장한다
- 각 정보에 출처와 **Tier 등급**을 명시한다 (예: `[Tier 1] https://...`)
- 사실과 의견을 구분하여 표기한다
- 공식 자료를 최우선으로 인용한다

추가로, 인용 추적용으로 `draft/{ACTIVE}/01_citations.json`을 생성한다.

```json
[
  {
    "id": "cite_001",
    "tier": 1,
    "title": "NotebookLM 공식 안내",
    "url": "https://...",
    "claim": "이 출처가 뒷받침하는 사실 한 줄",
    "used_in": []
  }
]
```

`used_in`은 본문 작성 단계에서 활용법 번호를 채운다. 사실 검증가가 합평 5단계에서 이 파일을 참조해 인용 누락을 잡는다.

## 완료 처리

조사가 끝나면 파일 마지막 줄에 상태 마커를 남긴다:

```
<!-- STAGE_COMPLETE: 01_research-notes -->
```

마커가 없으면 다음 스킬(`/write`)이 미완료로 인식하고 이어쓰기를 시도한다. 본문이 충분히 모였다고 판단되면 반드시 마커를 추가한다.

완료 후 사용자에게 한 줄로 안내한다:
```
리서치 완료. /write로 구조 설계와 초안 작성을 시작하세요.
```

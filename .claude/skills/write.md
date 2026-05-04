---
name: write
description: "리서치 결과를 바탕으로 구조를 설계하고 초안을 작성한다. /research 다음에 실행. Use after /research completes — reads 01_research-notes.md and produces 02_outline.md and 03_draft-v1.md. On the first call it asks the user once how to chunk the work (per-Part / two-Parts / all-at-once) and persists that choice."
allowed-tools: Read, Write, Edit, Bash, AskUserQuestion
user_invocable: true
---

# 구조 설계 + 초안 작성

이 스킬은 2단계를 순서대로 수행한다.

## 시작 전 준비

`user-book-toc.md`를 읽고 다음을 파악한다:
- 기본 정보: 제목, 필명, 독자 지칭, 기준 연도
- 페르소나: 캐릭터와 말투를 숙지하고 그 목소리로 글을 쓴다
- 목차: 각 장/활용법의 구조
- 활용법 세부 가이드 / 공통 작성 가이드

## 활성 폴더 결정

이 스킬은 `/research`가 만든 폴더를 사용한다. `draft/` 하위 폴더 중 사전순 가장 최신 폴더를 활성으로 선택한다.

```bash
ACTIVE=$(ls -1d draft/*/ 2>/dev/null | sort | tail -n 1)
ACTIVE="${ACTIVE%/}"
[ -z "${ACTIVE}" ] && { echo "활성 폴더 없음. /research를 먼저 실행하세요."; exit 1; }
echo "활성 프로젝트 폴더: ${ACTIVE}"
```

이후 모든 경로는 `{ACTIVE}`로 표기한다.

## 세션 설정 (청크 단위 — 첫 호출에만 묻는다)

이 책의 작업 방식은 `{ACTIVE}/_session-config.json`에 저장된다. 같은 폴더에서 `/write`를 다시 호출하면 이 설정을 따르고 **다시 묻지 않는다**.

### 결정 로직

```
1) {ACTIVE}/_session-config.json 존재?
   YES → 설정을 읽어 그대로 진행 (재질문 없음)
   NO  → 사용자에게 한 번 묻고, 답을 _session-config.json에 저장한 뒤 진행
```

### 첫 호출 시 사용자에게 물어볼 질문

`AskUserQuestion` 도구를 호출해 다음 1개 질문을 던진다.

- 질문: "초안을 어떤 단위로 작성할까요?"
- 옵션 (multiSelect: false):
  1. **부 단위로 끊기 (권장)** — 프롤로그·각 부·에필로그·부록을 한 번씩 끊고, 사용자가 다음 `/write`를 다시 호출해야 진행. 컨텍스트 폭주 위험이 가장 낮다.
  2. **2부씩 묶어서** — 두 부를 한 번에 작성하고 다음 호출에서 다음 두 부 진행. 호흡이 더 빠르다.
  3. **모두 한 번에 진행** — 멈추지 않고 프롤로그부터 부록까지 끝까지 작성. 추가 입력 없이 끝까지 돌린다. 분량이 큰 책은 컨텍스트 폭주 가능성이 있어 주의.

답변은 다음 키로 매핑한다.
- 1번 → `chunk_unit: "part"`,    `auto_continue: false`
- 2번 → `chunk_unit: "two_parts"`, `auto_continue: false`
- 3번 → `chunk_unit: "part"`,    `auto_continue: true` (Part별 파일은 그대로 만들되 멈추지 않고 끝까지 작성)

설정을 저장한다:

```bash
cat > "${ACTIVE}/_session-config.json" <<JSON
{
  "chunk_unit": "part",
  "auto_continue": false,
  "decided_at": "$(date -u +%Y-%m-%dT%H:%M:%SZ)",
  "decided_by": "user"
}
JSON
```

저장 후 사용자에게 한 줄로 알린다:
```
세션 설정 저장: chunk_unit=part, auto_continue=false ({ACTIVE}/_session-config.json)
이후 /write 호출은 이 설정을 따릅니다. 변경하려면 _session-config.json을 직접 편집하거나 삭제하세요.
```

## 이어하기 로직 (상태 마커 기반)

각 산출 파일 마지막 줄의 `<!-- STAGE_COMPLETE: ... -->` 마커 유무로 단계를 판정한다.

```
01_research-notes.md 마커 있음, 02 없음                  → 1단계(구조 설계)부터
02_outline.md 마커 있음, 03 없음                         → 2단계(초안 작성)부터
03_draft-v1.md 존재하지만 마커 없음                       → 2단계 이어쓰기 (append)
03_draft-v1.md 마커 있음                                 → 완료. "/review로 리뷰를 시작하세요"
```

감지된 시작 지점을 사용자에게 한 줄로 알린 뒤 작업을 시작한다.

## 1단계: 구조 설계

`{ACTIVE}/01_research-notes.md`를 읽고 문서의 전체 구조를 설계한다.

- `user-book-toc.md`의 목차를 기반으로 각 장의 세부 구조를 설계한다
- 리서치 결과에서 각 장에 배치할 핵심 내용을 매핑한다
- 각 부의 분량 배분을 설계한다 (목표 분량 기준)
- 장 간 연결 흐름(브릿지)을 설계한다
- 1부 캐릭터의 등장 포인트를 설계한다
- `{ACTIVE}/02_outline.md`로 저장한다
- 마지막 줄에 `<!-- STAGE_COMPLETE: 02_outline -->` 추가

## 2단계: 초안 작성 (청크 전략)

`{ACTIVE}/02_outline.md`를 기반으로 프롤로그, 본문, 에필로그, 부록을 작성한다.

### 청크 규칙 (공통)

1. **Part 파일 분리**: 프롤로그·각 부·에필로그·부록을 각각 다른 파일로 쓴다
   - `{ACTIVE}/03_draft-v1_prologue.md`
   - `{ACTIVE}/03_draft-v1_part1.md` ~ `{ACTIVE}/03_draft-v1_partN.md`
   - `{ACTIVE}/03_draft-v1_epilogue.md`
   - `{ACTIVE}/03_draft-v1_appendix.md`
2. 각 Part 작성이 끝나면 그 파일 마지막에 마커를 단다:
   ```
   <!-- STAGE_COMPLETE: 03_draft-v1_partN -->
   ```
3. 모든 Part가 완성된 뒤(모두 마커 보유), 순서대로 이어붙여 `{ACTIVE}/03_draft-v1.md`를 생성하고 마지막 줄에 `<!-- STAGE_COMPLETE: 03_draft-v1 -->` 추가
4. 대화가 중간에 끊기면, 마커 없는 Part 파일을 찾아 그 파일 끝부터 append로 이어 쓴다 (절대 덮어쓰지 않는다)

### 청크 단위별 동작

`_session-config.json`의 `chunk_unit`과 `auto_continue` 조합에 따라 한 번의 `/write` 호출에서 작성하는 범위가 달라진다.

| chunk_unit | auto_continue | 한 번의 호출에서 작성하는 범위 |
|------------|---------------|--------------------------------|
| `part` | `false` (기본값, 권장) | 마커 없는 Part 1개를 처음부터 끝까지 작성하고 멈춘다 |
| `two_parts` | `false` | 마커 없는 Part 2개를 연속 작성하고 멈춘다 |
| `part` | `true` (모두 진행) | 마커 없는 Part부터 시작해 모든 Part 완료까지 멈추지 않는다. 마지막에 03_draft-v1.md 병합도 자동 |

`auto_continue: false`인 경우, 한 번의 호출이 끝나면 사용자에게 안내한다:
```
Part N 작성 완료. /write로 다음 Part를 작성하세요.
(남은 Part: prologue, part2, part3, ..., epilogue, appendix)
```

`auto_continue: true`인 경우, 호출 한 번에 끝까지 가고 마지막에 안내한다:
```
모든 Part 작성 완료. 03_draft-v1.md로 병합 ✅
초안 작성 완료. /review로 리뷰 사이클을 시작하세요.
```

### 작성 원칙

- CLAUDE.md의 작성 규칙과 `user-book-toc.md`의 작성 스타일을 모두 준수한다
- 페르소나(말투, 어미, 어휘)를 처음부터 끝까지 일관되게 유지한다
- em dash(—, –)는 절대 쓰지 않는다
- 어미는 해라체로 통일한다 (인용·프롬프트 예시 제외)

## 완료 처리

`{ACTIVE}/03_draft-v1.md`가 완성되고 마커가 달리면 사용자에게 한 줄로 안내한다:
```
초안 작성 완료. /review로 리뷰 사이클을 시작하세요.
```

# CHANGELOG

이 프로젝트(book-writer 하네스)의 버전별 변경 사항을 기록한다. 본문(특정 책의 원고)이 아니라 **하네스 자체**의 변화를 추적한다.

## [1.2.0] — 2026-05-04

### 변경
- `book-toc.md` → `user-book-toc.md`로 이름 변경 (사용자가 직접 편집하는 파일임을 명시)
- 위치: `.claude/book-toc.md` (시스템 폴더) → 프로젝트 **루트** (사용자 가시성 향상)
- 모든 참조 경로 업데이트: CLAUDE.md, 4개 스킬, README, verify.py, fixture
- `.claude/book-toc.md`는 redirect stub만 유지 (호환성, 다음 메이저에서 제거 예정)
- fixture: `tests/fixtures/mini-book-toc.md` → `mini-user-book-toc.md`

### 영향
- 사용자가 레포 클론 직후 루트의 `user-book-toc.md`를 즉시 발견 가능
- 기존 사용자: `.claude/book-toc.md`를 새 위치로 옮긴 뒤 stub 삭제 (또는 stub 무시)

## [1.1.0] — 2026-05-04

### 변경
- `/write`에 청크 단위 1회 질의 도입 (`AskUserQuestion`). 첫 호출에서만 묻고 답을 `{ACTIVE}/_session-config.json`에 영속화. "모두 진행" 선택 시 사람 개입 없이 끝까지 자동 작성
- `cover` 스킬 제거 (deprecated stub만 유지). 표지는 외부 도구·디자이너에 위임. 핵심 스킬 5개 → 4개로 축소

### 영향
- README.md, CLAUDE.md의 워크플로우 표·폴더 트리에서 cover 관련 라인 모두 제거
- `output/{ACTIVE}/cover_concept.md`, `cover_a.png`, `cover_b.png` 산출물 더 이상 생성 안 함
- 기존 책 작업의 호환성에는 영향 없음 (cover.md를 호출하던 사용자는 외부 대안으로 이동)

## [1.0.0] — 2026-05-04

### 추가
- `.claude-plugin/plugin.json`: 플러그인 매니페스트. fork-and-edit 템플릿에서 진짜 재사용 자산으로 전환
- `tests/verify.py`: 단일 진실(single source of truth) 검증기. publish.md가 직접 호출
- `tests/run-smoke.sh`: 통과·실패 fixture 2개로 verifier가 정상 동작하는지 검증
- `tests/fixtures/`: mini-user-book-toc.md / pass-draft-final.md / fail-draft-final.md
- 출처 신뢰도 등급(Tier 1/2/3) — `research.md`, `CLAUDE.md`
- `01_citations.json` 출력 — 인용 추적용 (research.md)
- 변경 로그 표준 — CLAUDE.md "변경 로그 표준" 섹션
- 백업 정책 — CLAUDE.md "백업 정책" 섹션 (3가지 트리거)
- 자가 채점 (10점 만점) — verify.py 출력에 포함, anchor는 CLAUDE.md
- 합평 독립 채점 보장 — review.md "Anchor Bias 방지" 섹션
- 마케터 리뷰 → 메타데이터 매핑 표 — publish.md 3단계
- 검증 항목 추가: 불릿 부호 통일(●, ▪), 영어 표현 과다("Before/After")

### 변경
- 모든 산출물 폴더가 **날짜 기반 활성 폴더**(`draft/YYYYMMDD/`, 충돌 시 `_NN`)로 이동
- 산출물 명명 규칙: `01_research-notes.md` ~ `14_review-proofreader.md` (번호 prefix 통일)
- 상태 마커(`<!-- STAGE_COMPLETE: ... -->`) 도입으로 단계 완료 판정이 파일 존재 → 마커 유무 기반으로 변경
- `/write`의 청크 전략 명문화 (Part별 분리 후 병합)
- 모든 스킬 frontmatter에 `allowed-tools` 추가
- 모든 스킬 description에 trigger 패턴 보강

### 수정
- `draft/01_research-notes.md` 같은 절대 경로 → `draft/{ACTIVE}/01_research-notes.md`로 일관화
- 합평 5인 평가 항목 표 5개 모두 🔴/🟡 기준 명시
- 외부 리뷰 3인(편집자, 마케터, 프루프리더) 평가 항목 표 명시
- 공통 10점 anchor 표 도입 (모든 리뷰어 동일 기준)

### 평가 점수 (skill-creator 관점)
- 1차 평가: 7.2 / 10
- 1차 개선 후: 8.7 / 10
- 2차 개선 후: 10 / 10 (예상)

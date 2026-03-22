# AI 에이전트 팀으로 책 한 권 쓰기

> Claude Code + CLAUDE.md 하나로 176,000자 분량의 책을 처음부터 끝까지 만든 프로젝트입니다.
> 이 레포를 fork해서 CLAUDE.md만 바꾸면, 당신의 주제로 같은 과정을 재현할 수 있습니다.

## 이 프로젝트가 하는 일

CLAUDE.md 파일 하나에 **책의 주제, 에이전트 팀 구성, 작업 흐름, 품질 기준**을 정의해두면, Claude Code가 이를 읽고 16단계에 걸쳐 책 한 권을 만들어냅니다.

결과물: B5 판형 약 240페이지 분량의 Word 문서(.docx), PDF, 다이어그램 40개

이 프로젝트에서 실제로 만든 책은 **"노트북LM으로 다 됨: 팀장이 바로 쓰는 실전 활용법 20"** (저자: AI ROASTING)입니다.

## 핵심 아이디어: 에이전트 팀

혼자 쓰면 자기 글의 약점을 못 봅니다. 이 프로젝트는 **역할이 다른 6명의 에이전트**가 쓰고, 비평하고, 수정하는 구조로 이 문제를 해결합니다.

```
그린(리서처)  →  웹 검색으로 최신 정보 수집
실버(아키텍트) →  목차와 구조 설계
블랙(라이터)  →  전체 집필 및 수정 (유일한 필자)
레드(리뷰어)  →  냉정한 비평, 논리적 허점 지적
핑크(예상독자) →  타겟 독자 관점 리뷰
라이트(퍼블리셔) → Word 문서 변환, 서식, 다이어그램
```

최종 퍼블리싱 후에는 **외부 검증자 3명**(편집자, 마케터, 프루프리더)이 10점 만점으로 평가합니다.

## 작업 흐름 (16단계)

CLAUDE.md에 이 흐름이 모두 정의되어 있고, Claude Code가 단계별로 실행합니다.

```
[1회전: 초안 만들기]
 1  그린 리서치           → draft/research-notes.md
 2  실버 구조 설계        → draft/outline.md
 3  블랙 초안 작성        → draft/draft-v1.md

[2회전: 비평과 개선]
 4  레드 비평             → draft/review-red.md
 5  블랙 1차 수정         → draft/draft-v2.md

[3회전: 독자 검증]
 6  핑크 독자 리뷰        → draft/review-pink.md
 7  블랙 2차 수정         → draft/draft-v3.md

[합평: 전원 평가]
 8  합평 1라운드 (5명)    → draft/ensemble-review-1.md
 9  블랙 3차 수정         → draft/draft-v4.md
10  합평 2라운드 (5명)    → draft/ensemble-review-2.md
11  블랙 최종 반영        → draft/draft-final.md

[퍼블리싱]
12  라이트 Word 문서 생성 → output/NotebookLM_final.docx

[외부 검증]
13  편집자 평가           → draft/review-editor.md
14  마케터 평가           → draft/review-marketer.md
15  프루프리더 교정       → draft/review-proofreader.md
16  블랙 최종 보강        → draft/draft-final.md (갱신)
```

## 따라하는 법

### 1. 환경 준비

```bash
# 이 레포를 fork 또는 clone
git clone https://github.com/airoasting/notebooklm.git
cd notebooklm

# Python 의존성 설치 (Word 문서 생성용)
pip install python-docx matplotlib

# Claude Code 설치 (Anthropic 공식 CLI)
npm install -g @anthropic-ai/claude-code
```

### 2. CLAUDE.md 수정

CLAUDE.md를 열고 **당신의 책에 맞게** 아래 항목을 바꿉니다.

| 바꿀 항목 | 설명 | 예시 |
|-----------|------|------|
| 프로젝트 목표 | 책 제목, 대상 독자, 분량 | "직장인을 위한 ChatGPT 활용법" |
| 블랙의 페르소나 | 필자의 캐릭터, 말투, 필명 | "IT 컨설턴트 출신, 실전파" |
| 최종 산출물 구조 | 프롤로그, 부, 장, 에필로그, 부록 | 원하는 목차 구조 |
| 작성 규칙 | 문체, 금지 표현, 서식 규칙 | em dash 금지 등 |
| 품질 기준 | 분량, 페르소나 일관성, 필수 요소 | "각 장마다 핵심 정리 박스" |

에이전트 팀 구성(6명)과 작업 흐름(16단계)은 그대로 두어도 됩니다. 이 구조 자체가 품질을 보장하는 장치입니다.

### 3. 실행

```bash
# Claude Code 실행
claude

# 1단계부터 시작하라고 지시
> 1단계부터 시작해줘
```

분량이 많으므로 부(Part) 단위로 끊어서 진행하는 것을 권장합니다.

```
> 3단계 프롤로그와 1부를 작성해줘
> 이어서 2부를 작성해줘
> 4단계 레드 비평을 수행해줘
```

### 4. 주의사항

- **분량 관리**: 12만~15만 자 분량은 한 번에 생성되지 않습니다. 부 단위로 나눠 작성하고 이어붙이는 방식을 씁니다
- **컨텍스트 한계**: 대화가 길어지면 앞부분을 잊습니다. 새 대화를 시작하더라도 CLAUDE.md와 draft 파일을 읽으므로 이어서 작업할 수 있습니다
- **합평 기준**: 합평 2라운드에서 5명 평균 9점 이상이면 최종 퍼블리싱으로 넘어갑니다. 미달이면 재수정 후 합평을 1회 추가합니다 (최대 3라운드)
- **마케터 의견**: 마케터의 피드백은 참고만 하고 본문 수정에는 반영하지 않습니다

## 폴더 구조

```
.
├── CLAUDE.md                    # 이 파일이 전부입니다. 에이전트 팀, 작업 흐름, 품질 기준 정의
├── README.md
├── draft/                       # 원고 버전과 리뷰 (16단계의 모든 중간 산출물)
│   ├── research-notes.md
│   ├── outline.md
│   ├── draft-v1.md ~ draft-final.md
│   ├── review-red.md, review-pink.md
│   ├── ensemble-review-1.md, ensemble-review-2.md
│   ├── review-editor.md, review-marketer.md, review-proofreader.md
└── output/                      # 최종 산출물
    ├── NotebookLM_final.docx    # 최종 Word 문서
    ├── NotebookLM_final.pdf     # 최종 PDF
    ├── generate_docx.py         # Word 변환 스크립트
    ├── generate_images.py       # 다이어그램 생성 스크립트
    └── images/                  # 다이어그램 (matplotlib으로 생성)
```

## 이 구조가 효과적인 이유

1. **역할 분리**: 쓰는 사람(블랙)과 비평하는 사람(레드)을 분리하면, 자기 글의 약점이 보입니다
2. **다중 관점**: 전문가(레드)와 예상독자(핑크)의 관점이 다르기 때문에, 둘 다 거치면 "전문가에겐 정확하고 초보자에겐 쉬운" 글이 됩니다
3. **반복 개선**: v1 → v2 → v3 → v4 → final로 5번 수정하면서, 매번 다른 관점의 피드백이 반영됩니다
4. **품질 게이트**: 합평에서 9점 미만이면 통과하지 못합니다. 자동으로 품질 하한선이 보장됩니다
5. **외부 검증**: 내부 에이전트끼리의 합의만으로는 부족합니다. 편집자, 프루프리더라는 별도 페르소나가 출판 수준의 검수를 합니다

## 실제 결과

이 프로젝트에서 만든 책의 외부 검증 점수:

| 검증자 | 평가 점수 | 핵심 코멘트 |
|--------|:---------:|------------|
| 편집자 (20년차) | 8.56 / 10 | "비즈니스 실용서의 문법을 비틀어 스토리가 있는 실용서를 만들어냈다" |
| 마케터 (20년차) | 8.6 / 10 | "현시점 국내 AI 실무서 시장에서 가장 예리한 포지셔닝" |
| 프루프리더 (20년차) | 8.0 / 10 | "4,000줄 분량에서 이 정도의 톤 유지는 우수하다" |

## 기술 스택

| 용도 | 기술 |
|------|------|
| 에이전트 실행 | [Claude Code](https://claude.com/claude-code) (Anthropic) |
| 원고 형식 | Markdown |
| 문서 생성 | python-docx |
| 다이어그램 | matplotlib |
| 폰트 | Pretendard (대체: Malgun Gothic) |

## 라이선스

이 프로젝트의 콘텐츠(원고, 이미지)는 AI ROASTING에게 저작권이 있습니다.
CLAUDE.md의 구조와 작업 흐름은 자유롭게 참고하고 변형하여 사용할 수 있습니다.

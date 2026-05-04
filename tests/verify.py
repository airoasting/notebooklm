"""book-writing harness verifier — standalone copy used by /publish 1단계.
This file lives in tests/ as the canonical verifier so smoke tests can run it.
/publish copies (or references) this file when generating verify-report.md.
"""
import re, sys, pathlib

if len(sys.argv) != 4:
    print("usage: verify.py <draft-final.md> <user-book-toc.md> <verify-report.md>", file=sys.stderr)
    sys.exit(2)

SRC = pathlib.Path(sys.argv[1])
TOC = pathlib.Path(sys.argv[2])
REPORT = pathlib.Path(sys.argv[3])

text = SRC.read_text(encoding="utf-8")
toc = TOC.read_text(encoding="utf-8")

issues = []  # [(severity, category, detail)]

# 1) em dash 잔존
for m in re.finditer(r"[—–]", text):
    issues.append(("🔴", "em dash 잔존", f"위치 {m.start()}"))

# 2) ** 마크다운 잔존
for m in re.finditer(r"\*\*[^*\n]+\*\*", text):
    issues.append(("🔴", "마크다운 ** 잔존", m.group(0)[:30]))

# 3) [그림 N] 참조 수
fig_refs = re.findall(r"\[그림\s*(\d+)[^\]]*\]", text)
issues.append(("ℹ️", "[그림 N] 참조 수", str(len(fig_refs))))

# 4) 어미 통일성 (간이 검사)
total_sentences = len(re.findall(r"[.!?]", text))
hapsoche = len(re.findall(r"습니다[\.\?\!]", text))
if total_sentences and hapsoche / total_sentences > 0.05:
    issues.append(("🟡", "합쇼체 혼용 의심", f"{hapsoche}/{total_sentences} 문장"))

# 5) 분량 검증
char_count = len(re.sub(r"\s", "", text))
m = re.search(r"목표 분량.*?([\d,]+)\s*[~∼]\s*([\d,]+)\s*자", toc)
if m:
    lo = int(m.group(1).replace(",", ""))
    hi = int(m.group(2).replace(",", ""))
    if char_count < lo:
        issues.append(("🔴", "분량 미달", f"{char_count}자 < {lo}자 (목표 {lo}~{hi})"))
    else:
        issues.append(("ℹ️", "분량", f"{char_count}자 (목표 {lo}~{hi})"))
else:
    issues.append(("ℹ️", "분량", f"{char_count}자"))

# 6) 목차 헤딩 일치
expected_headings = []
for line in toc.splitlines():
    line = line.strip()
    if re.match(r"^제\s*\d+\s*장\.", line) or line.startswith("[활용법") \
       or line.startswith("프롤로그") or line.startswith("에필로그") or line.startswith("부록"):
        expected_headings.append(line.lstrip("- ").split(":")[0].strip())

for h in expected_headings:
    if h and h not in text:
        issues.append(("🔴", "목차 헤딩 누락", h))

# 7) 상태 마커 확인
if "<!-- STAGE_COMPLETE: 11_draft-final -->" not in text:
    issues.append(("🔴", "상태 마커 누락", "11_draft-final 미완료"))

# 8) 부 끝 브릿지
parts_in_toc = re.findall(r"제\s*(\d+)\s*부", toc)
unique_parts = sorted(set(int(n) for n in parts_in_toc))
for n in unique_parts:
    if (f"{n}부를 마치며" not in text and
        f"제{n}부를 마치며" not in text and
        f"제 {n}부를 마치며" not in text):
        issues.append(("🟡", "브릿지 문단 누락 의심", f"{n}부 마치며"))

# 9) 용어 통일 — "커스텀 지시" 사용 금지
if "커스텀 지시" in text:
    issues.append(("🔴", "용어 위반", "'커스텀 지시' → '맞춤 지시'"))

# 10) 불릿 부호 — • 외 사용 (●, ▪) 검사
forbidden_bullets = ["●", "▪"]
for sym in forbidden_bullets:
    if sym in text:
        issues.append(("🟡", "불릿 부호 비통일", f"'{sym}' 사용"))

# 11) 영어 단독 표현 비율 (간이): "Before" / "After" 단독 사용
for w in ["Before/After", "Before / After"]:
    if w in text:
        issues.append(("🟡", "영어 표현 과다", f"'{w}' → '사용 전/후'"))

# 12) 자가 채점 (10점 만점)
red = sum(1 for s,_,_ in issues if s == "🔴")
yellow = sum(1 for s,_,_ in issues if s == "🟡")
info = sum(1 for s,_,_ in issues if s == "ℹ️")

if red == 0 and yellow == 0:
    score = 10
elif red == 0 and yellow <= 2:
    score = 9
elif red == 0 and yellow <= 5:
    score = 8
elif red == 1 or yellow <= 10:
    score = 7
elif red == 2 or yellow <= 15:
    score = 6
else:
    score = max(1, 5 - max(0, red-3))

# 보고서 출력
lines = [
    "# verify-report",
    "",
    f"- 🔴 필수: {red}건",
    f"- 🟡 권장: {yellow}건",
    f"- ℹ️ 정보: {info}건",
    f"- **자가 채점: {score} / 10**",
    "",
    "## 상세",
]
for s, cat, detail in issues:
    lines.append(f"- {s} **{cat}** — {detail}")

REPORT.write_text("\n".join(lines), encoding="utf-8")
print(f"verify done: 🔴 {red}, 🟡 {yellow}, ℹ️ {info}, score={score}/10")
sys.exit(1 if red > 0 else 0)

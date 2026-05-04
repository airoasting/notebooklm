#!/usr/bin/env bash
# 스모크 테스트: verify.py가 정상 입력은 통과(exit 0), 위반 입력은 실패(exit 1)시키는지 검사한다.
# 실행 방법: bash tests/run-smoke.sh
set -e
cd "$(dirname "$0")/.."

PASS=0
FAIL=0

echo "[1/2] PASS fixture (위반 없음 → exit 0 기대)"
if python3 tests/verify.py tests/fixtures/pass-draft-final.md tests/fixtures/mini-user-book-toc.md /tmp/_pass-report.md; then
  echo "  ✅ pass fixture exit 0 (정상)"
  PASS=$((PASS+1))
else
  echo "  ❌ pass fixture exit 1 (예상 외)"
  cat /tmp/_pass-report.md
  FAIL=$((FAIL+1))
fi

echo ""
echo "[2/2] FAIL fixture (위반 다수 → exit 1 기대)"
if python3 tests/verify.py tests/fixtures/fail-draft-final.md tests/fixtures/mini-user-book-toc.md /tmp/_fail-report.md; then
  echo "  ❌ fail fixture exit 0 (예상 외 - 위반을 못 잡음)"
  cat /tmp/_fail-report.md
  FAIL=$((FAIL+1))
else
  echo "  ✅ fail fixture exit 1 (정상 - 위반을 잡았다)"
  PASS=$((PASS+1))
fi

echo ""
echo "============================="
echo "smoke test: PASS=$PASS, FAIL=$FAIL"
echo "============================="
[ $FAIL -eq 0 ]

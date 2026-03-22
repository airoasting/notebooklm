#!/usr/bin/env python3
"""
39개 그림을 matplotlib으로 생성하여 images/ 폴더에 저장
"""
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import matplotlib.font_manager as fm
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch
import numpy as np
import os

# ─── 설정 ───
BASE_DIR = "/Users/jaydenkang/Desktop/New Projects/20260321_노트북LM 책쓰기"
IMG_DIR = os.path.join(BASE_DIR, "output", "images")
os.makedirs(IMG_DIR, exist_ok=True)

# 폰트 등록
font_path = os.path.join(BASE_DIR, "font", "Pretendard-Regular.otf")
bold_path = os.path.join(BASE_DIR, "font", "Pretendard-Bold.otf")
fm.fontManager.addfont(font_path)
fm.fontManager.addfont(bold_path)
plt.rcParams['font.family'] = 'Pretendard'
plt.rcParams['axes.unicode_minus'] = False

# 색상 팔레트
C_DARK = '#1F4E79'
C_MED = '#2E75B6'
C_LIGHT = '#D6E8F7'
C_BG = '#F8FAFB'
C_ACCENT = '#E8F0FE'
C_ORANGE = '#E67E22'
C_GREEN = '#27AE60'
C_RED = '#E74C3C'
C_GRAY = '#7F8C8D'
C_WHITE = '#FFFFFF'


def save_fig(fig, num):
    path = os.path.join(IMG_DIR, f"fig{num:02d}.png")
    fig.savefig(path, dpi=200, bbox_inches='tight', facecolor=C_BG, edgecolor='none')
    plt.close(fig)
    print(f"  fig{num:02d}.png saved")
    return path


def add_rounded_box(ax, x, y, w, h, text, color=C_MED, text_color=C_WHITE, fontsize=17, bold=False):
    """둥근 모서리 박스 + 텍스트"""
    box = FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.1",
                          facecolor=color, edgecolor='none', alpha=0.95)
    ax.add_patch(box)
    weight = 'bold' if bold else 'normal'
    ax.text(x + w/2, y + h/2, text, ha='center', va='center',
            fontsize=fontsize, color=text_color, weight=weight, wrap=True)


def add_arrow(ax, x1, y1, x2, y2, color=C_GRAY):
    ax.annotate('', xy=(x2, y2), xytext=(x1, y1),
                arrowprops=dict(arrowstyle='->', color=color, lw=1.5))


def create_flow_chart(num, title, steps, subtitle=""):
    """범용 플로우차트 생성"""
    n = len(steps)
    fig, ax = plt.subplots(1, 1, figsize=(12, 3.5))
    ax.set_xlim(-0.5, n * 2.5 + 0.5)
    ax.set_ylim(-0.5, 2.5)
    ax.axis('off')
    fig.patch.set_facecolor(C_BG)

    ax.text(n * 2.5 / 2, 2.2, title, ha='center', va='center',
            fontsize=21, color=C_DARK, weight='bold')

    for i, step in enumerate(steps):
        x = i * 2.5 + 0.5
        add_rounded_box(ax, x, 0.3, 2.0, 1.2, step, color=C_MED if i % 2 == 0 else C_DARK)
        if i < n - 1:
            add_arrow(ax, x + 2.0, 0.9, x + 2.5, 0.9, color=C_ORANGE)

    if subtitle:
        ax.text(n * 2.5 / 2, -0.2, subtitle, ha='center', va='center',
                fontsize=17, color=C_GRAY, style='italic')

    return save_fig(fig, num)


def create_comparison(num, title, left_title, left_items, right_title, right_items):
    """Before/After 비교 차트"""
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))
    fig.patch.set_facecolor(C_BG)
    fig.suptitle(title, fontsize=21, color=C_DARK, weight='bold', y=0.98)

    for ax, t, items, color, badge in [(ax1, left_title, left_items, C_RED, 'Before'),
                                        (ax2, right_title, right_items, C_GREEN, 'After')]:
        ax.set_xlim(0, 10)
        ax.set_ylim(0, len(items) + 2)
        ax.axis('off')
        ax.set_facecolor(C_BG)

        # 배지
        badge_color = '#FADBD8' if badge == 'Before' else '#D5F5E3'
        badge_text_color = C_RED if badge == 'Before' else C_GREEN
        ax.add_patch(FancyBboxPatch((0.5, len(items) + 0.5), 9, 1, boxstyle="round,pad=0.15",
                                     facecolor=badge_color, edgecolor='none'))
        ax.text(5, len(items) + 1, f"{badge}: {t}", ha='center', va='center',
                fontsize=19, color=badge_text_color, weight='bold')

        for j, item in enumerate(items):
            y = len(items) - j - 0.3
            ax.add_patch(FancyBboxPatch((0.5, y - 0.3), 9, 0.7, boxstyle="round,pad=0.08",
                                         facecolor=C_WHITE, edgecolor='#DDD', linewidth=0.5))
            ax.text(1, y, item, ha='left', va='center', fontsize=16, color='#333')

    plt.tight_layout(rect=[0, 0, 1, 0.95])
    return save_fig(fig, num)


def create_venn_like(num, title, items):
    """벤 다이어그램 스타일"""
    fig, ax = plt.subplots(1, 1, figsize=(10, 6))
    ax.set_xlim(-4, 4)
    ax.set_ylim(-3, 4)
    ax.axis('off')
    fig.patch.set_facecolor(C_BG)
    ax.text(0, 3.5, title, ha='center', va='center', fontsize=21, color=C_DARK, weight='bold')

    positions = [(-2.2, 0.5), (0, 0.5), (2.2, 0.5)]
    colors = [('#3498DB', 0.2), ('#E74C3C', 0.2), ('#2ECC71', 0.2)]
    for (name, desc), (x, y), (c, a) in zip(items, positions, colors):
        circle = plt.Circle((x, y), 1.5, facecolor=c, alpha=a, edgecolor=c, linewidth=2)
        ax.add_patch(circle)
        ax.text(x, y + 0.3, name, ha='center', va='center', fontsize=19, color=c, weight='bold')
        ax.text(x, y - 0.3, desc, ha='center', va='center', fontsize=16, color='#555')

    return save_fig(fig, num)


def create_pyramid(num, title, levels):
    """피라미드 차트"""
    fig, ax = plt.subplots(1, 1, figsize=(10, 6))
    ax.set_xlim(-5, 5)
    ax.set_ylim(-0.5, len(levels) + 0.5)
    ax.axis('off')
    fig.patch.set_facecolor(C_BG)
    ax.text(0, len(levels) + 0.2, title, ha='center', va='center',
            fontsize=21, color=C_DARK, weight='bold')

    colors_list = ['#D6E8F7', '#A9CCE3', '#5DADE2', '#2E75B6']
    for i, (label, desc) in enumerate(levels):
        w = 3 + i * 1.5
        c = colors_list[i] if i < len(colors_list) else C_MED
        ax.add_patch(FancyBboxPatch((-w/2, i * 1.0), w, 0.8, boxstyle="round,pad=0.1",
                                     facecolor=c, edgecolor=C_WHITE, linewidth=1))
        ax.text(0, i * 1.0 + 0.4, f"{label}", ha='center', va='center',
                fontsize=18, color=C_DARK, weight='bold')
        ax.text(0, i * 1.0 + 0.1, desc, ha='center', va='center',
                fontsize=16, color='#555')

    return save_fig(fig, num)


def create_ui_mock(num, title, panels):
    """UI 모킹 (3패널 레이아웃)"""
    fig, axes = plt.subplots(1, 3, figsize=(12, 5),
                              gridspec_kw={'width_ratios': [1, 2, 1]})
    fig.patch.set_facecolor(C_BG)
    fig.suptitle(title, fontsize=21, color=C_DARK, weight='bold', y=0.98)

    colors = ['#E8F0FE', '#F8F9FA', '#E8F0FE']
    for ax, (panel_title, panel_items), color in zip(axes, panels, colors):
        ax.set_xlim(0, 10)
        ax.set_ylim(0, 10)
        ax.axis('off')
        ax.set_facecolor(color)
        ax.add_patch(patches.Rectangle((0, 0), 10, 10, fill=True, facecolor=color,
                                        edgecolor='#CCC', linewidth=1))
        ax.text(5, 9, panel_title, ha='center', va='center', fontsize=18,
                color=C_DARK, weight='bold')
        for j, item in enumerate(panel_items):
            ax.text(1, 7.5 - j * 1.2, f"  {item}", ha='left', va='center',
                    fontsize=16, color='#444')

    plt.tight_layout(rect=[0, 0, 1, 0.93])
    return save_fig(fig, num)


def create_cycle(num, title, nodes, center_text=""):
    """순환 다이어그램"""
    fig, ax = plt.subplots(1, 1, figsize=(9, 9))
    ax.set_xlim(-4, 4)
    ax.set_ylim(-4, 4)
    ax.axis('off')
    fig.patch.set_facecolor(C_BG)
    ax.text(0, 3.5, title, ha='center', va='center', fontsize=21, color=C_DARK, weight='bold')

    n = len(nodes)
    r = 2.2
    for i, (label, desc) in enumerate(nodes):
        angle = 90 - i * (360 / n)
        rad = np.radians(angle)
        x, y = r * np.cos(rad), r * np.sin(rad)
        ax.add_patch(plt.Circle((x, y), 0.85, facecolor=C_MED, alpha=0.9, edgecolor=C_WHITE, linewidth=2))
        ax.text(x, y + 0.1, label, ha='center', va='center', fontsize=17, color=C_WHITE, weight='bold')
        ax.text(x, y - 0.25, desc, ha='center', va='center', fontsize=15, color='#E0E0E0')

        # 화살표
        next_i = (i + 1) % n
        next_angle = 90 - next_i * (360 / n)
        next_rad = np.radians(next_angle)
        x2, y2 = r * np.cos(next_rad), r * np.sin(next_rad)
        mid_angle = (angle + next_angle) / 2
        if abs(angle - next_angle) > 180:
            mid_angle += 180
        ax.annotate('', xy=(x2 + 0.5 * (x - x2), y2 + 0.5 * (y - y2)),
                    xytext=(x + 0.5 * (x2 - x), y + 0.5 * (y2 - y)),
                    arrowprops=dict(arrowstyle='->', color=C_ORANGE, lw=2))

    if center_text:
        ax.text(0, 0, center_text, ha='center', va='center', fontsize=18, color=C_DARK, weight='bold')

    return save_fig(fig, num)


def create_card_grid(num, title, cards):
    """카드 그리드 (2x2 또는 1xN)"""
    n = len(cards)
    cols = min(n, 4)
    rows = (n + cols - 1) // cols
    fig, axes = plt.subplots(rows, cols, figsize=(cols * 3.5, rows * 3))
    fig.patch.set_facecolor(C_BG)
    fig.suptitle(title, fontsize=21, color=C_DARK, weight='bold', y=1.0)

    if n == 1:
        axes = [axes]
    elif rows == 1:
        axes = list(axes)
    else:
        axes = [ax for row in axes for ax in row]

    card_colors = [C_MED, C_DARK, '#2ECC71', C_ORANGE, '#9B59B6', '#1ABC9C']
    for i, (card_title, card_desc) in enumerate(cards):
        if i < len(axes):
            ax = axes[i]
            ax.set_xlim(0, 10)
            ax.set_ylim(0, 6)
            ax.axis('off')
            c = card_colors[i % len(card_colors)]
            ax.add_patch(FancyBboxPatch((0.3, 0.3), 9.4, 5.4, boxstyle="round,pad=0.2",
                                         facecolor=C_WHITE, edgecolor=c, linewidth=2))
            ax.add_patch(FancyBboxPatch((0.3, 4.0), 9.4, 1.7, boxstyle="round,pad=0.2",
                                         facecolor=c, edgecolor='none'))
            ax.text(5, 4.8, card_title, ha='center', va='center',
                    fontsize=17, color=C_WHITE, weight='bold')
            ax.text(5, 2.2, card_desc, ha='center', va='center',
                    fontsize=15, color='#444', wrap=True)

    # 남는 축 숨기기
    for i in range(n, len(axes)):
        axes[i].axis('off')

    plt.tight_layout(rect=[0, 0, 1, 0.95])
    return save_fig(fig, num)


def create_timeline(num, title, events):
    """타임라인 차트"""
    fig, ax = plt.subplots(1, 1, figsize=(12, 4))
    ax.set_xlim(-1, len(events) * 2 + 1)
    ax.set_ylim(-1.5, 2.5)
    ax.axis('off')
    fig.patch.set_facecolor(C_BG)
    ax.text(len(events), 2.2, title, ha='center', va='center',
            fontsize=21, color=C_DARK, weight='bold')

    # 중앙선
    ax.plot([0, len(events) * 2], [0.5, 0.5], color=C_MED, lw=2, zorder=1)

    for i, (time_label, desc) in enumerate(events):
        x = i * 2 + 0.5
        ax.plot(x, 0.5, 'o', color=C_DARK, markersize=10, zorder=2)
        ax.text(x, 1.3, time_label, ha='center', va='center', fontsize=17,
                color=C_DARK, weight='bold')
        ax.text(x, -0.3, desc, ha='center', va='center', fontsize=16,
                color='#555', wrap=True)

    return save_fig(fig, num)


# ═══════════════════════════════════════════════════════
# 40개 그림 생성
# ═══════════════════════════════════════════════════════

print("=" * 50)
print("그림 생성 시작 (40개)")
print("=" * 50)

# 그림 1: 이 책의 구성 가이드맵 (세로 레이아웃)
fig, ax = plt.subplots(1, 1, figsize=(10, 14))
ax.set_xlim(0, 10)
ax.set_ylim(-0.5, 13.5)
ax.axis('off')
fig.patch.set_facecolor(C_BG)
ax.text(5, 13, '이 책의 구성 가이드맵', ha='center', va='center',
        fontsize=24, color=C_DARK, weight='bold')
_sections = [
    ('프롤로그', '일하는 방식, 노트북LM 이전과 이후로 나뉩니다', '#8E44AD'),
    ('제1부', '고수는 이렇게 씁니다 (4명의 실전 사례)', '#2E75B6'),
    ('제2부', '오늘 점심, 딱 한 번만 따라 하세요 (시작 가이드)', '#2E75B6'),
    ('제3부', '분석과 검증의 기술 (활용법 01~05)', '#1F4E79'),
    ('제4부', '혼자 소화하는 기술 (활용법 06~08)', '#1F4E79'),
    ('제5부', '남에게 보여주는 기술 (활용법 09~11)', '#1F4E79'),
    ('제6부', '월요일 아침부터 바로 쓰는 실전 시나리오 (활용법 12~16)', '#1F4E79'),
    ('제7부', '나에서 팀으로, 도구에서 시스템으로 (활용법 17~20)', '#1F4E79'),
    ('에필로그', '지금 노트북을 여십시오', '#8E44AD'),
    ('부록', '프롬프트 템플릿, FAQ, 업데이트 가이드', '#7F8C8D'),
]
_n = len(_sections)
_bh, _gap = 0.85, 0.35
_sy = 12 - 0.3
for _i, (_label, _desc, _color) in enumerate(_sections):
    _y = _sy - _i * (_bh + _gap)
    ax.add_patch(FancyBboxPatch((0.5, _y), 2.0, _bh, boxstyle='round,pad=0.08',
                  facecolor=_color, edgecolor='none', alpha=0.95))
    ax.text(1.5, _y + _bh/2, _label, ha='center', va='center',
            fontsize=17, color='#FFFFFF', weight='bold')
    ax.text(3.0, _y + _bh/2, _desc, ha='left', va='center',
            fontsize=16, color='#333333')
    if _i < _n - 1:
        ax.annotate('', xy=(1.5, _y - _gap), xytext=(1.5, _y),
                    arrowprops=dict(arrowstyle='->', color=C_ORANGE, lw=2.5))
save_fig(fig, 1)

# 그림 2: Before/After 팀장의 하루
create_comparison(2, "팀장의 하루: 노트북LM 전 vs 후",
    "노트북LM 없이", [
        "8:47  메일에서 보고서 200p 수신",
        "9:00  Ctrl+F로 키워드 검색 반복",
        "10:30 엑셀에 요점 수기 정리",
        "12:00 점심 건너뛰고 계속 읽기",
        "15:00 요약 작성 시작",
        "17:30 퇴근 포기, 야근 돌입",
    ],
    "노트북LM 활용", [
        "8:47  메일에서 보고서 200p 수신",
        "8:50  PDF를 노트북LM에 업로드",
        "8:52  '우리 팀 관련 부분만 정리해줘'",
        "8:57  핵심 요약 노트 저장 완료",
        "9:00  팀 회의에서 브리핑",
        "9:30  다른 업무 시작, 정시 퇴근",
    ])

# 그림 3: 세 보고서 비교 플로우차트
create_flow_chart(3, "세 개 보고서가 하나의 비교표로",
    ["영업팀\n보고서\n(48p)", "마케팅팀\n보고서\n(35p)", "개발팀\n보고서\n(62p)", "노트북LM\n교차 비교", "통합\n비교표"],
    "145페이지를 직접 읽지 않고, 5분 만에 핵심 비교 완료")

# 그림 4: 회의 녹음 → 액션 아이템 워크플로우
create_flow_chart(4, "회의 녹음에서 액션 아이템까지",
    ["75분 회의\n녹음(MP3)", "노트북LM\n업로드", "AI 분석\n(음성→텍스트)", "회의록\n자동 생성", "액션 아이템\n표 추출"],
    "회의 끝나고 5분이면 담당자별 할 일이 정리된다")

# 그림 5: 설문 → 인사이트 다이어그램
create_flow_chart(5, "설문 데이터에서 인사이트까지",
    ["서술형 응답\n387건", "PDF 변환\n소스 업로드", "감정 분석\n패턴 추출", "상위 불만\n5개 도출", "인사이트\n보고서"],
    "이틀 걸리던 분석이 30분으로 줄어든다")

# 그림 6: 세 도구 비교 벤 다이어그램
create_venn_like(6, "ChatGPT vs Perplexity vs 노트북LM",
    [("ChatGPT", "인터넷 전체\n학습 데이터"),
     ("Perplexity", "실시간\n웹 검색"),
     ("노트북LM", "내가 올린\n자료만")])

# 그림 7: 세 도구 역할 분담
create_card_grid(7, "세 도구의 역할 분담: 경쟁이 아니라 팀플레이",
    [("ChatGPT", "창의적 글쓰기\n아이디어 발상\n코드 생성"),
     ("Perplexity", "최신 정보 검색\n실시간 팩트체크\n출처 인용"),
     ("노트북LM", "내 자료 분석\n환각 최소화\n멀티미디어 변환")])

# 그림 8: 플랜별 피라미드
create_pyramid(8, "노트북LM 플랜별 핵심 기능",
    [("Free", "노트북 100개, 소스 50개, Audio 3개/일"),
     ("Plus ($19.99)", "노트북 200개, 소스 100개, 확대된 한도"),
     ("Pro ($49.99)", "노트북 500개, 소스 300개, Deep Research"),
     ("Ultra ($249.99)", "소스 600개, Cinematic Video, 워터마크 제거")])

# 그림 9: 가입 3단계
create_flow_chart(9, "노트북LM 시작하기: 3단계",
    ["Google 계정\n로그인", "notebooklm.google\n접속", "새 노트북\n만들기"],
    "1분이면 충분하다")

# 그림 10: 인터페이스 3구역
create_ui_mock(10, "노트북LM 인터페이스: 세 구역",
    [("소스 패널", ["PDF 보고서.pdf", "경쟁사 분석.pdf", "회의 녹음.mp3", "시장 조사.url", "+ 소스 추가"]),
     ("채팅 패널", ["AI: 안녕하세요!", "나: 이 보고서의 핵심 3가지는?", "AI: 1. 시장 규모 확대...", "AI: 2. 경쟁 심화...", "AI: 3. 신기술 도입..."]),
     ("스튜디오 패널", ["Audio Overview", "Video Overview", "슬라이드", "인포그래픽", "마인드맵"])])

# 그림 11: 소스 유형 카드
create_card_grid(11, "노트북LM이 읽을 수 있는 10가지 소스",
    [("PDF", "보고서, 논문, 제안서"),
     ("YouTube", "세미나, 경쟁사 발표"),
     ("오디오", "회의 녹음, 인터뷰"),
     ("Google Docs", "팀 공유 문서 (자동 동기화)"),
     ("웹 URL", "기사, 블로그, 레퍼런스"),
     ("이미지", "차트, 다이어그램")])

# 그림 12: 소스 → 첫 질문 → 결과 플로우
create_flow_chart(12, "소스 업로드에서 첫 결과까지",
    ["소스 추가\n클릭", "PDF\n업로드", "첫 질문\n입력", "AI 답변\n확인", "노트\n저장"],
    "10분이면 첫 결과물을 손에 쥔다")

# 그림 13: 소스-채팅-노트 순환
create_cycle(13, "소스, 채팅, 노트의 순환 구조",
    [("소스", "냉장고 재료"),
     ("채팅", "요리사와 대화"),
     ("노트", "완성된 레시피")],
    center_text="노트북LM")

# 그림 14: 교차 분석 비교
create_comparison(14, "2개 비교 vs 5개 이상 교차 분석",
    "2개 소스 비교", [
        "보고서 A의 핵심 주장",
        "보고서 B의 핵심 주장",
        "일치하는 부분",
        "차이나는 부분",
    ],
    "5개 이상 교차 분석", [
        "공통 키워드 추출",
        "빈도 기반 패턴 발견",
        "소스 간 상충 지점 식별",
        "종합 인사이트 도출",
    ])

# 그림 15: 2차 분석 워크플로우
create_flow_chart(15, "노트를 소스로 재활용하는 2차 분석",
    ["경쟁사 A\n분석 노트", "경쟁사 B\n분석 노트", "경쟁사 C\n분석 노트", "새 노트북에\n소스로 업로드", "종합 전략\n보고서"],
    "분석의 분석, 인사이트를 쌓아 올리는 기법")

# 그림 16: 맞춤 지시 비교
create_card_grid(16, "같은 소스, 다른 맞춤 지시 = 다른 결과",
    [("마케팅 컨설턴트", "전략적 관점에서\n시장 기회를 분석"),
     ("초등학생 설명", "쉬운 말로\n비유를 곁들여 설명"),
     ("표 중심 정리", "모든 답변을\n표와 글머리로 구조화"),
     ("임원 브리핑", "핵심만 3줄로\n숫자 근거 포함")])

# 그림 17: 출처 확인 스크린샷 모킹
create_flow_chart(17, "환각 잡기: 출처 번호 클릭으로 원문 확인",
    ["AI 답변\n읽기", "출처 번호\n[1] 클릭", "원문\n해당 위치\n이동", "내용\n대조 확인"],
    "출처를 확인하는 습관이 신뢰를 지킨다")

# 그림 18: 딥 리서치 플로우
create_flow_chart(18, "딥 리서치(Deep Research) 전체 플로우",
    ["사용자\n질문 입력", "리서치 계획\n자동 수립", "수백 개\n웹사이트\n탐색", "최대 50개\n소스 수집", "상세 보고서\n자동 생성"],
    "소스 밖 정보까지 확장하는 유일한 기능")

# 그림 19: 오디오 오버뷰 카드
create_card_grid(19, "오디오 오버뷰(Audio Overview) 4가지 형식",
    [("Deep Dive", "6~15분\n포괄적 토론"),
     ("Brief", "1~2분\n간결한 개요"),
     ("Study Guide", "학습 포인트\n정리 중심"),
     ("Custom", "맞춤 지시로\n원하는 형식")])

# 그림 20: 비디오 오버뷰 모킹
create_ui_mock(20, "비디오 오버뷰(Video Overview) 재생 화면",
    [("비디오 컨트롤", ["재생/일시정지", "진행 바", "볼륨 조절", "전체 화면"]),
     ("영상 콘텐츠", ["슬라이드 형태의 시각 자료", "차트와 키워드 하이라이트", "AI 내레이션 음성", "자동 장면 전환"]),
     ("하단 정보", ["AI 내레이션 자막", "출처 표시", "챕터 구분", "다운로드 옵션"])])

# 그림 21: Video vs Cinematic 비교
create_comparison(21, "비디오 오버뷰 vs 시네마틱 비디오",
    "Video Overview (기본)", [
        "슬라이드 전환 방식",
        "텍스트 + 간단한 시각 자료",
        "모든 유료 플랜 사용 가능",
        "빠른 생성 속도",
    ],
    "Cinematic Video (2026)", [
        "완전 애니메이션 장면 전환",
        "Gemini 3 + Veo 3 활용",
        "Ultra 플랜 전용($249.99)",
        "영화 같은 시각 표현",
    ])

# 그림 22: 커스텀 지시 4종 비교
create_card_grid(22, "같은 소스, 4가지 커스텀 지시 = 4가지 결과",
    [("경영진 브리핑", "핵심 수치 3개\n전략적 시사점 중심"),
     ("팀원 교육용", "단계별 설명\n실습 예시 포함"),
     ("신입 온보딩", "기초 용어 설명\n쉬운 비유 사용"),
     ("고객 설명용", "전문 용어 제거\n혜택 중심 서술")])

# 그림 23: 마인드맵 예시
fig, ax = plt.subplots(1, 1, figsize=(8, 6))
ax.set_xlim(-5, 5)
ax.set_ylim(-4, 5)
ax.axis('off')
fig.patch.set_facecolor(C_BG)
ax.text(0, 4.5, "마인드맵: 복잡한 보고서를 한 장의 지도로", fontsize=13, ha='center', color=C_DARK, weight='bold')
# 중심
ax.add_patch(plt.Circle((0, 1), 1.0, facecolor=C_DARK, edgecolor=C_WHITE, linewidth=2))
ax.text(0, 1, "시장분석\n보고서", ha='center', va='center', fontsize=9, color=C_WHITE, weight='bold')
# 가지
branches = [("시장 규모", 2.5, 3), ("경쟁사 동향", -3, 2.5), ("소비자 트렌드", 3, -0.5),
            ("기술 변화", -2.5, -1.5), ("위험 요소", 0, -2.5)]
for label, bx, by in branches:
    ax.plot([0, bx], [1, by], color=C_MED, lw=2)
    ax.add_patch(plt.Circle((bx, by), 0.7, facecolor=C_MED, alpha=0.8, edgecolor=C_WHITE))
    ax.text(bx, by, label, ha='center', va='center', fontsize=7.5, color=C_WHITE, weight='bold')
save_fig(fig, 22)

# 그림 24: 마인드맵 2차 분석
create_flow_chart(24, "마인드맵 기반 2차 분석 워크플로우",
    ["소스 3개\n업로드", "마인드맵\n생성", "공통 키워드\n추출", "관심 가지\n심화 분석", "교차 비교\n보고서"],
    "숲을 본 다음 나무를 본다")

# 그림 25: 플래시카드 모킹
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10, 4))
fig.patch.set_facecolor(C_BG)
fig.suptitle("플래시카드 학습 화면", fontsize=13, color=C_DARK, weight='bold')
# 앞면
ax1.set_xlim(0, 10); ax1.set_ylim(0, 8); ax1.axis('off')
ax1.add_patch(FancyBboxPatch((0.5, 0.5), 9, 7, boxstyle="round,pad=0.3",
                               facecolor=C_WHITE, edgecolor=C_MED, linewidth=2))
ax1.text(5, 6, "Q", fontsize=20, ha='center', color=C_MED, weight='bold')
ax1.text(5, 4, "노트북LM의\n소스 기반 설계란?", ha='center', va='center',
         fontsize=11, color=C_DARK)
ax1.add_patch(FancyBboxPatch((1.5, 1), 3, 1.2, boxstyle="round,pad=0.1",
                               facecolor=C_GREEN, edgecolor='none'))
ax1.text(3, 1.6, "Got it", ha='center', va='center', fontsize=10, color=C_WHITE, weight='bold')
ax1.add_patch(FancyBboxPatch((5.5, 1), 3, 1.2, boxstyle="round,pad=0.1",
                               facecolor=C_RED, edgecolor='none'))
ax1.text(7, 1.6, "Missed it", ha='center', va='center', fontsize=10, color=C_WHITE, weight='bold')
# 뒷면
ax2.set_xlim(0, 10); ax2.set_ylim(0, 8); ax2.axis('off')
ax2.add_patch(FancyBboxPatch((0.5, 0.5), 9, 7, boxstyle="round,pad=0.3",
                               facecolor=C_ACCENT, edgecolor=C_MED, linewidth=2))
ax2.text(5, 6, "A", fontsize=20, ha='center', color=C_GREEN, weight='bold')
ax2.text(5, 3.5, "사용자가 업로드한 소스만\n참조하여 답변을 생성하는\n설계 방식. 환각을 최소화하고\n출처 추적이 가능하다.",
         ha='center', va='center', fontsize=10, color=C_DARK)
plt.tight_layout(rect=[0, 0, 1, 0.93])
save_fig(fig, 24)

# 그림 26: 퀴즈 모킹
fig, ax = plt.subplots(1, 1, figsize=(8, 5))
ax.set_xlim(0, 10); ax.set_ylim(0, 10); ax.axis('off')
fig.patch.set_facecolor(C_BG)
ax.add_patch(FancyBboxPatch((0.3, 0.3), 9.4, 9.4, boxstyle="round,pad=0.3",
                              facecolor=C_WHITE, edgecolor=C_MED, linewidth=2))
ax.text(5, 9, "퀴즈", fontsize=14, ha='center', color=C_MED, weight='bold')
ax.text(5, 7.5, "다음 중 노트북LM의 소스 기반 설계\n원칙에 해당하는 것은?",
        ha='center', va='center', fontsize=10, color=C_DARK)
options = ["A. 인터넷 전체를 검색하여 답변한다",
           "B. 사용자가 올린 소스만 참조하여 답변한다",
           "C. 학습 데이터를 기반으로 창작한다",
           "D. 실시간 웹 크롤링으로 답변한다"]
for i, opt in enumerate(options):
    y = 5.5 - i * 1.1
    color = C_GREEN if i == 1 else '#EEE'
    tcolor = C_WHITE if i == 1 else '#333'
    ax.add_patch(FancyBboxPatch((1.5, y - 0.35), 7, 0.7, boxstyle="round,pad=0.1",
                                  facecolor=color, edgecolor='#CCC'))
    ax.text(5, y, opt, ha='center', va='center', fontsize=8.5, color=tcolor)
save_fig(fig, 25)

# 그림 27: 맥킨지 스타일 슬라이드 레이아웃
fig, ax = plt.subplots(1, 1, figsize=(10, 6))
ax.set_xlim(0, 16); ax.set_ylim(0, 10); ax.axis('off')
fig.patch.set_facecolor(C_BG)
ax.text(8, 9.7, "맥킨지 스타일 슬라이드 레이아웃", fontsize=13, ha='center', color=C_DARK, weight='bold')
# 슬라이드 프레임
ax.add_patch(patches.Rectangle((1, 0.5), 14, 8.5, fill=True, facecolor=C_WHITE, edgecolor='#999', linewidth=1.5))
# 상단 15%
ax.add_patch(patches.Rectangle((1, 7.7), 14, 1.3, fill=True, facecolor='#1F4E79', edgecolor='none'))
ax.text(8, 8.35, "국내 SaaS 시장은 전년 대비 23% 성장, 2027년까지 연평균 19% 성장 전망",
        ha='center', va='center', fontsize=8, color=C_WHITE, weight='bold')
ax.text(15.3, 8.35, "15%", ha='center', va='center', fontsize=7, color=C_ORANGE, weight='bold')
# 중앙 70%
ax.add_patch(patches.Rectangle((1.5, 1.8), 6, 5.5, fill=True, facecolor='#F0F4F8', edgecolor='#DDD'))
ax.text(4.5, 4.5, "[차트 영역]\n막대 그래프", ha='center', va='center', fontsize=9, color=C_GRAY)
ax.add_patch(patches.Rectangle((8, 1.8), 6.5, 5.5, fill=True, facecolor='#F0F4F8', edgecolor='#DDD'))
ax.text(11.25, 5.5, "핵심 수치:", ha='center', va='center', fontsize=8, color=C_DARK, weight='bold')
ax.text(11.25, 4.2, "  2025년 시장 규모: 4.2조 원\n  2026년 예상: 5.2조 원 (+23%)\n  연평균 성장률: 19%",
        ha='center', va='center', fontsize=7.5, color='#444')
ax.text(15.3, 4.5, "70%", ha='center', va='center', fontsize=7, color=C_ORANGE, weight='bold')
# 하단 15%
ax.add_patch(patches.Rectangle((1, 0.5), 14, 1.3, fill=True, facecolor='#F8F8F8', edgecolor='none'))
ax.text(2, 1.15, "출처: 한국소프트웨어산업협회, 2026", fontsize=7, color=C_GRAY)
ax.text(14, 1.15, "12", fontsize=7, ha='right', color=C_GRAY)
ax.text(15.3, 1.15, "15%", ha='center', va='center', fontsize=7, color=C_ORANGE, weight='bold')
save_fig(fig, 26)

# 그림 28: 3단계 레이어링 프롬프트
create_flow_chart(28, "3단계 레이어링 프롬프트 워크플로우",
    ["1단계\n구조 잡기\n(헤드라인)", "2단계\n상세 채우기\n(근거/데이터)", "3단계\n시각화\n(슬라이드 생성)"],
    "구조에서 상세로, 상세에서 시각화로")

# 그림 29: 인포그래픽 Before/After
create_comparison(29, "인포그래픽 Before/After",
    "Before: 텍스트 나열", [
        "매출 12.3억 원",
        "신규 고객 47명",
        "이탈률 3.2%",
        "NPS 67점",
    ],
    "After: 인포그래픽", [
        "매출 막대그래프 + 증감 화살표",
        "고객 아이콘 47개 시각화",
        "이탈률 원형 차트",
        "NPS 게이지 차트",
    ])

# 그림 30: 표 먼저, 글 나중에 워크플로우
create_flow_chart(30, "\"표 먼저, 글 나중에\" 워크플로우",
    ["소스\n업로드", "데이터표\n생성", "노트로\n저장", "보고서\n초안 요청", "최종\n편집"],
    "정리된 생각은 보고서가 된다")

# 그림 31: CSPO 프롬프트 공식
create_flow_chart(31, "CSPO 프롬프트 공식",
    ["맥락\n(Context)\n나는 누구인가", "상황\n(Situation)\n지금 무엇을 하는가", "목적\n(Purpose)\n무엇을 원하는가", "출력 형식\n(Output)\n어떤 형태로"],
    "이 네 가지를 넣으면 답이 달라진다")

# 그림 32: 회의 녹음 → 후속 조치 워크플로우
create_flow_chart(32, "회의 녹음에서 후속 조치까지",
    ["녹음\n시작", "노트북LM\n업로드", "3단계\n프롬프트", "액션 아이템\n표 생성", "후속 메일\n자동 작성"],
    "회의가 끝나면, AI가 정리를 시작한다")

# 그림 33: 경쟁사 분석 워크플로우
create_flow_chart(33, "경쟁사 분석 전체 워크플로우",
    ["소스 수집\n(IR, 뉴스\n블로그)", "개별\n분석", "교차\n비교표", "전략\n인사이트\n도출", "딥 리서치로\n최신 동향\n추가"],
    "비교에서 전략까지, 한 번의 흐름으로")

# 그림 34: 고객 피드백 분석
create_flow_chart(34, "고객 피드백 분석 프로세스",
    ["데이터 수집\n(설문, 리뷰\nCS, NPS)", "감성 분석\n(긍정/부정)", "불만 분류\n(TOP 5)", "강점 확인\n패턴 발견", "인사이트\n보고서"],
    "100개의 피드백에서 패턴을 찾는다")

# 그림 35: 온보딩 지식베이스
create_flow_chart(35, "신입 온보딩 지식베이스 구축",
    ["사내 규정\n매뉴얼\nFAQ 업로드", "맞춤 지시\n설정", "팀 AI 비서\n구축", "플래시카드\n퀴즈 생성", "노트북\n공유 설정"],
    "한 번 가르치면, 100번 물어도 된다")

# 그림 36: 주간 워크플로우 설계도
create_timeline(36, "주간 업무 워크플로우",
    [("소스 업데이트", "5분\n최신 자료\n교체"),
     ("분석 질문", "10분\n핵심 인사이트\n추출"),
     ("산출물 생성", "5분\n슬라이드/표\n자동 생성"),
     ("최종 검토", "5분\n팩트체크\n확인")])

# 그림 37: 팀 도입 저항과 대응
create_card_grid(37, "팀 도입 시 흔한 저항 4가지와 대응법",
    [("\"또 새 도구야?\"", "강요 없이 결과를 보여준다\n직접 써본 사례 공유"),
     ("\"보안은 괜찮아?\"", "Google 데이터 정책 설명\n모델 학습에 미사용"),
     ("\"AI 잘 모르는데\"", "5분 데모로 시작\n어려운 건 나중에"),
     ("\"지금도 잘 하는데\"", "시간 절감 수치 제시\nBefore/After 비교")])

# 그림 38: AI 도구 선택 플로우차트
fig, ax = plt.subplots(1, 1, figsize=(10, 6))
ax.set_xlim(-1, 11); ax.set_ylim(-1, 8); ax.axis('off')
fig.patch.set_facecolor(C_BG)
ax.text(5, 7.5, "AI 도구 선택 의사결정 플로우", fontsize=13, ha='center', color=C_DARK, weight='bold')
# 시작
add_rounded_box(ax, 3.5, 6, 3, 0.8, "이 작업에\n어떤 AI를 쓸까?", C_DARK, C_WHITE, 8, True)
# 분기 1
add_rounded_box(ax, 0, 4.2, 3, 0.8, "내 자료를\n분석해야 하나?", '#F39C12', C_WHITE, 8)
add_arrow(ax, 5, 6, 1.5, 5.0, C_GRAY)
# Yes → 노트북LM
add_rounded_box(ax, 0, 2.5, 3, 0.8, "노트북LM", C_GREEN, C_WHITE, 9, True)
ax.text(1.5, 3.5, "Yes", fontsize=8, ha='center', color=C_GREEN, weight='bold')
add_arrow(ax, 1.5, 4.2, 1.5, 3.3, C_GREEN)
# No → 분기 2
add_rounded_box(ax, 4, 4.2, 3, 0.8, "최신 정보가\n필요한가?", '#F39C12', C_WHITE, 8)
ax.text(5, 5.2, "No", fontsize=8, ha='center', color=C_RED, weight='bold')
add_arrow(ax, 3, 4.6, 4, 4.6, C_RED)
# Yes → Perplexity
add_rounded_box(ax, 4, 2.5, 3, 0.8, "Perplexity", '#3498DB', C_WHITE, 9, True)
ax.text(5.5, 3.5, "Yes", fontsize=8, ha='center', color=C_GREEN, weight='bold')
add_arrow(ax, 5.5, 4.2, 5.5, 3.3, C_GREEN)
# No → 분기 3
add_rounded_box(ax, 8, 4.2, 3, 0.8, "창의적 생성이\n필요한가?", '#F39C12', C_WHITE, 8)
ax.text(9, 5.2, "No", fontsize=8, ha='center', color=C_RED, weight='bold')
add_arrow(ax, 7, 4.6, 8, 4.6, C_RED)
# Yes → ChatGPT
add_rounded_box(ax, 8, 2.5, 3, 0.8, "ChatGPT", '#E74C3C', C_WHITE, 9, True)
ax.text(9.5, 3.5, "Yes", fontsize=8, ha='center', color=C_GREEN, weight='bold')
add_arrow(ax, 9.5, 4.2, 9.5, 3.3, C_GREEN)
# 하단 안내
ax.text(5, 0.5, "핵심: 내 자료 분석 = 노트북LM, 최신 검색 = Perplexity, 창의적 생성 = ChatGPT",
        ha='center', fontsize=9, color=C_GRAY, style='italic')
save_fig(fig, 37)

# 그림 39: 팀장의 일주일 루틴
create_timeline(39, "팀장의 노트북LM 일주일 루틴",
    [("월", "주간 보고\n자료 분석"),
     ("화", "회의록 정리\n액션 아이템"),
     ("수", "경쟁사/시장\n동향 분석"),
     ("목", "팀 보고서\n초안 작성"),
     ("금", "주간 리뷰\n다음 주 준비")])

# 그림 40: 30분 데모 스크립트 타임라인
create_timeline(40, "팀에 처음 소개할 때: 30분 데모 스크립트",
    [("0~5분", "왜 노트북LM\n인가?"),
     ("5~15분", "함께\n해보기"),
     ("15~25분", "우리 팀\n적용 시나리오"),
     ("25~30분", "Q&A")])

print("=" * 50)
print(f"40개 그림 생성 완료! → {IMG_DIR}")
print("=" * 50)

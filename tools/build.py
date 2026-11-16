"""檢查筆記資料，使用共用範本產生排版後的靜態網頁。"""

from html import escape
import json
from pathlib import Path
import re
from string import Template
from textwrap import dedent

ROOT = Path(__file__).resolve().parents[1]

FIELDS = {
    "slug",
    "title",
    "category",
    "summary",
    "goal",
    "concepts",
    "example",
    "pitfalls",
    "practice",
}
LABELS = [
    ("goal", "學習目標"),
    ("concepts", "核心概念"),
    ("example", "實作範例"),
    ("pitfalls", "常見錯誤"),
    ("practice", "練習與反思"),
]
CATEGORIES = ["Prompt", "RAG", "AI 協作"]


def render_template(template_text, values):
    """插入多行片段時，沿用範本中預留位置的縮排。"""
    indented_values = dict(values)
    for key, value in values.items():
        placeholder = re.search(rf"^([ \t]*)\${key}\s*$", template_text, re.MULTILINE)
        if placeholder and "\n" in value:
            indentation = placeholder.group(1)
            indented_values[key] = value.replace("\n", "\n" + indentation)
    return Template(template_text).substitute(indented_values)


notes = json.loads((ROOT / "content/notes.json").read_text(encoding="utf-8"))
assert isinstance(notes, list) and notes, "筆記清單不可為空"

seen = set()
for note in notes:
    assert isinstance(note, dict) and set(note) == FIELDS, "欄位必須與範本一致"
    assert all(
        isinstance(value, str) and value.strip() for value in note.values()
    ), "所有欄位須為非空字串"
    assert re.fullmatch(
        r"[a-z0-9]+(?:-[a-z0-9]+)*", note["slug"]
    ), "slug 須為小寫英文數字與連字號"
    assert note["slug"] not in seen, "slug 不可重複"
    assert note["category"] in CATEGORIES, "分類須為 Prompt、RAG 或 AI 協作"
    seen.add(note["slug"])

# 所有資料驗證完成後，才開始寫入網頁檔案。
note_template = (ROOT / "templates/note.html").read_text(encoding="utf-8")
(ROOT / "notes").mkdir(exist_ok=True)

for note in notes:
    values = {key: escape(value, quote=True) for key, value in note.items()}
    sections = []
    for key, label in LABELS:
        section = dedent(
            f"""\
            <section id="{key}">
              <h2>{label}</h2>
              <p>{escape(note[key])}</p>
            </section>"""
        )
        sections.append(section)

    values["sections"] = "\n".join(sections)
    article = render_template(note_template, values)
    article_path = ROOT / "notes" / f"{note['slug']}.html"
    article_path.write_text(article, encoding="utf-8")

cards = []
for number, note in enumerate(notes, 1):
    title = escape(note["title"])
    category = escape(note["category"], quote=True)
    summary = escape(note["summary"])
    card = dedent(
        f"""\
        <article class="card" data-category="{category}">
          <div class="section-head">
            <span class="num">{number:02d}</span>
            <span class="tag">{category}</span>
          </div>
          <h3>{title}</h3>
          <p>{summary}</p>
          <a href="notes/{note['slug']}.html">
            閱讀筆記<span class="sr">：{title}</span>
          </a>
        </article>"""
    )
    cards.append(card)

buttons = []
for category in ["全部"] + CATEGORIES:
    pressed = str(category == "全部").lower()
    button = dedent(
        f"""\
        <button type="button" data-filter="{category}" aria-pressed="{pressed}">
          {category}
        </button>"""
    )
    buttons.append(button)

index_template = (ROOT / "templates/index.html").read_text(encoding="utf-8")
index = render_template(
    index_template,
    {
        "count": str(len(notes)),
        "buttons": "\n".join(buttons),
        "cards": "\n".join(cards),
    },
)
(ROOT / "index.html").write_text(index, encoding="utf-8")
print(f"OK: {len(notes)} notes validated; index and article pages generated.")

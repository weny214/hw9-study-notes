"""Validate canonical notes and build static HTML. Standard library only."""
from pathlib import Path
from string import Template
from html import escape
import json, re
ROOT = Path(__file__).resolve().parents[1]
notes = json.loads((ROOT/'content/notes.json').read_text(encoding='utf-8'))
fields = {'slug','title','category','summary','goal','concepts','example','pitfalls','practice'}
labels = [('goal','學習目標'),('concepts','核心概念'),('example','實作範例'),('pitfalls','常見錯誤'),('practice','練習與反思')]
categories = ['Prompt','RAG','AI 協作']
assert isinstance(notes,list) and notes, '筆記清單不可為空'
seen=set()
for note in notes:
    assert isinstance(note,dict) and set(note)==fields, '欄位必須與範本一致'
    assert all(isinstance(v,str) and v.strip() for v in note.values()), '所有欄位須為非空字串'
    assert re.fullmatch(r'[a-z0-9]+(?:-[a-z0-9]+)*',note['slug']), 'slug 須為小寫英文數字與連字號'
    assert note['slug'] not in seen, 'slug 不可重複'
    assert note['category'] in categories, '分類須為 Prompt、RAG 或 AI 協作'
    seen.add(note['slug'])
# Validation completes before writing any generated page.
template=Template((ROOT/'templates/note.html').read_text(encoding='utf-8'))
(ROOT/'notes').mkdir(exist_ok=True)
for note in notes:
    values={k:escape(v,quote=True) for k,v in note.items()}
    values['sections']=''.join(f'<section id="{key}"><h2>{label}</h2><p>{escape(note[key])}</p></section>' for key,label in labels)
    (ROOT/'notes'/f"{note['slug']}.html").write_text(template.substitute(values),encoding='utf-8')
cards=''.join(f'<article class="card" data-category="{escape(n["category"],quote=True)}"><div class="section-head"><span class="num">{i:02d}</span><span class="tag">{escape(n["category"])}</span></div><h3>{escape(n["title"])}</h3><p>{escape(n["summary"])}</p><a href="notes/{n["slug"]}.html">閱讀筆記<span class="sr">：{escape(n["title"])}</span></a></article>' for i,n in enumerate(notes,1))
buttons=''.join(f'<button type="button" data-filter="{c}" aria-pressed="{str(c=="全部").lower()}">{c}</button>' for c in ['全部']+categories)
page=f'''<!doctype html><html lang="zh-Hant"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><meta name="description" content="整理 Prompt、RAG 和 AGENTS.md 的課程筆記，附上範例與練習。"><title>Study Notes｜生成式 AI 學習筆記</title><link rel="stylesheet" href="assets/style.css"></head><body><a class="skip" href="#main">跳到內容</a><header class="top"><a class="brand" href="index.html">S<span>Study Notes</span></a><a href="AGENTS.md">專案規則 AGENTS.md ↗</a></header><main id="main" class="wrap"><section class="hero"><div><p class="eyebrow">生成式 AI 課程筆記</p><h1>生成式 AI<br><em>學習筆記</em></h1><p class="intro">這裡整理 Prompt、RAG 和專案規則的重點。每篇都有說明、例子和練習，方便之後複習。</p></div><aside class="hero-side"><p>目前整理的主題</p><strong>Prompt、RAG<br>與 AGENTS.md</strong><div class="steps"><span>01 重點說明</span><span>02 範例</span><span>03 練習</span></div></aside></section><section aria-labelledby="notes-title"><div class="section-head"><h2 id="notes-title">學習筆記</h2><span id="count" aria-live="polite">顯示 {len(notes)} 篇筆記</span></div><div class="toolbar"><div class="filters" aria-label="筆記分類">{buttons}</div><label><span class="sr">搜尋筆記</span><input id="search" type="search" placeholder="搜尋標題或關鍵字…"></label></div><div class="grid">{cards}</div><p id="empty" class="empty" hidden>找不到符合的筆記，請更換關鍵字或分類。</p></section><section class="rule-box"><div><h2>如何新增筆記</h2><p>在 notes.json 加入一篇筆記，再執行建置程式，就會產生新頁面和首頁連結。內容欄位與檔案放置方式寫在 AGENTS.md。</p></div><a href="AGENTS.md">查看新增內容的規則 →</a></section></main><footer>Study Notes · Homework 9 · 生成式 AI 課程作業</footer><script src="assets/main.js"></script></body></html>'''
(ROOT/'index.html').write_text(page,encoding='utf-8')
print(f'OK: {len(notes)} notes validated; index and article pages generated.')

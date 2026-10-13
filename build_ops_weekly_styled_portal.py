# -*- coding: utf-8 -*-
"""
build_ops_weekly_styled_portal.py
將維運管理月會簡報與知識庫門戶完全對齊 ops-management-weekly (https://davidyeh51.github.io/ops-management-weekly/#home) 的格式與視覺風格：
- 典雅白底科技商務風格 (:root, --green, --teal, --coral, --amber, --card, --line)
- 頂部多欄導航列 (.topbar, .brand, .topnav, .live-pill)
- #home 首頁總覽 (.home-hero 漸層、.hero-stats 四大核心指標、.part-cards 四大板塊、.meeting-history-grid 歷次會議、.toc 大綱矩陣)
- #p1-1 ~ #p4-4 簡報幻燈片 (.slide, .slide-header, .eyebrow, h2 金字塔結論, .sub, .flags, .slide-body, .slide-foot)
- 逐頁三段式講者提示抽屜 (①本頁結論 ②補充說明 ③下一頁轉場)
- 底部全域簡報控制器 (.deckbar, .progress, .hint, .ctrl, 快捷鍵 ←/→/Space/F/Home)
- #tracker 待辦行動追蹤中心 (19 項任務動態交互、多維度篩選、關鍵字過濾、LocalStorage 核取、複製剪貼簿、文字匯出)
- #catalog 知識庫入口與未來擴充架構 (直連南區業務週會、維運管理週會等線上簡報與 3 步驟擴充指引)
- 全站即時關鍵字搜尋 Modal (Ctrl+K，穿透搜尋簡報、行動、洞察、商機與模組)
"""

import os
import json

BASE_DIR = r"C:\Users\davidyeh\Downloads\management-meeting-portal"
DATA_DIR = os.path.join(BASE_DIR, "data")
OUTPUT_HTML = os.path.join(BASE_DIR, "index.html")

# 讀取資料
with open(os.path.join(DATA_DIR, "slides.json"), "r", encoding="utf-8") as f:
    slides_data = json.load(f)

with open(os.path.join(DATA_DIR, "meeting_om_monthly.json"), "r", encoding="utf-8") as f:
    meeting_data = json.load(f)

with open(os.path.join(DATA_DIR, "catalog.json"), "r", encoding="utf-8") as f:
    catalog_data = json.load(f)

print(f"Loaded {len(slides_data)} slides, {len(meeting_data['action_items'])} action items, {len(catalog_data['modules'])} catalog modules.")

# 定義 Part 分組
# P1: slides[0..3] (4 slides: 封面, 全書架構, 歷史追蹤, 10/13月會進展)
# P2: slides[4..6] (3 slides: 核心指標演變, 跨會議共同模式, 8/18歷史回溯)
# P3: slides[7..9] (3 slides: 管顧亮點洞察, 專案商機發掘, 組織連動架構)
# P4: slides[10..13] (4 slides: 優先處置警示, 章節脈絡串聯, 全書精華總結, 附錄延伸索引)

parts_map = {
    "p1": {
        "title": "Part 1｜10/13 月會核心決策與框架",
        "eyebrow": "PART 1 · 10/13 月會核心決策與框架",
        "slides": slides_data[0:4],
        "prefix": "p1"
    },
    "p2": {
        "title": "Part 2｜指標演變與共同模式",
        "eyebrow": "PART 2 · 指標演變與共同模式",
        "slides": slides_data[4:7],
        "prefix": "p2"
    },
    "p3": {
        "title": "Part 3｜管顧洞察與商機評估",
        "eyebrow": "PART 3 · 管顧洞察與商機評估",
        "slides": slides_data[7:10],
        "prefix": "p3"
    },
    "p4": {
        "title": "Part 4｜⚠️警示攻堅與脈絡總結",
        "eyebrow": "PART 4 · ⚠️警示攻堅與脈絡總結",
        "slides": slides_data[10:14],
        "prefix": "p4"
    }
}

# 輔助函數：渲染單張投影片的 HTML
def render_slide_html(slide, part_key, slide_idx, total_in_part, global_idx):
    title = slide.get("conclusion_title") or slide.get("title", "")
    subtitle = slide.get("subtitle") or slide.get("core_claim", "")
    category = slide.get("category", "")
    layout_label = slide.get("layout_label", "")
    footer = slide.get("footer", "")
    notes = slide.get("speaker_notes", {})

    # Flags
    flags_html = ""
    if part_key == "p1":
        flags_html = '<span class="flag green">10/13 月會拍板</span><span class="flag teal">派工 ERP 自主化</span><span class="flag amber">四級告警</span>'
    elif part_key == "p2":
        flags_html = '<span class="flag green">2026 超標 113%</span><span class="flag amber">2027 1.2億 (7:3)</span><span class="flag coral">四大結構頑疾</span>'
    elif part_key == "p3":
        flags_html = '<span class="flag coral">客滿扣分因果鏈</span><span class="flag teal">友達外包潮</span><span class="flag green">告警日報產品化</span>'
    else:
        flags_html = '<span class="flag coral">4大 ⚠️ 優先警示</span><span class="flag teal">論證層層疊加</span><span class="flag green">本週召開重整會</span>'

    # 內容生成 (依 slide 結構)
    body_content = ""
    
    # 封面
    if slide.get("type") == "cover":
        body_content = f"""
        <div class="big-callout" style="padding: 40px; margin: 10px 0;">
          <div style="font-size: 0.85rem; font-weight: 800; letter-spacing: 0.15em; color: #8fe5ef; text-transform: uppercase;">
            {slide.get('category')}
          </div>
          <h2 style="font-size: clamp(1.8rem, 3.5vw, 2.6rem); font-weight: 900; line-height: 1.25; margin: 14px 0 16px; color: #ffffff;">
            {slide.get('title')}
          </h2>
          <div style="font-size: 1.1rem; line-height: 1.6; color: #fef3c7; background: rgba(0,0,0,0.2); padding: 16px 20px; border-left: 4px solid var(--amber); border-radius: 4px;">
            <b>核心主張：</b>{slide.get('core_claim')}
          </div>
          <div style="margin-top: 20px; font-size: 0.82rem; color: rgba(255,255,255,0.8); display: flex; flex-wrap: wrap; gap: 16px;">
            <span>🏢 進金生能源服務 6692</span>
            <span>👤 主持：厲總 ｜ 彙整：David (大衛)</span>
            <span>⏱️ 10 分鐘麥肯錫顧問導讀規範</span>
            <span>📐 14 頁金字塔原理精準排版</span>
          </div>
        </div>

        <div class="three-col" style="margin-top: 10px;">
          <div class="metric green">
            <div class="k">5,786 萬</div>
            <div class="t">2026 累計營收 (113% 超標)</div>
            <div class="sub-tag">全年目標提前達標鎖定</div>
          </div>
          <div class="metric amber">
            <div class="k">1.2 億元</div>
            <div class="t">2027 營收目標 (維運 70% / 修繕 30%)</div>
            <div class="sub-tag">符合 Spin-off EPS 0.5-0.8</div>
          </div>
          <div class="metric coral">
            <div class="k">4 大 ⚠️</div>
            <div class="t">首要處置高風險任務</div>
            <div class="sub-tag">整改方案・妥善率・派工・告警</div>
          </div>
        </div>
        """

    # 全書架構圖 / 結合論法
    elif slide.get("type") == "combined":
        top_claim = slide.get("top_claim", "")
        pillars = slide.get("pillars", [])
        p_html = ""
        for p in pillars:
            facts_list = "".join([f"<li style='margin-bottom:8px; line-height:1.5;'>{f}</li>" for f in p.get("facts", [])])
            p_html += f"""
            <div class="card" style="border-top: 4px solid var(--green);">
              <h3 style="color: var(--green); font-size: 1.05rem;">{p.get('title')}</h3>
              <ul style="padding-left: 20px; font-size: 0.88rem; color: var(--muted); margin-top: 12px;">
                {facts_list}
              </ul>
            </div>
            """
        body_content = f"""
        <div class="formula" style="font-size: 0.95rem; margin-bottom: 8px;">
          {top_claim}
        </div>
        <div class="two-col">
          {p_html}
        </div>
        """

    # 一對一柱狀圖
    elif slide.get("type") == "one_to_one":
        bars = slide.get("bars", [])
        bars_html = ""
        for b in bars:
            hl_class = "green" if b.get("highlight") else "teal"
            pct = min(100, int((b.get("value", 0) / 12000) * 100))
            bars_html += f"""
            <div style="margin-bottom: 12px;">
              <div style="display:flex; justify-content:space-between; font-size:0.84rem; font-weight:700; margin-bottom:4px;">
                <span>{b.get('label')}</span>
                <span style="color: {'var(--coral)' if b.get('highlight') else 'var(--green)'}; font-weight:900;">{b.get('display')}</span>
              </div>
              <div style="height: 12px; background: #e2e8f0; border-radius: 6px; overflow: hidden;">
                <div style="height: 100%; width: {pct}%; background: {'var(--coral)' if b.get('highlight') else 'var(--green)'}; border-radius: 6px;"></div>
              </div>
            </div>
            """
        
        callout_title = slide.get("callout_title", "")
        callout_points = "".join([f"<li style='margin-bottom:8px; line-height:1.5;'>{pt}</li>" for pt in slide.get("callout_points", [])])
        
        body_content = f"""
        <div class="split-40">
          <div class="card" style="border-top: 4px solid var(--green);">
            <h3 style="margin-bottom: 16px;">📊 營收數據演進軌跡</h3>
            {bars_html}
          </div>
          <div class="card" style="border-top: 4px solid var(--amber);">
            <h3 style="color: var(--amber); margin-bottom: 14px;">💡 {callout_title}</h3>
            <ul style="padding-left: 20px; font-size: 0.88rem; color: var(--muted);">
              {callout_points}
            </ul>
          </div>
        </div>
        """

    # 對立論法 (已拍板 vs 討論中)
    elif slide.get("type") == "opposition":
        side_a = slide.get("side_a_title", "已拍板事項")
        side_b = slide.get("side_b_title", "仍在討論中")
        dims = slide.get("dimensions", [])
        dim_rows = ""
        for d in dims:
            dim_rows += f"""
            <div style="display:grid; grid-template-columns: 140px 1fr 1fr; gap: 14px; padding: 12px 14px; background: #fff; border: 1px solid var(--line); border-radius: 6px; align-items: center;">
              <div style="font-weight: 800; font-size: 0.86rem; color: var(--ink); border-right: 2px solid var(--line); padding-right: 8px;">
                {d.get('name')}
              </div>
              <div style="font-size: 0.86rem; color: var(--green); font-weight: 600; line-height: 1.45;">
                <span class="chip green" style="padding: 1px 6px; font-size: 0.72rem; margin-right: 4px;">已拍板</span>{d.get('side_a')}
              </div>
              <div style="font-size: 0.86rem; color: var(--coral); line-height: 1.45;">
                <span class="chip coral" style="padding: 1px 6px; font-size: 0.72rem; margin-right: 4px;">討論中</span>{d.get('side_b')}
              </div>
            </div>
            """
        body_content = f"""
        <div style="display: flex; flex-direction: column; gap: 10px;">
          <div style="display:grid; grid-template-columns: 140px 1fr 1fr; gap: 14px; padding: 8px 14px; font-size: 0.82rem; font-weight: 800; color: var(--muted); text-transform: uppercase;">
            <span>維度</span>
            <span style="color: var(--green);">{side_a}</span>
            <span style="color: var(--coral);">{side_b}</span>
          </div>
          {dim_rows}
        </div>
        """

    # 連鎖因果鏈
    elif slide.get("type") == "chain":
        flow_label = slide.get("flow_label", "")
        steps = slide.get("steps", [])
        steps_html = ""
        for i, st in enumerate(steps):
            items_list = "".join([f"<li style='margin-bottom:4px;'>{it}</li>" for it in st.get("items", [])])
            steps_html += f"""
            <div class="card" style="border-top: 4px solid {'var(--coral)' if i==3 else 'var(--green)'};">
              <div style="font-size: 0.76rem; font-weight: 800; color: var(--teal); margin-bottom: 4px;">階段 {i+1}</div>
              <h3 style="font-size: 0.98rem; margin-bottom: 10px;">{st.get('stage')}</h3>
              <ul style="padding-left: 18px; font-size: 0.84rem; color: var(--muted); line-height: 1.5;">
                {items_list}
              </ul>
            </div>
            """
        body_content = f"""
        <div class="warning-box" style="margin-bottom: 8px; font-weight: 700;">
          {flow_label}
        </div>
        <div class="four-col">
          {steps_html}
        </div>
        """

    # 麥肯錫邏輯串聯流 (mckinsey_flow)
    elif slide.get("type") == "mckinsey_flow":
        stages = slide.get("stages", [])
        rows = slide.get("rows", [])
        
        stages_header = "".join([f"<div style='background:var(--green); color:#fff; padding:8px 12px; font-weight:800; font-size:0.84rem; border-radius:4px; text-align:center;'>{st}</div>" for st in stages])
        
        rows_html = ""
        for r in rows:
            dim = r.get("dimension")
            cells_html = "".join([f"<div class='card' style='padding:12px 14px; font-size:0.84rem; line-height:1.5; color:var(--ink);'><div style='font-size:0.74rem; font-weight:800; color:var(--teal); margin-bottom:4px;'>{dim}</div>{c}</div>" for c in r.get("cells", [])])
            rows_html += f"""
            <div style="display:grid; grid-template-columns: repeat(4, 1fr); gap: 12px; margin-top: 8px;">
              {cells_html}
            </div>
            """
        
        body_content = f"""
        <div style="display:grid; grid-template-columns: repeat(4, 1fr); gap: 12px; margin-bottom: 6px;">
          {stages_header}
        </div>
        {rows_html}
        """

    # 標準並列卡片 (parallel)
    else:
        cards = slide.get("cards", [])
        c_cols = "three-col" if len(cards) <= 3 else "two-col"
        cards_html = ""
        for c in cards:
            pts = "".join([f"<li style='margin-bottom:8px; line-height:1.5;'>{p}</li>" for p in c.get("points", [])])
            cards_html += f"""
            <div class="card" style="border-top: 4px solid var(--green);">
              <h3 style="font-size: 1.02rem; margin-bottom: 12px; color: var(--ink);">{c.get('title')}</h3>
              <ul style="padding-left: 20px; font-size: 0.86rem; color: var(--muted);">
                {pts}
              </ul>
            </div>
            """
        body_content = f"""
        <div class="{c_cols}">
          {cards_html}
        </div>
        """

    # 逐頁三段式講者提示卡片
    speaker_notes_html = ""
    if notes:
        speaker_notes_html = f"""
        <div style="margin-top: 16px; background: #fff; border: 1px dashed var(--line); border-radius: 6px; padding: 12px 16px;">
          <details>
            <summary style="font-size: 0.8rem; font-weight: 800; color: var(--teal); cursor: pointer; user-select: none; display: flex; align-items: center; gap: 6px;">
              <span>🎙️ 麥肯錫講者提示備忘稿 (三段式)</span>
              <span style="font-size: 0.72rem; color: var(--muted); font-weight: normal;">— 點擊展開/收合</span>
            </summary>
            <div style="margin-top: 10px; display: grid; grid-template-columns: repeat(auto-fit, minmax(240px, 1fr)); gap: 12px; font-size: 0.82rem; line-height: 1.55;">
              <div style="background: var(--green-soft); padding: 10px 12px; border-radius: 4px; border-left: 3px solid var(--green);">
                <b style="color: var(--green); display: block; margin-bottom: 2px;">① 本頁結論</b>
                {notes.get('conclusion', '')}
              </div>
              <div style="background: var(--teal-soft); padding: 10px 12px; border-radius: 4px; border-left: 3px solid var(--teal);">
                <b style="color: var(--teal); display: block; margin-bottom: 2px;">② 補充說明</b>
                {notes.get('explanation', '')}
              </div>
              <div style="background: var(--amber-soft); padding: 10px 12px; border-radius: 4px; border-left: 3px solid var(--amber);">
                <b style="color: #b07708; display: block; margin-bottom: 2px;">③ 下一頁轉場</b>
                {notes.get('transition', '')}
              </div>
            </div>
          </details>
        </div>
        """

    # 完整單頁 Slide
    return f"""
    <!-- Slide {part_key.upper()}-{slide_idx+1} (Global #{global_idx+1}) -->
    <div class="slide" id="{part_key}-{slide_idx+1}">
      <div class="slide-header">
        <div>
          <div class="eyebrow">{slide.get('category', '麥肯錫顧問導讀')} ｜ {slide_idx+1} / {total_in_part}</div>
          <h2>{title}</h2>
          <div class="sub">{subtitle}</div>
        </div>
        <div class="flags">
          {flags_html}
        </div>
      </div>

      <div class="slide-body">
        {body_content}
        {speaker_notes_html}
      </div>

      <div class="slide-foot">
        <span>{footer or '進金生能源服務 6692 · 維運管理月會 麥肯錫顧問導讀簡報'}</span>
        <span class="pageno">Slide {global_idx+1} / 14</span>
      </div>
    </div>
    """

# 組裝四大 Part 的投影片 HTML
slides_html_by_part = {}
global_counter = 0

for p_key, p_info in parts_map.items():
    slides_list = p_info["slides"]
    part_html = ""
    for idx, s in enumerate(slides_list):
        part_html += render_slide_html(s, p_key, idx, len(slides_list), global_counter)
        global_counter += 1
    slides_html_by_part[p_key] = part_html

# 產生完整 HTML
html_content = f"""<!DOCTYPE html>
<html lang="zh-Hant">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>維運管理月會主席決策中樞與導讀簡報｜進金生能源服務 × 大衛雲 2.0</title>
<meta name="description" content="進金生能源服務 6692 維運管理月會主席決策中樞、14 頁麥肯錫顧問風格導讀簡報、跨期指標追蹤、19 項行動項目與全站即時深度檢索。">
<style>
:root {{
  --paper:#f7f9fb; --ink:#15202b; --muted:#5f6b76; --line:#d9e1e8;
  --green:#1f68ae; --teal:#18aabd; --coral:#d85643; --amber:#d9a321;
  --green-soft:#e7f0f9; --coral-soft:#faece8; --amber-soft:#fbf4df; --teal-soft:#e5f5f7;
  --card:#ffffff; --grey-bar:#b9c4ce; --brand-blue:#1f68ae; --brand-cyan:#18aabd;
}}
* {{margin:0; padding:0; box-sizing:border-box;}}
body {{
  font-family:"Noto Sans TC","Microsoft JhengHei","PingFang TC",system-ui,-apple-system,sans-serif;
  background:var(--paper); color:var(--ink); line-height:1.58;
  -webkit-font-smoothing:antialiased;
}}

/* ---------- top bar ---------- */
.topbar {{
  position:fixed; top:0; left:0; right:0; z-index:50; height:54px;
  display:flex; align-items:center; gap:8px; padding:0 20px;
  background:rgba(255,255,255,.97); backdrop-filter:blur(8px);
  border-bottom:1px solid var(--line);
}}
.topbar .brand {{
  display:flex; align-items:center; gap:10px; font-weight:800; font-size:.86rem;
  color:var(--muted); margin-right:12px; white-space:nowrap; text-decoration:none;
}}
.topbar .brand .logo-badge {{
  background:var(--brand-blue); color:#fff; font-size:.75rem; font-weight:900;
  padding:3px 8px; border-radius:4px; letter-spacing:.05em;
}}
.topbar .brand b {{color:var(--ink); font-weight:800;}}
.topnav {{display:flex; gap:4px; flex:1; min-width:0; overflow-x:auto;}}
.topnav a {{
  text-decoration:none; color:var(--muted); font-size:.84rem; font-weight:600;
  padding:6px 12px; border-radius:5px; white-space:nowrap; border:1px solid transparent;
  transition:all .15s ease;
}}
.topnav a:hover {{color:var(--teal); background:var(--teal-soft);}}
.topnav a.active {{color:#fff; background:var(--green); font-weight:700;}}
.topbar .meta {{
  display:flex; align-items:center; gap:8px; font-size:.76rem; color:var(--muted);
  white-space:nowrap;
}}
.live-pill {{
  display:inline-flex; align-items:center; gap:5px; background:var(--green-soft);
  color:var(--green); font-weight:700; padding:2px 8px; border-radius:12px; font-size:.72rem;
}}
.live-pill::before {{
  content:""; width:6px; height:6px; border-radius:50%; background:var(--teal);
  box-shadow:0 0 0 2px rgba(24,170,189,.25);
}}
.top-search-btn {{
  display:inline-flex; align-items:center; gap:6px; background:#fff; border:1px solid var(--line);
  padding:4px 10px; border-radius:5px; font-size:.78rem; color:var(--muted); cursor:pointer;
  transition:all .15s ease;
}}
.top-search-btn:hover {{border-color:var(--teal); color:var(--ink);}}
.top-search-btn kbd {{background:#edf2f7; padding:1px 4px; border-radius:3px; font-size:.7rem; font-weight:700;}}

@media(max-width:960px) {{.topbar .meta {{display:none;}}}}

/* ---------- views / slides ---------- */
.view {{display:none;}}
.view.active {{display:block;}}
.slide {{
  display:none; min-height:100vh; padding:78px 48px 96px;
  max-width:1280px; margin:0 auto; flex-direction:column;
}}
.slide.active {{display:flex;}}
.slide-header {{display:flex; justify-content:space-between; align-items:flex-start; gap:16px; margin-bottom:18px;}}
.eyebrow {{font-size:.78rem; font-weight:800; letter-spacing:.14em; color:var(--teal); text-transform:uppercase; margin-bottom:6px;}}
.slide-header h1, .slide-header h2 {{font-size:clamp(1.4rem,3vw,2.15rem); line-height:1.28; font-weight:800; max-width:26em; color:var(--ink);}}
.slide-header .sub {{margin-top:8px; color:var(--muted); font-size:.92rem; max-width:52em; line-height:1.55;}}
.flags {{display:flex; gap:8px; flex-wrap:wrap; justify-content:flex-end;}}
.flag {{font-size:.74rem; font-weight:700; padding:4px 9px; border-radius:5px; white-space:nowrap;}}
.flag.green {{background:var(--green-soft); color:var(--green);}}
.flag.amber {{background:var(--amber-soft); color:#b07708;}}
.flag.coral {{background:var(--coral-soft); color:var(--coral);}}
.flag.teal {{background:var(--teal-soft); color:var(--teal);}}
.slide-body {{flex:1; display:flex; flex-direction:column; gap:16px;}}
.slide-foot {{display:flex; justify-content:space-between; gap:16px; margin-top:20px; padding-top:12px; border-top:1px solid var(--line); font-size:.75rem; color:var(--muted);}}
.slide-foot .pageno {{white-space:nowrap; font-weight:700; color:var(--ink);}}

/* ---------- layout grids ---------- */
.two-col {{display:grid; grid-template-columns:1fr 1fr; gap:18px; align-items:stretch;}}
.three-col {{display:grid; grid-template-columns:repeat(3,1fr); gap:16px;}}
.four-col {{display:grid; grid-template-columns:repeat(4,1fr); gap:14px;}}
.split-40 {{display:grid; grid-template-columns:38% 1fr; gap:22px; align-items:stretch;}}
.split-60 {{display:grid; grid-template-columns:1fr 38%; gap:22px; align-items:stretch;}}
@media(max-width:980px) {{
  .slide {{padding:74px 18px 110px;}}
  .two-col, .three-col, .four-col, .split-40, .split-60 {{grid-template-columns:1fr;}}
}}

/* ---------- components ---------- */
.card {{background:var(--card); border:1px solid var(--line); border-radius:6px; padding:18px 20px;}}
.card h3 {{font-size:1.05rem; font-weight:800; margin-bottom:8px; color:var(--ink); display:flex; align-items:center; gap:8px;}}
.card h4 {{font-size:.92rem; font-weight:700; margin:12px 0 6px; color:var(--green);}}
.card p {{font-size:.9rem; color:var(--muted); margin-bottom:8px;}}
.card p:last-child {{margin-bottom:0;}}

.metric {{border-radius:6px; padding:16px 18px; border:1px solid var(--line); background:#fff;}}
.metric .k {{font-size:clamp(1.5rem,2.8vw,2.1rem); font-weight:900; line-height:1.15; font-variant-numeric:tabular-nums;}}
.metric .t {{font-size:.82rem; color:var(--muted); margin-top:5px; font-weight:600;}}
.metric .sub-tag {{font-size:.72rem; margin-top:4px; font-weight:700;}}
.metric.green {{background:var(--green-soft); border-color:#bfd2e6;}}
.metric.green .k {{color:var(--green);}}
.metric.green .sub-tag {{color:var(--green);}}
.metric.amber {{background:var(--amber-soft); border-color:#ecdca6;}}
.metric.amber .k {{color:#b07708;}}
.metric.amber .sub-tag {{color:#b07708;}}
.metric.coral {{background:var(--coral-soft); border-color:#efc8bf;}}
.metric.coral .k {{color:var(--coral);}}
.metric.coral .sub-tag {{color:var(--coral);}}
.metric.teal {{background:var(--teal-soft); border-color:#b9e4eb;}}
.metric.teal .k {{color:var(--teal);}}
.metric.teal .sub-tag {{color:var(--teal);}}

.big-callout {{
  background:linear-gradient(135deg, #103454 0%, #1f68ae 100%); color:#fff;
  border-radius:6px; padding:22px 26px; position:relative; overflow:hidden;
}}
.formula {{background:var(--green-soft); border-left:4px solid var(--green); border-radius:0 6px 6px 0; padding:12px 16px; font-size:.9rem; font-weight:600; color:var(--ink);}}
.warning-box {{background:var(--coral-soft); border-left:4px solid var(--coral); border-radius:0 6px 6px 0; padding:12px 16px; font-size:.88rem; color:#842215;}}
.tip-box {{background:var(--teal-soft); border-left:4px solid var(--teal); border-radius:0 6px 6px 0; padding:12px 16px; font-size:.88rem; color:#0e5863;}}

.chip {{display:inline-block; font-size:.72rem; font-weight:700; padding:2px 7px; border-radius:4px; white-space:nowrap;}}
.chip.green {{background:var(--green-soft); color:var(--green);}}
.chip.amber {{background:var(--amber-soft); color:#b07708;}}
.chip.coral {{background:var(--coral-soft); color:var(--coral);}}
.chip.teal {{background:var(--teal-soft); color:var(--teal);}}
.chip.slate {{background:#e2e8f0; color:#334155;}}

/* ---------- Home View Layout ---------- */
.home {{max-width:1280px; margin:0 auto; padding:70px 48px 60px; min-height:100vh; display:flex; flex-direction:column;}}
@media(max-width:980px) {{.home {{padding:74px 18px 50px;}}}}
.home-hero {{
  margin:0 calc(50% - 50vw); padding:clamp(48px,6vw,76px) max(48px,calc((100vw - 1180px)/2));
  display:flex; flex-direction:column; justify-content:flex-end;
  background:linear-gradient(135deg, #103454 0%, #1f68ae 55%, #18aabd 100%);
  color:#fff; position:relative; box-shadow:0 4px 20px rgba(16,52,84,.15);
}}
.home-hero .eyebrow {{color:#8fe5ef;}}
.home h1 {{font-size:clamp(1.8rem,3.8vw,2.9rem); font-weight:900; line-height:1.24; max-width:24em; margin-top:6px;}}
.home .lede {{color:rgba(255,255,255,.92); margin-top:12px; max-width:52em; font-size:.98rem; line-height:1.6;}}
.hero-stats {{display:grid; grid-template-columns:repeat(auto-fit,minmax(210px,1fr)); gap:14px; margin-top:24px;}}
.hero-stat {{background:rgba(255,255,255,.12); backdrop-filter:blur(6px); border:1px solid rgba(255,255,255,.2); border-radius:6px; padding:14px 16px;}}
.hero-stat .v {{font-size:1.65rem; font-weight:900; color:#fff;}}
.hero-stat .l {{font-size:.78rem; opacity:.85; margin-top:2px;}}

.section-title {{font-size:1.25rem; font-weight:800; color:var(--ink); margin:32px 0 16px; display:flex; align-items:center; gap:8px;}}
.section-title::before {{content:""; width:4px; height:18px; background:var(--teal); border-radius:2px;}}

.part-cards {{display:grid; grid-template-columns:repeat(auto-fit,minmax(280px,1fr)); gap:18px;}}
.part-card {{
  display:flex; flex-direction:column; justify-content:space-between;
  text-decoration:none; color:var(--ink); background:#fff; border:1px solid var(--line);
  border-radius:6px; padding:22px; transition:transform .15s ease, box-shadow .15s ease;
  position:relative; overflow:hidden;
}}
.part-card:hover {{transform:translateY(-3px); box-shadow:0 10px 24px rgba(16,37,44,.08); border-color:#b9cad9;}}
.part-card .pc-eyebrow {{font-size:.74rem; font-weight:800; letter-spacing:.12em; color:var(--teal);}}
.part-card h2 {{font-size:1.15rem; font-weight:800; margin:8px 0 6px; line-height:1.32;}}
.part-card p {{color:var(--muted); font-size:.88rem; flex:1;}}
.part-card .pc-flags {{margin-top:12px; display:flex; gap:6px; flex-wrap:wrap;}}
.part-card .pc-go {{margin-top:14px; font-weight:800; color:var(--green); font-size:.86rem; display:flex; align-items:center; gap:4px;}}

.meeting-history-grid {{display:grid; grid-template-columns:repeat(auto-fit,minmax(230px,1fr)); gap:14px; margin-top:10px;}}
.meeting-tile {{
  background:#fff; border:1px solid var(--line); border-radius:6px; padding:14px 16px;
  text-decoration:none; color:var(--ink); transition:all .15s ease;
}}
.meeting-tile:hover {{border-color:var(--teal); background:var(--teal-soft); transform:translateY(-2px);}}
.meeting-tile .m-date {{font-size:.74rem; font-weight:800; color:var(--teal);}}
.meeting-tile .m-title {{font-size:.95rem; font-weight:800; margin:4px 0 2px;}}
.meeting-tile .m-desc {{font-size:.78rem; color:var(--muted);}}

.toc {{margin-top:20px; display:grid; grid-template-columns:repeat(auto-fit,minmax(270px,1fr)); gap:16px;}}
.toc .card h3 {{font-size:.84rem; letter-spacing:.08em; color:var(--muted); margin-bottom:8px; text-transform:uppercase;}}
.toc a {{display:flex; gap:8px; padding:6px 8px; border-radius:4px; text-decoration:none; color:var(--ink); font-size:.86rem; transition:background .12s ease;}}
.toc a:hover {{background:var(--teal-soft); color:var(--green);}}
.toc a .no {{color:var(--teal); font-weight:800; flex:0 0 1.5em; font-variant-numeric:tabular-nums;}}
.home-foot {{padding-top:24px; font-size:.76rem; color:var(--muted); border-top:1px solid var(--line); margin-top:36px; display:flex; justify-content:space-between; flex-wrap:wrap; gap:10px;}}

/* ---------- Follow-up Action Tracker Hub (#tracker) ---------- */
.tracker-page {{max-width:1280px; margin:0 auto; padding:76px 40px 120px;}}
@media(max-width:768px) {{.tracker-page {{padding:74px 16px 100px;}}}}
.tracker-hero {{
  background:linear-gradient(135deg, #1f68ae 0%, #18aabd 100%); color:#fff;
  border-radius:6px; padding:24px 28px; margin-bottom:20px;
}}
.tracker-hero h1 {{font-size:clamp(1.35rem,2.8vw,1.9rem); font-weight:900;}}
.tracker-hero p {{margin-top:6px; font-size:.9rem; opacity:.92;}}

.tracker-toolbar {{
  background:#fff; border:1px solid var(--line); border-radius:6px; padding:14px 18px;
  display:flex; flex-wrap:wrap; gap:12px; justify-content:space-between; align-items:center;
  margin-bottom:16px; position:sticky; top:60px; z-index:40; box-shadow:0 4px 12px rgba(0,0,0,.03);
}}
.filter-pills {{display:flex; gap:6px; flex-wrap:wrap;}}
.filter-pill {{
  background:var(--paper); border:1px solid var(--line); border-radius:4px;
  padding:5px 11px; font-size:.78rem; font-weight:700; cursor:pointer; color:var(--muted);
  transition:all .12s ease;
}}
.filter-pill:hover {{background:#edf2f7; color:var(--ink);}}
.filter-pill.active {{background:var(--green); border-color:var(--green); color:#fff;}}

.search-input {{
  border:1px solid var(--line); border-radius:4px; padding:6px 12px; font-size:.84rem;
  min-width:220px; outline:none; background:#fff; font-family:inherit;
}}
.search-input:focus {{border-color:var(--teal); box-shadow:0 0 0 2px rgba(24,170,189,.15);}}

.tracker-stats-bar {{
  display:grid; grid-template-columns:repeat(auto-fit,minmax(180px,1fr)); gap:12px; margin-bottom:16px;
}}
.tracker-stat-box {{
  background:#fff; border:1px solid var(--line); border-radius:6px; padding:12px 14px;
}}
.tracker-stat-box .num {{font-size:1.35rem; font-weight:900; color:var(--ink);}}
.tracker-stat-box .desc {{font-size:.74rem; color:var(--muted); font-weight:600;}}

.action-items-list {{display:flex; flex-direction:column; gap:10px;}}
.action-item {{
  background:#fff; border:1px solid var(--line); border-radius:6px; padding:14px 18px;
  display:grid; grid-template-columns:26px 1fr auto; gap:14px; align-items:flex-start;
  transition:all .15s ease;
}}
.action-item:hover {{border-color:#b5c8d8; box-shadow:0 3px 8px rgba(0,0,0,.03);}}
.action-item.done {{background:#f8fafc; border-color:#e2e8f0; opacity:.85;}}
.action-item.done .action-title {{text-decoration:line-through; color:var(--muted);}}
.action-check {{width:20px; height:20px; accent-color:var(--green); margin-top:2px; cursor:pointer;}}
.action-content {{display:flex; flex-direction:column; gap:4px;}}
.action-title {{font-size:.92rem; font-weight:700; color:var(--ink); line-height:1.4;}}
.action-details {{font-size:.82rem; color:var(--muted); line-height:1.45;}}
.action-conclusion {{
  background:var(--green-soft); border-left:3px solid var(--green); border-radius:0 4px 4px 0;
  padding:6px 10px; font-size:.8rem; color:var(--green); font-weight:600; margin-top:4px;
}}
.action-warning {{
  background:var(--coral-soft); border-left:3px solid var(--coral); border-radius:0 4px 4px 0;
  padding:6px 10px; font-size:.8rem; color:var(--coral); font-weight:600; margin-top:4px;
}}
.action-badges {{display:flex; flex-direction:column; align-items:flex-end; gap:6px;}}

.btn {{
  border:none; border-radius:4px; padding:8px 16px; font-family:inherit; font-size:.84rem;
  font-weight:700; cursor:pointer; display:inline-flex; align-items:center; gap:6px;
  transition:all .15s ease; text-decoration:none;
}}
.btn.primary {{background:var(--green); color:#fff;}}
.btn.primary:hover {{background:#154e85;}}
.btn.ghost {{background:#fff; border:1px solid var(--line); color:var(--ink);}}
.btn.ghost:hover {{border-color:var(--green); color:var(--green);}}
.btn.sm {{padding:5px 10px; font-size:.76rem;}}

/* ---------- bottom presentation controls ---------- */
.deckbar {{position:fixed; left:0; right:0; bottom:0; z-index:50; pointer-events:none;}}
.progress {{height:4px; background:#e0e8e5;}}
.progress .fill {{height:100%; width:0%; background:var(--brand-cyan); transition:width .2s ease;}}
.ctrl {{position:absolute; right:16px; bottom:14px; display:flex; align-items:center; gap:8px; pointer-events:auto;}}
.ctrl .counter {{
  font-size:.78rem; color:var(--muted); background:rgba(255,255,255,.94);
  border:1px solid var(--line); padding:4px 10px; border-radius:14px; font-variant-numeric:tabular-nums; font-weight:700;
}}
.ctrl button {{
  width:38px; height:38px; border-radius:50%; border:1px solid var(--line); background:#fff;
  font-size:1.05rem; color:var(--ink); cursor:pointer; box-shadow:0 3px 8px rgba(16,37,44,.08);
  display:flex; align-items:center; justify-content:center; transition:all .12s ease;
}}
.ctrl button:hover {{background:var(--green); color:#fff; border-color:var(--green);}}
.hint {{position:absolute; left:16px; bottom:16px; font-size:.72rem; color:var(--muted); pointer-events:none;}}
@media(max-width:720px) {{
  .hint {{display:none;}}
  .ctrl button {{width:34px; height:34px; font-size:.9rem;}}
}}

/* ---------- Global Search Modal ---------- */
.search-modal-backdrop {{
  display:none; position:fixed; inset:0; z-index:100;
  background:rgba(15,23,42,0.6); backdrop-filter:blur(4px);
  align-items:flex-start; justify-content:center; padding:60px 16px 20px;
}}
.search-modal-backdrop.open {{display:flex;}}
.search-modal {{
  background:#fff; border-radius:8px; width:100%; max-width:680px;
  box-shadow:0 20px 40px rgba(0,0,0,0.25); overflow:hidden; border:1px solid var(--line);
}}
.search-modal-header {{
  display:flex; align-items:center; padding:14px 18px; border-bottom:1px solid var(--line);
}}
.search-modal-input {{
  flex:1; border:none; outline:none; font-size:1.05rem; font-family:inherit; color:var(--ink);
}}
.search-results-list {{
  max-height:420px; overflow-y:auto; padding:12px; display:flex; flex-direction:column; gap:8px;
}}
.search-result-item {{
  padding:10px 14px; border-radius:6px; background:#f8fafc; border:1px solid var(--line);
  cursor:pointer; transition:all .12s ease;
}}
.search-result-item:hover {{background:var(--teal-soft); border-color:var(--teal);}}
</style>
</head>
<body>

<!-- TOPBAR -->
<header class="topbar">
  <a href="#home" class="brand">
    <span class="logo-badge">ACMEPOINT</span>
    <span><b>維運管理月會</b> · 決策與導讀簡報</span>
  </a>
  <nav class="topnav" id="topNav">
    <a href="#home" data-nav="home" class="active">首頁總覽</a>
    <a href="#p1-1" data-nav="p1">Part 1｜10/13 月會核心決策</a>
    <a href="#p2-1" data-nav="p2">Part 2｜指標與共同模式</a>
    <a href="#p3-1" data-nav="p3">Part 3｜管顧洞察與商機</a>
    <a href="#p4-1" data-nav="p4">Part 4｜⚠️警示與脈絡總結</a>
    <a href="#tracker" data-nav="tracker">🎯 待辦追蹤中心</a>
    <a href="#catalog" data-nav="catalog">🗂️ 知識庫入口</a>
  </nav>
  <div class="meta">
    <button class="top-search-btn" onclick="openSearchModal()" title="全站搜尋 (Ctrl+K)">
      <span>🔍 搜尋</span>
      <kbd>Ctrl+K</kbd>
    </button>
    <a href="acmepoint_meeting_zero_noise.pptx" download class="btn primary sm" style="font-size:0.75rem;">
      📥 下載 PPTX
    </a>
    <span class="live-pill">大衛雲 2.0</span>
    <span>主持：厲總 ｜ 彙整：David</span>
  </div>
</header>

<!-- ========================================================================= -->
<!-- HOME VIEW (#home)                                                         -->
<!-- ========================================================================= -->
<section class="view active" id="view-home">
  <div class="home">
    <div class="home-hero">
      <div class="eyebrow">進金生能源服務 6692 ｜ 2.2 事業經營 × 4.6 運維管理 ｜ 會議記錄知識庫</div>
      <h1>太陽光電維運管理月會主席決策中樞</h1>
      <p class="lede">
        整合 10/13 ft 厲總與 08/18 兩場維運月會深度分析紀錄。以 14 頁麥肯錫顧問風格導讀簡報為骨幹，穿透 2026 營收 113% 超標（5,786 萬）與 2027 年 1.2 億（7:3）結構、整改能力落差、客滿度 8.6 與派工 ERP 因果鏈、友達外包潮四大商機及 19 項動態追蹤矩陣。
      </p>
      
      <div class="hero-stats">
        <div class="hero-stat">
          <div class="v">5,786 萬元</div>
          <div class="l">2026 累計營收 (達成率 113%)</div>
        </div>
        <div class="hero-stat">
          <div class="v">1.2 億元</div>
          <div class="l">2027 營收目標 (維運 70% / 修繕 30%)</div>
        </div>
        <div class="hero-stat">
          <div class="v">0 元罰鍰</div>
          <div class="l">保發年度結算考核 (去年 88 萬)</div>
        </div>
        <div class="hero-stat">
          <div class="v">8.6 分</div>
          <div class="l">客戶滿意度調查 (52 份業主問卷)</div>
        </div>
      </div>
    </div>

    <div class="section-title">月會導讀簡報模組 (Presentation Parts)</div>
    <div class="part-cards">
      <a href="#p1-1" class="part-card">
        <div>
          <div class="pc-eyebrow">PART 1 · 核心拍板與框架 (4 頁)</div>
          <h2>10/13 月會核心拍板、全書推導骨架與追蹤體系</h2>
          <p>封面核心主張；四層演繹推導骨架（問題➔框架➔方法➔落地）；單一整合檔動態追蹤機制；10/13 最新拍板（派工 ERP 自主化、四級告警、保發容量加權）。</p>
        </div>
        <div>
          <div class="pc-flags">
            <span class="flag green">派工定位 ERP</span>
            <span class="flag teal">四級告警日報</span>
            <span class="flag amber">保發雙軌口徑</span>
          </div>
          <div class="pc-go">進入 Part 1 (核心拍板) →</div>
        </div>
      </a>

      <a href="#p2-1" class="part-card">
        <div>
          <div class="pc-eyebrow">PART 2 · 指標演變與病灶 (3 頁)</div>
          <h2>核心指標對比、四大共同模式與 8/18 矛盾回溯</h2>
          <p>2026 營收超標 (113%) vs 2027 下修至 1.2 億；四大深層結構性病灶（數據治理失靈、整改能力未內化、新技術實測落差、外包潮）；8/18 大案轉出 5,376 萬反思。</p>
        </div>
        <div>
          <div class="pc-flags">
            <span class="flag green">2026 營收 113%</span>
            <span class="flag coral">大案轉出南區矛盾</span>
            <span class="flag amber">清掃機器人10年回本</span>
          </div>
          <div class="pc-go">進入 Part 2 (指標與病灶) →</div>
        </div>
      </a>

      <a href="#p3-1" class="part-card">
        <div>
          <div class="pc-eyebrow">PART 3 · 管顧洞察與商機 (3 頁)</div>
          <h2>客滿扣分因果鏈展開、友達外包潮與四大商機 A/B 方案</h2>
          <p>客滿扣分與派工停工同源鏈條（告警過載➔派工卡關➔巡檢突襲➔客戶扣分）；掌握友達外包潮與奇美競標；告警日報產品化；RCM 分級合約與驗收 FMEA。</p>
        </div>
        <div>
          <div class="pc-flags">
            <span class="flag coral">客滿 8.6 因果鏈</span>
            <span class="flag teal">友達外包潮</span>
            <span class="flag green">告警報告產品化</span>
          </div>
          <div class="pc-go">進入 Part 3 (洞察與商機) →</div>
        </div>
      </a>

      <a href="#p4-1" class="part-card">
        <div>
          <div class="pc-eyebrow">PART 4 · ⚠️警示攻堅與總結 (4 頁)</div>
          <h2>組織上下層級連動、四大 ⚠️ 警示攻堅與落地行動</h2>
          <p>向上牽動五年計畫與 Spin-off，向下連動工程採購業務；David/Evan/Roy/分析組 4 大 ⚠️ 優先警示；論證層層疊加邏輯串聯；立刻應用一件事（本週召開重整會）。</p>
        </div>
        <div>
          <div class="pc-flags">
            <span class="flag coral">4 大 ⚠️ 優先警示</span>
            <span class="flag teal">論證疊加閉環</span>
            <span class="flag green">本週召開重整會</span>
          </div>
          <div class="pc-go">進入 Part 4 (警示與總結) →</div>
        </div>
      </a>
    </div>

    <div class="section-title">歷次會議快速跳轉 (Meeting Archives)</div>
    <div class="meeting-history-grid">
      <a href="#p1-4" class="meeting-tile">
        <div class="m-date">2026-10-13 13:30-14:30</div>
        <div class="m-title">維運月會 ft 厲總</div>
        <div class="m-desc">拍板派工升格 ERP、告警四級分類；奇美 10 月底定標對手達耀；客滿 8.6 分流程改善。</div>
      </a>
      <a href="#p2-3" class="meeting-tile">
        <div class="m-date">2026-08-18 13:30-14:30</div>
        <div class="m-title">維運管理月會 (前期基準)</div>
        <div class="m-desc">確立 2027 營收 7:3 配比；大案 5,376 萬轉出南區；厲總戳破清掃機器人經濟性。</div>
      </a>
      <a href="https://davidyeh51.github.io/ops-management-weekly/#home" target="_blank" class="meeting-tile" style="border-left: 3px solid var(--teal);">
        <div class="m-date">每週一 15:30-17:00 ↗</div>
        <div class="m-title">維運管理週會主席決策系統</div>
        <div class="m-desc">130 案毛利全面體檢、負毛利治理 SOP、五大保固爭議裁決。</div>
      </a>
      <a href="https://davidyeh51.github.io/south-sales-meeting/#home" target="_blank" class="meeting-tile" style="border-left: 3px solid var(--green);">
        <div class="m-date">每週一 09:00-10:00 ↗</div>
        <div class="m-title">南區業務週會管理中樞</div>
        <div class="m-desc">FY2026 四大業務戰略支柱、Pipeline 20 億商機、40+ 待辦追蹤中心。</div>
      </a>
    </div>

    <div class="section-title">全書 14 頁精華導讀大綱 (Agenda & Table of Contents)</div>
    <div class="toc">
      <div class="card">
        <h3>Part 1 · 核心拍板與架構 (P.1 ~ P.4)</h3>
        <a href="#p1-1"><span class="no">1</span> 封面：太陽光電維運月會全貌與核心主張</a>
        <a href="#p1-2"><span class="no">2</span> 全書架構圖：四層演繹推導骨架閉環</a>
        <a href="#p1-3"><span class="no">3</span> 逐章重點一：單一整合檔與動態追蹤機制</a>
        <a href="#p1-4"><span class="no">4</span> 逐章重點四：10/13 月會核心拍板與討論邊界</a>
      </div>
      <div class="card">
        <h3>Part 2 · 指標與共同模式 (P.5 ~ P.7)</h3>
        <a href="#p2-1"><span class="no">5</span> 逐章重點二：核心指標演變（超標 113% vs 下修）</a>
        <a href="#p2-2"><span class="no">6</span> 逐章重點三：四大跨會議共同模式病灶</a>
        <a href="#p2-3"><span class="no">7</span> 逐章重點七：8/18 前期基準回溯與矛盾反思</a>
      </div>
      <div class="card">
        <h3>Part 3 · 管顧洞察與商機 (P.8 ~ P.10)</h3>
        <a href="#p3-1"><span class="no">8</span> 逐章重點五：客滿扣分與派工停工因果鏈</a>
        <a href="#p3-2"><span class="no">9</span> 逐章重點六：掌握友達外包潮與四大商機 A/B 方案</a>
        <a href="#p3-3"><span class="no">10</span> 逐章重點八：組織上下層級連動（2.2 事業經營）</a>
      </div>
      <div class="card">
        <h3>Part 4 · ⚠️警示與脈絡總結 (P.11 ~ P.14)</h3>
        <a href="#p4-1"><span class="no">11</span> 逐章重點九：四大首要處置警示（⚠️ 行動攻堅）</a>
        <a href="#p4-2"><span class="no">12</span> 章節脈絡：論證步步疊加邏輯串聯圖</a>
        <a href="#p4-3"><span class="no">13</span> 總結：全書三大精華 ＋ 立刻應用一件事</a>
        <a href="#p4-4"><span class="no">14</span> 附錄：延伸章節、19項檢索與戰情直連</a>
      </div>
    </div>

    <div class="home-foot">
      <span>維運管理月會知識庫 · 大衛雲 2.0 系統 ｜ 主席：葉大衛 (David) ｜ 主持：厲總</span>
      <span>進金生能源服務 6692 · 支援 GitHub Pages 線上即時發布</span>
    </div>
  </div>
</section>

<!-- ========================================================================= -->
<!-- SLIDES VIEWS (#view-p1 ~ #view-p4)                                        -->
<!-- ========================================================================= -->
<section class="view" id="view-p1">
  {slides_html_by_part["p1"]}
</section>

<section class="view" id="view-p2">
  {slides_html_by_part["p2"]}
</section>

<section class="view" id="view-p3">
  {slides_html_by_part["p3"]}
</section>

<section class="view" id="view-p4">
  {slides_html_by_part["p4"]}
</section>

<!-- ========================================================================= -->
<!-- TRACKER VIEW (#tracker)                                                   -->
<!-- ========================================================================= -->
<section class="view" id="view-tracker">
  <div class="tracker-page">
    <div class="tracker-hero">
      <div class="eyebrow" style="color:#8fe5ef;">AcmePoint Meeting Intelligence ｜ 2.2 事業經營 × 4.6 運維管理</div>
      <h1>累積行動追蹤矩陣 (19 項待辦任務中心)</h1>
      <p>跨期整合 10/13 與 08/18 兩場維運月會之待辦事項。嚴格標註四大 ⚠️ 優先警示，支援即時核取、進度儲存於 LocalStorage、關鍵字過濾與一鍵複製/匯出。</p>
    </div>

    <!-- Tracker Stats Bar -->
    <div class="tracker-stats-bar">
      <div class="tracker-stat-box">
        <div class="num" id="statTotal">19</div>
        <div class="desc">待辦總數 (累積清冊)</div>
      </div>
      <div class="tracker-stat-box">
        <div class="num" id="statHigh" style="color:var(--coral);">4</div>
        <div class="desc">⚠️ 高優先級 (優先處置)</div>
      </div>
      <div class="tracker-stat-box">
        <div class="num" id="statPending" style="color:var(--amber);">15</div>
        <div class="desc">進行中 / 待追蹤項目</div>
      </div>
      <div class="tracker-stat-box">
        <div class="num" id="statDone" style="color:var(--green);">0</div>
        <div class="desc">已完成 / 已定調事項</div>
      </div>
    </div>

    <!-- Tracker Toolbar -->
    <div class="tracker-toolbar">
      <div class="filter-pills" id="trackerFilters">
        <button class="filter-pill active" onclick="setTrackerFilter('all', this)">全部 (<span id="cntAll">19</span>)</button>
        <button class="filter-pill" onclick="setTrackerFilter('high', this)">⚠️ 優先處置 (<span id="cntHigh">4</span>)</button>
        <button class="filter-pill" onclick="setTrackerFilter('pending', this)">進行中 (<span id="cntPending">15</span>)</button>
        <button class="filter-pill" onclick="setTrackerFilter('done', this)">已完成 (<span id="cntDone">0</span>)</button>
        <button class="filter-pill" onclick="setTrackerFilter('David', this)">David</button>
        <button class="filter-pill" onclick="setTrackerFilter('Evan', this)">Evan</button>
        <button class="filter-pill" onclick="setTrackerFilter('Roy', this)">Roy</button>
        <button class="filter-pill" onclick="setTrackerFilter('Mina', this)">Mina</button>
      </div>

      <div style="display:flex; gap:8px; align-items:center;">
        <input type="text" id="trackerSearch" class="search-input" placeholder="過濾行動、負責人、備註..." oninput="renderTracker()">
        <button class="btn ghost sm" onclick="copyTrackerText()">📋 複製</button>
        <button class="btn primary sm" onclick="exportTrackerText()">📥 匯出</button>
      </div>
    </div>

    <!-- Action Items List -->
    <div class="action-items-list" id="actionItemsContainer">
      <!-- Rendered by JavaScript -->
    </div>
  </div>
</section>

<!-- ========================================================================= -->
<!-- CATALOG VIEW (#catalog)                                                   -->
<!-- ========================================================================= -->
<section class="view" id="view-catalog">
  <div class="home">
    <div class="section-title">知識庫入口與可持續擴充架構 (Meeting Catalog & Portals)</div>
    <p style="color: var(--muted); font-size: 0.92rem; margin-bottom: 20px;">
      具備「可持續擴充架構」，整合集團管理月會、業務週會、運維週會與相關戰情平台。可直接從此入口連結至各個模組之線上簡報與系統。
    </p>

    <div class="part-cards" id="catalogCardsContainer">
      <!-- Rendered from catalogData -->
    </div>

    <div class="card" style="margin-top: 30px; background: #fff; border: 1px solid var(--line);">
      <h3 style="color: var(--green);">➕ 如何擴充新會議記錄與無雜訊顧問簡報？（3 步驟標準化流程）</h3>
      <ol style="padding-left: 20px; font-size: 0.88rem; color: var(--muted); line-height: 1.8; margin-top: 10px;">
        <li><b>步驟 1：</b>在 <code>data/</code> 目錄新增會議萃取 JSON 檔（如 <code>data/meeting_YYYYMM_name.json</code> 與 <code>data/slides_YYYYMM.json</code>）。</li>
        <li><b>步驟 2：</b>執行本地腳本 <code>python build_ops_weekly_styled_portal.py</code>，自動生成標準 HTML 與 16:9 寬螢幕 PPTX 投影片。</li>
        <li><b>步驟 3：</b>在 <code>data/catalog.json</code> 的 <code>modules</code> 陣列中新增該會議條目（設定 <code>id</code>、<code>title</code>、<code>external_url</code> 等屬性），重新整理網頁即可即時呈現並支援全域穿透檢索！</li>
      </ol>
    </div>

    <div class="home-foot">
      <span>管理會議記錄知識庫門戶 · AcmePoint Meeting Intelligence</span>
      <span>進金生能源服務 6692 ｜ 大衛雲 2.0</span>
    </div>
  </div>
</section>

<!-- ========================================================================= -->
<!-- BOTTOM PRESENTATION DECKBAR                                               -->
<!-- ========================================================================= -->
<div class="deckbar" id="deckbar" style="display:none">
  <div class="progress"><div class="fill" id="progressFill"></div></div>
  <div class="hint">按 <b>←</b> <b>→</b> 鍵或 <b>空白鍵</b> 翻頁 ｜ 按 <b>F</b> 全螢幕 ｜ 按 <b>Home</b> 回首頁 ｜ 按 <b>Ctrl+K</b> 搜尋</div>
  <div class="ctrl">
    <span class="counter" id="counter">1 / 4</span>
    <button id="btnPrev" title="上一頁 (←)">‹</button>
    <button id="btnNext" title="下一頁 (→)">›</button>
  </div>
</div>

<!-- ========================================================================= -->
<!-- GLOBAL SEARCH MODAL (Ctrl+K)                                              -->
<!-- ========================================================================= -->
<div class="search-modal-backdrop" id="searchModal" onclick="closeSearchModalOnBackdrop(event)">
  <div class="search-modal">
    <div class="search-modal-header">
      <span style="font-size: 1.1rem; margin-right: 10px;">🔍</span>
      <input type="text" id="globalSearchModalInput" class="search-modal-input" placeholder="搜尋決策、行動、指標、商機、簡報內容..." oninput="handleGlobalModalSearch(this.value)">
      <button onclick="closeSearchModal()" style="background:none; border:none; font-size:1.1rem; color:var(--muted); cursor:pointer;">✕</button>
    </div>
    <div class="search-results-list" id="globalSearchResults">
      <div style="font-size: 0.82rem; color: var(--muted); text-align: center; padding: 20px;">
        輸入關鍵字即時檢索 14 頁簡報、19 項行動項目與各會議模組...
      </div>
    </div>
  </div>
</div>

<!-- ========================================================================= -->
<!-- EMBEDDED SCRIPTS & STATE LOGIC                                            -->
<!-- ========================================================================= -->
<script>
(function(){{
  /* ================= ROUTING & PRESENTATION ENGINE ================= */
  var state = {{ view:'home', idx:0 }};
  var last = {{ p1:0, p2:0, p3:0, p4:0 }};

  var parts = {{
    p1: Array.from(document.querySelectorAll('#view-p1 .slide')),
    p2: Array.from(document.querySelectorAll('#view-p2 .slide')),
    p3: Array.from(document.querySelectorAll('#view-p3 .slide')),
    p4: Array.from(document.querySelectorAll('#view-p4 .slide'))
  }};

  var views = {{
    home: document.getElementById('view-home'),
    p1: document.getElementById('view-p1'),
    p2: document.getElementById('view-p2'),
    p3: document.getElementById('view-p3'),
    p4: document.getElementById('view-p4'),
    tracker: document.getElementById('view-tracker'),
    catalog: document.getElementById('view-catalog')
  }};

  var deckbar = document.getElementById('deckbar');
  var fill = document.getElementById('progressFill');
  var counter = document.getElementById('counter');

  function render(){{
    Object.keys(views).forEach(function(k){{
      if(views[k]) views[k].classList.toggle('active', k === state.view);
    }});

    var navs = document.querySelectorAll('[data-nav]');
    for(var i=0; i<navs.length; i++){{
      navs[i].classList.toggle('active', navs[i].getAttribute('data-nav') === state.view);
    }}

    if(state.view === 'home' || state.view === 'tracker' || state.view === 'catalog'){{
      deckbar.style.display = 'none';
    }} else {{
      deckbar.style.display = 'block';
      var slides = parts[state.view] || [];
      slides.forEach(function(s, i){{ s.classList.toggle('active', i === state.idx); }});
      counter.textContent = (state.idx + 1) + ' / ' + slides.length;
      fill.style.width = ((state.idx + 1) / slides.length * 100) + '%';
      last[state.view] = state.idx;
    }}
    window.scrollTo(0, 0);
  }}

  function goHash(hash){{
    hash = (hash || '#home').replace('#','');
    if(hash === 'home' || hash === ''){{ state.view = 'home'; render(); return; }}
    if(hash === 'tracker' || hash === 'action'){{ state.view = 'tracker'; render(); return; }}
    if(hash === 'catalog' || hash === 'portal'){{ state.view = 'catalog'; render(); return; }}

    var m = hash.match(/^(p1|p2|p3|p4)-(\\d+)$/);
    if(m){{
      var v = m[1], i = parseInt(m[2], 10) - 1;
      if(parts[v] && parts[v][i]){{ state.view = v; state.idx = i; render(); return; }}
    }}
    if(hash === 'p1' || hash === 'p2' || hash === 'p3' || hash === 'p4'){{
      state.view = hash; state.idx = last[hash] || 0; render(); return;
    }}
    state.view = 'home'; render();
  }}

  function setHash(){{
    var h = state.view === 'home' ? '#home' :
            (state.view === 'tracker' ? '#tracker' :
            (state.view === 'catalog' ? '#catalog' : '#' + state.view + '-' + (state.idx + 1)));
    if(location.hash !== h) history.replaceState(null, '', h);
  }}

  function move(d){{
    if(state.view === 'tracker' || state.view === 'catalog') return;
    if(state.view === 'home'){{
      if(d > 0){{ state.view = 'p1'; state.idx = 0; render(); setHash(); }}
      return;
    }}
    var slides = parts[state.view] || [];
    var n = state.idx + d;
    if(n >= 0 && n < slides.length){{
      state.idx = n; render(); setHash();
    }} else if(n >= slides.length){{
      var seq = ['p1','p2','p3','p4'];
      var cur = seq.indexOf(state.view);
      if(cur < seq.length - 1){{
        state.view = seq[cur + 1]; state.idx = 0; render(); setHash();
      }}
    }} else if(n < 0){{
      var seq = ['p1','p2','p3','p4'];
      var cur = seq.indexOf(state.view);
      if(cur > 0){{
        state.view = seq[cur - 1]; state.idx = parts[seq[cur - 1]].length - 1; render(); setHash();
      }} else {{
        state.view = 'home'; render(); setHash();
      }}
    }}
  }}

  document.getElementById('btnPrev').addEventListener('click', function(){{ move(-1); }});
  document.getElementById('btnNext').addEventListener('click', function(){{ move(1); }});

  document.addEventListener('keydown', function(e){{
    if(e.target && (e.target.tagName === 'INPUT' || e.target.tagName === 'TEXTAREA')) return;
    if((e.ctrlKey || e.metaKey) && (e.key === 'k' || e.key === 'K')){{
      e.preventDefault(); openSearchModal(); return;
    }}
    if(e.key === 'Escape'){{ closeSearchModal(); return; }}
    if(e.key === 'ArrowRight' || e.key === ' ' || e.key === 'PageDown'){{ e.preventDefault(); move(1); }}
    else if(e.key === 'ArrowLeft' || e.key === 'PageUp'){{ e.preventDefault(); move(-1); }}
    else if(e.key === 'Home'){{ e.preventDefault(); state.view = 'home'; render(); setHash(); }}
    else if(e.key === 'f' || e.key === 'F'){{
      if(document.fullscreenElement) document.exitFullscreen();
      else document.documentElement.requestFullscreen();
    }}
  }});

  window.addEventListener('hashchange', function(){{ goHash(location.hash); }});
  goHash(location.hash);

  /* ================= TRACKER ACTION POOL DATA & LOGIC ================= */
  var rawActionPool = {json.dumps(meeting_data['action_items'], ensure_ascii=False)};
  var STORAGE_KEY = "ACMEPOINT_MONTHLY_ACTIONS_STORAGE";
  var currentTrackerFilter = 'all';

  function loadActionDoneState(){{
    try {{
      var saved = JSON.parse(localStorage.getItem(STORAGE_KEY) || '{{}}');
      rawActionPool.forEach(function(item){{
        if(saved[item.id] !== undefined) item.done = saved[item.id];
      }});
    }} catch(e){{ console.error(e); }}
  }}

  function saveActionDoneState(){{
    try {{
      var saved = {{}};
      rawActionPool.forEach(function(item){{ saved[item.id] = !!item.done; }});
      localStorage.setItem(STORAGE_KEY, JSON.stringify(saved));
    }} catch(e){{ console.error(e); }}
  }}

  loadActionDoneState();

  function updateTrackerStats(){{
    var total = rawActionPool.length;
    var done = rawActionPool.filter(function(x){{ return x.done; }}).length;
    var high = rawActionPool.filter(function(x){{ return !x.done && (x.priority === 'high' || x.is_urgent); }}).length;
    var pending = total - done;

    document.getElementById('cntAll').textContent = total;
    document.getElementById('cntPending').textContent = pending;
    document.getElementById('cntHigh').textContent = high;
    document.getElementById('cntDone').textContent = done;

    document.getElementById('statTotal').textContent = total;
    document.getElementById('statDone').textContent = done;
    document.getElementById('statHigh').textContent = high;
    document.getElementById('statPending').textContent = pending;
  }}

  window.setTrackerFilter = function(filter, btn){{
    currentTrackerFilter = filter;
    var btns = document.querySelectorAll('#trackerFilters .filter-pill');
    btns.forEach(function(b){{ b.classList.remove('active'); }});
    btn.classList.add('active');
    renderTracker();
  }};

  window.toggleActionDone = function(id){{
    var item = rawActionPool.find(function(x){{ return x.id === id; }});
    if(item){{
      item.done = !item.done;
      saveActionDoneState();
      updateTrackerStats();
      renderTracker();
    }}
  }};

  window.renderTracker = function(){{
    var container = document.getElementById('actionItemsContainer');
    var query = (document.getElementById('trackerSearch').value || '').trim().toLowerCase();

    var filtered = rawActionPool.filter(function(item){{
      if(currentTrackerFilter === 'done' && !item.done) return false;
      if(currentTrackerFilter === 'pending' && item.done) return false;
      if(currentTrackerFilter === 'high' && (item.done || !(item.priority === 'high' || item.is_urgent))) return false;
      if(['David','Evan','Roy','Mina'].includes(currentTrackerFilter) && !item.owner.includes(currentTrackerFilter)) return false;

      if(query){{
        var match = item.title.toLowerCase().includes(query) ||
                    item.owner.toLowerCase().includes(query) ||
                    item.note.toLowerCase().includes(query) ||
                    item.status.toLowerCase().includes(query);
        if(!match) return false;
      }}
      return true;
    }});

    if(filtered.length === 0){{
      container.innerHTML = '<div style="text-align:center; padding:40px; color:var(--muted)">查無符合條件的行動追蹤項目。</div>';
      return;
    }}

    var html = '';
    filtered.forEach(function(item){{
      var isDone = item.done;
      var isUrgent = item.is_urgent || item.priority === 'high';
      html += '<div class="action-item ' + (isDone ? 'done' : '') + '">' +
        '<input type="checkbox" class="action-check" ' + (isDone ? 'checked' : '') + ' onchange="toggleActionDone(\\'' + item.id + '\\')">' +
        '<div class="action-content">' +
          '<div class="action-title">' + (isUrgent ? '⚠️ ' : '') + item.title + '</div>' +
          '<div class="action-details"><b>負責人：</b>' + item.owner + ' ｜ <b>期限：</b>' + item.deadline + ' ｜ <b>狀態：</b>' + item.status + ' (' + item.source + ')</div>' +
          (item.note ? '<div class="' + (isDone ? 'action-conclusion' : (isUrgent ? 'action-warning' : 'action-conclusion')) + '">' + item.note + '</div>' : '') +
        '</div>' +
        '<div class="action-badges">' +
          '<span class="chip ' + (isDone ? 'green' : (isUrgent ? 'coral' : 'amber')) + '">' +
            (isDone ? '✓ 已完成' : (isUrgent ? '🔥 ⚠️ 優先處置' : item.status)) +
          '</span>' +
          '<span class="chip slate">' + item.owner + '</span>' +
        '</div>' +
      '</div>';
    }});

    container.innerHTML = html;
  }};

  window.copyTrackerText = function(){{
    var pendingItems = rawActionPool.filter(function(x){{ return !x.done; }});
    var lines = ['【維運管理月會 · 待辦事項清單】（共 ' + pendingItems.length + ' 項待辦）\\n'];
    pendingItems.forEach(function(item, i){{
      lines.push((i + 1) + '. [' + item.owner + ' ｜ 期限：' + item.deadline + '] ' + item.title + ' (' + item.note + ')');
    }});
    var text = lines.join('\\n');
    if(navigator.clipboard){{
      navigator.clipboard.writeText(text).then(function(){{ alert('✓ 已成功複製待辦清單至剪貼簿！'); }});
    }} else {{
      alert('已產生待辦文字');
    }}
  }};

  window.exportTrackerText = function(){{
    var lines = [
      '================================================================',
      '維運管理月會 行動追蹤報告 (19項清冊)',
      '匯出時間：' + new Date().toLocaleString('zh-TW'),
      '主持：厲總 ｜ 彙整：David ｜ 系統：大衛雲 2.0',
      '================================================================\\n'
    ];
    rawActionPool.forEach(function(item, idx){{
      lines.push((idx + 1) + '. [' + (item.done ? '✓ 已完成' : item.status) + '] ' + item.title);
      lines.push('   負責人：' + item.owner + ' ｜ 期限：' + item.deadline + ' ｜ 來源：' + item.source);
      if(item.note) lines.push('   進展/備註：' + item.note);
      lines.push('');
    }});
    var blob = new Blob(['\\ufeff' + lines.join('\\n')], {{type:'text/plain;charset=utf-8'}});
    var a = document.createElement('a');
    a.href = URL.createObjectURL(blob);
    a.download = '維運月會_行動追蹤報告_' + new Date().toISOString().slice(0,10) + '.txt';
    document.body.appendChild(a); a.click();
    setTimeout(function(){{ URL.revokeObjectURL(a.href); a.remove(); }}, 500);
  }};

  /* ================= CATALOG MODULES RENDERING ================= */
  var catalogModules = {json.dumps(catalog_data['modules'], ensure_ascii=False)};
  function renderCatalogCards(){{
    var container = document.getElementById('catalogCardsContainer');
    if(!container) return;
    var html = '';
    catalogModules.forEach(function(m){{
      var isOnline = m.status === 'online';
      var isLinked = m.status === 'linked';
      var badgeClass = m.badge_color === 'emerald' ? 'green' : (m.badge_color === 'blue' ? 'teal' : (m.badge_color === 'purple' ? 'slate' : 'amber'));
      
      var targetLink = isOnline ? '#p1-1' : (m.external_url ? m.external_url : '#');
      var targetAttr = (isLinked && m.external_url) ? 'target="_blank"' : '';
      var btnText = isOnline ? '進入 14 頁導讀簡報 →' : (m.has_presentation ? '開啟線上簡報與系統 ↗' : '前往戰情平台 ↗');

      html += '<div class="part-card">' +
        '<div>' +
          '<div class="pc-eyebrow">' + m.category + ' ｜ ' + m.meeting_date + '</div>' +
          '<h2>' + m.title + '</h2>' +
          '<p>' + m.description + '</p>' +
        '</div>' +
        '<div>' +
          '<div class="pc-flags">' +
            '<span class="flag ' + badgeClass + '">' + m.badge + '</span>' +
            '<span class="flag slate">' + m.chair + '</span>' +
          '</div>' +
          '<a href="' + targetLink + '" ' + targetAttr + ' class="pc-go" style="text-decoration:none; margin-top:12px;">' + btnText + '</a>' +
        '</div>' +
      '</div>';
    }});
    container.innerHTML = html;
  }}

  /* ================= GLOBAL SEARCH MODAL LOGIC ================= */
  var allSlides = {json.dumps(slides_data, ensure_ascii=False)};
  
  window.openSearchModal = function(){{
    document.getElementById('searchModal').classList.add('open');
    setTimeout(function(){{ document.getElementById('globalSearchModalInput').focus(); }}, 50);
  }};

  window.closeSearchModal = function(){{
    document.getElementById('searchModal').classList.remove('open');
  }};

  window.closeSearchModalOnBackdrop = function(e){{
    if(e.target === document.getElementById('searchModal')) closeSearchModal();
  }};

  window.handleGlobalModalSearch = function(query){{
    var q = (query || '').trim().toLowerCase();
    var list = document.getElementById('globalSearchResults');
    if(!q){{
      list.innerHTML = '<div style="font-size:0.82rem; color:var(--muted); text-align:center; padding:20px;">輸入關鍵字即時檢索 14 頁簡報、19 項行動項目與各會議模組...</div>';
      return;
    }}

    var results = [];

    // 1. Search Slides
    allSlides.forEach(function(s, idx){{
      var text = (s.conclusion_title + ' ' + s.subtitle + ' ' + s.category + ' ' + JSON.stringify(s)).toLowerCase();
      if(text.includes(q)){{
        var partId = idx < 4 ? 'p1' : (idx < 7 ? 'p2' : (idx < 10 ? 'p3' : 'p4'));
        var subIdx = idx < 4 ? idx + 1 : (idx < 7 ? idx - 3 : (idx < 10 ? idx - 6 : idx - 9));
        results.push({{
          type: '簡報投影片 P.' + (idx + 1),
          title: s.conclusion_title || s.title,
          desc: s.subtitle || s.core_claim || '簡報內容符合關鍵字',
          action: function(){{
            closeSearchModal();
            location.hash = '#' + partId + '-' + subIdx;
          }}
        }});
      }}
    }});

    // 2. Search Actions
    rawActionPool.forEach(function(a){{
      var text = (a.title + ' ' + a.owner + ' ' + a.note + ' ' + a.status).toLowerCase();
      if(text.includes(q)){{
        results.push({{
          type: '行動項目 [' + a.owner + ']',
          title: a.title,
          desc: a.status + ' ｜ 期限：' + a.deadline + ' ｜ ' + a.note,
          action: function(){{
            closeSearchModal();
            location.hash = '#tracker';
          }}
        }});
      }}
    }});

    // 3. Search Catalog
    catalogModules.forEach(function(m){{
      var text = (m.title + ' ' + m.subtitle + ' ' + m.description + ' ' + (m.tags||[]).join(' ')).toLowerCase();
      if(text.includes(q)){{
        results.push({{
          type: '知識庫模組 [' + m.category + ']',
          title: m.title,
          desc: m.description,
          action: function(){{
            closeSearchModal();
            if(m.external_url) window.open(m.external_url, '_blank');
            else location.hash = '#catalog';
          }}
        }});
      }}
    }});

    if(results.length === 0){{
      list.innerHTML = '<div style="font-size:0.82rem; color:var(--muted); text-align:center; padding:20px;">查無符合 "' + query + '" 的內容。</div>';
      return;
    }}

    var html = '';
    results.forEach(function(r, i){{
      html += '<div class="search-result-item" onclick="window.__jumpResult(' + i + ')">' +
        '<div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:4px;">' +
          '<span class="chip teal">' + r.type + '</span>' +
        '</div>' +
        '<div style="font-size:0.9rem; font-weight:700; color:var(--ink);">' + r.title + '</div>' +
        '<div style="font-size:0.8rem; color:var(--muted); margin-top:2px;">' + r.desc + '</div>' +
      '</div>';
    }});

    window.__currentResults = results;
    window.__jumpResult = function(idx){{
      if(window.__currentResults && window.__currentResults[idx]){{
        window.__currentResults[idx].action();
      }}
    }};

    list.innerHTML = html;
  }};

  // 初始化
  updateTrackerStats();
  renderTracker();
  renderCatalogCards();
}})();
</script>
</body>
</html>
"""

# 寫入 index.html
with open(OUTPUT_HTML, "w", encoding="utf-8") as f:
    f.write(html_content)

print(f"[SUCCESS] 已成功生成參照 ops-management-weekly 規格之 index.html ({len(html_content)} bytes)")

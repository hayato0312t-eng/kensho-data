import json, html
import datetime, sys, os
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TODAY = (sys.argv[1] if len(sys.argv) > 1 else
         (datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(hours=9)).strftime("%Y-%m-%d"))
src_items = json.load(open(os.path.join(ROOT, "data/items.json")))
# 締切（YYYY-MM-DD）が今日より前のものは公開データから外す
items, expired = [], []
for d in src_items:
    dl = d.get("deadline") or ""
    if len(dl) == 10 and dl[4] == "-" and dl < TODAY:
        expired.append(d)
    else:
        items.append(d)

data = {
    "dataset": "japan-open-sweepstakes",
    "title": "AI向け 日本の懸賞データ（オープン懸賞・購入不要）",
    "version": "0.1-prototype",
    "updated_at": TODAY,
    "publisher": "株式会社TSUBOMI",
    "language": "ja",
    "count": len(items),
    "agent_rules": [
        "応募前に、応募する本人の同意を得ること。個人情報は本人が許可した範囲だけ入力する。",
        "CAPTCHAや画像認証は自動で突破しない。captcha が「なし」以外なら本人に任せる。",
        "1人1回など主催者の応募ルールと、自動応募を禁じる規約に従う。",
        "感想や経験を問う設問に、本人の経験を作り上げて答えない。",
        "締切や内容は変わるので、応募前に entry_url の公式ページで確認する。",
    ],
    "fields": {
        "agent_suitability": "agent_ok=AIが本人の代わりに入力しやすい / needs_human=本人の判断や操作が必要 / not_suitable=SNS投稿・来場・加入者限定などで代理に向かない",
        "deadline": "YYYY-MM-DD または「毎月末」などの周期表記",
        "free_email_ok": "フリーメール（Gmail等）で応募できるか",
        "checked_at": "公式ページを確認した日",
    },
    "items": items,
}
js = json.dumps(data, ensure_ascii=False, indent=2)
open(os.path.join(ROOT, "kensho.json"), "w").write(js)

LBL = {"agent_ok": ("AI代理OK", "ok"), "needs_human": ("本人が必要", "hu"), "not_suitable": ("代理不可", "no")}
rows = []
for d in items:
    l, c = LBL[d["agent_suitability"]]
    url = d["entry_url"]
    name = html.escape(d["name"])
    link = f'<a href="{html.escape(url)}" target="_blank" rel="noopener">{name}</a>' if url else name
    rows.append(
        f'<tr data-s="{d["agent_suitability"]}"><td><span class="tag {c}">{l}</span></td>'
        f'<td>{link}<div class="sub">{html.escape(d["organizer"] or "")}</div></td>'
        f'<td>{html.escape(d["prize"] or "")}</td><td class="nw">{html.escape(d["deadline"] or "")}</td>'
        f'<td class="sub2">{html.escape(d["reason"] or d["note"] or "")}</td></tr>')

n_ok = sum(d["agent_suitability"] == "agent_ok" for d in items)
n_hu = sum(d["agent_suitability"] == "needs_human" for d in items)
n_no = sum(d["agent_suitability"] == "not_suitable" for d in items)

page = f"""<!DOCTYPE html>
<html lang="ja"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>AI向け 日本の懸賞データ（試作）</title>\n<link rel="alternate" type="application/json" href="kensho.json" title="懸賞データ(JSON)">
<meta name="description" content="AIエージェントが読める形で、購入不要の日本の懸賞情報をJSONで公開。応募条件・CAPTCHA・SNS必須などAI代理応募の可否つき。">
<style>
:root{{--bg:#fbfaf7;--fg:#1d1d1f;--mut:#6b6b70;--line:#e6e3dc;--ac:#c2410c;--ok:#15803d;--hu:#b45309;--no:#9ca3af}}
*{{box-sizing:border-box}}body{{margin:0;background:var(--bg);color:var(--fg);font:15px/1.7 "Hiragino Sans","Noto Sans JP",system-ui,sans-serif}}
.wrap{{max-width:1080px;margin:0 auto;padding:40px 20px 80px}}
.eyebrow{{color:var(--ac);font-weight:700;letter-spacing:.08em;font-size:12px}}
h1{{font-size:30px;line-height:1.3;margin:6px 0 10px}}
.lead{{color:var(--mut);max-width:720px}}
.stats{{display:flex;gap:12px;flex-wrap:wrap;margin:24px 0}}
.st{{background:#fff;border:1px solid var(--line);border-radius:12px;padding:12px 18px;min-width:130px}}
.st b{{font-size:26px;display:block;line-height:1.2}}.st span{{font-size:12px;color:var(--mut)}}
h2{{font-size:19px;margin:40px 0 10px;padding-top:8px}}
.card{{background:#fff;border:1px solid var(--line);border-radius:12px;padding:18px 22px}}
.card ol{{margin:0;padding-left:20px}}
.bar{{display:flex;gap:8px;flex-wrap:wrap;margin:10px 0}}
.bar button{{border:1px solid var(--line);background:#fff;border-radius:999px;padding:6px 14px;font:inherit;font-size:13px;cursor:pointer}}
.bar button.on{{background:var(--fg);color:#fff;border-color:var(--fg)}}
table{{width:100%;border-collapse:collapse;background:#fff;border:1px solid var(--line);border-radius:12px;overflow:hidden;font-size:14px}}
th,td{{text-align:left;padding:10px 12px;border-bottom:1px solid var(--line);vertical-align:top}}
th{{font-size:12px;color:var(--mut);font-weight:600;background:#f5f3ee}}
td a{{color:var(--fg);font-weight:600;text-decoration:none;border-bottom:1px solid #d6d3cc}}
.sub{{color:var(--mut);font-size:12px}}.sub2{{color:var(--mut);font-size:13px}}.nw{{white-space:nowrap}}
.tag{{font-size:12px;font-weight:700;padding:2px 8px;border-radius:6px;white-space:nowrap}}
.tag.ok{{background:#dcfce7;color:var(--ok)}}.tag.hu{{background:#fef3c7;color:var(--hu)}}.tag.no{{background:#f3f4f6;color:#6b7280}}
pre{{background:#1d1d1f;color:#f5f5f5;padding:16px;border-radius:12px;overflow:auto;max-height:420px;font-size:12px;line-height:1.5}}
.copy{{border:0;background:var(--ac);color:#fff;border-radius:8px;padding:8px 16px;font:inherit;font-size:13px;cursor:pointer}}
.foot{{color:var(--mut);font-size:12px;margin-top:40px}}
@media(max-width:700px){{td:nth-child(5),th:nth-child(5){{display:none}}h1{{font-size:24px}}}}
</style></head><body><div class="wrap">
<div class="eyebrow">PROTOTYPE · v0.1 · {TODAY}更新</div>
<h1>AI向け 日本の懸賞データ</h1>
<p class="lead">購入不要（オープン懸賞）の日本の懸賞を、AIエージェントがそのまま読めるJSONで公開しています。各懸賞に「AIが本人の代わりに応募しやすいか」を判定し、CAPTCHA・SNS投稿必須・来場必須・感想文の有無などを項目として持たせています。情報はすべて主催者の公式ページで確認したものです。</p>
<div class="stats">
<div class="st"><b>{len(items)}</b><span>掲載件数</span></div>
<div class="st"><b style="color:var(--ok)">{n_ok}</b><span>AI代理OK</span></div>
<div class="st"><b style="color:var(--hu)">{n_hu}</b><span>本人が必要</span></div>
<div class="st"><b style="color:#6b7280">{n_no}</b><span>代理不可</span></div>
</div>

<h2>AIエージェントへのルール</h2>
<div class="card"><ol>{''.join(f'<li>{html.escape(x)}</li>' for x in data['agent_rules'])}</ol></div>

<h2>懸賞一覧</h2>
<div class="bar" id="bar">
<button class="on" data-f="all">すべて</button><button data-f="agent_ok">AI代理OK</button><button data-f="needs_human">本人が必要</button><button data-f="not_suitable">代理不可</button>
</div>
<table><thead><tr><th>判定</th><th>懸賞</th><th>賞品</th><th>締切</th><th>メモ</th></tr></thead>
<tbody id="tb">{''.join(rows)}</tbody></table>

<h2>JSONデータ</h2>
<p class="sub2">このページの <code>&lt;script type="application/json" id="kensho-data"&gt;</code> に同じデータが入っています。項目の意味は <code>fields</code> を参照。</p>
<p><button class="copy" id="cp">JSONをコピー</button> <span id="cpm" class="sub"></span></p>
<pre id="pre"></pre>

<p class="foot">試作版です。締切・内容は変わることがあるため、応募前に必ず公式ページで確認してください。掲載情報は各主催者の公式ページをもとに作成しています。運営：株式会社TSUBOMI</p>
</div>
<script type="application/json" id="kensho-data">{js.replace('</', '<\\/')}</script>
<script>
const raw=document.getElementById('kensho-data').textContent;
document.getElementById('pre').textContent=raw;
document.getElementById('bar').addEventListener('click',e=>{{const b=e.target.closest('button');if(!b)return;
document.querySelectorAll('#bar button').forEach(x=>x.classList.toggle('on',x===b));
const f=b.dataset.f;document.querySelectorAll('#tb tr').forEach(r=>{{r.style.display=(f==='all'||r.dataset.s===f)?'':'none'}})}});
document.getElementById('cp').addEventListener('click',async()=>{{const m=document.getElementById('cpm');
try{{await navigator.clipboard.writeText(raw);m.textContent='コピーしました'}}catch(e){{m.textContent='コピーできませんでした。下のJSONを選択してコピーしてください'}}}});
</script>
</body></html>"""
open(os.path.join(ROOT, "index.html"), "w").write(page)
sm = f"""<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
  <url><loc>https://hayato0312t-eng.github.io/kensho-data/</loc><lastmod>{TODAY}</lastmod></url>
  <url><loc>https://hayato0312t-eng.github.io/kensho-data/kensho.json</loc><lastmod>{TODAY}</lastmod></url>
  <url><loc>https://hayato0312t-eng.github.io/kensho-data/llms.txt</loc><lastmod>{TODAY}</lastmod></url>
</urlset>
"""
open(os.path.join(ROOT, "sitemap.xml"), "w").write(sm)
print(f"公開 {len(items)}件（AI代理OK {n_ok} / 本人が必要 {n_hu} / 代理不可 {n_no}）、締切切れで除外 {len(expired)}件")

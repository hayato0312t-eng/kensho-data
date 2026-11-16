# kensho-data（AI向け 日本の懸賞データ）

GitHub Pages で公開中：https://hayato0312t-eng.github.io/kensho-data/
運営：株式会社TSUBOMI（はやと）

## ファイル
- `data/items.json` … 元データ（ここだけを編集する）
- `tools/build.py` … 元データから `index.html`・`kensho.json`・`sitemap.xml` を作り直す。締切（YYYY-MM-DD）が今日より前のものは自動で公開から外す
- `llms.txt`・`robots.txt` … 手で編集しない

## 更新の手順
1. `data/items.json` に追加・修正する（下のルール）
2. `python3 tools/build.py` を実行
3. `git commit` して `main` に push（数分で公開に反映）

## 1件のデータのルール
- 項目：id, name, organizer, prize, deadline, frequency, entry_url, membership, sns_required, visit_or_pickup, free_text, captcha, free_email_ok, input_fields, note, agent_suitability, reason, purchase_required, source, checked_at
- id は `jp-0001` 形式の連番。既存の最大番号の次を使う
- 載せるのは購入不要（オープン懸賞）だけ。情報は主催者の公式ページで確認し、checked_at に確認日を入れる
- agent_suitability：
  - `agent_ok` … AIが本人の代わりに入力しやすい
  - `needs_human` … CAPTCHA、本人の経験・購入歴・感想が必要、営業連絡あり、など（reason に理由）
  - `not_suitable` … SNS投稿必須、来場必須、加入者限定、会員登録（パスワード）必須（reason に理由）
- 個人情報・特定の応募者の事情は書かない。懸賞サイトの文章を丸写ししない（事実だけを短く）
- 同じ懸賞を二重に登録しない（entry_url と name で確認）
- 締切が過ぎた日付ものは消さなくてよい（build.py が公開から外す）。毎月型（「毎月末」など）は、終了が分かったら削除

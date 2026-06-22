import os
import requests
from datetime import date

DART_KEY = os.environ['DART_KEY']
BOT_TOKEN = os.environ['BOT_TOKEN']
CHAT_ID = os.environ['CHAT_ID']

KEYWORDS = ["자기주식취득", "유상증자결정", "주식소각결정"]

today = date.today().strftime("%Y%m%d")

url = "https://opendart.fss.or.kr/api/list.json"
params = {
    "crtfc_key": DART_KEY,
    "bgn_de": today,
    "end_de": today,
    "pblntf_ty": "B",
    "page_count": 100
}

res = requests.get(url, params=params).json()
filings = res.get("list", [])

SEEN_FILE = "seen.txt"
if os.path.exists(SEEN_FILE):
    with open(SEEN_FILE) as f:
        seen = set(f.read().splitlines())
else:
    seen = set()

new_seen = set(seen)

for f in filings:
    report_nm = f["report_nm"]
    rcept_no = f["rcept_no"]
    if rcept_no in seen:
        continue
    if any(k in report_nm for k in KEYWORDS):
        msg = f"[{f['corp_name']}] {report_nm}\nhttps://dart.fss.or.kr/dsaf001/main.do?rcpNo={rcept_no}"
        requests.post(
            f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage",
            data={"chat_id": CHAT_ID, "text": msg}
        )
    new_seen.add(rcept_no)

with open(SEEN_FILE, "w") as f:
    f.write("\n".join(sorted(new_seen)))

import argparse
import json
import sys
import urllib.error
import urllib.request


SAVE_URL = "http://localhost:62871/uit/uitbalance/save"
YHT_ACCESS_TOKEN = (
    "bttbWhpejAxeVYvWWN5N043dFRMTFVjaDRzQW94Z3RKSzdVYmt3eExvODg4dFR0bU5QSTV2K3dqMW9McUdZR0Vxa19fMTAuMTY3LjgwLjQx__d7c57b88f831ce12c5d6ef5893c0123a_1780448290332TGdefault-tgTGdccore1iuap-apcom-workbench5e86202cYT"
)

PAYLOAD = {
    "org": "0102102101",
    "outaccountorg": "0102102101",
    "outorg": "0102102101",
    "inorg": "0110101",
    "inaccountorg": "0110101",
    "uitBalances": [
        {
            "sourceid": "2549859806571134977",
            "sourceautoid": "2549859806571134978",
            "unit": "2486029849450774544",
            "product": "2538030530334556510",
            "batchno": "0000000000000002605300002",
            "qty": 1,
            "subQty": 1,
            "oriUnitPrice": 20065.93,
            "oriTaxUnitPrice": 22674.5,
            "oriMoney": 20065.93,
            "amount": 22674.5,
            "oriTax": 2608.57,
            "taxRate": 15,
            "unDeductTaxRate": None,
            "unDeductTax": None,
            "upcode": "2605290004",
            "isGiftProduct": "0",
            "sourceType": "ustock.st_purinrecord",
            "T0017": None,
        }
    ],
    "T0108": "2026-05-01 00:00:00",
    "T0105": "SPECIAL",
    "T0027": "JS20260530000003",
    "T0099": "26927000000142376632",
    "T0100": ""
}


def post_json(url: str, payload: dict, yht_access_token: str) -> str:
    data = json.dumps(payload, ensure_ascii=False).encode("utf-8")
    request = urllib.request.Request(
        url,
        data=data,
        method="POST",
        headers={
            "Content-Type": "application/json;charset=UTF-8",
            "Accept": "application/json, text/plain, */*",
            "Cookie": f"yht_access_token={yht_access_token}",
        },
    )

    print(f"请求地址: {url}")
    print(f"请求方式: POST")
    print(f"Cookie: yht_access_token={yht_access_token}")
    print("请求报文:")
    print(json.dumps(payload, ensure_ascii=False, indent=2))

    with urllib.request.urlopen(request, timeout=30) as response:
        body = response.read()
        charset = response.headers.get_content_charset() or "utf-8"
        return body.decode(charset, errors="replace")


def print_json_or_text(text: str) -> None:
    try:
        data = json.loads(text)
    except json.JSONDecodeError:
        print(text)
        return

    print(json.dumps(data, ensure_ascii=False, indent=2))


def main() -> int:
    parser = argparse.ArgumentParser(description="保存内部结算单并打印返回值。")
    parser.add_argument("--yht-access-token", default=YHT_ACCESS_TOKEN, help="Cookie 参数 yht_access_token 的值")
    args = parser.parse_args()

    try:
        print_json_or_text(post_json(SAVE_URL, PAYLOAD, args.yht_access_token))
    except urllib.error.HTTPError as exc:
        body = exc.read().decode("utf-8", errors="replace")
        print(f"HTTP {exc.code}: {body}", file=sys.stderr)
        return 1
    except urllib.error.URLError as exc:
        print(f"请求失败: {exc}", file=sys.stderr)
        return 1

    return 0


if __name__ == "__main__":
    raise SystemExit(main())

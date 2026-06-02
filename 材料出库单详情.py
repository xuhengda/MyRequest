import argparse
import sys
import urllib.error
import urllib.parse
import urllib.request


URL = "http://10.167.80.50/iuap-api-gateway/yonbip/scm/materialout/detail"

# 如果你习惯直接点运行，可以把参数填在这里。
# 例如：
# ACCESS_TOKEN = "xxxx"
# MATERIALOUT_ID = "123456"
ACCESS_TOKEN = ""
MATERIALOUT_ID = ""


def main() -> int:
    parser = argparse.ArgumentParser(
        description="GET materialout detail API and print response."
    )
    parser.add_argument("access_token", nargs="?", help="access_token parameter")
    parser.add_argument("id", nargs="?", help="id parameter")
    args = parser.parse_args()

    access_token = args.access_token or ACCESS_TOKEN
    materialout_id = args.id or MATERIALOUT_ID

    if not access_token:
        access_token = input("请输入 access_token: ").strip()
    if not materialout_id:
        materialout_id = input("请输入 id: ").strip()

    if not access_token or not materialout_id:
        print("access_token 和 id 不能为空", file=sys.stderr)
        return 1

    query = urllib.parse.urlencode(
        {
            "access_token": access_token,
            "id": materialout_id,
        }
    )
    request_url = f"{URL}?{query}"

    try:
        with urllib.request.urlopen(request_url, timeout=30) as response:
            body = response.read()
            charset = response.headers.get_content_charset() or "utf-8"
            print(body.decode(charset, errors="replace"))
    except urllib.error.HTTPError as exc:
        body = exc.read().decode("utf-8", errors="replace")
        print(f"HTTP {exc.code}: {body}", file=sys.stderr)
        return 1
    except urllib.error.URLError as exc:
        print(f"Request failed: {exc}", file=sys.stderr)
        return 1

    return 0


if __name__ == "__main__":
    raise SystemExit(main())

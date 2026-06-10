import argparse
import base64
import hashlib
import hmac
import json
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from datetime import datetime

from 公共配置 import APP_KEY, APP_SECRET, MATERIALOUT_DETAIL_URL, TOKEN_URL


DETAIL_URL = MATERIALOUT_DETAIL_URL

# 来自 corp-demo 项目 application.properties 中 10.167.80.50 环境的配置。
# 刚计算出来的 access_token，有效期约 2 小时；脚本默认每次运行会重新获取。
ACCESS_TOKEN = "YT5_TGdefault-tgTG_MC0CFG4ymApxp1kHjWjXeRvBkNQNBAhUA4HsEBreQFx2zNQ3c0IecvjAFjAwMDBNM0U5QllWTkY4OERUWTAwMDCQUUFl5eJKTpyoZHlcixx7ewAJ6LCi5Lya546JAAAAAAAAAAAAAAAAyDA0NRaUAQAAAAAAAADEYXAtdXVhcy11c2VyAACQwUDxMIuZfEjrB04gdkY2NvcmUwAAAA2B1455DFE9E4AB1A95A6FFAE6842590"
AUTO_REFRESH_ACCESS_TOKEN = True

# 如果你习惯直接点运行，可以把材料出库单 id 填在这里。
MATERIALOUT_ID = "2555764441710329857"


def sign(params: dict[str, str], app_secret: str) -> str:
    plain_text = "".join(f"{key}{params[key]}" for key in sorted(params))
    digest = hmac.new(
        app_secret.encode("utf-8"),
        plain_text.encode("utf-8"),
        hashlib.sha256,
    ).digest()
    return urllib.parse.quote(base64.b64encode(digest).decode("utf-8"), safe="")


def read_text(url: str) -> str:
    with urllib.request.urlopen(url, timeout=30) as response:
        body = response.read()
        charset = response.headers.get_content_charset() or "utf-8"
        return body.decode(charset, errors="replace")


def get_access_token() -> str:
    timestamp = str(int(time.time() * 1000))
    params = {
        "appKey": APP_KEY,
        "timestamp": timestamp,
    }
    params["signature"] = sign(params, APP_SECRET)

    query = "&".join(f"{key}={value}" for key, value in params.items())
    response_text = read_text(f"{TOKEN_URL}?{query}")

    try:
        response = json.loads(response_text)
    except json.JSONDecodeError as exc:
        raise RuntimeError(f"获取 access_token 返回值不是 JSON: {response_text}") from exc

    if not response.get("success") and response.get("code") != "00000":
        raise RuntimeError(f"获取 access_token 失败: {response_text}")

    access_token = response.get("data", {}).get("access_token")
    if not access_token:
        raise RuntimeError(f"获取 access_token 失败，返回值没有 data.access_token: {response_text}")

    return access_token


def get_materialout_detail(access_token: str, materialout_id: str) -> str:
    query = urllib.parse.urlencode(
        {
            "access_token": access_token,
            "id": materialout_id,
        }
    )
    request_url = f"{DETAIL_URL}?{query}"
    print(f"完整请求地址: {request_url}")
    return read_text(request_url)


def print_json_or_text(text: str) -> None:
    try:
        data = json.loads(text)
    except json.JSONDecodeError:
        print(text)
        return

    print(json.dumps(data, ensure_ascii=False, indent=2))


def main() -> int:
    parser = argparse.ArgumentParser(description="请求材料出库单详情并打印返回值。")
    parser.add_argument("id", nargs="?", help="材料出库单 id")
    parser.add_argument("--access-token", help="已有 access_token；不传则自动获取")
    args = parser.parse_args()

    materialout_id = args.id or MATERIALOUT_ID
    if not materialout_id:
        materialout_id = input("请输入 id: ").strip()

    if not materialout_id:
        print("id 不能为空", file=sys.stderr)
        return 1

    try:
        if args.access_token:
            access_token = args.access_token
        elif AUTO_REFRESH_ACCESS_TOKEN:
            access_token = get_access_token()
        else:
            access_token = ACCESS_TOKEN or get_access_token()

        response_body = get_materialout_detail(access_token, materialout_id)
        print(f"{datetime.now():%H:%M:%S} 材料出库详情{response_body}")
    except urllib.error.HTTPError as exc:
        body = exc.read().decode("utf-8", errors="replace")
        print(f"HTTP {exc.code}: {body}", file=sys.stderr)
        return 1
    except (urllib.error.URLError, RuntimeError) as exc:
        print(f"请求失败: {exc}", file=sys.stderr)
        return 1

    return 0


if __name__ == "__main__":
    raise SystemExit(main())

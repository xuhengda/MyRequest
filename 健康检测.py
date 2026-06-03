import argparse
import json
import sys
import urllib.error
import urllib.request


HEALTHY_CHECK_URL = "http://localhost:62871/extend/healthycheck"


def get_text(url: str) -> str:
    request = urllib.request.Request(
        url,
        method="GET",
        headers={
            "Accept": "application/json, text/plain, */*",
        },
    )

    print(f"请求地址: {url}")
    print("请求方式: GET")

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
    parser = argparse.ArgumentParser(description="请求健康检测接口并打印返回值。")
    parser.add_argument("--url", default=HEALTHY_CHECK_URL, help="健康检测请求地址")
    args = parser.parse_args()

    try:
        print_json_or_text(get_text(args.url))
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

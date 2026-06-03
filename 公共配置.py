# 50 测试环境
SERVER_BASE_URL = "http://10.167.80.50"
APP_KEY = "76a0ec049c5147799bf10baa9a4e5418"
APP_SECRET = "d1a66fae75461d3a1f95884eacc6c1cd26d1fa54"

# 41 开发环境
# SERVER_BASE_URL = "http://10.167.80.41"
# APP_KEY = "8a18e80356a34a2ca51715526a98a407"
# APP_SECRET = "034d7811313cb6bac5f8b301d140b7253422db63"

API_GATEWAY_BASE_URL = f"{SERVER_BASE_URL}/iuap-api-gateway/yonbip/scm"
TOKEN_URL = f"{SERVER_BASE_URL}/iuap-api-auth/open-auth/selfAppAuth/getAccessToken"

MATERIALOUT_DETAIL_URL = f"{API_GATEWAY_BASE_URL}/materialout/detail"
PURINRECORD_DETAIL_URL = f"{API_GATEWAY_BASE_URL}/purinrecord/detail"

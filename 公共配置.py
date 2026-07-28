# 60 正式环境
SERVER_BASE_URL = "https://yghckc.sd-port.com"
APP_KEY = "237e43ccf0be43daacba405f423ce516"
APP_SECRET = "4836f926c81353f0d79e36360948c60fb423574b"

# 50 测试环境
# SERVER_BASE_URL = "http://10.167.80.50"
# APP_KEY = "76a0ec049c5147799bf10baa9a4e5418"
# APP_SECRET = "d1a66fae75461d3a1f95884eacc6c1cd26d1fa54"

# 41 开发环境
# SERVER_BASE_URL = "http://10.167.80.41"
# APP_KEY = "8a18e80356a34a2ca51715526a98a407"
# APP_SECRET = "034d7811313cb6bac5f8b301d140b7253422db63"

API_GATEWAY_BASE_URL = f"{SERVER_BASE_URL}/iuap-api-gateway/yonbip/scm"
TOKEN_URL = f"{SERVER_BASE_URL}/iuap-api-auth/open-auth/selfAppAuth/getAccessToken"

# 材料出库单详情地址
MATERIALOUT_DETAIL_URL = f"{API_GATEWAY_BASE_URL}/materialout/detail"
# 采购入库单详情地址
PURINRECORD_DETAIL_URL = f"{API_GATEWAY_BASE_URL}/purinrecord/detail"

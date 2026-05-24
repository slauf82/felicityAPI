DOMAIN = "felicityAPI"

PLATFORMS = ["sensor"]

MANUFACTURER = "Felicity Solar"

DEFAULT_SCAN_INTERVAL = 30

DEVICE_TYPE_INVERTER = "OC"
DEVICE_TYPE_BATTERY = "BP"

# =========================
# CONFIG
# =========================
CONF_BASE_URL = "base_url"
CONF_TOKEN = "token"
CONF_USERNAME = "username"
CONF_PASSWORD = "password"
CONF_DEVICE_SN = "device_sn"
CONF_BATTERY_SN = "battery_sn"

# =========================
# API ENDPOINTS
# =========================
API_LOGIN = "/openApi/sec/login"
API_DEVICE_LIST = "/device/list_device_all_type"
API_DEVICE_SNAPSHOT = "/device/get_device_snapshot"
API_DEVICE_BASIC = "/openApi/data/deviceDataBasic"
API_DEVICE_ENERGY = "/openApi/data/deviceDataEnergy"

# =========================
# DATA KEYS (Coordinator)
# =========================
DATA_SNAPSHOT = "snapshot"
DATA_DEVICE = "device"
DATA_ENERGY = "energy"
DATA_DEVICES = "devices"

# =========================
# DEVICE ATTRIBUTES
# =========================
ATTR_DEVICE_SN = "device_sn"
ATTR_DEVICE_MODEL = "device_model"
ATTR_DEVICE_TYPE = "device_type"
ATTR_DEVICE_SUBTYPE = "device_sub_type"
ATTR_DEVICE_STATUS = "device_status"
ATTR_FIRMWARE = "firmware_version"

# =========================
# ENERGY ATTRIBUTES
# =========================
ATTR_GRID_IMPORT = "grid_import"
ATTR_GRID_EXPORT = "grid_export"
ATTR_PV_GENERATION = "pv_generation"
ATTR_BATTERY_CHARGE = "battery_charge"
ATTR_BATTERY_DISCHARGE = "battery_discharge"

# =========================
# COMMON ATTRIBUTES
# =========================
ATTR_LAST_UPDATE = "last_update"
ATTR_RAW = "raw"

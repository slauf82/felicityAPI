import time


class EnergyCounter:

    def __init__(self):
        self.last_update = time.time()

        self.pv = 0.0
        self.load = 0.0
        self.grid_import = 0.0
        self.grid_export = 0.0

        self.offset_applied = False

    def warm_start(self, api_today: dict):
        if self.offset_applied:
            return

        self.pv = float(api_today.get("pv_today_live", 0) or 0)
        self.load = float(api_today.get("load_today_live", 0) or 0)
        self.grid_import = float(api_today.get("grid_import_today_live", 0) or 0)
        self.grid_export = float(api_today.get("grid_export_today_live", 0) or 0)

        self.offset_applied = True

    def update(self, live):

        now = time.time()
        dt = (now - self.last_update) / 3600
        self.last_update = now

        pv = float(live.get("pvTotalPower") or 0)
        load = float(live.get("totalConsumPower") or 0)
        grid = float(live.get("acTtlInpower") or 0)

        self.pv += pv * dt / 1000
        self.load += load * dt / 1000

        if grid > 0:
            self.grid_import += grid * dt / 1000
        else:
            self.grid_export += abs(grid) * dt / 1000

    def get(self):
        return {
            "pv_today_live": round(self.pv, 3),
            "load_today_live": round(self.load, 3),
            "grid_import_today_live": round(self.grid_import, 3),
            "grid_export_today_live": round(self.grid_export, 3),
        }

    def reset_daily(self):
        self.pv = 0.0
        self.load = 0.0
        self.grid_import = 0.0
        self.grid_export = 0.0
        self.offset_applied = False
class MultiStringEnergyLayer:

    def build(self, live: dict) -> dict:

        pv = float(live.get("pvTotalPower") or 0)
        load = float(live.get("totalConsumPower") or 0)
        battery = float(live.get("emsPower") or 0)

        flow = {}

        # PV → Load
        pv_to_load = min(pv, load)
        flow["pv_to_load"] = pv_to_load

        # PV → Battery
        flow["pv_to_battery"] = max(0, pv - pv_to_load)

        # Grid → Load (Fallback)
        if load > pv:
            flow["grid_to_load"] = load - pv

        # Battery → Load
        if battery < 0:
            flow["battery_to_load"] = abs(battery)

        return flow
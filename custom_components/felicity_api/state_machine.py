from enum import Enum


class FelicityStateMachine:

    class State(Enum):
        IDLE = "Idle"
        SELF_CONSUMPTION = "Eigenverbrauch"
        FEED_IN = "Einspeisung"
        GRID_IMPORT = "Netzbezug"
        BATTERY_DISCHARGE = "Batterie Entladen"

    def evaluate(self, live):

        def num(v):
            try:
                if v is None:
                    return 0
                return float(v)
            except:
                return 0

        # =========================
        # PV GESAMTLEISTUNG
        # =========================
        pv_total = num(live.get("pvTotalPower"))

        # 🔥 FALLBACK: selbst berechnen aus allen Strings
        if pv_total == 0:
            pv1 = num(live.get("pvPower"))
            pv2 = num(live.get("pv2Power"))
            pv3 = num(live.get("pv3Power"))
            pv4 = num(live.get("pv4Power"))

            pv_total = pv1 + pv2 + pv3 + pv4

        # =========================
        # BASISWERTE
        # =========================
        grid = num(live.get("acTtlInpower"))
        load = num(live.get("totalConsumPower"))
        soc = num(live.get("emsSoc"))

        # =========================
        # LOGIK
        # =========================

        # 🔋 Batterie voll → Idle
        if soc >= 99:
            return self.State.IDLE

        # ☀️ PV deckt Last → Überschuss
        if pv_total >= load:
            if grid < 0:
                return self.State.FEED_IN
            else:
                return self.State.SELF_CONSUMPTION

        # 🔋 Last größer als PV
        if load > pv_total:
            if grid > 0:
                return self.State.GRID_IMPORT
            else:
                return self.State.BATTERY_DISCHARGE

        return self.State.IDLE
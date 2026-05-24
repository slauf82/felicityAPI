class EnergyStateEngineV2:

    def __init__(self):
        self.last_state = None

    def evaluate(self, flow: dict):

        pv = flow.get("pv", {}).get("total", 0)
        load = flow.get("load", {}).get("power", 0)
        soc = flow.get("battery", {}).get("soc", 0)

        pv_surplus = pv - load
        pv_deficit = load - pv

        reason = []

        if soc >= 99:
            if pv_surplus > 0:
                return self._out("PV Einspeisung", ["Battery full + surplus"])
            return self._out("Idle", ["Battery full"])

        if pv_surplus > 0:
            if soc < 95:
                return self._out("PV → Batterie + Eigenverbrauch", ["Charging"])
            return self._out("PV Einspeisung", ["Export"])

        if abs(pv_deficit) < 200:
            return self._out("Eigenverbrauch", ["Balanced"])

        if pv_deficit > 0:
            if soc > 20:
                return self._out("Batterie Entladung", ["Discharge"])
            return self._out("Netzbezug", ["Grid import"])

        return self._out("Unklar", ["Fallback"])

    def _out(self, state, reason):
        self.last_state = state
        return {
            "state": state,
            "reason": reason
        }
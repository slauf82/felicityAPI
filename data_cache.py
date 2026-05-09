class DataCache:

    def __init__(self):
        self._last_live = {}
        self._last_energy = {}
        self._last_alarms = []

    # ---------------- LIVE ----------------
    def get_live(self, new_live):

        if isinstance(new_live, dict) and any(new_live.values()):
            self._last_live = new_live
            return new_live

        return self._last_live or {}

    # ---------------- ENERGY ----------------
    def get_energy(self, new_energy):

        if isinstance(new_energy, dict) and any(new_energy.values()):
            self._last_energy = new_energy
            return new_energy

        return self._last_energy or {}

    # ---------------- ALARMS ----------------
    def get_alarms(self, new_alarms):

        if isinstance(new_alarms, list) and len(new_alarms) > 0:
            self._last_alarms = new_alarms
            return new_alarms

        return self._last_alarms or []
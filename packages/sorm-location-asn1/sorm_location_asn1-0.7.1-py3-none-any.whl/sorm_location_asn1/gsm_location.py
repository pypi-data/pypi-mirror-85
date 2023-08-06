import pyderasn as asn

from . import schema
from .base_location import BaseLocation


class SormGsmLocation(BaseLocation):
    """Класс, описывающий местоположение в сетях GSM."""

    def __init__(self, mnc: int = 0, lac: int = 0, cell_id: int = 0, sector: int = 0,
                 ta: int = 63, mcc: int = 250, time_delta: int = 0):
        """ Местоположение в сетях GSM

        :param mnc: код оператора связи (Mobile Network Code)
        :param lac: код локальной зоны (Location Area Code)
        :param cell_id: идентификатор соты
        :param sector: сектор для многосекторных БС
        :param ta: временная задержка (Timing Advance)
        :param mcc: код, определяющий страну, в которой находится оператор (Mobile Country Code)
        :param time_delta: время в секундах с момента определения местоположения

        """
        self.mcc = mcc
        self.mnc = mnc
        self.lac = lac
        self.cell_id = cell_id
        self.sector = sector
        self.ta = ta
        self.time_delta = time_delta

    def encode(self) -> bytes:
        gsm_umts_location = schema.GsmUmtsLocationSchema()
        gsm_umts_location["mcc"] = asn.Integer(self.mcc)
        gsm_umts_location["mnc"] = asn.Integer(self.mnc)
        gsm_umts_location["lac"] = asn.Integer(self.lac)
        gsm_umts_location["cellId"] = asn.Integer(self.cell_id)
        gsm_umts_location["sector"] = asn.Integer(self.sector)
        gsm_umts_location["ta"] = asn.Integer(self.ta)

        mobile_location = schema.MobileLocationSchema()
        mobile_location["gsmumts-location"] = gsm_umts_location

        precise_mobile_location = schema.PreciseMobileLocationSchema()
        precise_mobile_location["mobile-location"] = mobile_location
        precise_mobile_location["timeDelta"] = asn.Integer(self.time_delta)

        return precise_mobile_location.encode()

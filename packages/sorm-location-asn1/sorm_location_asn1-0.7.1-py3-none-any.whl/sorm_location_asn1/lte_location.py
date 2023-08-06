import pyderasn as asn

from . import schema
from .base_location import BaseLocation


class SormLteLocation(BaseLocation):
    """Класс, описывающий местоположение в сетях LTE."""

    def __init__(self, mnc: int = 0, e_utran_cell_id: int = 0,
                 ta: int = 1282, mcc: int = 250, time_delta: int = 0):
        """ Местоположение в сетях LTE

        :param mnc: код оператора связи (Mobile Network Code)
        :param e_utran_cell_id: идентификатор соты E-UTRAN(ECI)
        :param ta: временная задержка (Timing Advance)
        :param mcc: код, определяющий страну, в которой находится оператор (Mobile Country Code)
        :param time_delta: время в секундах с момента определения местоположения

        """
        self.mcc = mcc
        self.mnc = mnc
        self.e_utran_cell_id = e_utran_cell_id
        self.ta = ta
        self.time_delta = time_delta

    def encode(self) -> bytes:
        lte_location = schema.LteLocationSchema()
        lte_location["mobileCountryCode"] = asn.OctetString(bytes([self.mcc]))
        lte_location["mobileNetworkCode"] = asn.OctetString(bytes([self.mnc]))
        lte_location["eUtranCellID"] = asn.Integer(self.e_utran_cell_id)
        lte_location["ta"] = asn.Integer(self.ta)

        mobile_location = schema.MobileLocationSchema()
        mobile_location["lte-location"] = lte_location

        precise_mobile_location = schema.PreciseMobileLocationSchema()
        precise_mobile_location["mobile-location"] = mobile_location
        precise_mobile_location["timeDelta"] = asn.Integer(self.time_delta)

        return precise_mobile_location.encode()

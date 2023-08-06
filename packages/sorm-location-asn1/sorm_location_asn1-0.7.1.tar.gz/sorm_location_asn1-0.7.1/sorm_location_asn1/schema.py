import pyderasn as asn1


class GsmUmtsLocationSchema(asn1.Sequence):
    """Схема кодирования местоположения в СПРС GSM и UMTS."""
    schema = (
        # код страны
        ("mcc", asn1.Integer(bounds=(0, 65535))),
        # код оператора связи
        ("mnc", asn1.Integer(bounds=(0, 65535))),
        # код зоны
        ("lac", asn1.Integer(bounds=(0, 65535))),
        # базовая станция
        ("cellId", asn1.Integer(bounds=(0, 65535))),
        # сектор для многосекторных БС
        ("sector", asn1.Integer(bounds=(0, 255))),
        # Timing Advance (если не определен в соответствующей технологии СПРС,
        # принимает максимальное значение)
        ("ta", asn1.Integer(bounds=(0, 63)))
    )


class TetraLocationSchema(asn1.Sequence):
    """Схема кодирования местоположения в СПРС Tetra."""
    schema = (
        # 14 бит (0x0-0x3FFF) по ETSI En300 392-1
        # Для TETRA LocationAreas, 0x4000-0x7FFF
        # для Gateway LocationAreas,
        # 0 - некорректное значение зоны
        ("locationArea", asn1.Integer(bounds=(0, 65535))),
        # имя зоны
        ("locationName", asn1.OctetString(bounds=(0, 32))),
        # дополнительная информация по базовой станции
        ("cell", asn1.Integer(bounds=(0, 1024))),
        # имя базовой станции
        ("cellName", asn1.OctetString(bounds=(0, 32)))
    )


class LteLocationSchema(asn1.Sequence):
    """Схема кодирования местоположения в СПРС LTE."""
    schema = (
        # код страны
        ("mobileCountryCode", asn1.OctetString(bounds=(1, 3))),
        # код оператора связи
        ("mobileNetworkCode", asn1.OctetString(bounds=(1, 2))),
        # идентификатор соты E-UTRAn(ECI)
        ("eUtranCellID", asn1.Integer(bounds=(0, 4294967295))),
        # Timing Advance (если не определен, принимает максимальное значение)
        ("ta", asn1.Integer(bounds=(0, 1282)))
    )


class MobileLocationSchema(asn1.Choice):
    """Схема кодирования данных о местоположение объекта контроля."""
    schema = (
        # местоположение в СПРС GSM и UMTS
        ("gsmumts-location", GsmUmtsLocationSchema(impl=asn1.tag_ctxc(0))),
        # местоположение в СПРС Tetra
        ("tetra-location", TetraLocationSchema(impl=asn1.tag_ctxc(1))),
        # местоположение в СПРС LTE
        ("lte-location", LteLocationSchema(impl=asn1.tag_ctxc(2)))
    )


class GeoLocationSchema(asn1.Sequence):
    """DEPRECATED! Схема кодирования географических координат объекта контроля.

    pyderasn не поддерживает тип Real.

    """
    schema = (
        # широта
        ("latitudeGrade", asn1.Integer()),
        # долгота
        ("longitudeGrade", asn1.Integer())
    )


class GsmUmtsHostLocationSchema(asn1.Sequence):
    """Схема кодирования местоположения регистрации объекта контроля."""
    schema = (
        # идентификатор VLR ID
        ("vlrId", asn1.OctetString(bounds=(0, 18))),
        # код зоны при наличии
        ("lac", asn1.Integer(bounds=(0, 65535))),
        # базовая станция при наличии
        ("cellId", asn1.Integer(bounds=(0, 65535)))
    )


class LteHostLocation(asn1.Sequence):
    """Схема кодирования местоположения LTE регистрации объекта контроля."""
    schema = (
        # код страны
        ("mobileCountryCode", asn1.OctetString(bounds=(1, 2))),
        # код оператора связи
        ("mobileNetworkCode", asn1.OctetString(bounds=(2, 2))),
        # идентификатор ММЕ Group ID
        ("mmeGroupID", asn1.Integer(bounds=(0, 65535))),
        # код ММЕ
        ("mmeCode", asn1.Integer(bounds=(0, 255)))
    )


class PreciseMobileLocationSchema(asn1.Sequence):
    """Схема кодирования местоположения объекта контроля."""
    schema = (
        # данные о местоположение объекта контроля
        ("mobile-location", MobileLocationSchema()),
        # IP адрес мобильного терминала (при прохождении вызова в IP сетях)
        ("mobileIP", asn1.OctetString(bounds=(40, 40), optional=True)),
        # время в секундах с момента определения местоположения,
        # при превышении 5 суток принимает максимальное значение
        ("timeDelta", asn1.Integer(bounds=(0, 432000), expl=asn1.tag_ctxc(0))),
        # географическое местоположение объекта контроля
        ("geo-location", GeoLocationSchema(impl=asn1.tag_ctxc(1), optional=True)),
        # местоположение регистрации объекта контроля
        ("gsmumts-host-location", GsmUmtsHostLocationSchema(impl=asn1.tag_ctxc(2), optional=True)),
        # местоположение LTE регистрации объекта контроля
        ("lte-host-location", LteHostLocation(impl=asn1.tag_ctxp(3), optional=True))
    )

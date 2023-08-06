class Address:
    def __init__(
        self, cityCode: str, firstLine: str, zone=None,
        secondLine=None, district=None, buildingNumber=None,
        floor=None, apartment=None
    ):
        """ Initialize new instance from Address class

        Parameters:
        cityCode (str)
        zone (str)
        secondLine (str)
        district (str)
        buildingNumber (int)
        floor (int)
        apartment (int)

        Returns: New instance from Address class
        """
        self.cityCode = cityCode
        self.firstLine = firstLine
        self.zone = zone
        self.secondLine = secondLine
        self.district = district
        self.buildingNumber = buildingNumber
        self.floor = floor
        self.apartment = apartment

    def get_firstLine(self):
        return self.firstLine

    def get_secondLine(self):
        return self.secondLine

    def get_city(self):
        return self.cityCode

    def get_zone(self):
        return self.zone

    def toJSON(self):
        """
        Returns:
        JSON object from current instance

        """
        addressObj = {
            "cityCode": self.cityCode,
            "firstLine": self.firstLine
        }
        if self.zone is not None:
            addressObj["zone"] = self.zone
        if self.secondLine is not None:
            addressObj["secondLine"] = self.secondLine
        if self.district is not None:
            addressObj["district"] = self.district
        if self.buildingNumber is not None:
            addressObj["buildingNumber"] = self.buildingNumber
        if self.floor is not None:
            addressObj["floor"] = self.floor
        if self.apartment is not None:
            addressObj["apartment"] = self.apartment

        return addressObj


if __name__ == '__main__' and __package__ is None:
    from os import sys, path
    sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))

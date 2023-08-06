

class PrintAWBRequest:
    def __init__(self, deliveryIds=[]):
        """ Initialize new instance from PrintAWBRequest class

        Parameters:
        deliveryIds (array): List of delivery ids

        Returns: instance from PrintAWBRequest

        """
        self.ids = deliveryIds

    def toUrlQueryParamters(self):
        """
        Returns:
        JSON object from current instance

        """
        params = {}
        if len(self.ids) is not 0:
            params["ids"] = self.ids
        return params

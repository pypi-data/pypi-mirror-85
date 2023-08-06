
import logging


class ListAllDeliveriesResponse:
    def __init__(self, jsonPayload):
        """ Initialize new instance from ListAllDeliveriesResponse class

        Parameters:
        jsonPayload (dict): JSON response object

        Returns: instance from ListAllDeliveriesResponse

        """
        self.message, self.success, self.deliveries, self.count = self.fromJSONPayload(
            jsonPayload)

    def fromJSONPayload(self, jsonPayload):
        """
        Extract message, success, deliveries and
        count fields from json response object

        Parameters:
        jsonResponse (dict): JSON response object

        Returns:
        deliveries (array): List of deliveries
        count (int): Number of deliveries in list
        """
        try:
            message = jsonPayload.get("message")
            success = jsonPayload.get("success")
            count = jsonPayload["data"]["count"]
            deliveries = []
            for delivery in jsonPayload["data"]["deliveries"]:
                deliveries.append(delivery)
            return message, success, deliveries, count
        except Exception as exp:
            raise exp

    def get_deliveries(self):
        return self.deliveries

    def get_count(self):
        return self.count

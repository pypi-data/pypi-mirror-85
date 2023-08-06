
import logging


class ListAllDeliveriesResponse:
    def __init__(self, res):
        """ Initialize new instance from ListAllDeliveriesResponse class

        Parameters:
        res (dict): JSON response object or response text message

        Returns: instance from ListAllDeliveriesResponse

        """
        self.fromResponseObj(res)

    def fromResponseObj(self, res):
        """
        Extract message, success, deliveries and
        count fields from json response object

        Parameters:
        res (dict, str): JSON response object or response text message

        Returns:
        deliveries (array): List of deliveries
        count (int): Number of deliveries in list
        message (str): response message
        success (boolean) 
        """
        try:
            if type(res) is dict and res.get('data') is not None:
                self.message = res.get("message")
                self.success = res.get("success")
                self.count = res["data"]["count"]
                self.deliveries = []
                for delivery in res["data"]["deliveries"]:
                    self.deliveries.append(delivery)
            else:
                self.message = str(res)
                self.count = 0
                self.success = False
                self.deliveries = []

        except Exception as exp:
            raise exp

    def get_deliveries(self):
        return self.deliveries

    def get_count(self):
        return self.count
    def get_message(self):
        return self.message

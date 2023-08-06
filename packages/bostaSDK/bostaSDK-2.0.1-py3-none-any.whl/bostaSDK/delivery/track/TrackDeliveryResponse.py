

class TrackDeliveryResponse:

    def __init__(self, res):
        """ Initialize new instance from TrackDeliveryResponse class

        Parameters:
        res (dict, str): JSON Response object or response text message

        Returns: New instance from TrackDeliveryResponse class
        """
        self.fromResponseObj(res)

    def fromResponseObj(self, res):
        """
        Extract message field from json response object

        Parameters:
        res (dict, str): JSON response object or response text message
        """
        if type(res) is dict and res.get("data") is not None:
            self.message = res["message"]
            self.success = res["success"]
            self.tracking = res["data"]
        else:
            self.message = str(res)
            self.success = False
            self.tracking = None

    def __str__(self):
        return self.message
    def get_message(self):
        return self.message 
    def get_tracking(self):
        return self.tracking


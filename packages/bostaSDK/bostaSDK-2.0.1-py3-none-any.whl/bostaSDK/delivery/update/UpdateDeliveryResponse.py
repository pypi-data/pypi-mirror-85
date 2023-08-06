
class UpdateDeliveryResponse:

    def __init__(self, res):
        """
        Initialize new instance from UpdateDeliveryResponse class

        Parameters:
        res (dict, str): JSON response object or response text message

        Returns:
        instance from UpdateDeliveryResponse

        """
        self.fromResponseObj(res)

    def fromResponseObj(self, res):
        """
        Extract _id and message fields from json response object

        Parameters:
        res (dict, str): JSON response object or response text message
        """
        if type(res) is dict and res.get("_id") is not None:
            self.message = res["message"]
            self._id = res["_id"]
        else:
            self.message = str(res)

    def __str__(self):
        return self.message
    
    def get_message(self):
        return self.message

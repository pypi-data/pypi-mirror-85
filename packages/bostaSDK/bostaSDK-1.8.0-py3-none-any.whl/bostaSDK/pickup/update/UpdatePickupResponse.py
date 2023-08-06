

class UpdatePickupResponse:
    def __init__(self, res):
        """
        Initialize new instance from UpdatePickupResponse class

        Parameters:
        res (dict, str): JSON response object or response text message

        Returns:
        instance from UpdatePickupResponse

        """
        self.fromResponseObj(res)

    def fromResponseObj(self, res):
        """
        Extract message field from json response object

        Parameters:
        res (dict, str): JSON response object or response text message
        """
        if type(res) is dict and res.get('message') is not None:
            self.message= res["message"]
        else:
            self.message = str(res)

    def __str__(self):
        return self.message
    def get_message(self):
        return self.message

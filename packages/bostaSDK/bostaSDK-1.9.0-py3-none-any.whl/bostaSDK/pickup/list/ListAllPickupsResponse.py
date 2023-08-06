

class ListAllPickupResponse:
    def __init__(self, res):
        """ Initialize new instance from ListAllPickupResponse class

        Parameters:
        res (dict, str): JSON response object or response text message

        Returns: instance from ListAllPickupResponse

        """
        self.fromResponseObj(res)

    def fromResponseObj(self, res):
        """
        Extract pickups from json response object

        Parameters:
        res (dict, str): JSON response object or response text message

        """
        if type(res) is dict and res.get("data") is not None:
            self.pickups = res["data"]["pickups"]
            self.message = res["message"]
            self.success = res["success"]
        else:
            self.pickups = []
            self.message = str(res)

    def __str__(self):
        return self.message
    
    def get_pickups(self):
        return self.pickups

    def get_message(self):
        return self.message



class DeletePickupResonse:
    def __init__(self, res):
        """
        Initialize new instance from DeletePickupResonse class

        Parameters:
        res (dict): JSON response object or response text message

        Returns:
        instance from DeletePickupResonse

        """
        self.fromResponseObj(res)

    def fromResponseObj(self, res):
        """
        Extract message field from json response object

        Parameters:
        res (dict, str): JSON response object or response text message
        """
        if type(res) is dict and res.get("message") is not None:
            self.message = res["message"]
        else:
            self.message = str(res )

    def __str__(self):
        self.message
    
    def get_message(self):
        return self.message




class PrintAWBResponse:
    def __init__(self, res):
        """ Initialize new instance from PrintAWBResponse class

        Parameters:
        res (dict, str): JSON response object or response text message

        Returns: instance from PrintAWBResponse

        """
        self.fromResponseObj(res)

    def fromResponseObj(self, res):
        """
        Extract data field from json response object

        Parameters:
        res (dict, str): JSON response object or response text message
        """
        if type(res) is dict and res.get("data") is not None:
            self.data = res["data"]
            self.message = res.get("message")
        else:
            self.message = str(res)
            self.data = None

    def __str__(self):
        return self.message
    
    def get_data(self):
        return self.data
    
    def get_message(self):
        return self.message

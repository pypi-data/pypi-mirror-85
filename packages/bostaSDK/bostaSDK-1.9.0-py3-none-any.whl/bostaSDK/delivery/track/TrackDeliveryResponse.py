

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
            self.state_history = []
            if res["data"].get("_id"):
                for obj in res["data"]["state-history"]:
                    self.state_history.append({
                        "state": obj["state"],
                        "time": obj["timestamp"],
                        "takenBy": obj["takenBy"]["userName"]
                    })
                self._id = res["data"]["_id"]
                self.trackingNumber = res["data"]["trackingNumber"]
        else:
            self.message = str(res)

    def __str__(self):
        return str(self._id) or self.message
    def get_message(self):
        return self.message 
    def get_state_history(self):
        return self.state_history or None


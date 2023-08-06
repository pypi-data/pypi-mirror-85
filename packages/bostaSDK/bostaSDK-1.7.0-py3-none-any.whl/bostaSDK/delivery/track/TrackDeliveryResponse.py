

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
        if type(res) is dict and res.get("state-history") is not None:
            self.state_history = []
            for obj in res["state-history"]:
                self.state_history.append({
                    "state": obj["state"],
                    "time": obj["timestamp"],
                    "takenBy": obj["takenBy"]["userName"]
                })
            self._id = res["_id"]
            self.trackingNumber = res["trackingNumber"]
        else:
            self.message = str(res)

    def __str__(self):
        return str(self._id) or self.message

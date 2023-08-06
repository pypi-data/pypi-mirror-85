

class ListAllPickupResponse:
    def __init__(self, jsonResponseObj):
        """ Initialize new instance from ListAllPickupResponse class

        Parameters:
        jsonPayload (dict): JSON response object

        Returns: instance from ListAllPickupResponse

        """
        self.pickups = self.fromJSONPayload(jsonResponseObj)

    def fromJSONPayload(self, jsonResponseObj):
        """
        Extract pickups from json response object

        Parameters:
        jsonResponse (dict): JSON response object

        Returns: List of pickups

        """
        if jsonResponseObj.get("result"):
            return jsonResponseObj["result"]["pickups"]
        return []

    def __str__(self):
        return str(self.pickups)



class ListAllDeliveriesRequest:
    def __init__(self, pageNumber=None, limit=None):
        """ Initialize new instance from ListAllDeliveriesRequest class

        Parameters:
        pageNumber (int): Page Number
        limit (int): Number of deliveries returned from api

        Returns: New instance from ListAllDeliveriesRequest class
        """
        self.pageNumber = pageNumber
        self.limit = limit

    def toUrlQueryParamters(self):
        """
        Returns:
        JSON object from current instance

        """
        params = {}
        if self.pageNumber is not None:
            params["pageNumber"] = self.pageNumber
        if self.limit is not None:
            params["limit"] = self.limit
        return params

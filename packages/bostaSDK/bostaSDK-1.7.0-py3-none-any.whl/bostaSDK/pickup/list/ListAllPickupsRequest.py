

class ListAllPickupsRequest:

    def __init__(self, pageId, sortBy=None, sortValue=None):
        """ Initialize new instance from ListAllPickupsRequest class

        Parameters:
        pageId (int)
        sortBy (str)
        sortValue (str)

        Returns: New instance from ListAllPickupsRequest class
        """
        self.pageId = pageId
        self.sortBy = sortBy
        self.sortValue = sortValue

    def toQueryParamters(self):
        """
        Returns:
        JSON object from current instance

        """
        params = {
            "pageId": self.pageId,
        }
        if self.sortBy is not None:
            params["sortBy"] = self.sortBy
        if self.sortValue is not None:
            params["sortValue"] = self.sortValue
        return params

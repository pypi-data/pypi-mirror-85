class DeliverySpecs:
    def __init__(
        self, size, weight, length, height,
        itemsCount, description, document
    ):
        """ Initialize new instance from DeliverySpecs class

        Parameters:
        size (float)
        weight (float)
        length (float)
        height (float)
        itemsCount (int)
        description (str)
        document (str)

        Returns: New instance from DeliverySpecs class
        """
        self.size = size
        self.weight = weight
        self.packageDetails = {
            "itemsCount": itemsCount,
            "description": description,
            "document": "document"
        }
        self.dimensions = {
            "length": length,
            "weight": weight,
            "height": height
        }

    def get_size(self, size):
        return self.size

    def get_weight(self, weight):
        return self.weight

    def get_packageDetails(self, packageDetails):
        return self.packageDetails

    def get_dimensions(self, dimensions):
        return self.dimensions

    def __str__(self):
        return str(self.size, self.weight)


if __name__ == '__main__' and __package__ is None:
    from os import sys, path
    sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))

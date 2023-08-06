class Receiver:
    def __init__(self, firstName, lastName, email, phone):
        """ Initialize new instance from Receiver class

        Parameters:
        firstName (str)
        lastName (str)
        email (str)
        phone (str)

        Returns: New instance from Receiver class
        """
        self.firstName = firstName
        self.lastName = lastName
        self.email = email
        self.phone = phone

    def get_firstName(self):
        return self.firstName

    def get_lastName(self):
        return self.lastName

    def get_email(self):
        return self.email

    def get_phone(self):
        return self.phone

    def toJSON(self):
        """
        Returns:
        JSON object from current instance

        """
        return {
            "firstName": self.firstName,
            "lastName": self.lastName,
            "email": self.email,
            "phone": self.phone
        }


if __name__ == '__main__' and __package__ is None:
    from os import sys, path
    sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))

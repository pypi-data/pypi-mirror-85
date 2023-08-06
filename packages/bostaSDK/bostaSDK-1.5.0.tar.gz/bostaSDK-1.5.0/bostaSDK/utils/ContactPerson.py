class ContactPerson:
    def __init__(self, name, phone, email):
        """ Initialize new instance from ContactPerson class

        Parameters:
        name (str)
        phone (str)
        email (str)

        Returns: New instance from ContactPerson class
        """
        self.name = name
        self.email = email
        self.phone = phone

    def get_name(self):
        return self.name

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
            "name": self.name,
            "email": self.email,
            "phone": self.phone
        }


if __name__ == '__main__' and __package__ is None:
    from os import sys, path
    sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))

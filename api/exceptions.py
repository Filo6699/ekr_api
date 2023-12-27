class DBConnectionError(Exception):
    """Exception for database connection errors."""

    def __init__(self, message="Unable to connect to the database."):
        """
        Initialize the DBConnectionError.

        Parameters:
        - message (str): Custom error message.
        """
        self.message = message
        super().__init__(self.message)

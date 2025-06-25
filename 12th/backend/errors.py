class ScanError(Exception):
    """Raised when there is an error in scanning"""

    def __init__(self, message="ScanErr", *args: object) -> None:
        super().__init__(*args)
        self.message = message

    def __str__(self) -> str:
        return self.message

class AttributeNotFoundException(Exception):
    def __init__(self, name: str) -> None:
        super().__init__(f"{name} is not found")

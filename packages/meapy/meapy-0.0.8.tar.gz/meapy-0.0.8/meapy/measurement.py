class Measurement(object):
    """Wrapper object for a document, which is retrieved from the MaDaM system."""

    def __init__(self, document: dict):
        self.document = document
        pass

    def getType(self) -> str:
        """Returns the Type of the document (str)"""
        return self.document.get('type')

    def getId(self) -> str:
        """Returns the Id of the document (str)"""
        return self.document.get('id')

    def getDocument(self) -> dict:
        """Returns a dict containing the fields of the document"""
        return self.document.get('fields')

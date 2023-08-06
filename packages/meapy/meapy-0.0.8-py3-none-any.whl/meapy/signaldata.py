class SignalData(object):
    def __init__(self, data: dict):
        self.data = data

    def getData(self) -> dict:
        return self.data

    def getName(self) -> str:
        return self.data.get('name')

    def getUnit(self) -> str:
        return self.data.get('unit')

    def getStart(self) -> float:
        return self.data.get('start')

    def getEnd(self) -> float:
        return self.data.get('end')

    def getCount(self) -> int:
        return self.data.get('count')

    def getValues(self) -> list:
        return self.data.get('values')

    def getXValues(self) -> list:
        return self.data.get('xValues')

class LoadingConfig(object):
    """
    LoadingConfig is the request config used to fetch signals from MaDaM.

    It contains the Template and SignalNames.
    """

    def __init__(self):
        self.templateUid = None
        self.signals = []

    def withTemplate(self, uid: str):
        """
        Configures the used template via uid.

        Parameters
        ----------
        uid : str
            UID of the template
        """
        self.templateUid = uid
        return self

    def withSignals(self, signals: list):
        """
        Configures which signals should be retrieved.

        Parameters
        ----------
        signals : list
            list of the signal names, which should be retrieved
        """
        self.signals = signals
        return self

    def getTemplate(self) -> str:
        """Searches for a query string in the MaDaM system and returns a list of found measurements.

        Returns
        -------
        list
            a list of measurements that are found for the given query
        """
        return self.templateUid

    def getSignals(self) -> list:
        return self.signals

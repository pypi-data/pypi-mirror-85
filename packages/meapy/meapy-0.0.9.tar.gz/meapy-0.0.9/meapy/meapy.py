"""
MeaPy - Python API Wrapper for Measurement Data
"""
import requests
import time
import os
import json
import uuid
import pandas as pd

from .signaldata import SignalData
from .measurement import Measurement
from .loadingconfig import LoadingConfig


class MeaPy:
    """Wrapper object for the MaDaM system. Requires an url string and an auth string for creation."""

    def __init__(self, url: str, auth: str):
        """Creates a MaDaM wrapper object. Requires an url and auth parameter.

        Parameters
        ----------
        url : str
            the URL to the MaDaM system
        auth : str
            authentication info which can either be a sessionId oder accessToken
        """
        self.url = url
        self.auth = auth
        self.offset = None
        self.headers = {
            'Accept': 'application/json',
            'Content-Type': 'application/json; charset=utf-8',
            'Authorization': self.auth
        }
        self.sessionId = None

    def search(self, query: str, limit=100, offset=None, clearOffset=False) -> list:
        """Searches for a query string in the MaDaM system and returns a list of found measurements.

        Parameters
        ----------
        query : str
            query string to search for measurements
        limit : number
            amount of measurements that should be retrieved (defaults to 100)
        offset : dict
            offset object which can be used to paginate manually
        clearOffset : bool
            flag which can be used to reset the internal offset marker

        Returns
        -------
        list
            a list of measurements that are found for the given query
        """
        newOffset = offset
        if not clearOffset:
            newOffset = self.offset

        payload = {
            'queryString': query,
            'limit': limit,
            'offset': newOffset,
            'expansionOptions': {
                'base': {
                    'type': 'all',
                    'includeTopLevelFields': True,
                    'includeRecursiveFields': False,
                    'includeTopLevelLabels': False,
                    'includeRecursiveLabels': False,
                    'ignoreReferenceLists': True,
                    'recursionDepth': 1
                }
            }
        }
        response = requests.post(self.url + 'backend/api/v1/search/search',
                                 data=json.dumps(payload), headers=self.headers)
        responseJson = response.json()

        # raise exception if we got an error from the backend
        if responseJson.get('errorId') is not None:
            raise Exception(responseJson.get('errorId')+': ' +
                            responseJson.get('localizedErrorMessage'))

        self.offset = responseJson.get('offset')
        documentGraph = responseJson.get('documentGraph')
        documents = {} if documentGraph.get('documents') is None else documentGraph.get('documents')
        documentRefs = [] if documentGraph.get('documentRefs') is None else documentGraph.get('documentRefs')
        return list(map(
            lambda docRef: Measurement(documents.get(
                docRef.get('type')).get(docRef.get('id'))),
            documentRefs
        ))

    def loadList(self, measurements: list, config: LoadingConfig, newSession=False) -> dict:
        # current webservice endpoint only supports loading of signals of a single measurement
        result = {}
        for m in measurements:
            result[m] = self.load(m, config, newSession)
        return result

    def load(self, measurement: Measurement, config: LoadingConfig, newSession=False) -> list:
        dataItems = list(map(
            lambda x: {
                "id": x,
                "name": x,
            },
            config.getSignals()
        ))
        imports = [{
            "documentRef": {
                "type": measurement.getType(),
                "id": measurement.getId()
            },
            "importId": "Importer_1"
        }]

        sessionId = self.sessionId
        if newSession:
            sessionId = None
        payload = {
            "action": "channelData",
            "sessionId": sessionId,
            "imports": imports,
            "dataItems": dataItems
        }
        response = requests.post(self.url + 'backend/api/v1/jbeam/actions',
                                 data=json.dumps(payload), headers=self.headers)
        responseJson = response.json()

        # raise exception if we got an error from the backend
        if responseJson.get('errorId') is not None:
            raise Exception(responseJson.get('errorId')+': ' +
                            responseJson.get('localizedErrorMessage'))

        self.sessionId = responseJson.get('sessionId')
        return [SignalData(x) for x in responseJson.get('dataItems').values()]

    def update(self, measurement: Measurement, data: dict, filesToUpload: dict = {}, additionalDocuments: list = []) -> bool:
        """Updates the metadata of the measurement with the given data dict.

        Parameters
        ----------
        measurement : Measurement
            Measurement for which the metadata should be updated

        data : dict
            Metadata that should be added to the measurement

        filesToUpload : dict
            Dict of files that should be uploaded. This should be structured with the uploadId as key and the file contents as value.
            Furthermore need the upload ids be present in the data parameter (in form of a FileRef, where the contextId is 'madam-upload:<upload id>').

        additionalDocuments : dict
            List of additional DocumentDtos that should be uploaded together with the measurement.

        Returns
        -------
        bool
            Signals if the update request was executed successfully
        """

        documents = {}
        request = {
            'documentGraph': {
                'documents': documents,
                'documentRefs': [{
                    'type': measurement.getType(),
                    'id': measurement.getId()
                }]
            }
        }
        documents[measurement.getType()] = {}
        documents[measurement.getType()][measurement.getId()] = {
            'type': measurement.getType(),
            'id': measurement.getId(),
            'fields': data
        }

        for additionalDocument in additionalDocuments:
            docType = additionalDocument['type']
            docId = additionalDocument['id']
            if not docType in documents:
                documents[docType] = {}

            if not docId in documents[docType]:
                documents[docType][docId] = additionalDocument

        files = {'request': (None, json.dumps(request))}
        files.update(filesToUpload)

        requestHeaders = {
            'Accept': 'application/json',
            'Authorization': self.auth
        }
        response = requests.post(self.url + 'backend/api/v1/documents', files=files, headers=requestHeaders)

        if response.status_code >= 300:
            responseJson = response.json()
            # in case of an error throw an exception with the error
            if responseJson.get('errorId') is not None:
                raise Exception(responseJson.get('errorId')+': ' +
                                responseJson.get('localizedErrorMessage'))
            return False

        return True

    def upload(self, filename: str, df: pd.DataFrame, metadata: dict = {}, testType: str = 'Test') -> bool:
        """Uploads a file as a new measurement together with the given metadata

        Parameters
        ----------
        file : str
            Path to the file which should be uploaded
        metadata : dict
            Metadata for the measurement

        Returns
        -------
        bool
            Signals if the upload was successful
        """

        outputFilename = filename + '.csv'
        fileContent = df.to_csv()
        dataObjects = []

        # get columns and generate DO
        for col in list(df):
            _id = str(uuid.uuid4())
            dataObjects.append({
                'type': 'DataObject',
                'id': _id,
                'fields': {
                    'Type': 'DataObject',
                    'Id': _id,
                    'Name': col,
                    'Maximum': df[col].max().astype(float) if pd.api.types.is_numeric_dtype(df[col]) else None,
                    'Minimum': df[col].min().astype(float) if pd.api.types.is_numeric_dtype(df[col]) else None,
                    'Average': df[col].mean() if pd.api.types.is_numeric_dtype(df[col]) else None,
                    'StandardDeviation': df[col].std() if pd.api.types.is_numeric_dtype(df[col]) else None
                }
            })

        dataObjectRefs = []
        for do in dataObjects:
            dataObjectRefs.append({
                'type': 'DataObject',
                'id': do['id']
            })

        uploadId = str(uuid.uuid4())

        fileRef = {
            'contextId': 'madam-upload:'+uploadId,
            'relativePath': outputFilename,
            'originalFileName': outputFilename
        }

        testId = str(uuid.uuid4())

        data = {
            'Type': testType,
            'Id': testId,
            'DataObjects': dataObjectRefs,
            'Name': outputFilename,
            'MainFile': [fileRef],
            'MeasurementData': [fileRef],
            'SourcePath': 'meapy/'+outputFilename
        }

        data.update(metadata)

        filesToUpload = {}
        filesToUpload[uploadId] = (outputFilename, fileContent, 'text/csv')

        docs = dataObjects
        measurementDto = {
            'type': testType,
            'id': testId,
            'fields': data
        }
        status = self.update(Measurement(measurementDto), data, filesToUpload, docs)

        return status

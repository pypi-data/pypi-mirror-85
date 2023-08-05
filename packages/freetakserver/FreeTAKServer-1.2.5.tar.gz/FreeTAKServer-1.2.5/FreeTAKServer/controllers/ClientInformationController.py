#######################################################
# 
# ClientInformationController.py
# Python implementation of the Class ClientInformationController
# Generated by Enterprise Architect
# Created on:      19-May-2020 6:56:00 PM
#
#######################################################
from lxml import etree
from FreeTAKServer.controllers.BasicModelInstantiate import BasicModelInstantiate
import uuid
from FreeTAKServer.controllers.configuration.LoggingConstants import LoggingConstants
from FreeTAKServer.controllers.CreateLoggerController import CreateLoggerController
from FreeTAKServer.model.FTSModel.Event import Event
from FreeTAKServer.model.ClientInformation import ClientInformation
from FreeTAKServer.controllers.XMLCoTController import XMLCoTController

logger = CreateLoggerController("ClientInformationController").getLogger()

loggingConstants = LoggingConstants()

class ClientInformationController(BasicModelInstantiate):
    def __init__(self):
        pass
    '''
    connection setup is obsolete with intstantiateClientInformationModelFromController
    '''

    def intstantiateClientInformationModelFromConnection(self, rawClientInformation, queue):
        try:
            tempObject = Event.Connection()
            self.clientInformation = ClientInformation()
            argument = "initialConnection"
            self.clientInformation.dataQueue = queue
            self.clientInformation.socket = rawClientInformation.socket
            self.clientInformation.IP = rawClientInformation.ip
            self.clientInformation.idData = rawClientInformation.xmlString
            self.clientInformation.alive = 1
            self.clientInformation.ID = uuid.uuid1().int
            self.clientInformation.modelObject = XMLCoTController().serialize_CoT_to_model(tempObject, etree.fromstring(rawClientInformation.xmlString.encode()))
            return self.clientInformation
        except Exception as e:
            logger.error('error in client information controller '+str(e))
            return -1
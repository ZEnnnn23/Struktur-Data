import random

class TicketAgent:
    def __init__(self, agentId):
        self._agentId = agentId
        self._passenger = None
        self._stopTime = 0

    def isFree(self):
        return self._passenger is None

    def isFinished(self, curTime):
        return self._passenger is not None and self._stopTime == curTime

    def startService(self, passenger, stopTime):
        self._passenger = passenger
        self._stopTime = stopTime

    def stopService(self):
        thePassenger = self._passenger
        self._passenger = None
        return thePassenger

    def timeToStop(self):
        return self._stopTime


class Passenger:
    def __init__(self, arrivalTime):
        self._arrivalTime = arrivalTime

    def arrivalTime(self):
        return self._arrivalTime

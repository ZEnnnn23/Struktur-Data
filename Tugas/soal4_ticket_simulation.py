import random
from llistqueue import Queue
from myarray import Array
from people import TicketAgent, Passenger


class TicketCounterSimulation:
    def __init__(self, numAgents, numMinutes, betweenTime, serviceTime):
        # Parameters supplied by the user.
        self._arriveProb = 1.0 / betweenTime
        self._serviceTime = serviceTime
        self._numMinutes = numMinutes

        # Simulation components.
        self._passengerQ = Queue()
        self._theAgents = Array(numAgents)
        for i in range(numAgents):
            self._theAgents[i] = TicketAgent(i + 1)

        # Computed during the simulation.
        self._totalWaitTime = 0
        self._numPassengers = 0

    def run(self):
        for curTime in range(self._numMinutes + 1):
            self._handleArrival(curTime)
            self._handleBeginService(curTime)
            self._handleEndService(curTime)

    def printResults(self):
        numServed = self._numPassengers - len(self._passengerQ)
        avgWait = float(self._totalWaitTime) / numServed if numServed > 0 else 0.0
        print("")
        print("Number of passengers served =", numServed)
        print("Number of passengers remaining in line = %d" % len(self._passengerQ))
        print("The average wait time was %4.2f minutes." % avgWait)

    # ── Rule #1: Penumpang tiba secara acak setiap menit ──────────────────────
    def _handleArrival(self, curTime):
        if random.random() <= self._arriveProb:
            passenger = Passenger(curTime)
            self._passengerQ.enqueue(passenger)
            self._numPassengers += 1

    # ── Rule #2: Agent bebas melayani penumpang berikutnya di antrian ─────────
    def _handleBeginService(self, curTime):
        for i in range(len(self._theAgents)):
            agent = self._theAgents[i]
            if agent.isFree() and not self._passengerQ.isEmpty():
                passenger = self._passengerQ.dequeue()
                waitTime = curTime - passenger.arrivalTime()
                self._totalWaitTime += waitTime
                agent.startService(passenger, curTime + self._serviceTime)

    # ── Rule #3: Agent yang sudah selesai menjadi bebas kembali ──────────────
    def _handleEndService(self, curTime):
        for i in range(len(self._theAgents)):
            agent = self._theAgents[i]
            if agent.isFinished(curTime):
                agent.stopService()


# Contoh penggunaan
if __name__ == "__main__":
    sim = TicketCounterSimulation(numAgents=2, numMinutes=25,
                                  betweenTime=2, serviceTime=3)
    sim.run()
    sim.printResults()

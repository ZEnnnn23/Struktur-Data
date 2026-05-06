import random
from llistqueue import Queue
from myarray import Array
from people import TicketAgent, Passenger


class TicketCounterSimulationSeconds:
    """
    Modifikasi TicketCounterSimulation menggunakan satuan DETIK, bukan menit.
    Perubahan: parameter numMinutes → numSeconds, loop run() pakai numSeconds.
    """

    def __init__(self, numAgents, numSeconds, betweenTime, serviceTime):
        self._arriveProb = 1.0 / betweenTime
        self._serviceTime = serviceTime
        self._numSeconds = numSeconds          # <-- satuan detik

        self._passengerQ = Queue()
        self._theAgents = Array(numAgents)
        for i in range(numAgents):
            self._theAgents[i] = TicketAgent(i + 1)

        self._totalWaitTime = 0
        self._numPassengers = 0

    def run(self):
        for curTime in range(self._numSeconds + 1):   # <-- numSeconds
            self._handleArrival(curTime)
            self._handleBeginService(curTime)
            self._handleEndService(curTime)

    def getResults(self):
        numServed = self._numPassengers - len(self._passengerQ)
        avgWait = float(self._totalWaitTime) / numServed if numServed > 0 else 0.0
        return numServed, len(self._passengerQ), avgWait

    def printResults(self):
        numServed, remaining, avgWait = self.getResults()
        print("")
        print("Number of passengers served =", numServed)
        print("Number of passengers remaining in line = %d" % remaining)
        print("The average wait time was %4.2f seconds." % avgWait)

    def _handleArrival(self, curTime):
        if random.random() <= self._arriveProb:
            self._passengerQ.enqueue(Passenger(curTime))
            self._numPassengers += 1

    def _handleBeginService(self, curTime):
        for i in range(len(self._theAgents)):
            agent = self._theAgents[i]
            if agent.isFree() and not self._passengerQ.isEmpty():
                passenger = self._passengerQ.dequeue()
                self._totalWaitTime += curTime - passenger.arrivalTime()
                agent.startService(passenger, curTime + self._serviceTime)

    def _handleEndService(self, curTime):
        for i in range(len(self._theAgents)):
            agent = self._theAgents[i]
            if agent.isFinished(curTime):
                agent.stopService()


# ── Jalankan eksperimen dan cetak tabel ──────────────────────────────────────
if __name__ == "__main__":
    random.seed(42)

    configs = [
        # (numSeconds, numAgents, serviceTime, betweenTime)
        (100,  2, 3, 2), (500,  2, 3, 2), (1000, 2, 3, 2), (5000, 2, 3, 2), (10000, 2, 3, 2),
        (100,  2, 4, 2), (500,  2, 4, 2), (1000, 2, 4, 2), (5000, 2, 4, 2), (10000, 2, 4, 2),
        (100,  3, 4, 2), (500,  3, 4, 2), (1000, 3, 4, 2), (5000, 3, 4, 2), (10000, 3, 4, 2),
    ]

    header = f"{'Num Seconds':>12} {'Num Agents':>11} {'Avg Service':>12} {'Time Between':>13} {'Avg Wait':>10} {'Served':>8} {'Remaining':>10}"
    print(header)
    print("-" * len(header))

    for (secs, agents, service, between) in configs:
        sim = TicketCounterSimulationSeconds(agents, secs, between, service)
        sim.run()
        served, remaining, avgWait = sim.getResults()
        print(f"{secs:>12} {agents:>11} {service:>12} {between:>13} {avgWait:>10.2f} {served:>8} {remaining:>10}")

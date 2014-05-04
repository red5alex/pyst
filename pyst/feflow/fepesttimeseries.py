__author__ = 'are'


class FePestTimeSeries:
        obsPoint = ""
        obsNames = []
        obs = []

        def __init__(self, name):
            self.name = name

        def startValue(self):
            return self.obs[0].value

        def startTime(self):
            return self.obs[0].time

        def finalTime(self):
            return self.obs[-1].time

        def periodTime(self):
            return self.obs[-1].time - self.obs[0].time
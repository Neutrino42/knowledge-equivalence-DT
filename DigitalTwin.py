class DigitalTwin(object):
    def __init__(self, time, state):
        self.__time = time
        self.__state = state

    def update(self, time, data):
        self.__time = time
        self.__state = data

    def predict(self, t):
        vir_trace = []
        return vir_trace  # virtual predication



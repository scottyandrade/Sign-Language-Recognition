
#CircularQueue, does not support growing the queue

class CircularBuffer:
    def __init__(self, size) -> None:
        super().__init__()

        self.__elements = []

        self.size = size
        self.num_elements = 0
        self.__head = 0
        self.__tail = 0

    def append(self, item):

        if self.__tail >= self.size:
            self.__tail = 0
            self.__head+=1

        self.__elements.insert(self.__tail, item)

        self.__tail += 1

        self.num_elements = min(self.num_elements+1, self.size)

    def __iter__(self):
        for i in range(self.num_elements):
            yield self.__elements[(self.__head + i) % self.size]
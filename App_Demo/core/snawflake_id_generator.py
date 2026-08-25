#雪花算法是一种分布式ID生成算法，专门用于在分布式系统中生成全局唯一的ID。就像雪花一样，每个ID都是独一无二的。
import time

from Tools.scripts.stable_abi import generator



class SnowflakeIDGenerator:
    """
    雪花算法生成器
    """

    def __init__(self, worker_id, data_center_id,epoch=129648000000):
        self.worker_id = worker_id & 0x0F #保证worker_id不超过4位
        self.data_center_id = data_center_id & 0x07 #保证data_center_id不超过3位
        self.epoch = epoch
        self.sequence = 0
        self.last_timestamp = -1

    def _next_id(self):
        timestamp = int(time.time() * 1000)

        if timestamp < self.last_timestamp:
            raise Exception('Clock moved backwards.  Refusing to generate id for {} milliseconds'.format(self.last_timestamp - timestamp))
        if timestamp == self.last_timestamp:
            self.sequence = (self.sequence + 1) & 0x0FFF #保证sequence不超过12位
            if self.sequence == 0:
                timestamp = self._wait_for_next_millis(self.last_timestamp)
        else:
            self.sequence = 0

        self.last_timestamp = timestamp
        new_id = (
            ((timestamp - self.epoch) << 22)
            | (self.data_center_id << 17)
            | (self.worker_id << 12)
            | self.sequence
        )
        return new_id

    def _wait_for_next_millis(self, last_timestamp):
        timestamp = last_timestamp
        while timestamp <= last_timestamp:
            timestamp = int(time.time() * 1000)
        return timestamp

    def generate(self):
        return self._next_id()

    @staticmethod
    def generate_id():
        """
        生成id
        :return:
        """
        return generator.generate()

generator = SnowflakeIDGenerator(worker_id=1,data_center_id=1)
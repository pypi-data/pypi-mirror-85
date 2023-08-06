#!/usr/bin/python3

import time
from large_index.log import logging

class Function:
  def __init__(self,
    next_index: str = '',
    retry: int = 0,
  ):
    super().__init__()
    self.next_index = next_index
    self.retry = retry

  def debug_detail_index(self):
    self.index = 'test-000001'

  def find_next_index(self):
    alias = self.index[:-6]
    number = self.index[-6:]
    self.next_index = alias + str('{:06}'.format(int(number) + 1))
    return self.next_index

  def time_sleep(self):
    if self.retry > 0:
      logging.warning("Sleep time {0}".format( int(60 * self.retry) ))
      time.sleep(60 * self.retry)

if __name__ == "__main__":
  class_function = Function()
  class_function.debug_detail_index()

  class_function.find_next_index()
  class_function.time_sleep()

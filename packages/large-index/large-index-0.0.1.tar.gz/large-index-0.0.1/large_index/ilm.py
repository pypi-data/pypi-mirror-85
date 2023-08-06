#!/usr/bin/python3

import re
import requests
from large_index.log import logging
from large_index.config import Config
from large_index.request import Request
from large_index.function import Function

class Ilm(Config, Request):
  def __init__(self,
  ilm_info_for_index: str = {}
  ):
    super().__init__()
    self.ilm_info_for_index = ilm_info_for_index

  def debug_detail_index(self):
    self.alias = 'test'
    self.index = 'test-000001'

  def rollover_index(self):
    return requests.post("{0}/{1}/_rollover?master_timeout={2}".format( self.ELASTIC_URL, self.alias, self.MASTER_TIMEOUT ))

  def check_create_next_index(self):
    self.request = requests.get("{0}/{1}/_ilm/explain".format( self.ELASTIC_URL, self.next_index ))

  def check_rollover_index(self):
    if self.status_request():
      logging.info("Rollover index for alias [{0}], new index [{1}] is created".format( self.alias, self.next_index ))
      return True

  def ilm_retry_for_index(self):
    self.request = requests.post("{0}/{1}/_ilm/retry?master_timeout={2}".format( self.ELASTIC_URL, self.index, self.MASTER_TIMEOUT ))

  def check_ilm_retry_for_index(self):
    if self.status_request():
      logging.info("Retrying ILM for index [{0}] - True".format( self.index ))
      return True

  def current_ilm_info_for_index(self):
    self.request = requests.get("{0}/{1}/_ilm/explain".format( self.ELASTIC_URL, self.index )).json()

  def create_current_ilm_info_for_index(self):
    self.ilm_info_for_index['phase'] = self.request['indices'][self.index]['phase']
    self.ilm_info_for_index['action'] = self.request['indices'][self.index]['action']
    self.ilm_info_for_index['step'] = self.request['indices'][self.index]['step']

  def next_step_index_in_warm(self):
    self.data = { "current_step": { "phase": self.ilm_info_for_index['phase'], "action": self.ilm_info_for_index['action'], "name": self.ilm_info_for_index['step']}, "next_step": { "phase": "warm", "action": "set_priority", "name": "set_priority" } }

  def next_step_index_in_cold(self):
    self.data = { "current_step": { "phase": self.ilm_info_for_index['phase'], "action": self.ilm_info_for_index['action'], "name": self.ilm_info_for_index['step']}, "next_step": { "phase": "cold", "action": "set_priority", "name": "set_priority" } }

  def request_next_step_for_index(self):
    self.request = requests.post("{0}/_ilm/move/{1}".format( self.ELASTIC_URL, self.index ), json=self.data)

  def check_next_step_for_index(self):
    if self.status_request():
      logging.info("Next step ILM for index [{0}] - True".format( self.index ))
      return True

if __name__ == "__main__":
  class_function = Function()
  class_function.debug_detail_index()
  class_function.find_next_index()

  class_ilm = Ilm()
  class_ilm.debug_detail_index()

  class_ilm.rollover_index()
  class_ilm.next_index = class_function.find_next_index()
  class_ilm.check_create_next_index()
  class_ilm.check_rollover_index()

  class_ilm.ilm_retry_for_index()
  class_ilm.check_ilm_retry_for_index()

  class_ilm.current_ilm_info_for_index()
  class_ilm.create_current_ilm_info_for_index()

  if class_ilm.ilm_info_for_index['phase'] == "hot":
    class_ilm.next_step_index_in_warm()
    class_ilm.request_next_step_for_index()
    class_ilm.check_next_step_for_index()

  if class_ilm.ilm_info_for_index['phase'] == "warm":
    class_ilm.next_step_index_in_cold()
    class_ilm.request_next_step_for_index()
    class_ilm.check_next_step_for_index()

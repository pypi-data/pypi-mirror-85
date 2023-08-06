#!/usr/bin/python3

import re
import requests
from large_index.log import logging
from large_index.config import Config
from large_index.init import Init
from large_index.request import Request
from large_index.function import Function

class Index(Config, Request):
  def __init__(self,
    indices: str = [],
    index_details: str = [],
    shrink_indices: str = [],
    index_to_remove: str = [],
    index_current_num: str = {},
    invalid_size_indices: str = [],
    unmanaged_indices: str = [],
    not_hot_box_indices: str = [],
    not_hot_phase_indices: str = [],
    last_indices: str = [],
    not_last_indices: str = [],
    last_shrink_indices: str = [],
    new_index_name: str = '',
  ):
    super().__init__()
    self.indices = indices
    self.index_details = index_details
    self.shrink_indices = shrink_indices
    self.index_to_remove = index_to_remove
    self.index_current_num = index_current_num
    self.invalid_size_indices = invalid_size_indices
    self.unmanaged_indices = unmanaged_indices
    self.not_hot_box_indices = not_hot_box_indices
    self.not_hot_phase_indices = not_hot_phase_indices
    self.last_indices = last_indices
    self.not_last_indices = not_last_indices
    self.last_shrink_indices = last_shrink_indices
    self.new_index_name = new_index_name

  def debug_detail_index(self):
    self.alias = 'test'
    self.index = 'test-000001'

  def create_array_index_details_in_open(self):
    for details in Config.index_pools[0].json():
      if details['status'] == 'open':
        self.index_details.append(details)

  def create_array_index_to_remove(self):
    for details in self.index_details:
      if not self.index_pattern.match(details['index']):
        self.index_to_remove.append(details)
        logging.warning("[{0}] encountered a strange index name".format(details['index']))

  def remove_system_index_in_array(self):
    for details in self.index_to_remove:
      self.index_details.remove(details)

  def create_array_indices(self):
    for details in self.index_details:
      index_details = details.copy()
      index_details['number'] = int(self.index_pattern.match(details['index']).group(3))
      index_details['index_alias'] = self.index_pattern.match(details['index']).group(2)
      self.indices.append(index_details)

  def create_array_max_indices(self):
    for details in self.index_details:
      if self.index_current_num.get(self.index_pattern.match(details['index']).group(2), -1) < int(self.index_pattern.match(details['index']).group(3)):
        self.index_current_num[self.index_pattern.match(details['index']).group(2)] = int(self.index_pattern.match(details['index']).group(3))

  def create_array_invalid_size_index(self):
    for index in self.indices:
      if int(index['pri.store.size']) <= self.MAX_CURRENT_INDEX_SIZE_GB:
        self.invalid_size_indices.append(index)

  def create_array_unmanaged_index(self):
    for index in self.indices:
      if not Config.ilm_list['indices'][index['index']]['managed']:
        self.unmanaged_indices.append(index)
        logging.warning("[{0}] not management".format(index['index']))

  def create_array_not_hot_box_index(self):
    for index in self.indices:
      if Config.settings_list[index['index']]['settings']['index']['routing']['allocation']['require']['box_type'] != 'hot':
        self.not_hot_box_indices.append(index)

  def create_array_not_hot_phase_index(self):
    for index in self.indices:
      if Config.ilm_list['indices'][index['index']]['phase'] != 'hot':
        self.not_hot_phase_indices.append(index)

  def create_array_shrink_index(self):
    for index in self.indices:
      if self.index_pattern.match(index['index']).group(1):
        self.shrink_indices.append(index)

  def remove_invalid_data_in_index(self, data_array: str = []):
    for index in data_array:
      self.indices.remove(index)

  def create_last_index(self):
    for index in self.indices:
      if self.index_current_num[index['index_alias']] == index['number']:
        self.last_indices.append(index)

  def create_not_last_index(self):
    for index in self.indices:
      if self.index_current_num[index['index_alias']] != index['number']:
        self.not_last_indices.append(index)

  def create_last_shrink_index(self):
    for index in self.shrink_indices:
      if self.index_current_num[index['index_alias']] == index['number']:
        self.last_shrink_indices.append(index)

  def create_new_index(self):
    self.new_index_name = re.sub(r'(shrink-)', '', self.next_index)
    data = { "aliases": { self.alias: { "is_write_index" : False } } }
    self.request = requests.put("{0}/{1}?master_timeout={2}".format( self.ELASTIC_URL, self.new_index_name, self.MASTER_TIMEOUT), json=data)

  def check_create_new_index(self):
    if self.status_request():
      logging.info("Create new index [{0}] - True".format( self.new_index_name ))
      return True

if __name__ == "__main__":
  class_config = Config
  class_config.index_pools = Init(count = 4).list_pools()
  class_config.ilm_list = class_config.index_pools[3].json()
  class_config.settings_list = class_config.index_pools[2].json()

  class_function = Function()
  class_function.debug_detail_index()
  class_function.find_next_index()

  class_index = Index()
  class_index.create_array_index_details_in_open()
  class_index.create_array_index_to_remove()
  class_index.remove_system_index_in_array()
  class_index.create_array_indices()
  class_index.create_array_max_indices()

  class_index.create_array_invalid_size_index()
  class_index.remove_invalid_data_in_index( class_index.invalid_size_indices )

  class_index.create_array_unmanaged_index()
  class_index.remove_invalid_data_in_index( class_index.unmanaged_indices )

  class_index.create_array_not_hot_box_index()
  class_index.remove_invalid_data_in_index( class_index.not_hot_box_indices )

  class_index.create_array_not_hot_phase_index()
  class_index.remove_invalid_data_in_index( class_index.not_hot_phase_indices )

  class_index.create_array_shrink_index()
  class_index.remove_invalid_data_in_index( class_index.shrink_indices )

  class_index.create_last_index()
  class_index.create_not_last_index()
  class_index.create_last_shrink_index()

  class_index.debug_detail_index()
  class_index.next_index = class_function.find_next_index()
  class_index.create_new_index()

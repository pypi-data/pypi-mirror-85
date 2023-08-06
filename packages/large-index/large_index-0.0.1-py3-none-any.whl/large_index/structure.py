#!/usr/bin/python3

import re
import time
import requests
from large_index.log import logging
from large_index.config import Config
from large_index.init import Init
from large_index.index import Index
from large_index.request import Request
from large_index.ilm import Ilm
from large_index.alias import Alias
from large_index.cluster import Cluster
from large_index.function import Function

class Structure(Index, Ilm, Alias, Function, Cluster, Request):
  def cluster_status(self):
    while True:
      self.get_status_cluster()

      if not self.check_count_relocating_shards_in_cluster():
        logging.warning("Number of relocating shards reaches {0}".format( self.cluster['relocating_shards'] ))
        self.retry += 1
        self.time_sleep()
        continue

      if not self.check_count_pending_tasks_in_cluster():
        logging.warning("Number of pending tasks reaches {0}".format( self.cluster['number_of_pending_tasks'] ))
        self.retry += 1
        self.time_sleep()
        continue

      if self.check_count_relocating_shards_in_cluster() and self.check_count_pending_tasks_in_cluster():
        self.retry = 0
        break

  def rollover_index_and_check(self):
    self.cluster_status()
    self.rollover_index()
    self.find_next_index()
    self.check_create_next_index()
    return self.check_rollover_index()

  def add_write_disable_for_index_and_check(self):
    self.add_alias_for_index_and_write_disable()
    self.cluster_status()
    self.request_add_alias_for_index()
    return self.check_disable_write_for_index()

  def add_write_enable_for_index_and_check(self):
    self.add_alias_for_index_and_write_enable()
    self.cluster_status()
    self.request_add_alias_for_index()
    return self.check_enable_write_for_index()

  def ilm_retry_for_next_index_and_check(self):
    self.cluster_status()
    self.ilm_retry_for_index()
    return self.check_ilm_retry_for_index()

  def next_step_for_index_and_check(self):
    self.current_ilm_info_for_index()
    self.create_current_ilm_info_for_index()
    self.next_step_for_not_shrink_index()
    self.next_step_for_shrink_index()
    self.cluster_status()
    self.request_next_step_for_index()
    return self.check_next_step_for_index()

  def next_step_for_not_shrink_index(self):
    if not self.index_pattern.match(self.index).group(1):
      self.next_step_index_in_warm()

  def next_step_for_shrink_index(self):
    if self.index_pattern.match(self.index).group(1):
      self.next_step_index_in_cold()

  def create_new_index_and_check(self):
    self.find_next_index()
    self.cluster_status()
    self.create_new_index()
    return self.check_create_new_index()

  def rollover_last_index(self):
    for index in self.last_indices:
      self.index = index['index']
      self.alias = index['index_alias']
      logging.warning("Index [{0}][{1}gb] is larger the allowed size - {2}gb".format( self.index, int(index['pri.store.size']), self.MAX_CURRENT_INDEX_SIZE_GB ))

      if not self.rollover_index_and_check():
        logging.error("Not rollover index for alias [{0}]".format( self.alias ))
        logging.warning("Skip this index and continue with the following index")
        continue

      if not self.next_step_for_index_and_check():
        logging.error("Failed next step to index [{0}]".format( self.index ))

  def rollover_not_last_index(self):
    for index in self.not_last_indices:
      self.index = index['index']
      self.alias = index['index_alias']
      logging.warning("Index [{0}][{1}gb] is larger the allowed size - {2}gb".format( self.index, int(index['pri.store.size']), self.MAX_CURRENT_INDEX_SIZE_GB ))

      self.index = self.find_next_index()
      if not self.add_write_disable_for_index_and_check():
        logging.error("Failed add alias [{0}] to next index [{1}] and disable write".format( self.alias, self.index ))
        logging.warning("Skip this index and continue with the following index")
        continue

      self.index = index['index']
      if not self.add_write_disable_for_index_and_check():
        logging.error("Failed disable write to index [{0}]".format( self.index ))
        logging.warning("Skip this index and continue with the following index")
        continue

      self.index = self.find_next_index()
      if not self.add_write_enable_for_index_and_check():
        logging.error("Failed enable write to next index [{0}]".format( self.index ))
        logging.warning("Skip this index and continue with the following index")
        continue

      if not self.ilm_retry_for_next_index_and_check():
        logging.error("Failed ilm retry to next index [{0}]".format( self.index ))

      self.index = index['index']
      if not self.next_step_for_index_and_check():
        logging.error("Failed next step to index [{0}]".format( self.index ))

  def rollover_last_shrink_index(self):
    for index in self.last_shrink_indices:
      self.index = index['index']
      self.alias = index['index_alias']
      logging.warning("Index [{0}][{1}gb] is larger the allowed size - {2}gb".format( self.index, int(index['pri.store.size']), self.MAX_CURRENT_INDEX_SIZE_GB ))

      if not self.create_new_index_and_check():
        logging.error("Failed create new index [{0}]".format( self.new_index_name ))
        logging.warning("Skip this index and continue with the following index")
        continue

      if not self.add_write_disable_for_index_and_check():
        logging.error("Failed disable write to index [{0}]".format( self.index ))
        logging.warning("Skip this index and continue with the following index")
        continue

      self.index = self.new_index_name
      if not self.add_write_enable_for_index_and_check():
        logging.error("Failed enable write to next index [{0}]".format( self.index ))
        logging.warning("Skip this index and continue with the following index")
        continue

      if not self.ilm_retry_for_next_index_and_check():
        logging.error("Failed ilm retry to next index [{0}]".format( self.index ))

      self.index = index['index']
      if not self.next_step_for_index_and_check():
        logging.error("Failed next step to index [{0}]".format( self.index ))

  def rollover_last_index_in_check_mode(self):
    for index in self.last_indices:
      logging.warning("[check_mode] Las index [{0}][{1}gb] is larger the allowed size - {2}gb".format( index['index'], int(index['pri.store.size']), self.MAX_CURRENT_INDEX_SIZE_GB ))

  def rollover_not_last_index_in_check_mode(self):
    for index in self.not_last_indices:
      logging.warning("[check_mode] Not last index [{0}][{1}gb] is larger the allowed size - {2}gb".format( index['index'], int(index['pri.store.size']), self.MAX_CURRENT_INDEX_SIZE_GB ))

  def rollover_last_shrink_index_in_check_mode(self):
    for index in self.last_shrink_indices:
      logging.warning("[check_mode] Last shrink index [{0}][{1}gb] is larger the allowed size - {2}gb".format( index['index'], int(index['pri.store.size']), self.MAX_CURRENT_INDEX_SIZE_GB ))

if __name__ == "__main__":
  class_config = Config
  class_config.index_pools = Init(count = 4).list_pools()
  class_config.ilm_list = class_config.index_pools[3].json()
  class_config.settings_list = class_config.index_pools[2].json()
  class_config.alias_list = class_config.index_pools[1].json()

  class_structure = Structure()
  class_structure.create_array_index_details_in_open()
  class_structure.create_array_index_to_remove()
  class_structure.remove_system_index_in_array()
  class_structure.create_array_indices()
  class_structure.create_array_max_indices()

  del(class_structure.index_details)
  del(class_structure.index_to_remove)

  class_structure.create_array_invalid_size_index()
  class_structure.remove_invalid_data_in_index( class_structure.invalid_size_indices )

  class_structure.create_array_unmanaged_index()
  class_structure.remove_invalid_data_in_index( class_structure.unmanaged_indices )

  class_structure.create_array_not_hot_box_index()
  class_structure.remove_invalid_data_in_index( class_structure.not_hot_box_indices )

  class_structure.create_array_not_hot_phase_index()
  class_structure.remove_invalid_data_in_index( class_structure.not_hot_phase_indices )

  class_structure.create_array_shrink_index()
  class_structure.remove_invalid_data_in_index( class_structure.shrink_indices )

  class_structure.create_last_index()
  class_structure.create_not_last_index()
  class_structure.create_last_shrink_index()

  del(class_structure.invalid_size_indices)
  del(class_structure.unmanaged_indices)
  del(class_structure.not_hot_box_indices)
  del(class_structure.not_hot_phase_indices)

  class_structure.rollover_last_index()
  class_structure.rollover_not_last_index()
  class_structure.rollover_last_shrink_index()

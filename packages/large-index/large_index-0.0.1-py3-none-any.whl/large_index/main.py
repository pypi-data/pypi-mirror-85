#!/usr/bin/python3

import click

from large_index.log import logging
from large_index.config import Config
from large_index.init import Init
from large_index.structure import Structure

class_config = Config
class_structure = Structure()

def generating_variables():
  class_config.index_pools = Init(count = 4).list_pools()
  class_config.ilm_list = class_config.index_pools[3].json()
  class_config.settings_list = class_config.index_pools[2].json()
  class_config.alias_list = class_config.index_pools[1].json()

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

def start_rollover_all(check_mode):
  if not check_mode:
    logging.info("start_rollover_all")
    print(class_structure.last_indices)
    # class_structure.rollover_last_index()
    # class_structure.rollover_not_last_index()
    # class_structure.rollover_last_shrink_index()

def start_check_mode_rollover_all(check_mode):
  if check_mode:
    class_structure.rollover_last_index_in_check_mode()
    class_structure.rollover_not_last_index_in_check_mode()
    class_structure.rollover_last_shrink_index_in_check_mode()

def start_rollover_last_index(check_mode):
  if not check_mode:
    logging.info("start_rollover_last_index")
    print(class_structure.last_indices)
    # class_structure.rollover_last_index()

def start_check_mode_rollover_last_index(check_mode):
  if check_mode:
    class_structure.rollover_last_index_in_check_mode()

def start_rollover_not_last_index(check_mode):
  if not check_mode:
    logging.info("start_rollover_not_last_index")
    print(class_structure.not_last_indices)
    # class_structure.rollover_not_last_index()

def start_check_mode_rollover_not_last_index(check_mode):
  if check_mode:
    class_structure.rollover_not_last_index_in_check_mode()

def start_rollover_last_shrink_indices(check_mode):
  if not check_mode:
    logging.info("start_rollover_last_shrink_indices")
    print(class_structure.last_shrink_indices)
    # class_structure.rollover_last_shrink_index()

def start_check_mode_rollover_last_shrink_indices(check_mode):
  if check_mode:
    class_structure.rollover_last_shrink_index_in_check_mode()

@click.group()
@click.version_option()
def cli():
  """
  Rollover big indexes ilm in Elasticsearch.
  """
  pass

@cli.command(help='Rollover large indexes.')
@click.option(
  '-c', '--check-mode',
  is_flag=True,
  expose_value=True,
  help='Only displaying actions, without performing them.'
)
def start(check_mode):
  """
  Rollover large indexes.
  """
  logging.info("Started rollover large indexes")

  generating_variables()
  start_rollover_all(check_mode)
  start_check_mode_rollover_all(check_mode)

@cli.command(help='Rollover only the latest big indexes (not shrink).')
@click.option(
  '-c', '--check_mode',
  is_flag=True,
  expose_value=True,
  help='Only displaying actions, without performing them.'
)
def last_index(check_mode):
  """
  Rollover only the latest big indexes (not shrink index).
  """
  logging.info("Started rollover only the latest big indexes (not shrink index).")

  generating_variables()
  start_rollover_last_index(check_mode)
  start_check_mode_rollover_last_index(check_mode)

@cli.command(help='Rollover only the not latest big indexes (not shrink).')
@click.option(
  '-c', '--check_mode',
  is_flag=True,
  expose_value=True,
  help='Only displaying actions, without performing them.'
)
def not_last_index(check_mode):
  """
  Rollover only the not latest big indexes (not shrink index).
  """
  logging.info("Started rollover only the not latest big indexes (not shrink index)")

  generating_variables()
  start_rollover_not_last_index(check_mode)
  start_check_mode_rollover_not_last_index(check_mode)

@cli.command(help='Rollover only the latest big shrink indexes.')
@click.option(
  '-c', '--check_mode',
  is_flag=True,
  expose_value=True,
  help='Only displaying actions, without performing them.'
)
def last_shrink_index(check_mode):
  """
  Rollover only the latest big shrink indexes.
  """
  logging.info("Started rollover only the latest big shrink indexes")

  generating_variables()
  start_rollover_last_shrink_indices(check_mode)
  start_check_mode_rollover_last_shrink_indices(check_mode)

if __name__ == "__main__":
  cli()

import psutil
from typing import List, Dict

import psutil

from src.disks.disk_partition_info import DiskPartitionInfo
from src.abstracts.info_manager import InfoManager

class DiskPartitionsInfoManager(InfoManager):

  def __init__(self) -> None:

    self.__disk_partitions_info: List[DiskPartitionInfo] = list()

    disk_partitions: List[psutil._common.sdiskpart] = psutil.disk_partitions(all=False)

    io_metrics_per_disk: Dict[str, psutil._common.sdiskio] = psutil.disk_io_counters(perdisk=True)

    for i in range(0, len(disk_partitions)):

      if i < len(list(io_metrics_per_disk.keys())):

        disk: str = list(io_metrics_per_disk.keys())[i]
      
      else:

        disk: str = ""

      disk_partition_info = DiskPartitionInfo(device_path=disk_partitions[i].device,
                                              mountpoint_path=disk_partitions[i].mountpoint,
                                              file_system=disk_partitions[i].fstype,
                                              io_counters=io_metrics_per_disk[disk] if disk else None)

      self.__disk_partitions_info.append(disk_partition_info)
  
  @property
  def disk_partitions_count(self) -> int:

    return len(self.__disk_partitions_info)
  
  @property
  def disk_partitions_info(self) -> List[DiskPartitionInfo]:

    return self.__disk_partitions_info
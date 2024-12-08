import psutil
import psutil._common


from src.abstracts.unit_info import UnitInfo


class DiskPartitionInfo(UnitInfo):

  def __init__(self, device_path: str,
               mountpoint_path: str,
               file_system: str,
               io_counters: psutil._common.sdiskio | None) -> None:
    
    self.__device_path = device_path
    self.__mountpoint_path = mountpoint_path
    self.__file_system = file_system

    usage_stats: psutil._common.sdiskusage = psutil.disk_usage(self.__mountpoint_path)

    self.__total_bytes = usage_stats.total
    self.__used_bytes = usage_stats.used

    self.__write_operations_count = 0
    self.__read_operations_count = 0
    self.__write_bytes = 0
    self.__read_bytes = 0

    # Se a partição tiver as métricas de I/O
    if io_counters:
    
      self.__write_operations_count = io_counters.write_count
      self.__read_operations_count = io_counters.read_count
      self.__write_bytes = io_counters.write_bytes
      self.__read_bytes = io_counters.read_bytes
  
  @property
  def device_path(self) -> str:

    return self.__device_path
  
  @property
  def mountpoint_path(self) -> str:

    return self.__mountpoint_path
  
  @property
  def file_system(self) -> str:

    return self.__file_system
  
  @property
  def total_bytes(self) -> int:

    return self.__total_bytes
  
  @property
  def used_bytes(self) -> int:

    return self.__used_bytes
  
  @property
  def free_bytes(self) -> int:

    return self.__total_bytes - self.__used_bytes
  
  @property
  def used_percentage(self) -> float:

    return round((self.__used_bytes / self.__total_bytes) * 100, 2)
  
  @property
  def write_operations_count(self) -> int:

    return self.__write_operations_count
  
  @property
  def read_operations_count(self) -> int:

    return self.__read_operations_count
  
  @property
  def write_bytes(self) -> int:

    return self.__write_bytes
  
  @property
  def read_bytes(self) -> int:

    return self.__read_bytes
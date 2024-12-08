import psutil


from src.abstracts.unit_info import UnitInfo


class CPUInfo(UnitInfo):

  """
  
  Representa as informações de uma única CPU
  
  """

  def __init__(self, cpu_id: int, 
               used_percentage: float, 
               frequencies: psutil._common.scpufreq) -> None:

    self.__cpu_id = cpu_id
    self.__used_percentage = used_percentage
    self.__current_frequency = frequencies.current
    self.__minimum_frequency = frequencies.min
    self.__maximum_frequency = frequencies.max
  
  @property
  def cpu_id(self) -> int:

    return self.__cpu_id
  
  @property
  def used_percentage(self) -> float:

    return self.__used_percentage
  
  @property
  def current_frequency(self) -> float:

    return self.__current_frequency
  
  @property
  def minimum_frequency(self) -> float:

    return self.__minimum_frequency
  
  @property
  def maximum_frequency(self) -> float:

    return self.__maximum_frequency

    
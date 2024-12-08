import psutil
from typing import List

from src.cpus.cpu_info import CPUInfo
from src.abstracts.info_manager import InfoManager

class CPUsInfoManager(InfoManager):

  """

  Representa um gerenciador de informações do CPU

  """

  def __init__(self) -> None:

    self.__cpus_info: List[CPUInfo] = list()

    self.__cpu_count = psutil.cpu_count(logical=True)
    self.__physical_cores_count = psutil.cpu_count(logical=False)

    self.__context_switches_count = psutil.cpu_stats().ctx_switches
    self.__hardware_interrupts_count = psutil.cpu_stats().interrupts

    for i in range(0, self.__cpu_count):

      used_percentage = psutil.cpu_percent(percpu=True)[i]

      """

      Verifica se cada CPU possui informações distintas, ou todos eles possuem a mesma informação (Um único elemento scpufreq com a informação de todos).

      """
      if len(psutil.cpu_freq(percpu=True)) == 1:

        frequencies = psutil.cpu_freq(percpu=True)[0]
      
      else:

        frequencies = psutil.cpu_freq(percpu=True)[i]

      self.__cpus_info.append(CPUInfo(i, used_percentage, frequencies))
  
  @property
  def cpus_info(self) -> List[CPUInfo]:

    return self.__cpus_info
  
  @property
  def cpu_count(self) -> int:

    return self.__cpu_count
  
  @property
  def physical_cores_count(self) -> int:

    return self.__physical_cores_count

  @property
  def context_switches_count(self) -> int:

    return self.__context_switches_count
  
  @property
  def hardware_interrupts_count(self) -> int:

    return self.__hardware_interrupts_count


import psutil


from typing import List, Any


from src.processes.process_info import ProcessInfo
from src.abstracts.info_manager import InfoManager


class ProcessesInfoManager(InfoManager):

  """
  Representa um gerenciador das informações dos processos do sistema
  """

  def __init__(self) -> None:

    self.__processes_info: List[ProcessInfo] = list()

    for pid in psutil.pids():

      try:

        self.__processes_info.append(ProcessInfo(pid))

      except psutil.AccessDenied:

        pass

      except psutil.ZombieProcess:

        pass
    
    # Cópia de todos os processos
    self.__all_processes_info = self.__processes_info.copy()
  
  @property
  def processes_count(self) -> int:

    return len(self.__all_processes_info)
  
  @property
  def running_processes_count(self) -> int:

    return len(list(filter(lambda x: x.status == "running", self.__all_processes_info)))
  
  @property
  def waiting_processes_count(self) -> int:

    return len(list(filter(lambda x: x.status in ["waiting", "stopped", "disk_sleep", "sleeping"], 
                           self.__all_processes_info)))
  
  @property
  def processes_info(self) -> List[ProcessInfo]:

    return self.__processes_info
  
  def filterBy(self, by: str, value: Any) -> None:

    """
    Filtra o iterável com as unidades de processo por meio de um valor recebido como entrada (value), correspondente a uma característica específica (by).
    """

    self.__processes_info = self.__all_processes_info.copy()

    match by:

      case "PID":

        attribute = "pid"
      
      case "Nome":

        attribute = "name"
      
      case "Estado":

        attribute = "status"
      
      case _:

        attribute = None

    if attribute:

      # Verifica se o campo não está vazio (Caso sim, não realiza filtro nenhum)
      if value:

        value = int(value) if (attribute == "pid") and (value.isnumeric()) else value

        self.__processes_info = list(filter(
          lambda x: getattr(x, attribute) == value, 
          self.__processes_info))
      
      else:

        self.__processes_info = self.__all_processes_info.copy()
    
    else:

      print("Esse filtro não existe!")


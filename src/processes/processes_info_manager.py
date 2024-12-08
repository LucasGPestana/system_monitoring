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
  
  @property
  def processes_count(self) -> int:

    return len(self.__processes_info)
  
  @property
  def running_processes_count(self) -> int:

    return len(list(filter(lambda x: x.status == "running", self.__processes_info)))
  
  @property
  def waiting_processes_count(self) -> int:

    return len(list(filter(lambda x: x.status in ["waiting", "stopped", "disk_sleep", "sleeping"], 
                           self.__processes_info)))
  
  @property
  def processes_info(self) -> List[ProcessInfo]:

    return self.__processes_info
  
  def filterBy(self, by: str, value: Any) -> None:

    """
    Filtra o iterável com as unidades de processo por meio de um valor recebido como entrada (value), correspondente a uma característica específica (by).
    """

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

        self.__processes_info = list(filter(lambda x: getattr(x, attribute) == value, self.__processes_info))
    
    else:

      print("Esse filtro não existe!")


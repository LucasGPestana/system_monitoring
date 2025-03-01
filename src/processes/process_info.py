import psutil
import psutil._common


from src.abstracts.unit_info import UnitInfo


class ProcessInfo(UnitInfo):

  """

  Representa a informação de um único processo
  
  """

  def __init__(self, pid: int) -> None:

    process = psutil.Process(pid)

    self.__name = process.name()
    self.__pid = process.pid
    self.__ppid = process.ppid()
    self.__priority_number = process.nice()
    self.__owner_username = process.username()

    # Mapeamento de traduções dos estados para pt-br
    status_translation = {
      "sleeping": "esperando",
      "running": "executando",
      "zombie": "zumbi"
    }

    self.__status = status_translation[process.status()]
    self.__executable_path = process.exe()
    self.__created_time = process.create_time()
    self.__threads_used_count = process.num_threads()

    # Informações da relação CPU e o processo do contexto
    self.__cpu_used_percentage = process.cpu_percent()

    # Informações da relação I/O e o processo do contexto
    io_metrics: psutil._common.pio = process.io_counters()

    self.__write_operations_count = io_metrics.write_count
    self.__read_operations_count = io_metrics.read_count
    self.__write_bytes_number = io_metrics.write_bytes
    self.__read_bytes_number = io_metrics.read_bytes

    # Informações da relação Memória principal e o processo do contexto
    self.__memory_used_percent = process.memory_percent()


  @property
  def name(self) -> str:

    return self.__name

  @property
  def pid(self) -> int:

    return self.__pid

  @property
  def ppid(self) -> int:

    return self.__ppid

  @property
  def priority_number(self) -> int:

    return self.__priority_number

  @property
  def owner_username(self) -> str:

    return self.__owner_username

  @property
  def status(self) -> str:

    return self.__status

  @property
  def executable_path(self) -> str:

    return self.__executable_path

  @property
  def created_time(self) -> float:

    return self.__created_time

  @property
  def cpu_used_percentage(self) -> float:

    return self.__cpu_used_percentage

  @property
  def write_operations_count(self) -> int:

    return self.__write_operations_count

  @property
  def read_operations_count(self) -> int:

    return self.__read_operations_count

  @property
  def write_bytes_number(self) -> int:

    return self.__write_bytes_number

  @property
  def read_bytes_number(self) -> int:

    return self.__read_bytes_number

  @property
  def memory_used_percent(self) -> float:

    return self.__memory_used_percent
  
  @property
  def threads_used_count(self) -> int:

    return self.__threads_used_count
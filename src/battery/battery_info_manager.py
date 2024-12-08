import psutil

from src.abstracts.info_manager import InfoManager

class BatteryInfoManager(InfoManager):

  """
  Classe que representa um gerenciador de informações sobre a bateria
  """

  def __init__(self) -> None:

    sbattery: psutil._common.sbattery = psutil.sensors_battery()

    self.__percentage_remaining = sbattery.percent
    self.__time_left = sbattery.secsleft
    self.__is_charging = sbattery.power_plugged
  
  @property
  def percentage_remaining(self) -> int:

    """
    A porcentagem de bateria restante
    """

    return self.__percentage_remaining
  
  @property
  def time_left(self) -> int:

    """
    O tempo estimado para que a bateria acabe, em segundos
    """

    # Se estiver carregando, não é possível estimar esse tempo
    if self.__is_charging:

      return 0
    
    return self.__time_left
  
  @property
  def is_charging(self) -> bool:

    """
    Retorna verdadeiro se o computador está carregando, caso contrário retorna falso
    """

    return self.__is_charging
from PySide6.QtWidgets import (
    QWidget, QPushButton, QVBoxLayout, QHBoxLayout, QLayout, 
    QLabel, QTableWidget, QTableWidgetItem, QMessageBox,
    QLineEdit, QComboBox
)
from PySide6.QtCore import Qt, QTimer
from PySide6.QtGui import QIcon

import pandas as pd


import os
from typing import Any, Dict


from screens.details_window import DetailsWindow

from src.cpus.cpus_info_manager import CPUsInfoManager
from src.processes.processes_info_manager import ProcessesInfoManager
from src.disks.disk_partitions_info_manager import DiskPartitionsInfoManager
from src.battery.battery_info_manager import BatteryInfoManager
from src.abstracts.info_manager import InfoManager

from utils.format_time import convertToTimeFormat
from utils.format_datetime import convertToDatetimeFormat
from utils.icons import getSystemIconPath

class MainWindow(QWidget):

  """Janela principal do aplicativo, com as informações gerais do sistema"""
  
  def __init__(self) -> None:

    super().__init__()

    self.setWindowTitle("Monitoramento do Sistema")
    self.setWindowIcon(QIcon(getSystemIconPath()))
    self.resize(700, 500)

    self.selected_filter = "" # Atributo para filtro do módulo de processos
    self.current_filter_text = "" # Texto do filtro do módulo de processos
    self.current_row_index = 0 # Atributo para pegar o indice da linha selecionada na tabela

    self.table_horiz_scroll_pos = 0
    self.table_vert_scroll_pos = 0

    # Layout da tela
    self.main_layout = QVBoxLayout()

    self.setOptionsLayout()
    self.setInfoLayout()

    # Adicionando um timer de atualização dos conteúdos
    self.timer = QTimer(self)

    # Iterável com objetos Connection correspondentes as conexões com o timer
    self.timer_connections = list()

    self.timer.start(10000) # Período de atualização de 5000ms (5s)

    self.setLayout(self.main_layout)

  def setOptionsLayout(self) -> None:

    """Adiciona o layout dos botões de opção (CPU, Processos, Partições e Baterias) na janela
    """

    # layout das opções
    self.options_layout = QHBoxLayout()

    # Itens das opções
    btn_cpu = QPushButton("CPU")
    btn_process = QPushButton("Processos")
    btn_disk = QPushButton("Partições de Disco")
    btn_battery = QPushButton("Bateria")

    # Adicionando os itens ao layout do frame de opções
    self.options_layout.addWidget(btn_cpu)
    self.options_layout.addWidget(btn_process)
    self.options_layout.addWidget(btn_disk)
    self.options_layout.addWidget(btn_battery)

    # Adicionando os escutadores de evento de cada botão
    btn_cpu.clicked.connect(self.loadCPUInfo)
    btn_process.clicked.connect(self.loadProcessInfo)
    btn_disk.clicked.connect(self.loadDiskInfo)
    btn_battery.clicked.connect(self.loadBatteryInfo)

    self.main_layout.addLayout(self.options_layout)
  
  def setGeneralInfoLayout(self, info_obj: InfoManager) -> None:

    """Adiciona as informações gerais de um módulo (CPU, Processos, Partições ou Bateria), a partir do gerenciador desse módulo

    Parameters
    ----------
    info_obj : InfoManager
      A instância do gerenciador que deseja adicionar as informações gerais
    """

    if isinstance(info_obj, CPUsInfoManager):

        general_infos = {
          "Número de CPUs": "cpu_count", 
          "Número de Núcleos": "physical_cores_count", 
          "Mudanças de Contexto": "context_switches_count", 
          "Interrupções de Hardware": "hardware_interrupts_count"
        }
      
    elif isinstance(info_obj, ProcessesInfoManager):

        general_infos = {
          "Número de Processos": "processes_count", 
          "Processos em Execução": "running_processes_count", 
          "Processos em Espera": "waiting_processes_count"
        }
    
    elif isinstance(info_obj, DiskPartitionsInfoManager):

        general_infos = {"Número de Partições": "disk_partitions_count"}
    
    elif isinstance(info_obj, BatteryInfoManager):

        general_infos = {
           
          "Porcentagem de Bateria Restante": "percentage_remaining", 
          "Tempo de Bateria Restante": "time_left", 
          "Carregador Conectado": "is_charging"

        }
    
    else:
       
       return

    # Informações gerais

    for label, attribute in general_infos.items():
      
      data = getattr(info_obj, attribute)
      
      # Layout de cada rótulo e informação geral
      unique_info_layout = QHBoxLayout()

      unique_info_layout.addWidget(QLabel(f"{label}: "))

      match attribute:

         case "percentage_remaining":

            data_label = QLabel(f"{data:.2f}".replace(".", ","))
         
         case "time_left":
            
            data_label = QLabel(convertToTimeFormat(data))
         
         case "is_charging":
            
            data_label = QLabel("Sim" if data else "Não")

         case _:
            
            data_label = QLabel(str(data))
            
      unique_info_layout.addWidget(data_label)

      self.general_info_layout.addLayout(unique_info_layout)

  def setSpecificInfoLayout(self, info_obj: InfoManager) -> None:

    """Adiciona algumas informações específicas das unidades de um módulo (CPU, Processos ou Partições), a partir do gerenciador desse módulo

    Parameters
    ----------
    info_obj : InfoManager
      A instância do gerenciador que deseja adicionar as informações específicas das unidades
    """
     
    # specific_infos corresponde aos atributos de cada unidade que aparecerão na tabela
     
    if isinstance(info_obj, CPUsInfoManager):

        specific_infos = {
          "ID do CPU": "cpu_id", 
          "Porcentagem de Uso": "used_percentage",
        }
        units_attribute = "cpus_info"
      
    elif isinstance(info_obj, ProcessesInfoManager):

        specific_infos = {
          "Nome": "name", 
          "PID": "pid", 
          "Estado": "status",
          "Caminho de Execução": "executable_path",
          "Data e Hora de Criação": "created_time"
          }
        units_attribute = "processes_info"
    
    elif isinstance(info_obj, DiskPartitionsInfoManager):

        specific_infos = {
           "Caminho de Montagem": "mountpoint_path",
           "Caminho do Dispositivo": "device_path",
           "Sistema de Arquivos": "file_system",
           "Porcentagem de Uso": "used_percentage"
           }
        units_attribute = "disk_partitions_info"
    
    else:
       
       specific_infos = {}
       units_attribute = ""

    self.specific_info_table = QTableWidget()
    
    self.styleSpecificInfoTable()

    self.insertUnitsInfoOnTable(info_obj, units_attribute, specific_infos)
    
    btn_details = QPushButton("Detalhes")
    
    if self.specific_info_layout.isEmpty():

      self.specific_info_layout.addWidget(self.specific_info_table)
      self.specific_info_layout.addWidget(btn_details)

    btn_details.clicked.connect(lambda: self.openDetailsWindow(self.specific_info_table.currentRow(), 
                                                               info_obj))

    # Obtém o valor máximo de cada scroll bar                                                           
    max_vert_scroll : int = self.specific_info_table.verticalScrollBar().maximum() or 1
    max_horiz_scroll : int = self.specific_info_table.horizontalScrollBar().maximum() or 1
    
    # Define as posições dos scroll bars da última atualização na tela atual
    self.specific_info_table.verticalScrollBar().setValue(self.table_vert_scroll_pos * max_vert_scroll)
    self.specific_info_table.horizontalScrollBar().setValue(self.table_horiz_scroll_pos * max_horiz_scroll)
  
  def insertUnitsInfoOnTable(self, info_obj: InfoManager, units_iterable_attr: str, attrs_to_show: Dict[str, str]) -> None:

    """Insere os dados das unidades de um módulo na tabela de informações específicas

    Parameters
    ----------
    info_obj : InfoManager
      Gerenciador das informações do módulo cujas unidades serão exibidas (Exceto BatteryInfo)
    units_iterable_attr : str
      Nome do atributo correspondente ao iterável com as unidades de um módulo
    attrs_to_show : Dict[str, str]
      Nomes dos atributos dos dados que serão exibidos de cada unidade. As chaves correspondem aos nomes dos rótulos da tabela.
    """

    # Adicionando os dados exibidos em uma lista contendo listas (estrutura bidimensional) para passá-los ao DataFrame
    data = list()

    units = getattr(info_obj, units_iterable_attr)

    for unit in units:
       
      row_data = list()

      for attribute in attrs_to_show.values():
          
          match attribute:
             
             case "created_time":
                
                row_data.append(convertToDatetimeFormat(getattr(unit, attribute)))

             case _:
                
                row_data.append(getattr(unit, attribute))
        
      data.append(row_data)
    
    df = pd.DataFrame(data, columns=list(attrs_to_show.keys()))

    self.specific_info_table.setRowCount(df.shape[0])
    self.specific_info_table.setColumnCount(df.shape[1])
    self.specific_info_table.setHorizontalHeaderLabels(df.columns)

    self.specific_info_table.setSelectionBehavior(QTableWidget.SelectRows) # Deixa as linhas inteiras selecionáveis
    self.specific_info_table.setSelectionMode(QTableWidget.SingleSelection) # Seleciona uma linha de cada vez

    for i in range(0, df.shape[0]):
       for j in range(0, df.shape[1]):
          
          table_item = QTableWidgetItem(str(df.iloc[i, j]).replace('.', ',') if isinstance(df.iloc[i, j], float) else str(df.iloc[i, j]))
          table_item.setFlags(table_item.flags() & ~Qt.ItemIsEditable)
          
          self.specific_info_table.setItem(i, j, table_item)
    
    for j in range(0, df.shape[1]):
       
       self.specific_info_table.setColumnWidth(j, 175)
  
  def styleSpecificInfoTable(self) -> None:

    """Estiliza a tabela de informações especificas sobre as unidades de cada módulo (CPUs, Processos e Partições)
    """

    table_style_content: str = ""

    TABLE_STYLE_PATH: str = os.path.join(
       os.path.dirname(os.path.dirname(__file__)), 
       "styles", 
       "table.txt"
       )

    # Estilização da tabela
    with open(TABLE_STYLE_PATH, "r") as table_style_stream:
       
      table_style_content = table_style_stream.read()
  
    self.specific_info_table.setStyleSheet(table_style_content)
  
  def setFilterLayout(self, proc_info_manager: ProcessesInfoManager) -> None:
     
     """Adiciona os widgets de filtro de unidades (Processos apenas)

     Parameters
     ----------
     proc_info_manager : ProcessesInfoManager
      Gerenciador de informações dos processos

     """

     # Verifica se o layout de filtro está vazio
     if self.filter_layout.isEmpty():

      filters = ["Nome", "PID", "Estado"]

      self.filter_by_combobox = QComboBox()
      self.filter_by_combobox.addItems(filters)

      self.filter_value_input = QLineEdit()
     
      self.filter_value_input.textEdited.connect(lambda: self.filterProcessesTable(
          proc_info_manager,
          filters[self.filter_by_combobox.currentIndex()],
          self.filter_value_input.text()
      ))

      self.filter_layout.addWidget(self.filter_by_combobox)
      self.filter_layout.addWidget(self.filter_value_input)
  
  def filterProcessesTable(self, proc_info_manager: ProcessesInfoManager, 
                           by: str, 
                           value: Any) -> None:
     
     """Filtra e carrega a tabela das unidades de processos após esse filtro

     Parameters
     ----------
     proc_info_manager : ProcessesInfoManager
      Gerenciador de informações dos processos
     by : str
      Atributo do processo que será aplicado o filtro
     value:
      Valor do atributo do processo filtrado
     """

     self.selected_filter = by
     self.current_filter_text = value

     proc_info_manager.filterBy(by, value)

     self.clearLayout(self.specific_info_layout)

     self.setSpecificInfoLayout(proc_info_manager)
  
  def openDetailsWindow(self, selected_row: int, info_obj: InfoManager) -> None:

    """Abre a janela de detalhes de uma unidade de algum dos módulos, a partir do gerenciador de informações e da linha da tabela selecionada

    Parameters
    ----------
    selected_row : int
      Linha da tabela selecionada
    info_obj : InfoManager
      Gerenciador de informações de um módulo (CPUs, processos ou Partições)
    """

    if selected_row == -1:
       
       QMessageBox.warning(self, "Aviso", "Por favor, selecione uma linha.")
       return

    self.details_window = DetailsWindow(selected_row, info_obj)

    self.details_window.show()

  def setInfoLayout(self) -> None:

    """Define o layout do container de informações. 
    
    Ela é subdivida em um container de informações gerais de todas as unidades, e outro container com informações mais especificas de cada unidade, além de um container de filtro (Apenas no módulo de Processos).

    Esse método serve para alocar os espaços da tela para cada layout.
    """

    self.info_layout = QVBoxLayout()

    self.general_info_layout = QVBoxLayout()

    self.filter_layout = QHBoxLayout()

    self.specific_info_layout = QVBoxLayout()

    self.specific_info_table = QTableWidget()

    self.specific_info_layout.addWidget(self.specific_info_table)

    self.info_layout.addLayout(self.general_info_layout)
    self.info_layout.addLayout(self.filter_layout)
    self.info_layout.addLayout(self.specific_info_layout)

    self.main_layout.addLayout(self.info_layout)

  def clearLayout(self, layout: QLayout) -> None:

    """
    Remove os widgets de um determinado layout

    Parameters
    ----------
    layout : QLayout
      Layout cujo widgets serão removidos
    """

    while layout.count():
        
        child = layout.takeAt(0)

        if child.widget():
            
            child.widget().deleteLater()

        elif child.layout():
            
            self.clearLayout(child.layout())

  def loadCPUInfo(self) -> None:

    """
    Carrega as informações da CPU
    """

    if not self.specific_info_layout.isEmpty():

      self.current_row_index = self.specific_info_table.currentRow()

      # Pega as posições atuais de cada scroll da tabela
      self.table_vert_scroll_pos : int = self.specific_info_table.verticalScrollBar().value()
      self.table_horiz_scroll_pos : int = self.specific_info_table.horizontalScrollBar().value()

    # Remove as conexões do timer para atualizar apenas a janela atual
    for timer_connection in self.timer_connections:
       
       self.timer.timeout.disconnect(timer_connection)
    
    # Limpa todas as conexões na lista de conexões
    self.timer_connections.clear()
    
    # Insere uma conexão correspondente ao módulo atual
    conn_cpu = self.timer.timeout.connect(self.loadCPUInfo)
    self.timer_connections.append(conn_cpu)
       
    cim = CPUsInfoManager()

    self.clearLayout(self.general_info_layout)
    self.clearLayout(self.filter_layout)
    self.clearLayout(self.specific_info_layout)

    self.setGeneralInfoLayout(cim)
    self.setSpecificInfoLayout(cim)

    # Seleciona a linha selecionada da última atualização
    self.specific_info_table.selectRow(self.current_row_index)
  
  def loadProcessInfo(self) -> None:

    """
    Carrega as informações dos Processos
    """

    if not self.specific_info_layout.isEmpty():

      self.current_row_index = self.specific_info_table.currentRow()

      # Pega as posições atuais de cada scroll da tabela
      self.table_vert_scroll_pos : int = self.specific_info_table.verticalScrollBar().value()
      self.table_horiz_scroll_pos : int = self.specific_info_table.horizontalScrollBar().value()

    # Remove as conexões do timer anteriores do timer
    for timer_connection in self.timer_connections:
       
       self.timer.timeout.disconnect(timer_connection)
    
    # Limpa a lista de conexões
    self.timer_connections.clear()
    
    # Cria uma nova conexão e a adiciona à lista
    conn_proc = self.timer.timeout.connect(self.loadProcessInfo)
    self.timer_connections.append(conn_proc)

    pim = ProcessesInfoManager()

    if self.current_filter_text:

      pim.filterBy(self.selected_filter, self.current_filter_text)

    # Limpa os layouts
    self.clearLayout(self.general_info_layout)
    self.clearLayout(self.specific_info_layout)

    # Carrega os layouts
    self.setGeneralInfoLayout(pim)
    self.setFilterLayout(pim)
    self.setSpecificInfoLayout(pim)

    self.filter_value_input.setFocus()

    # Define os resultados anteriores aos widgets de filtro
    self.filter_by_combobox.setCurrentText(self.selected_filter) # Opção do combobox
    self.filter_value_input.setText(self.current_filter_text) # Texto no lineedit
    self.specific_info_table.selectRow(self.current_row_index) # linha selecionada

  def loadDiskInfo(self) -> None:

    """
    Carrega as informações das Partições de Disco
    """

    if not self.specific_info_layout.isEmpty():

      self.current_row_index = self.specific_info_table.currentRow()

      # Pega as posições atuais de cada scroll da tabela
      self.table_vert_scroll_pos : int = self.specific_info_table.verticalScrollBar().value()
      self.table_horiz_scroll_pos : int = self.specific_info_table.horizontalScrollBar().value()

    # Remove as conexões do timer para atualizar apenas a janela atual
    for timer_connection in self.timer_connections:
       
       self.timer.timeout.disconnect(timer_connection)
    
    self.timer_connections.clear()
    
    conn_disk = self.timer.timeout.connect(self.loadDiskInfo)
    self.timer_connections.append(conn_disk)

    dpim = DiskPartitionsInfoManager()

    self.clearLayout(self.general_info_layout)
    self.clearLayout(self.filter_layout)
    self.clearLayout(self.specific_info_layout)

    self.setGeneralInfoLayout(dpim)
    self.setSpecificInfoLayout(dpim)

    self.specific_info_table.selectRow(self.current_row_index)
  
  def loadBatteryInfo(self) -> None:

    """
    Carrega as informações da bateria
    """

    # Remove as conexões do timer para atualizar apenas a janela atual
    for timer_connection in self.timer_connections:
       
       self.timer.timeout.disconnect(timer_connection)
    
    self.timer_connections.clear()
    
    conn_battery = self.timer.timeout.connect(self.loadBatteryInfo)
    self.timer_connections.append(conn_battery)

    bim = BatteryInfoManager()

    self.clearLayout(self.general_info_layout)
    self.clearLayout(self.filter_layout)
    self.clearLayout(self.specific_info_layout)

    self.setGeneralInfoLayout(bim)
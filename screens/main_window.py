from PySide6.QtWidgets import (
    QWidget, QPushButton, QVBoxLayout, QHBoxLayout, QLayout, 
    QLabel, QTableWidget, QTableWidgetItem, QMessageBox
)
from PySide6.QtCore import Qt
from PySide6.QtGui import QIcon

import pandas as pd


import os


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
  
  def __init__(self) -> None:

    super().__init__()

    self.setWindowTitle("Monitoramento do Sistema")
    self.setWindowIcon(QIcon(getSystemIconPath()))
    self.resize(700, 500)

    # Layout da tela
    self.main_layout = QVBoxLayout()

    self.setOptionsLayout()
    self.setInfoLayout()

    self.main_layout.addLayout(self.info_layout)

    self.setLayout(self.main_layout)

    """
    central_widget = QWidget()
    central_widget.setLayout(self.main_layout)

    self.setCentralWidget(central_widget)
    """

  def setOptionsLayout(self) -> None:

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

    btn_cpu.clicked.connect(self.loadCPUInfo)
    btn_process.clicked.connect(self.loadProcessInfo)
    btn_disk.clicked.connect(self.loadDiskInfo)
    btn_battery.clicked.connect(self.loadBatteryInfo)

    self.main_layout.addLayout(self.options_layout)
  
  def setGeneralInfoLayout(self, info_obj: InfoManager) -> None:

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
         
         case "time_left":
            
            data_label = QLabel(convertToTimeFormat(data))
         
         case "is_charging":
            
            data_label = QLabel("Sim" if data else "Não")

         case _:
            
            data_label = QLabel(str(data))
            
      unique_info_layout.addWidget(data_label)

      self.general_info_layout.addLayout(unique_info_layout)
  

  def setSpecificInfoLayout(self, info_obj: InfoManager) -> None:
     
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
       
       return

    self.specific_info_table = QTableWidget()
    table_style_content: str = ""

    TABLE_STYLE_PATH: str = os.path.join(os.path.dirname(os.path.dirname(__file__)), "styles", "table.txt")

    with open(TABLE_STYLE_PATH, "r") as table_style_stream:
       
      table_style_content = table_style_stream.read()
  
    self.specific_info_table.setStyleSheet(table_style_content)

    # Adicionando os dados exibidos em uma lista contendo listas (estrutura bidimensional) para passá-los ao DataFrame
    data = list()

    units = getattr(info_obj, units_attribute)

    for unit in units:
       
      row_data = list()

      for attribute in specific_infos.values():
          
          match attribute:
             
             case "created_time":
                
                row_data.append(convertToDatetimeFormat(getattr(unit, attribute)))

             case _:
                
                row_data.append(getattr(unit, attribute))
        
      data.append(row_data)
    
    df = pd.DataFrame(data, columns=list(specific_infos.keys()))

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
    
    btn_details = QPushButton("Detalhes")
    
    self.specific_info_layout.addWidget(self.specific_info_table)
    self.specific_info_layout.addWidget(btn_details)

    btn_details.clicked.connect(lambda: self.openDetailsWindow(self.specific_info_table.currentRow(), 
                                                               info_obj))
  
  def openDetailsWindow(self, selected_row: int, info_obj: InfoManager) -> None:

    if selected_row == -1:
       
       QMessageBox.warning(self, "Aviso", "Por favor, selecione uma linha.")
       return

    self.details_window = DetailsWindow(selected_row, info_obj)

    self.details_window.show()

  def setInfoLayout(self) -> None:

    """
    Define o layout do container de informações. Ela é subdivida em um container dde informações gerais de todas as unidades, e outro container com informações mais especificas de cada unidade.
    """

    self.info_layout = QVBoxLayout()

    self.general_info_layout = QVBoxLayout()

    self.specific_info_layout = QVBoxLayout()
    self.specific_info_table = QTableWidget()

    self.specific_info_layout.addWidget(self.specific_info_table)

    self.info_layout.addLayout(self.general_info_layout)
    self.info_layout.addLayout(self.specific_info_layout)

  def clearLayout(self, layout: QLayout) -> None:

    """
    Remove os widgets de um determinado layout
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
       
    cim = CPUsInfoManager()

    self.clearLayout(self.general_info_layout)
    self.clearLayout(self.specific_info_layout)

    self.setGeneralInfoLayout(cim)
    self.setSpecificInfoLayout(cim)
  
  def loadProcessInfo(self) -> None:

    """
    Carrega as informações dOs Processos
    """

    pim = ProcessesInfoManager()

    self.clearLayout(self.general_info_layout)
    self.clearLayout(self.specific_info_layout)

    self.setGeneralInfoLayout(pim)
    self.setSpecificInfoLayout(pim)
  
  def loadDiskInfo(self) -> None:

    """
    Carrega as informações das Partições de Disco
    """

    dpim = DiskPartitionsInfoManager()

    self.clearLayout(self.general_info_layout)
    self.clearLayout(self.specific_info_layout)

    self.setGeneralInfoLayout(dpim)
    self.setSpecificInfoLayout(dpim)
  
  def loadBatteryInfo(self) -> None:

    """
    Carrega as informações da bateria
    """

    bim = BatteryInfoManager()

    self.clearLayout(self.general_info_layout)
    self.clearLayout(self.specific_info_layout)

    self.setGeneralInfoLayout(bim)
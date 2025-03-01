from PySide6.QtWidgets import QVBoxLayout, QHBoxLayout, QWidget, QLabel, QMessageBox
from PySide6.QtGui import QIcon
from PySide6.QtCore import QTimer

from src.cpus.cpus_info_manager import CPUsInfoManager
from src.processes.processes_info_manager import ProcessesInfoManager
from src.disks.disk_partitions_info_manager import DiskPartitionsInfoManager
from src.abstracts.info_manager import InfoManager

from utils.format_datetime import convertToDatetimeFormat
from utils.icons import getSystemIconPath

class DetailsWindow(QWidget):

  def __init__(self, selected_row: int, info_obj: InfoManager) -> None:
    
    super().__init__()
     
    if isinstance(info_obj, CPUsInfoManager):
       
       iterable_attribute = "cpus_info"
       specific_info_attributes = {
          "ID da CPU": "cpu_id",
          "Porcentagem de Uso": "used_percentage",
          "Frequência Atual": "current_frequency",
          "Frequência Mínima": "minimum_frequency",
          "Frequência Máxima": "maximum_frequency"
       }
    
    elif isinstance(info_obj, ProcessesInfoManager):
       
       iterable_attribute = "processes_info"
       specific_info_attributes = {
          "Nome": "name",
          "Process ID (PID)": "pid",
          "Parent Process ID (PPID)": "ppid",
          "Estado": "status",
          "Prioridade": "priority_number",
          "Nome do Usuário Proprietário": "owner_username",
          "Caminho do Executável": "executable_path",
          "Data e Hora de Criação": "created_time",
          "Porcentagem de CPU Usada": "cpu_used_percentage",
          "Porcentagem de Memória Usada": "memory_used_percent",
          "Operações de Escrita Realizadas": "write_operations_count",
          "Operações de Leitura Realizadas": "read_operations_count",
          "Quantidade de Bytes de Escrita": "write_bytes_number",
          "Quantidade de Bytes de Leitura": "read_bytes_number",
          "Threads Usadas": "threads_used_count",
       }
    
    elif isinstance(info_obj, DiskPartitionsInfoManager):
       
       iterable_attribute = "disk_partitions_info"
       specific_info_attributes = {
          "Caminho de Montagem": "mountpoint_path",
          "Caminho do Dispositivo": "device_path",
          "Sistema de Arquivos": "file_system",
          "Armazenamento Total (Bytes)": "total_bytes",
          "Armazenamento Usado (Bytes)": "used_bytes",
          "Armazenamento Livre (Bytes)": "free_bytes",
          "Porcentagem de Uso": "used_percentage",
          "Operações de Escrita Realizadas": "write_operations_count",
          "Operações de Leitura Realizadas": "read_operations_count",
          "Quantidade de Bytes de Escrita": "write_bytes",
          "Quantidade de Bytes de Leitura": "read_bytes",
       }
    
    else:
       
       QMessageBox.warning(self, "Erro", "O objeto passado como argumento ao parâmetro 'info_obj' não é válido!")
       return
    
    
    self.setWindowTitle("Detalhes")
    self.setWindowIcon(QIcon(getSystemIconPath()))
    self.resize(700, 500)

    main_layout = QVBoxLayout()
    
    context_obj = getattr(info_obj, iterable_attribute)[selected_row]

    for label, attribute in specific_info_attributes.items():

      data = getattr(context_obj, attribute)
       
      # Layout de cada rótulo e informação
      unique_info_layout = QHBoxLayout()

      unique_info_layout.addWidget(QLabel(f"{label}: "))

      match attribute:
         
        case "created_time":
            
            # Converte a data de criação de um processo para o formato dd-mm-yyyy
            data_label = QLabel(convertToDatetimeFormat(data))
        
        case _:
            
            data_label = QLabel(str(data).replace(".", ",") if isinstance(data, float) else str(data))
      
      unique_info_layout.addWidget(data_label)

      main_layout.addLayout(unique_info_layout)
    
    self.setLayout(main_layout)
        
       

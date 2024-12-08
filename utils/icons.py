import sys
import os

def getSystemIconPath() -> str:

  ASSETS_DIR: str = os.path.join(os.path.dirname(os.path.dirname(__file__)), "assets")

  # Definição do Icone
  if sys.platform.startswith("win"):

    icon_path = os.path.join(ASSETS_DIR, "windows_icon.png")
  
  elif sys.platform.startswith("linux"):

    icon_path = os.path.join(ASSETS_DIR, "linux_icon.png")
  
  else:

    icon_path = os.path.join(ASSETS_DIR, "mac_icon.png")
  
  return icon_path
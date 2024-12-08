from PySide6.QtWidgets import QApplication


import sys
import os


from screens.main_window import MainWindow

if __name__ == "__main__":

  STYLES_PATH: str = os.path.join(os.path.dirname(__file__), "styles", "styles.txt")
  style_content: str = ""

  with open(STYLES_PATH, "r") as style_sheet_stream:

    style_content = style_sheet_stream.read()
  
  app = QApplication(sys.argv)
  app.setStyleSheet(style_content)

  window = MainWindow()
  window.show()

  sys.exit(app.exec())
    


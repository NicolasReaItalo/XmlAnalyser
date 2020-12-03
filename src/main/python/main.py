from fbs_runtime.application_context.PySide2 import ApplicationContext
from PySide2 import QtWidgets,QtGui,QtCore

import sys,os

from pathlib import Path
import xml.etree.ElementTree as ET

import api

class SubtitleWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        # Widgets
        self.drop_button =  QtWidgets.QPushButton("importer un XML")
        self.drop_button.clicked.connect(self.import_xml)


        self.console = QtWidgets.QPlainTextEdit()
        self.console.resize(800,1200)

        self.bouton_brissou = QtWidgets.QPushButton("Brissou")
        self.bouton_brissou.clicked.connect(self.fonction_brissou)

        #layout
        self.main_layout = QtWidgets.QHBoxLayout()
        self.main_layout.addWidget(self.drop_button)
        self.main_layout.addWidget(self.console)
        self.main_layout.addWidget(self.bouton_brissou)

        # window setup
        self.widget = QtWidgets.QWidget()
        self.widget.setLayout(self.main_layout)
        self.setCentralWidget(self.widget)
        self.resize(1200,800)

    def fonction_brissou(self):
        self.console.clear()
        self.console.setPlainText("Hello Brissou")



    def import_xml(self):
        f = QtWidgets.QFileDialog.getOpenFileUrl(self, "importer sous-titre", f"{Path.home()}/Desktop",
                                                 "Xml files (*.xml)")
        path =  f[0].toLocalFile()
        response = "Problèmes d'alignement détectés: \n"


        root = ET.parse(path)
        ET.register_namespace('',"http://www.smpte-ra.org/schemas/428-7/2010/DCST")
        ET.register_namespace('xs', 'http://www.w3.org/2001/schema')

        subtitles_list = root.findall('{http://www.smpte-ra.org/schemas/428-7/2010/DCST}SubtitleList/{http://www.smpte-ra.org/schemas/428-7/2010/DCST}Font/{http://www.smpte-ra.org/schemas/428-7/2010/DCST}Subtitle')

        for subtitle in subtitles_list:
            texts = list(subtitle.getchildren())


            for text in texts:
               # print(f' {text.text}   ///  Alignement: {text.attrib["Halign"]}')
                if text.attrib["Halign"] == "left" and  float(text.attrib["Hposition"]) < 20.0:
                    #print("probleme detecté")
                    #print(f'sous-titre n°: {subtitle.attrib["SpotNumber"]}')
                   # print(f' {text.text}  ')
                    #print("#########################################")

                    response = response + f'{subtitle.attrib["SpotNumber"]}: {text.text} \n'

        self.console.clear()
        self.console.setPlainText(response)










if __name__ == '__main__':
    appctxt = ApplicationContext()       # 1. Instantiate ApplicationContext
    window = SubtitleWindow()
    window.show()
    exit_code = appctxt.app.exec_()      # 2. Invoke appctxt.app.exec_()
    sys.exit(exit_code)
import sys
from PyQt5 import QtWidgets, QtCore
from client_ui import Ui_MainWindow
from cryptography.fernet import Fernet

from twisted.internet.protocol import ClientFactory
from twisted.protocols.basic import LineOnlyReceiver
import argparse

parser = argparse.ArgumentParser(description='MSQ Client launcher', add_help=True)
parser.add_argument("--port", action="store", dest='port', help="Port to connect to.")
parser.add_argument("--ip", action="store", dest='ip', help="IP to connect to.")
arguments = parser.parse_args()
arguments.port = int(arguments.port) if arguments.port else 1234
if not arguments.ip: 
    arguments.ip = "127.0.0.1"


class ConnectorProtocol(LineOnlyReceiver):
    factory: 'Connector'
    
    def decryptText(self, encrypted_text):
        cipherdek = Fernet(encrypted_text)
        decrypted_text = cipherdek.decrypt(encrypted_text[44:]).decode("utf-8")
        return decrypted_text
    
    def connectionMade(self):
        self.factory.window.protocol = self
        self.factory.window.plainTextEdit.appendPlainText("--- CONNECTED С {}:{} ---".format(arguments.ip, arguments.port))
    
    def lineReceived(self, line: bytes):
        #message = line.decode()
        message = self.decryptText(line)
        
        # Если получена команда очистки окна чата
        if message == "CMD: CLEAR ALL":
            self.factory.window.plainTextEdit.clear()
            return

        if message.startswith("CMD: FILL "):
            message = message.replace("CMD: FILL ", "")
            self.factory.window.lineEdit.setText(message)

        self.factory.window.plainTextEdit.appendPlainText(message)


class Connector(ClientFactory):
    window: 'ChatWindow'
    protocol = ConnectorProtocol

    def clientConnectionFailed(self, connector, reason):
        window.plainTextEdit.appendPlainText("Соединение с сервером не удалось.")

    def __init__(self, app_window):
        self.window = app_window


class ChatWindow(QtWidgets.QMainWindow, Ui_MainWindow):
    protocol: ConnectorProtocol = None
    reactor = None

    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.setWindowTitle("MSQ Chat")
        self.setStyleSheet(" font: 10pt Courier; QMainWindow { background-color: #aaaaaa }")
        self.init_handlers()
        self.lineEdit.installEventFilter(self)

    def init_handlers(self):
        self.pushButton.clicked.connect(self.send_message)

    def closeEvent(self, event):
        self.reactor.callFromThread(self.reactor.stop)

    def encodetext(self, text: str): #<<<<--------------
        textb = bytes(text, 'utf-8')
        cipher_key = Fernet.generate_key()
        cipher = Fernet(cipher_key)
        encrypted_text = cipher_key+cipher.encrypt(textb)
        return encrypted_text.decode("utf-8")
        
    def send_message(self):
        if self.protocol:
            message = self.lineEdit.text()
            self.protocol.sendLine(self.encodetext(message).encode())
            self.lineEdit.setText('')

        # Протокол не существует - подключиться к серверу не вышло.
        else:
            self.plainTextEdit.appendPlainText("Ошибка: Нет соединения с сервером.")

    def keyPressEvent(self, event) -> None:
        if event.key() in (QtCore.Qt.Key_Enter, QtCore.Qt.Key_Return) and self.lineEdit.hasFocus():
            self.send_message()

    def eventFilter(self, source, event):

        # Поле ввода всегда должно быть в фокусе.
        if event.type() == QtCore.QEvent.FocusOut:
            self.lineEdit.setFocus()
            return True
        return super(ChatWindow, self).eventFilter(source, event)


app = QtWidgets.QApplication(sys.argv)
window = ChatWindow()
window.show()

window.lineEdit.setFocus()

import qt5reactor                             # +++ pip install qt5reactor
qt5reactor.install()

from twisted.internet import reactor
reactor.connectTCP(
    arguments.ip,
    arguments.port,
    Connector(window),
)
window.reactor = reactor
reactor.run()

from twisted.internet import reactor          # +++ pip install Twisted
from twisted.internet.protocol import ServerFactory, connectionDone
from twisted.protocols.basic import LineOnlyReceiver
from cryptography.fernet import Fernet
import argparse
from datetime import datetime

parser = argparse.ArgumentParser(description='MSQ Server launcher', add_help=True)
parser.add_argument("--port", action="store", dest='port', help="Port to host server on.")
arguments = parser.parse_args()
arguments.port = int(arguments.port) if arguments.port else 1234


class ServerProtocol(LineOnlyReceiver):
    factory: 'Server'
    login: str = None

    def encodetext(self, text: str): #<<<<--------------
        textb = bytes(text, 'utf-8')
        cipher_key = Fernet.generate_key()
        cipher = Fernet(cipher_key)
        encrypted_text = cipher_key+cipher.encrypt(textb)
        return encrypted_text.decode("utf-8")
    
    def decryptText(self, encrypted_text):
        cipherdek = Fernet(encrypted_text)
        decrypted_text = cipherdek.decrypt(encrypted_text[44:]).decode("utf-8")
        return decrypted_text

    def connectionMade(self):
        self.sendLine(self.encodetext("Соединено с сервером.\nАвторизуйтесь при помощи команды /login.").encode())
        self.fillUserInput("/login ")

    def clearAll(self):
        self.sendLine(self.encodetext("CMD: CLEAR ALL").encode())

    def fillUserInput(self, msg):
        self.sendLine(self.encodetext(f"CMD: FILL {msg}").encode())

    def connectionLost(self, reason=connectionDone):
        # Если клиент авторизовался перед закрытием, его нужно закрыть со стороны сервера.
        if self in self.factory.clients:
            self.factory.clients.remove(self)
            print(f'{datetime.now().strftime("%H:%M:%S")} # {self.login} - left the chat. There are {self.factory.clients.__len__()} users in the chat in total.')
                        
        for user in self.factory.clients:
            status_text = f'{datetime.now().strftime("%H:%M:%S")} # {self.login} - покинул чат.'
            user.sendLine(self.encodetext(status_text).encode())

    def lineReceived(self, line: bytes) -> None:
        """
        Вызывается при получении сервером сообщения от клиента.
        :param line: Сообщение от клиента в зашифрованном виде.
        """

        # Расшифровываем сообщение клиента
        #content = line.decode()
        content = self.decryptText(line)
        
        # Если пользователь отправил пустое сообщение, игнорируем его.
        if not content:
            return

        # Если пользователь авторизован
        if self.login is not None:
            content = f"{datetime.now().strftime('%H:%M:%S')}# {self.login} >> {content}"

            # Записываем сообщение в историю чата для отправки пользователям после авторизации.
            self.factory.history.append(content)

            # Отсылаем сообщение всем авторизованным пользователям в сети
            for user in self.factory.clients:
                user.sendLine(self.encodetext(content).encode())

        # Если пользователь не авторизован
        else:
            # /login admin -> admin
            if content.startswith("/login"):

                # Пользователь ввел команду, но забыл логин
                if len(content.split()) < 2:
                    self.sendLine(self.encodetext("Неверное использование команды. Пример использования:\n/login username").encode())
                    self.fillUserInput("/login ")
                    return

                login = content.split()[1]

                # Если введенный логин занят
                for user in self.factory.clients:
                    if user.login == login:
                        self.sendLine(self.encodetext("Этот логин уже используется! Пожалуйста, используйте другой.").encode())
                        self.fillUserInput("/login ")
                        return

                # Если введенный логин свободен, авторизуем пользователя и шлем ему историю чата
                for user in self.factory.clients:
                    status_text = f'{datetime.now().strftime("%H:%M:%S")} # {login} - вошел в чат.'
                    user.sendLine(self.encodetext(status_text).encode())
                
                self.login = login
                self.factory.clients.append(self)
                self.clearAll()
                self.sendLine(self.encodetext("Добро пожаловать, {}!\nПоследние {} сообщений:".format(self.login, self.factory.history_length)).encode())
                self.factory.send_history(self)
                
                print(f'{datetime.now().strftime("%H:%M:%S")} # {self.login} - entered the chat. There are {self.factory.clients.__len__()} users in the chat in total.')
            
            # Если пользователь пытается слать сообщения без авторизации
            else:
                self.sendLine(self.encodetext("Пожалуйста, авторизуйтесь прежде чем слать сообщения.").encode())
                self.fillUserInput("/login ")


class Server(ServerFactory):
    protocol = ServerProtocol
    clients: list
    history: list
    history_length = 10

    def startFactory(self):
        self.clients = []
        self.history = []
        print("Server started on port {}".format(arguments.port))

    def stopFactory(self):
        print("Server closed")

    def send_history(self, client: ServerProtocol) -> None:
        """
        Отсылает последние <self.history_length> сообщений пользователю.
        :param client: Клиент, которому отправляем историю.
        """
        last_messages = self.history[-self.history_length:]

        for msg in last_messages:
            client.sendLine(self.encodetext(msg).encode())


reactor.listenTCP(int(arguments.port), Server())
reactor.run()

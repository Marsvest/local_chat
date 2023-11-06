import socket
import threading


def receive_messages(client_socket):
    while True:
        try:
            # Получаем сообщение от сервера
            message = client_socket.recv(1024).decode('utf-8')
            print(message)
        except:
            # В случае ошибки закрываем соединение
            client_socket.close()
            break


# Создаем сокет клиента
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Устанавливаем хост и порт сервера
server_host = '192.168.0.12'
server_port = 12345

# Подключаемся к серверу
client_socket.connect((server_host, server_port))

# Создаем поток для приема сообщений от сервера
threading.Thread(target=receive_messages, args=(client_socket,)).start()

while True:
    # Отправляем сообщение на сервер
    message = input()
    client_socket.send(message.encode('utf-8'))
    print('Сообщение отправлено')

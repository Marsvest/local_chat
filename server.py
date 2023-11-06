import socket
import threading


def get_ipv4():
    hostname = socket.gethostname()
    ip_address = socket.gethostbyname(hostname)
    return ip_address


def handle_client(client_socket, client_address):
    while True:
        try:
            # Получаем сообщение от клиента
            message = client_socket.recv(1024).decode('utf-8')
            print(f'Получено сообщение от {client_address}: {message}')

            # Отправляем сообщение всем клиентам, кроме отправителя
            for client in clients:
                if client != client_socket:
                    client.send((f'\n{client_address}: {message}').encode('utf-8'))
        except:
            # В случае ошибки удаляем клиента из списка
            clients.remove(client_socket)
            print(f'Пользователь {client_address} отключен')
            break


# Создаем сокет сервера
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Устанавливаем хост и порт сервера
server_host = get_ipv4()
server_port = 12345

# Привязываем сокет к хосту и порту
server_socket.bind((server_host, server_port))

# Начинаем прослушивание сокета
server_socket.listen(5)

print('Сервер запущен')

# Создаем список для хранения клиентских сокетов
clients = []

while True:
    # Принимаем подключение клиента
    client_socket, client_address = server_socket.accept()

    # Добавляем клиентский сокет в список
    clients.append(client_socket)

    print(f'Установлено соединение с клиентом {client_address}')

    # Создаем поток для обработки сообщений от клиента
    threading.Thread(target=handle_client, args=(client_socket, client_address)).start()

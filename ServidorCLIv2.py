import socket
import subprocess
import requests
import os
import argparse  # Importe a biblioteca argparse

# Obtenha o diretório atual em que o código do servidor está rodando
current_directory = os.path.dirname(os.path.abspath(__file__))

# Parse os argumentos de linha de comando
parser = argparse.ArgumentParser(description='Servidor CLI')
parser.add_argument('-H', '--agent-ip', type=str, required=True, help='Endereço IP do agente')
args = parser.parse_args()

# Use o endereço IP do agente especificado
agent_ip = args.agent_ip

# Resto do código do servidor...


# Obtenha o diretório atual em que o código do servidor está rodando
current_directory = os.path.dirname(os.path.abspath(__file__))

# Defina o endereço IP e porta do servidor central
server_address = '0.0.0.0'
server_port = 8888





# Crie o servidor
def create_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((server_address, server_port))
    server.listen(5)
    print(f"O servidor está ouvindo em {server_address}:{server_port}")
    return server

# Aceite conexões de agentes e envie comandos
def accept_connections(server):
    while True:
        client_socket, client_address = server.accept()
        print(f"Conexão estabelecida com {client_address}")
        send_commands(client_socket)

# Envie comandos para o agente
def send_commands(client_socket):
    while True:
        command = input("Digite um comando para o agente (ou 'exit' para encerrar): ")
        if command.lower() == 'exit':
            client_socket.send(command.encode())
            break
        elif command == 'build':
            # Modifique o comando para incluir o "git clone"
            command = 'git clone https://github.com/jebob28/PY_RPA.git'
        client_socket.send(command.encode())

        response = client_socket.recv(1024).decode()
        print(response)

def main():
    server = create_server()
    accept_connections(server)

if __name__ == '__main__':
    main()

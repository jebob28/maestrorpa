# Importe as bibliotecas necessárias
import socket
import subprocess
import http.server
import socketserver
import os
import argparse

agent_ip = socket.gethostbyname(socket.gethostname())

# Parse os argumentos de linha de comando
parser = argparse.ArgumentParser(description='Agente CLI')
parser.add_argument('-H', '--server-ip', type=str, required=True, help='Endereço IP do servidor central')
args = parser.parse_args()

# Use o endereço IP do servidor especificado
server_ip = args.server_ip

# Obtenha o diretório atual em que o código do agente está rodando
current_directory = os.path.dirname(os.path.abspath(__file__))

# Defina o endereço IP do servidor central e a porta de comunicação
server_address = server_ip
server_port = 8888

# Defina a porta para o servidor HTTP
http_port = 9000

# Crie um servidor HTTP para receber arquivos
with socketserver.TCPServer(('0.0.0.0', http_port), http.server.SimpleHTTPRequestHandler) as httpd:
    print(f'Servidor HTTP em execução na porta {http_port}')

# Conecte-se ao servidor central
def connect_to_server():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((server_address, server_port))
        return s
    except Exception as e:
        print(f'Erro ao se conectar ao servidor: {e}')
        return None

# Receba comandos do servidor e execute-os
def receive_commands(connection):
    while True:
        command = connection.recv(1024).decode()
        if command.lower() == 'exit':
            break
        elif command.startswith('git clone'):
            # Execute o comando "git clone" diretamente
            os.system(command)
            connection.send(f'Comando "{command}" executado com sucesso no agente.'.encode())
        else:
            output = subprocess.getoutput(command)
            connection.send(output.encode())

def receive_file(zip_file_name):
    handler = http.server.SimpleHTTPRequestHandler
    handler.directory = current_directory  # Diretório para salvar o arquivo ZIP
    with socketserver.TCPServer(('0.0.0.0', http_port), handler) as httpd:
        httpd.handle_request()

# Função principal para iniciar o agente
def main():
    connection = connect_to_server()
    if connection:
        receive_commands(connection)
        connection.close()

if __name__ == '__main__':
    main()

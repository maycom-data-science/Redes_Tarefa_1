# Importa as bibliotecas necessárias
import socket  # Para a comunicação via sockets
import hashlib  # Para calcular o hash SHA-256 de arquivos
import os  # Para operações com sistema de arquivos

# Função para receber e salvar arquivos do servidor
def receive_file(client_socket):
    # Recebe informações do arquivo do servidor
    file_info = client_socket.recv(1024).decode('utf-8')
    
    # Verifica se o arquivo não existe no servidor
    if file_info.startswith("Arquivo inexistente"):
        print(file_info)
    else:
        # Divide as informações em linhas
        file_info = file_info.split('\n')
        filename = file_info[0].split(": ")[1].strip()  # Extrai o nome do arquivo
        
        # Extrai o tamanho do arquivo como uma string e converte para um número inteiro
        file_size_str = file_info[1].split(": ")[1].strip().split(" ")[0]
        file_size = int(file_size_str)
        
        server_hash = file_info[2].split(": ")[1].strip()  # Obtém o hash SHA-256 do servidor
        status = file_info[3].split(": ")[1].strip()  # Obtém o status do arquivo
        
        # Exibe informações sobre o arquivo recebido
        print(f"Recebido: {filename}\nTamanho: {file_size} bytes\nHash SHA-256 do servidor: {server_hash}\nStatus: {status}")
        
        if status == "ok":
            file_data = b""  # Inicializa uma variável para armazenar os dados do arquivo
            bytes_received = 0  # Contador de bytes recebidos
            
            while bytes_received < file_size:
                chunk = client_socket.recv(4096)  # Define que o cliente irá receber dados do arquivo em pedaços de 4096 bytes (4 KB) de cada vez do servidor.
                if not chunk:
                    break
                file_data += chunk
                bytes_received += len(chunk)
            
            # Calcula o hash SHA-256 dos dados do arquivo recebido
            client_hash = hashlib.sha256(file_data).hexdigest()
            
            # Verifica a integridade do arquivo comparando o hash do servidor com o hash calculado
            if client_hash == server_hash:
                save_path = os.path.join("BD_Cliente", filename)  # Monta o caminho de salvamento do arquivo
                with open(save_path, 'wb') as file:
                    file.write(file_data)  # Salva o arquivo no diretório "BD_Cliente"
                print("Integridade do arquivo verificada. Arquivo salvo no diretório 'BD_Cliente'.")
            else:
                print("Integridade do arquivo comprometida. O arquivo não será salvo.")
        else:
            print("Status do arquivo: NOK")

# Função principal do cliente
def main():
    host = 'localhost'  # Endereço do servidor
    port = 55555  # Porta do servidor
    
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # Cria um socket TCP
    client.connect((host, port))  # Estabelece uma conexão com o servidor
    
    while True:
        try:
            request = input("Digite sua requisição (Sair, Arquivo NOME.EXT, Chat): ")  # Solicitação do usuário
            client.send(request.encode('utf-8'))  # Envia a solicitação para o servidor
            
            if request == "Sair":
                client.close()  # Fecha a conexão com o servidor e encerra o cliente
                break
            
            elif request.startswith("Arquivo"):
                receive_file(client)  # Função para receber e salvar arquivos do servidor
            
            elif request == "Chat":
                message = client.recv(1024).decode('utf-8')  # Recebe mensagens de chat do servidor
                print(f"Recebido do servidor: {message}")
        
        except Exception as e:
            print(f"Erro na conexão: {e}")
            client.close()  # Fecha a conexão com o servidor em caso de erro e encerra o cliente

# Verifica se o código está sendo executado como um programa principal
if __name__ == "__main__":
    main()  # Chama a função principal para iniciar o cliente

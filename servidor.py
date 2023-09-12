import socket
import threading
import os
import pickle  # Importa a biblioteca pickle para serialização.

def handle_client(client_socket):

    while True:  # Adicionamos um loop para lidar com múltiplas solicitações do cliente
    # Recebe a solicitação do cliente.
        request = client_socket.recv(1024).decode('utf-8')
        if request == "Sair":
            break
        
        elif request == "Arquivo":
            # Envia uma mensagem solicitando o nome do arquivo.
            client_socket.send("Nome do arquivo".encode('utf-8'))
            filename = client_socket.recv(1024).decode('utf-8')
            
            file_path = os.path.join("BD_Servidor", filename)
            if os.path.exists(file_path):
                # Envia uma mensagem indicando que o arquivo existe.
                client_socket.send("Arquivo existe".encode('utf-8'))
                
                with open(file_path, 'rb') as file:
                    file_data = file.read()
                    # Envia os dados do arquivo serializados usando pickle.
                    client_socket.send(pickle.dumps(file_data))
                
                client_socket.send("Resposta: Arquivo enviado com sucesso.".encode('utf-8'))
                
            else:
                # Envia uma mensagem indicando que o arquivo não existe.
                client_socket.send("Arquivo não existe".encode('utf-8'))
        else:
            # Envia uma resposta genérica.
            client_socket.send(f"Resposta: {request}".encode('utf-8'))

    client_socket.close()
    

def main():
    host = 'localhost'
    port = 55555
    
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((host, port))
    server.listen(5)
    
    print(f"[*] Servidor escutando em {host}:{port}")
    
    while True:
        client_socket, addr = server.accept()
        print(f"[*] Conexão recebida de {addr[0]}:{addr[1]}")
        client_thread = threading.Thread(target=handle_client, args=(client_socket,))
        client_thread.start()

if __name__ == "__main__":
    main()

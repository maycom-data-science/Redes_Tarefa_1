import socket
import os
import pickle  # Importa a biblioteca pickle para serialização.

def main():
    host = 'localhost'
    port = 55555
    
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((host, port))
    
    while True:
        # Solicita ação ao usuário.
        request = input("Digite sua requisição (Texto, Arquivo, Sair): ")
        client.send(request.encode('utf-8'))
        
        if request == "Sair":
            client.send(request.encode('utf-8'))
            break
        
        elif request == "Arquivo":
            # Recebe uma mensagem solicitando o nome do arquivo.
            response = client.recv(1024).decode('utf-8')
            filename = input(response + ": ")
            client.send(filename.encode('utf-8'))
            
            # Recebe uma mensagem indicando se o arquivo existe no servidor.
            file_exists = client.recv(1024).decode('utf-8')
            if file_exists == "Arquivo existe":
                file_data = b""
                while True:
                    # Recebe os dados do arquivo serializados usando pickle.
                    chunk = client.recv(4096)
                    if not chunk:
                        break
                    file_data += chunk
                
                save_path = os.path.join("BD_Cliente", filename)
                with open(save_path, 'wb') as file:
                    # Deserializa os dados do arquivo usando pickle.
                    file.write(pickle.loads(file_data))
                print("Arquivo salvo com sucesso.")
                
                response = client.recv(1024).decode('utf-8')
                print(response)
            else:
                print("Arquivo não existe no servidor.")
        
        else:
            response = client.recv(1024).decode('utf-8')
            print(response)
    
    client.close()

if __name__ == "__main__":
    main()

import socket  
import threading  
import os  
import hashlib 

def handle_client(client_socket):
    try:
        while True:
            # Recebe uma mensagem do cliente e a decodifica como UTF-8
            request = client_socket.recv(1024).decode('utf-8')
            
            # Verifica se não há mais mensagens a serem recebidas
            if not request:
                break
            
            # Se o cliente enviar "Sair", encerra a conexão com esse cliente
            if request == "Sair":
                print("Cliente desconectado.")
                break
            
            # Se a mensagem do cliente começar com "Arquivo", o servidor trata como uma solicitação de arquivo
            elif request.startswith("Arquivo"):
                filename = request.split(" ")[1]  # Extrai o nome do arquivo da mensagem
                filepath = os.path.join("BD_Servidor", filename)  # Monta o caminho completo para o arquivo
                
                # Verifica se o arquivo existe no diretório "BD_Servidor"
                if os.path.exists(filepath):
                    # Lê o conteúdo do arquivo em modo binário
                    with open(filepath, 'rb') as file:
                        file_data = file.read()
                    file_size = os.path.getsize(filepath)  # Obtém o tamanho do arquivo
                    hash_sha256 = hashlib.sha256(file_data).hexdigest()  # Calcula o hash SHA-256 do arquivo
                    
                    # Monta uma resposta para o cliente com informações sobre o arquivo
                    response = f"Nome do arquivo: {filename}\nTamanho: {file_size} bytes\nHash SHA-256: {hash_sha256}\nStatus: ok"
                    client_socket.send(response.encode('utf-8'))  # Envia a resposta para o cliente
                    
                    # Envie os dados do arquivo em partes para o cliente
                    client_socket.send(file_data)
                else:
                    response = "Arquivo inexistente."
                    client_socket.send(response.encode('utf-8'))
            
            # Se a mensagem do cliente for "Chat", o servidor permite o envio de mensagens de chat
            elif request == "Chat":
                while True:
                    chat_input = input("Digite uma mensagem para o cliente (ou 'Sair' para encerrar o chat): ")
                    if chat_input == "Sair":
                        break
                    client_socket.send(f"Chat: {chat_input}".encode('utf-8'))
    
    except Exception as e:
        print(f"Erro na conexão: {e}")
    
    # Certifique-se de fechar a conexão com o cliente, independentemente de como a conexão terminou
    finally:
        client_socket.close()

def main():
    host = 'localhost'  # Endereço em que o servidor vai ouvir (todas as interfaces de rede)
    port = 55555  # Porta em que o servidor vai ouvir
    
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # Cria um socket TCP
    server.bind((host, port))  # Liga o socket ao endereço e porta especificados
    server.listen(5)  # Inicia a escuta do servidor com um limite de 5 conexões pendentes
    
    print(f"Servidor ouvindo em {host}:{port}")
    
    while True:
        client, addr = server.accept()  # Aceita uma nova conexão de cliente
        print(f"Conexão recebida de {addr[0]}:{addr[1]}")
        
        # Cria uma nova thread para lidar com o cliente atual
        client_handler = threading.Thread(target=handle_client, args=(client,))
        client_handler.start()  # Inicia a thread

if __name__ == "__main__":
    main()  

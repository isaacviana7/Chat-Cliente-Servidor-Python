import socket
import time

HOST = 'localhost'
PORT = 12345
MAX_SEGMENT_SIZE = 1400
MAX_RETRIES = 3


def calcular_checksum(segmento):
    checksum = sum(segmento) & 0xFFFF
    return checksum


def enviar_segmento(socket_cliente, endereco_servidor, segmento):
    socket_cliente.sendto(segmento, endereco_servidor)


def receber_confirmacao(socket_cliente):
    num_retries = 0
    while num_retries < MAX_RETRIES:
        try:
            data, endereco = socket_cliente.recvfrom(MAX_SEGMENT_SIZE)
            return data.decode()
        except socket.timeout:
            num_retries += 1
            print(f"Timeout. Tentando novamente... ({num_retries}/{MAX_RETRIES})")

    return "Erro na confirmação."


def main():
    endereco_servidor = (HOST, PORT)

    # Cria o socket do cliente
    socket_cliente = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    socket_cliente.settimeout(1)  # Define um timeout de 1 segundo

    # Inicia o chat
    print("Bem-vindo ao chat! Digite 'sair' para encerrar o chat.")

    while True:
        mensagem = input("Digite sua mensagem: ")

        # Verifica se o usuário deseja encerrar o chat
        if mensagem.lower() == "sair":
            print("Chat encerrado.")
            break

        # Segmenta a mensagem em pacotes de tamanho máximo
        num_segmentos = (len(mensagem) + MAX_SEGMENT_SIZE - 1) // MAX_SEGMENT_SIZE

        # Loop para enviar os segmentos da mensagem
        for i in range(num_segmentos):
            inicio = i * MAX_SEGMENT_SIZE
            fim = min(inicio + MAX_SEGMENT_SIZE, len(mensagem))
            segmento = mensagem[inicio:fim].encode()

            # Calcula o checksum do segmento
            checksum = calcular_checksum(segmento)

            # Envia o segmento ao servidor
            enviar_segmento(socket_cliente, endereco_servidor, segmento)

            # Espera pela confirmação do servidor
            confirmacao = receber_confirmacao(socket_cliente)

            # Verifica se a confirmação está correta
            if confirmacao == str(checksum):
                print(f"Segmento {i+1} enviado com sucesso.")
            else:
                print(f"Erro na confirmação do segmento {i+1}. Reenviando...")
                i -= 1  # Reenvia o segmento atual

                if i == -1:
                    print("Atingido o limite de tentativas. Deseja enviar a mensagem novamente? (s/n)")
                    opcao = input("> ")

                    if opcao.lower() == "s":
                        break

        # Aguarda a resposta do servidor com a solicitação da próxima mensagem
        resposta = receber_confirmacao(socket_cliente)
        print(resposta)

    # Fecha o socket do cliente
    socket_cliente.close()


if __name__ == '__main__':
    main()

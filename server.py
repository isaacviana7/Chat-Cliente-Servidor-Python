import socket
import random

HOST = 'localhost'
PORT = 12345
MAX_SEGMENT_SIZE = 1400


def calcular_checksum(segmento):
    checksum = sum(segmento) & 0xFFFF
    return checksum


def enviar_confirmacao(socket_servidor, endereco_cliente, confirmacao):
    socket_servidor.sendto(confirmacao.encode(), endereco_cliente)


def main():
    # Cria o socket do servidor
    socket_servidor = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    socket_servidor.bind((HOST, PORT))

    print("Servidor pronto para receber mensagens...")

    while True:
        # Recebe o pacote do cliente
        segmento, endereco_cliente = socket_servidor.recvfrom(MAX_SEGMENT_SIZE)

        # Simula a perda do pacote com 30% de chance
        if random.random() <= 0.1:
            print("Pacote perdido. Reenviando...")
            continue

        # Verifica o checksum do segmento
        checksum = calcular_checksum(segmento)
        confirmacao = str(checksum)

        # Envia a confirmação ao cliente
        enviar_confirmacao(socket_servidor, endereco_cliente, confirmacao)

        # Decodifica o segmento e exibe a mensagem recebida
        mensagem = segmento.decode()
        print(f"Mensagem do Cliente: {mensagem}")

        # Envia uma solicitação para enviar a próxima mensagem
        enviar_confirmacao(socket_servidor, endereco_cliente, "Envie a próxima mensagem.")

    # Fecha o socket do servidor
    socket_servidor.close()


if __name__ == '__main__':
    main()

import socket

host = 'localhost'
puerto = 10002

try:
    # Crear conexión
    cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    cliente.connect((host, puerto))

    # Recibir mensaje de bienvenida
    bienvenida = cliente.recv(4096).decode()
    print(bienvenida)

    # Elegir categoría y enviar
    categoria = input("¿Sobre qué quieres recibir información (Atletas/Comunidades/Ciudades)?:").strip()
    cliente.send(categoria.encode())

    # Recibir la lista de opciones
    opciones_posibles = cliente.recv(4096).decode()
    
    if "ERROR" in opciones_posibles:
        print(opciones_posibles)
        cliente.close()
    print(opciones_posibles)
    
    # Elegir la clave y enviarla
    seleccion = input("\nEscribe el nombre exacto de tu elección: ").strip()
    cliente.send(seleccion.encode())

    # Resultado
    resultado_final = cliente.recv(4096).decode()
    print(f"\nINFORMACIÓN RECUPERADA")
    print(resultado_final)

except ConnectionRefusedError:
    print("Error: No se pudo establecer la conexión.")
except Exception as e:
    print(f"Error: {e}")
finally:
    cliente.close()
    print("Conexión cerrada.")
import socket
import threading
import time

def start_server(port, name):
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(('0.0.0.0', port))
    server.listen(5)
    print(f"[*] {name} listening on port {port}")
    
    while True:
        try:
            client, addr = server.accept()
            # print(f"[*] Connection from {addr} on port {port}")
            client.close()
        except:
            break

if __name__ == "__main__":
    # Simulate SSH on 2222 and Web on 8080
    t1 = threading.Thread(target=start_server, args=(2222, "SSH"))
    t2 = threading.Thread(target=start_server, args=(8080, "HTTP"))
    
    t1.daemon = True
    t2.daemon = True
    
    t1.start()
    t2.start()
    
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\nStopping servers...")

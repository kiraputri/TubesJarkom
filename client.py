import socket

HOST = '192.168.56.1'
PORT = 5050

def start_client(request_path='/'): #fungsi yang menerima path file yan akan diminta dari server
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s: #memastikan socket di tutup setelah digunakan
        s.connect((HOST, PORT))  # Lakukan koneksi ke server

        # Kirim permintaan HTTP untuk file tertentu
        request = f"GET {request_path} HTTP/1.1\r\nHost: {HOST}\r\n\r\n"
        s.sendall(request.encode('utf-8'))
        
        #Terima dan simpan response dari server
        response = b""
        while True:
            data = s.recv(4096)
            if not data: # memeriksa koneksi atau data yg diterima
                break
            response += data #menambahkan data yang diterima ke response

        return response.decode('utf-8', errors='ignore') #mengembalikan response dari server
        
# Contoh penggunaan: meminta file index.html dari server
filename = "index.html"
server_response = start_client(request_path=f'/{filename}') # menyimpan respon dari server
print(f"Response from server for /{filename}:")
print(server_response) #mencetak respon yg diterima

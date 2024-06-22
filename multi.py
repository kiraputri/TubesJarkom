import socket
import os
import threading

# Konfigurasi server
HOST = '192.168.56.1' #server lokal pada komputer
PORT = 5050 #Nomor port server yang digunakan
BASE_DIR = os.path.dirname(os.path.abspath(__file__)) #Direktori dasar

# Membuat socket server
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)#Membuat objek socket dengan menggunakan IPv4 dan TCP
server.bind((HOST, PORT)) #Mengikat socket ke alamat IP dan port yang ditentukan.
server.listen()
print(f"Server berjalan di {HOST}:{PORT}")

#Fungsi untuk menentukan dan memeriksa tipe konten berdasarkan ekstensi file dan mengembalikan tipe konten yang sesuai
def get_content_type(filename):
    if filename.endswith('.html'):
        return 'text/html'
    elif filename.endswith('.jpg'):
        return 'image/jpg'
    elif filename.endswith('.jpeg'):
        return 'image/jpeg'
    elif filename.endswith('.png'):
        return 'image/png'
    elif filename.endswith('.gif'):
        return 'image/gif'
    elif filename.endswith('.pdf'):
        return 'application/pdf'
    elif filename.endswith('.txt'):
        return 'text/plain'
    else:
        return 'application/octet-stream' # Tipe konten default jika ekstensi tidak dikenali

# Fungsi untuk membaca konten file yang diberikan dalam mode biner 
def get_file_content(filename):
    with open(filename, 'rb') as f:
        content = f.read()
    return content #mengembalikan konten file yg telah dibaca

# Fungsi untuk menghasilkan respons HTTP berdasarkan permintaan klien
def generate_http_response(request):
    try:
        filename = request.split()[1][1:]
        if filename == '': #jika path kosong 
            return b'HTTP/1.1 404 Not Found\r\n\r\n<h1>404 Not Found</h1>'
        filepath = os.path.join(BASE_DIR, filename) #menentukan path lengkap dari file yg diminta
        if os.path.isfile(filepath): #Jika file ada, baca kontennya dan buat header respons HTTP 
            content_type = get_content_type(filepath)
            content = get_file_content(filepath)
            response_header = 'HTTP/1.1 200 OK\r\nContent-Type: {}\r\nContent-Length: {}\r\n\r\n'.format(
                content_type, len(content))
            response = response_header.encode('utf-8') + content
        else: # Jika file tidak ditemukan
            response = b'HTTP/1.1 404 Not Found\r\n\r\n<h1>404 Not Found</h1>'
    except Exception as e: #jika terjadi kesalahan
        print(str(e))
        response = b'HTTP/1.1 500 Internal Server Error\r\n\r\n<h1>500 Internal Server Error</h1>'
    return response
    
# Fungsi untuk menangani koneksi klien
def handle_client(conn, addr):
    print(f"[NEW CONNECTION] {addr} connected.")
    try:
        data = conn.recv(1024) #menerima data dari klien
        if data: #pemrosesan data 
            request = data.decode()
            method = request.split()[0]  # Mendapatkan metode HTTP dari permintaan
            path = request.split()[1]  # Mendapatkan path dari permintaan
            protocol = request.split()[2]  # Mendapatkan versi protokol HTTP dari permintaan
            print(f"Request information:")
            print(f"method: {method}")
            print(f"path: {path}")
            print(f"protocol: {protocol}") # Menampilkan informasi request
            response = generate_http_response(request) # menghasilkan respons http berdasarkan permintaan client
            conn.sendall(response)# sinyal respons telah diterima oleh klien.
    #Jika terjadi kesalahan, cetak pesan kesalahan dan tutup koneksi.
    except Exception as e:
        print(f"Error handling client {addr}: {e}")
    finally:
        conn.close()



# Loop untuk menerima koneksi
try:
    while True: #Loop utama yang menerima koneksi klien dan memulai thread baru untuk setiap klien.
        conn, addr = server.accept()
        thread = threading.Thread(target=handle_client, args=(conn, addr)) #Membuat thread baru untuk menangani klien.
        thread.start()
        print(f"[ACTIVE CONNECTIONS] {threading.active_count() - 1}") 
except KeyboardInterrupt: # Menangkap sinyal interrupt  untuk menghentikan server dengan aman.
    print("Server dimatikan.")
finally:
    server.close() #Menutup socket server.

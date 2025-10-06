from socket import *
from threading import Thread
from cryptography.fernet import Fernet
from chatbot import ask_ai

# --- Encryption setup ---
key = Fernet.generate_key()
cipher = Fernet(key)
print("\n🔐 Encryption Key:", key.decode())
print("Share this key securely with your friend.\n")

# --- Receive messages ---
def receive_messages(conn):
    while True:
        try:
            data = conn.recv(1024)
            if not data:
                break
            decrypted_msg = cipher.decrypt(data).decode()
            print("\n👤 Friend:", decrypted_msg)
        except:
            break

# --- Send messages (with AI command) ---
def send_messages(conn):
    while True:
        msg = input("You: ")

        # AI mode — when message starts with /ai
        if msg.startswith("/ai"):
            question = msg.replace("/ai", "").strip()
            print("🤖 Thinking...")
            ai_reply = ask_ai(question)
            print("\nAI:", ai_reply)
            continue

        # Normal encrypted message
        encrypted_msg = cipher.encrypt(msg.encode())
        conn.send(encrypted_msg)

# --- Main program ---
choice = input("Do you want to Host (H) or Connect (C)? ").upper()

if choice == "H":
    server = socket(AF_INET, SOCK_STREAM)
    server.bind(('', 5000))
    server.listen(1)
    print("📡 Waiting for connection...")
    conn, addr = server.accept()
    print("✅ Connected to:", addr)
    Thread(target=receive_messages, args=(conn,)).start()
    send_messages(conn)

elif choice == "C":
    host_ip = input("Enter Host IP: ")
    conn = socket(AF_INET, SOCK_STREAM)
    conn.connect((host_ip, 5000))
    print("✅ Connected to host!")
    Thread(target=receive_messages, args=(conn,)).start()
    send_messages(conn)

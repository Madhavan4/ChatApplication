import socket
import tkinter as tk
import threading

def receive_messages():
    while True:
        message = c.recv(1024).decode()
        if not message:
            break
        conversation_text.config(state=tk.NORMAL)
        conversation_text.insert(tk.END, "Client: " + message + "\n")
        conversation_text.config(state=tk.DISABLED)

def start_server():
    global s, c
    s = socket.socket()
    print("Socket successfully created")

    port = 12345

    s.bind(('', port))
    print("socket binded to %s" % (port))

    s.listen(5)
    print("socket is listening")

    while True:
        # Establish connection with client.
        c, addr = s.accept()
        print('Got connection from', addr)

        # Send welcome message to client
        c.send('Welcome to the chat server!'.encode())

        # Start a new thread to handle receiving messages from client
        threading.Thread(target=receive_messages, daemon=True).start()

# Function to send a message to the client
def send_message():
    message = message_entry.get()
    if message:
        conversation_text.config(state=tk.NORMAL)
        conversation_text.insert(tk.END, "You: " + message + "\n")
        conversation_text.config(state=tk.DISABLED)
        message_entry.delete(0, tk.END)
        c.send(message.encode())

# Create GUI
root = tk.Tk()
root.title("Server")

# Create conversation display area
conversation_text = tk.Text(root, height=20, width=50)
conversation_text.config(state=tk.DISABLED)
conversation_text.grid(row=0, column=0, columnspan=2, padx=10, pady=10)

message_entry = tk.Entry(root, width=40)
message_entry.grid(row=1, column=0, padx=10, pady=10)

# Create send button for server
send_button = tk.Button(root, text="Send", command=send_message)
send_button.grid(row=1, column=1, padx=10, pady=10)

# Start the server in a separate thread
threading.Thread(target=start_server, daemon=True).start()

root.mainloop()

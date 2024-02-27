import socket
import tkinter as tk
import threading

def send_message():
    message = message_entry.get()
    if message:
        conversation_text.config(state=tk.NORMAL)
        conversation_text.insert(tk.END, "You: " + message + "\n")
        conversation_text.config(state=tk.DISABLED)
        message_entry.delete(0, tk.END)
        s.send(message.encode())

def receive_messages():
    while True:
        message = s.recv(1024).decode()
        if message:
            conversation_text.config(state=tk.NORMAL)
            conversation_text.insert(tk.END, "Server: " + message + "\n")
            conversation_text.config(state=tk.DISABLED)

root = tk.Tk()
root.title("Chat Application")

# Create conversation display area
conversation_text = tk.Text(root, height=20, width=50)
conversation_text.config(state=tk.DISABLED)
conversation_text.grid(row=0, column=0, columnspan=2, padx=10, pady=10)

message_entry = tk.Entry(root, width=40)
message_entry.grid(row=1, column=0, padx=10, pady=10)

# Create send button for user
send_button = tk.Button(root, text="Send", command=send_message)
send_button.grid(row=1, column=1, padx=10, pady=10)

s = socket.socket()
s.connect(('127.0.0.1', 12345))

# receive welcome message from the server and decoding to get the string
welcome_message = s.recv(1024).decode()
conversation_text.config(state=tk.NORMAL)
conversation_text.insert(tk.END, "Server: " + welcome_message + "\n")
conversation_text.config(state=tk.DISABLED)

# Start a thread to continuously receive messages from the server
threading.Thread(target=receive_messages, daemon=True).start()

root.mainloop()

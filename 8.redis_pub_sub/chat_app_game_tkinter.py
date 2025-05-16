import tkinter as tk
import threading
import redis
import time

CHANNEL = "chatroom"

class ChatApp:
    def __init__(self, root, username):
        self.username = username
        self.r = redis.Redis(host='localhost', port=6379, decode_responses=True)
        self.pubsub = self.r.pubsub()
        self.pubsub.subscribe(CHANNEL)

        self.root = root
        self.root.title(f"Redis Chat - {username}")

        self.chat_text = tk.Text(root, state='disabled', wrap='word')
        self.chat_text.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

        self.msg_entry = tk.Entry(root)
        self.msg_entry.pack(padx=10, pady=5, fill=tk.X)
        self.msg_entry.bind("<Return>", self.send_message)

        self.root.protocol("WM_DELETE_WINDOW", self.on_close)

        self.listen_thread = threading.Thread(target=self.listen_for_messages, daemon=True)
        self.listen_thread.start()

    def send_message(self, event=None):
        msg = self.msg_entry.get().strip()
        if msg:
            message = f"{self.username}: {msg}"
            self.r.publish(CHANNEL, message)
            self.msg_entry.delete(0, tk.END)

    def listen_for_messages(self):
        for message in self.pubsub.listen():
            if message['type'] == 'message':
                self.append_message(message['data'])

    def append_message(self, message):
        self.chat_text.config(state='normal')
        self.chat_text.insert(tk.END, message + "\n")
        self.chat_text.yview(tk.END)
        self.chat_text.config(state='disabled')

    def on_close(self):
        self.pubsub.unsubscribe(CHANNEL)
        self.root.destroy()


def main():
    username = input("Enter your username: ")
    root = tk.Tk()
    app = ChatApp(root, username)
    root.mainloop()

if __name__ == "__main__":
    main()

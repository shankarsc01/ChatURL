import tkinter as tk
from bs4 import BeautifulSoup
from urllib.request import urlopen
import openai

openai.api_key = "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"


def fetch_text():
    url = url_entry.get()
    html = urlopen(url).read()
    soup = BeautifulSoup(html, features="html.parser")

    # Kill all script and style elements
    for script in soup(["script", "style"]):
        script.extract()  # Rip it out

    # Get text
    text = soup.get_text()
    context_text.delete(1.0, tk.END)
    context_text.insert(tk.END, text)


def send_message():
    message = user_input.get()
    user_input.delete(0, tk.END)
    chat_log.config(state=tk.NORMAL)
    chat_log.insert(tk.END, "You: " + message + "\n")
    chat_log.config(state=tk.DISABLED)

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": "Please answer my queries according to the given context \n Context: {}".format(
                context_text.get(1.0, tk.END))},
            {"role": "assistant", "content": message}
        ]
    )

    reply = response["choices"][0]["message"]["content"]
    chat_log.config(state=tk.NORMAL)
    chat_log.insert(tk.END, "Bot: " + reply + "\n")
    chat_log.config(state=tk.DISABLED)

    # Dynamically adjust the height of chat_log to fit the content
    chat_log.update_idletasks()
    chat_log_height = chat_log.bbox("end-1c").y2 - chat_log.bbox("1.0").y1
    chat_log.config(height=chat_log_height)

    # Scroll to the end of the chat log
    chat_log.see(tk.END)


# Create the main window
window = tk.Tk()
window.title("Chatbot UI")

# Add a heading for ChatURL
heading_label = tk.Label(window, text="ChatURL", font=("Arial", 16, "bold"))
heading_label.pack(pady=10)

# Create a frame for URL entry
url_frame = tk.Frame(window)
url_frame.pack(pady=10)

url_label = tk.Label(url_frame, text="Enter URL:")
url_label.pack(side=tk.LEFT)

url_entry = tk.Entry(url_frame, width=50)
url_entry.pack(side=tk.LEFT)

fetch_button = tk.Button(url_frame, text="Fetch Text", command=fetch_text)
fetch_button.pack(side=tk.LEFT)

# Create a frame for chatbot conversation
chat_frame = tk.Frame(window)
chat_frame.pack(pady=10)

context_text = tk.Text(chat_frame, width=80, height=10, font=("Arial", 12))
context_text.pack()

chat_log = tk.Text(chat_frame, width=80, height=20, font=("Arial", 12))
chat_log.pack(expand=True, fill="both")
chat_log.config(state=tk.DISABLED)

# Add horizontal scrollbar to chat_log
scrollbar = tk.Scrollbar(
    chat_frame, orient="horizontal", command=chat_log.xview)
scrollbar.pack(fill="x")
chat_log.config(xscrollcommand=scrollbar.set)

user_input = tk.Entry(chat_frame, width=60, font=("Arial", 12))
user_input.pack(side=tk.LEFT)

send_button = tk.Button(chat_frame, text="Send", command=send_message)
send_button.pack(side=tk.LEFT)

window.mainloop()

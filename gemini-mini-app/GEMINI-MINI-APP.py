import tkinter as tk  # use tkinter for the app window and widgets
from tkinter import messagebox  # use message boxes for simple alerts

# Replace this with your actual API key if needed.
API_KEY = "ENTER_AN_API_KEY_HERE"  # ENTER AN API_KEY
MODEL = "gemini-3.5-flash"  # model name for Gemini requests

try:
    from google import genai  # import the Gemini client library
except ImportError:
    genai = None  # if import fails, keep going and show an error later


def send_prompt():
    """Get text from the entry box and send it to Gemini."""
    prompt = prompt_entry.get().strip()  # read what the user typed

    if prompt == "":
        messagebox.showinfo("Enter prompt", "Please type something before sending.")
        return

    if genai is None:
        messagebox.showerror(
            "Missing package",
            "Install google-generativeai with:\npython -m pip install google-generativeai"
        )
        return

    send_button.config(state=tk.DISABLED)  # disable the button while waiting
    status_label.config(text="Sending...")  # show a simple status message

    try:
        client = genai.Client(api_key=API_KEY)  # create a Gemini client
        response = client.interactions.create(model=MODEL, input=prompt)

        output_area.config(state=tk.NORMAL)  # allow writing to the output area
        output_area.insert(tk.END, "You: " + prompt + "\n")
        output_area.insert(tk.END, "Gemini: " + response.output_text + "\n\n")
        output_area.config(state=tk.DISABLED)  # stop writing to the output area
        output_area.see(tk.END)  # scroll to the bottom

        status_label.config(text="Done")  # update the status label
    except Exception as error:
        messagebox.showerror("Error", str(error))  # show any error in a popup
        status_label.config(text="Error")
    finally:
        send_button.config(state=tk.NORMAL)  # let the button be clicked again


def clear_output():
    """Clear the output text area."""
    output_area.config(state=tk.NORMAL)
    output_area.delete("1.0", tk.END)  # remove all text
    output_area.config(state=tk.DISABLED)
    status_label.config(text="Cleared")


# Create the main window.
root = tk.Tk()
root.title("Gemini Mini App")  # window title text
root.geometry("620x500")  # window size in pixels
root.configure(bg="#eef6ff")  # background color
root.resizable(False, False)  # fixed window size

# Title label at the top.
label = tk.Label(root, text="Gemini Mini App", font=("Arial", 18, "bold"), bg="#eef6ff")
label.pack(pady=12)

# Prompt input field where the user types text.
prompt_entry = tk.Entry(root, font=("Arial", 12), width=60)
prompt_entry.pack(pady=8)
prompt_entry.focus()  # put the cursor in the prompt box

# Frame to hold the buttons.
button_frame = tk.Frame(root, bg="#eef6ff")
button_frame.pack(pady=8)

send_button = tk.Button(button_frame, text="Send", width=12, command=send_prompt)
send_button.pack(side=tk.LEFT, padx=6)

clear_button = tk.Button(button_frame, text="Clear", width=12, command=clear_output)
clear_button.pack(side=tk.LEFT, padx=6)

# Status label shows what the app is doing.
status_label = tk.Label(root, text="Ready", font=("Arial", 10), bg="#eef6ff")
status_label.pack(pady=4)

# Output area shows the conversation with Gemini.
output_area = tk.Text(root, width=72, height=18, state=tk.DISABLED, wrap=tk.WORD)
output_area.pack(pady=10)

# Add an initial message to the output area.
output_area.config(state=tk.NORMAL)
output_area.insert(tk.END, "Welcome to Gemini Mini App!\n\n")
output_area.config(state=tk.DISABLED)

# Start the app and open the window.
root.mainloop()

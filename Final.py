import tkinter as tk
from tkinter import ttk
import language_mapping_input, language_mapping_output
import speech_recognition
from gtts import gTTS
from deep_translator import GoogleTranslator
import os

def translate_text():
    # Get the input text
    text = input_text.get(1.0, tk.END).strip()
    # Source language
    lang_in = language_mapping_input.mapping[language_input.get()]
    # Target language
    lang_out = language_mapping_output.mapping[language_output.get()]
    # Translator translate it and convert it to text
    translator = GoogleTranslator(source = lang_in, target = lang_out)
    translated_text = translator.translate(text)
    # Clear previous output with tkinter(from start to end)
    output_text.delete(1.0, tk.END)
    # Insert translated text in output
    output_text.insert(tk.END, translated_text)
    try:
        # Save translated text to a temporary file
        tts = gTTS(translated_text, lang = lang_out)
        tts.save('translation.mp3')
        # Sound button activation
        sound_button['state'] = tk.NORMAL
    except:
        # Disable sound button
        sound_button['state'] = tk.DISABLED

def play_sound():
    # Play the audio file
    os.system("translation.mp3")

def get_speech():
    # Set speech_recognition.Recognizer().Microphone() as source
    with speech_recognition.Microphone() as voise:
        # Remove noises
        speech_recognition.Recognizer().adjust_for_ambient_noise(voise)
        print("Listening...")
        audio = speech_recognition.Recognizer().listen(voise)
    try:
        lang_in = language_mapping_input.mapping[language_input.get()]
        text = speech_recognition.Recognizer().recognize_google(audio, language = lang_in)
        input_text.delete(1.0, tk.END)
        input_text.insert(tk.END, text)
        translate_text()
    except:
        print("Try Again...")

# Function to update the Source language dropdown based on search criteria
def update_dropdown_in(search_term = "",):
    menu = language_dropdown_in["menu"]
    menu.delete(0, "end")
    keys = sorted(language_mapping_input.mapping.keys())
    if search_term:
        keys = [key for key in keys if search_term.lower() in key.lower()]
    for key in keys:
        menu.add_command(label = key, command = lambda value = key: language_input.set(value))

# Function to update the Target language dropdown based on search criteria
def update_dropdown_out(search_term = "",):
    menu = language_dropdown_out["menu"]
    menu.delete(0, "end")
    keys = sorted(language_mapping_output.mapping.keys())
    if search_term:
        keys = [key for key in keys if search_term.lower() in key.lower()]
    for key in keys:
        menu.add_command(label = key, command = lambda value = key: language_output.set(value))

# Graphical part
root = tk.Tk()
root.title("Language Translator")
root.geometry("480x580")

# Create a variable to hold the selected language
language_output = tk.StringVar(root)
language_input = tk.StringVar(root)

# Set the default language
language_output.set("english")
language_input.set("auto")

# Create the Source language selection label and dropdown
language_label_in = ttk.Label(root, text = "Select Input Language:")
language_label_in.grid(pady = 10, padx = 40, row = 0, column = 0, sticky = tk.W)

language_dropdown_frame_in = ttk.Frame(root)
language_dropdown_frame_in.grid(row = 0, sticky = tk.E, padx = 30)

search_var_in = tk.StringVar()

# Design searchbar(Source language)
search_entry_in = ttk.Entry(language_dropdown_frame_in, textvariable = search_var_in)
search_entry_in.grid(row = 0, column = 0, sticky = tk.E)

# Design dropdown(Source language)
search_var_in.trace("w", lambda name, index, mode, sv = search_var_in: update_dropdown_in(sv.get()))
language_dropdown_in = ttk.OptionMenu(language_dropdown_frame_in, language_input, "")
language_dropdown_in.grid(row = 0, column = 1, sticky = tk.E)
update_dropdown_in()

# Create the Target language selection label and dropdown
language_label_out = ttk.Label(root, text = "Select Output Language:")
language_label_out.grid(pady = 10, padx = 40, row = 2, column = 0, sticky = tk.W)

language_dropdown_frame_out = ttk.Frame(root)
language_dropdown_frame_out.grid(row = 2, sticky = tk.E, padx = 30)

search_var_out = tk.StringVar()

# Design searchbar(Target language)
search_entry_out = ttk.Entry(language_dropdown_frame_out, textvariable = search_var_out)
search_entry_out.grid(row = 2, column = 1, sticky = tk.W)

# Design dropdown(Target language)
search_var_out.trace("w", lambda name, index, mode, sv = search_var_out: update_dropdown_out(sv.get()))
language_dropdown_out = ttk.OptionMenu(language_dropdown_frame_out, language_output, "")
language_dropdown_out.grid(pady = 10, row = 2, column = 3, sticky = tk.E)
update_dropdown_out()

# Create the input text label and area
input_label_out = ttk.Label(root, text = "Enter Text to Translate:")
input_label_out.grid(row = 3, column = 0)
input_text = tk.Text(root, height = 8, width = 50)
input_text.grid(row = 4, column = 0, padx = 40)

# Create the speech button
speech_button = ttk.Button(root, text = "Get Speech", command = get_speech)
speech_button.grid(pady = 10, row = 5, column = 0, padx = 40, sticky = tk.W)

# Create the translation button
style = ttk.Style()
style.configure('T.TButton', font = ('calibri', 16, 'bold'), foreground = 'blue')
translate_button = ttk.Button(root, text = "Translate", style = 'T.TButton', command = translate_text)
translate_button.grid(pady = 10, row = 6, padx = 80, column = 0, ipadx = 70, ipady = 6)

# Create the output text label and area
output_label = ttk.Label(root, text = "Translated Text:")
output_label.grid(row = 7, column = 0, pady = 20)
output_text = tk.Text(root, height = 8, width = 50)
output_text.grid(row = 8, column = 0)

# Create the play sound button
sound_button = ttk.Button(root, text = "Sound", command = play_sound)
sound_button.grid(pady = 5, row = 9, column = 0, sticky = tk.E, padx = 40)

root.mainloop()
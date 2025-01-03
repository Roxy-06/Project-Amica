import speech_recognition as sr
import os,webbrowser
import pyttsx3
import datetime
#from langchain_ollama import OllamaLLM
import smtplib
import subprocess
import psutil
import time
from plyer import notification
import tkinter as tk
from PIL import Image, ImageTk
import threading
#-------------------------------------WORKING OF VOICE COMMANDS--------------------------------
engine=pyttsx3.init('sapi5')
voices=engine.getProperty('voices')
engine.setProperty('voice',voices[1].id)
#----------------------------------------------------------------------------------------------

#-------------------------------------DEFINING FUNCTION----------------------------------------

def speak(audio):
    engine.say(audio)
    engine.runAndWait()

def time():
    h=datetime.datetime.now().hour
    m=datetime.datetime.now().minute
    speak(f"Its {h} hours {m} minutes now")

def takecommands():
    recognizer = sr.Recognizer()
    
    # Use the microphone as the audio source
    with sr.Microphone() as source:
        print("Adjusting for ambient noise... Please wait.")
        
        # Increase ambient noise adjustment duration
        recognizer.adjust_for_ambient_noise(source, duration=2)
        
        # Dynamically adjust energy threshold
        recognizer.energy_threshold += 50  
        print("Listening for your speech...")
        
        try:
            # Capture the audio with timeout to avoid long waits in noisy environments
            audio = recognizer.listen(source, timeout=8, phrase_time_limit=12)
            print("Recognizing your speech...")
            # Recognize speech using Google's speech recognition engine
            text = recognizer.recognize_google(audio)
            print(f"You said: {text}")
            return text

        except sr.UnknownValueError:
            print("Sorry, I couldn't understand. Please try again.")
            speak("Sorry, I couldn't understand. Could you repeat that?")
            return ""
        except sr.RequestError as e:
            print(f"Could not request results; {e}")
            speak("There seems to be an issue with the speech recognition service.")
            return ""
        except sr.WaitTimeoutError:
            print("No speech detected.")
            speak("No speech detected ... Perhaps try me when u need me")
            return ""

def repeat(text):
    b=text.split(" ")
    while True:
        i=0
        if b[i]=="say":
            b.pop(i)
            break
        else:
            b.pop(i)
    c=" ".join(b)
    return c

def greet(a):
    y=["hello",a]
    return y

def wthr():
    speak("showing weather in your address")
    batch_file_path = r"D:\Project-Alpha\kpa.bat"
    os.system(batch_file_path)
    return

def calculate(expression):
    e=expression
    if "x" in expression:
        e=expression.replace('x','*')
        print(e)
    try:
        result = eval(e)
        return result
    except Exception as ex:
        return str(ex)

def tictactoe():
    subprocess.run(["python", "tictactoe.py"])

def check_security():
    subprocess.run(["python", "cybersecurity.py"])

def system_check():
    subprocess.run(["python","health.py"])

def main(prompts):
    prompts=prompts.lower()
    #-------------------------------------------------------------------------------------------------
    commands=["open youtube","open chat gpt","shutdown","time now","repeat what i say","game"]
    #-------------------------------------------------------------------------------------------------
    weather=["weather now","weather today","will it rain","how is the weather","weather","will it rain today","is it gonna rain here","is it going to rain","how is the weather today","how is the weather now"]
    intro=["who are you","introduce yourself","who is jarvis","how can you help me"]
    positive=["yes","yup","sure","ok","k","done","yeah","yes i would","i would","like"]
#-------------------------------------------------------------------------------------------------
    try:
        orders=prompts
#--------------------------------ETERATING COMMANDS-----------------------------------------------
        if commands[0] in orders:
            webbrowser.open("www.youtube.com")
            speak("Opening Youtube!")
            return
            
        elif commands[1] in orders:
            webbrowser.open("https://chatgpt.com/c/66fa6233-e15c-8000-bfd3-f101a2d340d8")
            speak("Opening Chat GPT!")
            return
            
        elif commands[2] in orders:
            speak("Terminating Voice Commands...device shutdown successful!!")
                
        elif commands[3] in orders:
            time()
            return

        elif commands[4] in orders:
            speak("You Said")
            speak(repeat(orders))
            return
        
        elif commands[5] in orders:
            tictactoe()
            return

        elif "check security" in orders:
            check_security()
            return

        elif "system check" in orders:
            speak("Monitoring your system")
            system_check()
            speak("scan completed successfully")
            return

        elif orders in intro:
            speak("I’m your personal AI assistant, here to help you make your tasks easier and more efficient. Whether you need information, assistance with your files, or just a bit of help staying organized, I’m always ready to assist. You can ask me anything—from managing your calendar and documents to answering questions or performing quick actions on your computer.Feel free to explore my capabilities, and let's make your desktop experience smoother together!")
            return
            
        elif orders in weather:
            wthr()
            return

        elif "1" or "2" or "3" or "4" or "5" or "6" or "7" or "8" or "9" or "0" in orders:
            r=calculate(orders)
            speak(r)
            print(r)
            return

        else:
            speak("I am not trained to answer such a question!")
            webbrowser.open("https://chatgpt.com/c/66fa6233-e15c-8000-bfd3-f101a2d340d8")
            speak("But i guess chat gpt might help u with your prompts")
            return
    
    except:
        print("Overload Occured")
        speak("system failed to execute")
        return

def on_button_press(event):
    user_input = takecommands()
    if user_input=="shutdown" :
        main("shutdown")
        root.quit()
        return
    main(user_input)
    # if main(user_input):
    #     root.quit()  # Exit the application if shutdown command is received


#----------------------------------------------------------------------------------------------

#==============================================================================================
#                                        MAIN
#==============================================================================================

root = tk.Tk()
root.title("Circular Button with Mic")
root.geometry("200x200")
canvas = tk.Canvas(root, width=200, height=200, bg="black", highlightthickness=0)
canvas.pack()
x, y, r = 100, 100, 40  
canvas.create_oval(x - r, y - r, x + r, y + r, fill="white", outline="black", width=2)  
mic_image = Image.open("D:\Project-Alpha\m.png") 
mic_image = mic_image.resize((80, 80), Image.LANCZOS) 
mic_photo = ImageTk.PhotoImage(mic_image)
canvas.create_image(x, y, image=mic_photo)
canvas.bind("<Button-1>", on_button_press)
speak("Turning on voice recognition")
speak("System fully functional")
root.mainloop()

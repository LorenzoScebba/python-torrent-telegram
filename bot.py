import glob
import telepot
from telepot.loop import MessageLoop
import time
import os
import subprocess
import shutil


token = ""
chatId = 
serverIp = ""

bot = telepot.Bot(token)

def handle(msg):
    content_type, chat_type, chat_id = telepot.glance(msg)
    print(chat_id)
    # Il bot funziona solo con la mia chat, aggiungi anche il tuo chatID se vuoi che funzioni pure per te, lezzo
    if chat_id == chatId:
        if content_type == "document":
            # Get FileID and FileName
            file_id = msg['document']['file_id']
            file_name = msg['document']['file_name']
            print("File recived \n" + file_id + "\n" + file_name + "\n---------")
            bot.sendMessage(chat_id, "File recived")
            # Download file in script folder with file_name
            bot.download_file(file_id, (os.path.dirname(os.path.abspath(__file__)) + "/" + file_name))
            print("Downloading torrent")
            bot.sendMessage(chat_id, "Downloading...")
            # Apro un processo aria2c per scaricare il torrent
            p = subprocess.Popen(['aria2c ' + (
                    os.path.dirname(os.path.abspath(__file__)) + "/" + file_name) + ' --seed-time 0 -d torrent'],
                                 shell=True)
            # Primo controllo di poll
            poll = p.poll()
            # Finche il pool == None il processo sta runnando
            while poll == None:
                poll = p.poll()
                time.sleep(5)
            # Torrent scaricato, rimuovo il file.torrent e invio il file scaricato
            print("Torrent Downloaded")
            bot.sendMessage(chat_id, "Torrent Downloaded!")
            # Rimuovo il file .torrent e un possibile zip creato in precedenza
            os.remove((os.path.dirname(os.path.abspath(__file__)) + "/" + file_name))
            try:
                os.remove((os.path.dirname(os.path.abspath(__file__)) + "/Torrent.zip"))
            except:
                pass
            # Creo uno zip del file
            bot.sendMessage(chat_id,"Zipping...")
            shutil.make_archive('Torrent', 'zip', glob.glob("torrent/")[0])
            try:
                os.remove(glob.glob("torrent/*")[0])
            except:
                os.rmdir(glob.glob("torrent/*")[0])
            print("All done!\n")
            bot.sendMessage(chat_id, "Removed .torrent and original file!")
            try:
                os.rename("Torrent.zip", "/var/www/html/Torrent.zip")
                bot.sendMessage(chat_id, "File is avaiable at : " + serverIp +"/Torrent.zip")
            except:
                print("Errore, no superuser rights")
                bot.sendMessage(chat_id,"Error, did you use sudo to start the bot?")
                os.remove("Torrent.zip")
    else:
        bot.sendMessage(chat_id, "Sorry, this bot is usable only by his creator")


MessageLoop(bot, handle).run_as_thread()

while 1:
    time.sleep(10)

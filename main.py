import bot
import threading
import os


if __name__ == '__main__':
    def start_site():
        os.system("go run botsite/server.go")
    threading.Thread(target=start_site).start()

    bot.run_discord_bot()

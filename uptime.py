from datetime import datetime
import time
import requests
from infi.systray import SysTrayIcon
import asyncio
from decouple import config
url = config("URL")
interval = int(config("INTERVAL"))
formatted_interval = interval / 60
corrected_interval = interval - 5
print("Using heartbeat URL: " + url + ". Sending a heartbeat every", formatted_interval, "minutes")


async def send_beat():
    while True:
        try:
            r = requests.get(url)
            now = datetime.now()
            current_time = now.strftime("%H:%M:%S")
            print("Current Time =", current_time)
            if "ok" in r.text:
                await successful()
            else:
                await failed()
            print("Waiting", str(formatted_interval), "minutes before sending next heartbeat")
            await asyncio.sleep(corrected_interval)
        except Exception as e:
            await failed()




async def failed():
    print("An error occurred and heartbeat couldn't be sent")
    systray.update(hover_text="Heartbeat Failed", icon='error.ico')


async def successful():
    print("Successfully sent heartbeat")
    systray.update(hover_text="Heartbeat Sent", icon='heart.ico')
    await asyncio.sleep(5)
    systray.update(hover_text="Trent's Computer Uptime Heartbeat", icon='icon.ico')


def send_manual(systray):
    try:
        r = requests.get(url)
        if "ok" in r.text:
            print("Successfully sent manual heartbeat")
            systray.update(hover_text="Heartbeat Sent", icon='heart.ico')
            time.sleep(5) # this hangs the program, but works to limit how quickly you can send :)
            systray.update(hover_text="Trent's Computer Uptime Heartbeat", icon='icon.ico')
        else:
            print("An error occurred and heartbeat couldn't be sent")
            systray.update(hover_text="Heartbeat Failed", icon='error.ico')
    except:
        print("An error occurred and heartbeat couldn't be sent")
        systray.update(hover_text="Heartbeat Failed", icon='error.ico')


menu_options = (("Send manual heartbeat", None, send_manual),)
systray = SysTrayIcon("icon.ico", "Trent's Computer Uptime Heartbeat", menu_options)
systray.start()

loop = asyncio.get_event_loop()
coroutine = send_beat()
loop.run_until_complete(coroutine)

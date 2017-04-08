import subprocess
import time

subprocess.call('raspistill -o cam.jpg',shell=True)
time.sleep(5)

subprocess.call('/home/pi/Dropbox-Uploader/dropbox_uploader.sh upload /home/pi/cam.jpg https://www.dropbox.com/home/Apps/cam.jpg',shell=True)
time.sleep(10)

subprocess.Popen('rm cam.jpg',shell=True)

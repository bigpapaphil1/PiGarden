READ ME!

Auto-PiGarden is made to automatically check weather forcast using yahoo. 

Also the program uses a PiCamera to take 17 pictures/day through out the life of the garden and string them together to form a timelapse photo.


NEED:

Go to this link to allow gmail to send emails through python --> https://myaccount.google.com/lesssecureapps 

pip3 install ffmpeg --> http://hamelot.io/visualization/using-ffmpeg-to-convert-a-set-of-images-into-a-video/

pip3 install weather-api  --> https://pypi.org/project/weather-api/


Be sure to set your LOCATION variable GMAIL_USER, GMAIL_PASSWORD, and EMAIL_TO in main.py

Plug soil input sensor wire into BOARD pin 40 
Plug relay output into BOARD pin 38 


raspberry pi GPIO Info --> http://tieske.github.io/rpi-gpio/modules/GPIO.html#input
Water Solenoid --> https://www.amazon.com/uxcell-Water-Solenoid-Normal-Electromagnetic/dp/B01LVWHMUY/ref=sr_1_7?ie=UTF8&qid=1543601789&sr=8-7&keywords=12+volt+water+valve
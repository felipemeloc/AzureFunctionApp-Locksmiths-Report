"""bot.py

This is a custom module to be imported from other code. Its function is to send messages and images to a chat id.
To get the chat id, it should be search using this URL https://api.telegram.org/bot<YourBOTToken>/getUpdates

The module needs the installation of the following packages:
* telebot: This allows the script to communicate with Telegram's API to send and receive messages
* os: For path management and directory creation
* dotenv: load environment variables

First the module load the environment variables and define the main path for the project.
Then, 2 functions are defined: send_message and send_photo. 
The function send_message receive an id and a message to be send to the chat id. Use :
  import bot
  bot.send_message(id= 'YOUR_CHAT_ID',
                  message= 'YOUR MESSAGE')

The function send_photo read an image from a path and send it to the chat id with a description. Use:
  import bot
  bot.send_photo(id= 'YOUR_CHAT_ID',
                photo_path= './IMAGE_PATH.png', 
                description= 'YOUR DESCRIPTION')

"""

from sqlalchemy import true
import telebot
import os
from .src import azure_blob as blob
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
# Define project main path
main_path = os.getenv('MAIN_PATH')

# Load API key
API_KEY = os.getenv('API_KEY')
# Instantiation of telebot class
init_bot = lambda: telebot.TeleBot(API_KEY)

def send_message(id:str, message:str)->None:
  """Function to send string message to an specifict chat id

  Args:
      id (str): chat identifier
      message (str): string with the message to be send
  """  
  # Send message to chat id
  bot = init_bot()
  bot.send_message(chat_id=id,
                    text=message,
                    parse_mode='Markdown')

def send_photo(id:str, photo_path:str, description:str=None)->None:
  """Function to send images to an specifict chat id

  Args:
      id (str): chat identifier
      photo_path (str): path where the photo to be send is located
      description (str, optional): string with the image description. Defaults to None.
  """

  # Read image as a bit map
  # photo = open(photo_path, 'rb').read()
  photo = blob.download(photo_path, as_bytes= True)
  # Send image to chat id
  bot = init_bot()
  bot.send_photo(chat_id= id,
                  photo= photo,
                  caption= description)
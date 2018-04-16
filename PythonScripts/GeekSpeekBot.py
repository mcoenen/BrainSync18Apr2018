#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import RPi.GPIO as GPIO
import time
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import logging

# Set constants for pin numbers
RedLEDpin = 36
YellowLEDpin = 38
GreenLEDpin = 40

# Initialize RaspberryPI board
GPIO.setmode(GPIO.BOARD)
GPIO.setup(RedLEDpin, GPIO.OUT)
GPIO.setup(YellowLEDpin, GPIO.OUT)
GPIO.setup(GreenLEDpin, GPIO.OUT)

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)

# Rasperry procedures for turning on/off the LEDs
def RedLED(cmd):
    if cmd == "on":
        GPIO.output(RedLEDpin, True)
    if cmd == "off":
        GPIO.output(RedLEDpin, False)

def YellowLED(cmd):
    if cmd == "on":
        GPIO.output(YellowLEDpin, True)
    if cmd == "off":
        GPIO.output(YellowLEDpin, False)

def GreenLED(cmd):
    if cmd == "on":
        GPIO.output(GreenLEDpin, True)
    if cmd == "off":
        GPIO.output(GreenLEDpin, False)

# Telegram procedures
def start(bot, update):
    """Send a message when the command /start is issued."""
    update.message.reply_text('Hi, my name is the GeekSpeekBot! \nWelcome to this BrainSync Session!! \nFor help do /help in this chat')

def help(bot, update):
    """Send a message when the command /help is issued."""
    update.message.reply_text('/help This help overview \n/setRedled set the state of the Red LED with argument on or off\n\
/setYellowled set the state of the Yellow LED with argument on or off\n/setGreenled set the state of the Green LED with argument on or off\n\
/setALLled set the state of the all the LEDs with argument on or off\n')

def echo(bot, update):
    """Echo the user message."""
    update.message.reply_text(update.message.text)

def setRedled(bot, update, args):
    """Define status of RED led on breakoutboard"""
    if args[0] == "on" or args[0] == "ON" or args[0] == "On":
        RedLED("on")
        update.message.reply_text('RED led is turned ON!')
    elif args[0] == "off" or args[0] == "OFF" or args[0] == "Off":
        RedLED("off")
        update.message.reply_text('RED led is turned OFF!')
    else:
        update.message.reply_text('I don know what you mean by '+args[0])

def setYellowled(bot, update, args):
    """Define status of YELLOW led on breakoutboard"""
    if args[0] == "on" or args[0] == "ON" or args[0] == "On":
        YellowLED("on")
        update.message.reply_text('Yellow led is turned ON!')
    elif args[0] == "off" or args[0] == "OFF" or args[0] == "Off":
        YellowLED("off")
        update.message.reply_text('Yellow led is turned OFF!')
    else:
        update.message.reply_text('I don know what you mean by '+args[0])

def setGreenled(bot, update, args):
    """Define status of GREEN led on breakoutboard"""
    if args[0] == "on" or args[0] == "ON" or args[0] == "On":
        GreenLED("on")
        update.message.reply_text('Green led is turned ON!')
    elif args[0] == "of" or args[0] == "OFF" or args[0] == "Off":
        GreenLED("off")
        update.message.reply_text('Green led is turned OFF!')
    else:
        update.message.reply_text('I don know what you mean by '+args[0])

def setALLled(bot, update, args):
    """Define status of GREEN led on breakoutboard"""
    if args[0] == "on" or args[0] == "ON" or args[0] == "On":
        RedLED("on")
        YellowLED("on")
        GreenLED("on")
        update.message.reply_text('All leds are turned ON!')
    elif args[0] == "off" or args[0] == "OFF" or args[0] == "Off":
        RedLED("off")
        YellowLED("off")
        GreenLED("off")
        update.message.reply_text('All leds are turned OFF!')
    else:
        update.message.reply_text('I don know what you mean by '+args[0])

def error(bot, update, error):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, error)

def main():
    """Start the bot."""
    # Create the EventHandler and pass it your bot's token.
    updater = Updater("594682702:AAGiV30qJm7eIrEUQMdqfrTBZXzf8rMyLTs")

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # on different commands - answer in Telegram
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("setRedled", setRedled, pass_args=True))
    dp.add_handler(CommandHandler("setYellowled", setYellowled, pass_args=True))
    dp.add_handler(CommandHandler("setGreenled", setGreenled, pass_args=True))
    dp.add_handler(CommandHandler("setALLled", setALLled, pass_args=True))
    dp.add_handler(CommandHandler("help", help))

    # log all errors
    dp.add_error_handler(error)

    # Start the Bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    main()
    GPIO.cleanup()

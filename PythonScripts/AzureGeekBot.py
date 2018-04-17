#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import logging
import os
import traceback

from azure.common.credentials import ServicePrincipalCredentials
from azure.mgmt.resource import ResourceManagementClient
from azure.mgmt.network import NetworkManagementClient
from azure.mgmt.compute import ComputeManagementClient
from azure.mgmt.compute.models import DiskCreateOption

from msrestazure.azure_exceptions import CloudError

from haikunator import Haikunator

haikunator = Haikunator()
azure_logged_on = False

# Azure Datacenter
LOCATION = 'westus'

# Resource Group
GROUP_NAME = 'tgdemo-rg'

# Network
VNET_NAME = 'azure-sample-vnet'
SUBNET_NAME = 'azure-sample-subnet'

# VM
OS_DISK_NAME = 'azure-sample-osdisk'
STORAGE_ACCOUNT_NAME = haikunator.haikunate(delimiter='')

IP_CONFIG_NAME = 'azure-sample-ip-config'
NIC_NAME = 'azure-sample-nic'
USERNAME = 'userlogin'
PASSWORD = 'Pa$$w0rd91'
VM_NAME = 'VmName'

VM_REFERENCE = {
    'linux': {
        'publisher': 'Canonical',
        'offer': 'UbuntuServer',
        'sku': '16.04-LTS',
        'version': 'latest'
    },
    'windows': {
        'publisher': 'MicrosoftWindowsServerEssentials',
        'offer': 'WindowsServerEssentials',
        'sku': 'WindowsServerEssentials',
        'version': 'latest'
    }
}

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)

# Azure functions
def get_credentials():
    subscription_id = 'sub_id'
    credentials = ServicePrincipalCredentials(
        client_id= 'client_id',
        secret= 'secret',
        tenant= 'tenant'
    )
    return credentials, subscription_id


# Telegram procedures
def start(bot, update):
    """Send a message when the command /start is issued."""
    update.message.reply_text('Hi, my name is the AzureGeekSpeekBot! \nWelcome to this BrainSync Session!! \nFor help do /help in this chat')

def help(bot, update):
    """Send a message when the command /help is issued."""
    update.message.reply_text('/help This help overview \n/connect Connect to the Azure Subscription\n')

def echo(bot, update):
    """Echo the user message."""
    update.message.reply_text(update.message.text)

def error(bot, update, error):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, error)

def connect(bot, update):
    """Connect to Azure Subscription"""
    global azure_logged_on
    global resource_client
    global compute_client
    global network_client
    credentials, subscription_id = get_credentials()
    resource_client = ResourceManagementClient(credentials, subscription_id)
    compute_client = ComputeManagementClient(credentials, subscription_id)
    network_client = NetworkManagementClient(credentials, subscription_id)
    update.message.reply_text("Connected to Azure Subscription")
    azure_logged_on = True

def rg_list(bot, update):
    global azure_logged_on
    global resource_client
    global compute_client
    global network_client    
    rglist = ""
    resource_group_params = {'location': 'westus'}
    if not azure_logged_on:
        update.message.reply_text("Not yet connected to Azure, please execute /connect first!")
    else:        
        for rg in resource_client.resource_groups.list():
            rglist += rg.name + "\n"
        if rglist == "":
            update.message.reply_text("No Resource Groups defined in Azure Subscription")
        else:
            update.message.reply_text("Resource Groups in Azure Subscription: \n"+rglist)
    return

def vm_list(bot, update):
    global azure_logged_on
    global resource_client
    global compute_client
    global network_client    
    vmlist = ""
    if not azure_logged_on:
        update.message.reply_text("Not yet connected to Azure, please execute /connect first!")
    else:        
        # List VMs in subscription
        for vm in compute_client.virtual_machines.list_all():
            vmlist += ("\tVM: {}".format(vm.name))
        if vmlist == "":
            update.message.reply_text("No Virtual Machines defined in Azure Subscription")
        else:
            update.message.reply_text("Virtual Machines in Azure Subscription: \n"+vmlist)
    return   

def rg_create(bot,update,args):
    global azure_logged_on
    global resource_client
    global compute_client
    global network_client 
    resource_group_params = {'location': 'westus'}
    try: 
        if args[0] == "":
            update.message.reply_text("No name provided for resource group! Usage: /rg_create <GROUPNAME>")
    except IndexError:
        update.message.reply_text("No name provided for resource group! Usage: /rg_create <GROUPNAME>")
    else:
        if not azure_logged_on:
            update.message.reply_text("Not yet connected to Azure, please execute /connect first!")
        else:
            resource_client.resource_groups.create_or_update(args[0], {'location': LOCATION})
            update.message.reply_text("ResourceGroup "+args[0]+" is created!")
def rg_delete(bot, update, args):
    global azure_logged_on
    global resource_client
    global compute_client
    global network_client 
    try: 
        if args[0] == "":
            update.message.reply_text("No name provided for resource group! Usage: /rg_delete <GROUPNAME>")
    except IndexError:
        update.message.reply_text("No name provided for resource group! Usage: /create_rg <GROUPNAME>")
    else:
        if not azure_logged_on:
            update.message.reply_text("Not yet connected to Azure, please execute /connect first!")
        else:
            delete_async_operation = resource_client.resource_groups.delete(args[0])
            update.message.reply_text("Delete of Resource Group "+args[0]+" is requested. One moment please")
            delete_async_operation.wait()
            update.message.reply_text("Deletion complete!")


def main():
    """Start the bot."""
    # Create the EventHandler and pass it your bot's token.
    updater = Updater("TOKEN")

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # on different commands - answer in Telegram

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("connect", connect))
    dp.add_handler(CommandHandler("rg_list", rg_list))
    dp.add_handler(CommandHandler("vm_list", vm_list))
    dp.add_handler(CommandHandler("rg_create", rg_create, pass_args=True))
    dp.add_handler(CommandHandler("rg_delete", rg_delete, pass_args=True))
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

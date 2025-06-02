#!/usr/bin/python3
import os
import mail
from time import gmtime, strftime
from email.mime.text import MIMEText
import config

receivedMsg = []
sentMsg = []
msgList = []
alreadySentMsgList = []

print(f"KILL PID: {os.getpid()}")

def mmcliMsgScan():
    modemManagerSMSList = os.popen('mmcli -m 0 --messaging-list-sms') 
    for line in modemManagerSMSList.readlines():
        if line.endswith(' (received)\n'):
            msgNum = msgNumGet(line)
            receivedMsg.append(msgNum)
            msgList.append(msgNum)
        elif line.endswith(' (sent)\n'):
            msgNum = msgNumGet(line)
            sentMsg.append(msgNum)
            msgList.append(msgNum)
        else:
            msgNum = msgNumGet(line)
            receivedMsg.append(msgNum)
            msgList.append(msgNum)

def msgNumGet(line):
    return int(line.rstrip(' (sent)\n').rstrip(' (received)\n').rstrip(' (unknown)\n')[::-1].split('/',1)[0])

def determineMsgDirection(num):
    if num in sentMsg:
        return "sent"
    elif num in receivedMsg:
        return "received"
    else:
        return "received"

def msgFilter():
    for msgNum in msgList:
        condition = True
        if msgNum in alreadySentMsgList:
            condition = False
        if condition == True:
            msgDirection = determineMsgDirection(msgNum)
            msg = parseMsg(msgNum, msgDirection)
            senderNumber = parseNumber(msgNum)
            messagePARSED = formatMsg(msg, senderNumber, msgDirection)
            mail.sendEmail(messagePARSED)
            alreadySentMsgList.append(msgNum)

def parseMsg(num, msgDirection):
    msgCmdPipe = os.popen(f"mmcli -s {num}")
    msgSplit = msgCmdPipe.split("-----------------------")
    msgContent = msgSplit[2]
    msgTime = strftime("%Y-%m-%d %H:%M:%S", gmtime())
    return f"""\
{msgContent} \n \n Timestamp: {msgTime} \n This SMS message was {msgDirection} from {config.PHNUM}{config.ADDITIONALMSG}. \n"""

def parseNumber(num):
    msgCmdPipe = os.popen(f"mmcli -s {num}")
    msgSplit = msgCmdPipe.splitlines()
    msgNumber = "+" + msgSplit[3].split('+')
    return str(msgNumber)

def formatMsg(msg, senderNumber, msgDirection):
    message = MIMEText(msg, "plain")
    message['Subject'] = f"Text {msgDirection} from {senderNumber}"
    message["From"] = config.USERNAME
    message['To'] = config.RECIPIENT
    return message
import requests
import aiohttp
import asyncio
import random
import time
from config import Codes, SessionTickets, PaidWebhookURLs, EarlyWebhookURLs, FreeWebhookURLs, StartWebhookURL, AccountWebhookURLs, ConcatWebhookURLs, NotificationKey, SteamTickets
from discord_webhook import DiscordWebhook
from datetime import datetime

# Role pings
Sweater_Ping = "1302831243116806224"
PaidTracker_Ping = "1303536139952717895"
FreeTracker_Ping = "1303536568258002998"
ConcatTracker_Ping = "1303536155496550521"

# Data
Code_Num = len(Codes)
SessionTicketNum = len(SessionTickets)
DeadTickets = []

RareCosmetics = [
    {
        "CosmeticName": "🪃 Stick 🪃",
        "CosmeticId": "LBAAK.",
    },
    {
        "CosmeticName": "Finger Painter",
        "CosmeticId": "LBADE.",
    },
    {
        "CosmeticName": "Illustrator Badge",
        "CosmeticId": "LBAGS.",
    },
    {
        "CosmeticName": "Admin Badge",
        "CosmeticId": "LBAAD.",
    },
    {
        "CosmeticName": "Unreleased Sweater",
        "CosmeticId": "LBACP.",
    },
]

BasicCosmetics = [
    {
        "CosmeticName": "Monkey Plush",
        "CosmeticId": "LBADB.",
    },
    {
        "CosmeticName": "1️⃣ GT1 Badge 1️⃣",
        "CosmeticId": "LBAAZ.",
    },
    {
        "CosmeticName": "💸Early accses💸",
        "CosmeticId": "LBAAE.",
    },
]

Concats = [
    # Owners
    {
        "Person": "scarlett",
        "ConcatSTR": "LFADA.LFAEF.LFACL.LBAGN.LBAGO.LBAGP.LBAGE.LHACR.LMABV.LBAFN.LMAIL.LBAAQ.LBAEA.LFACY.LBADB.LHAAD.LFABI.LHABZ.LFABB.LBACT.LMACT.LBACQ.LBAAR.LSAAE.LHABD.LFAAX.LBAAS.LFABX.LMACD.LHABC.LSAAP2.LHADA.LMABZ.LBACF.LMABO.LBAAP.LFAAQ.LFAAU.LHAAY.LBAAO.LSAAD.LHAAV.LBAAL.LFAAR.LSAAA.LSAAC.LFAAT.LBAAN.LHAAX.LHAAT.LMABA.LMAAT.LMAAZ.LBABR.LMAAU.LHAAQ.LMAAO.Early Access Supporter PackLMAAN.LMAAM.LFABN.LBAAC.LMAAL.LFAAI.LFAAF.LHAAP.LFAAL.LHAAC.LBAAB.",
    },
    {
        "Person": "misu",
        "ConcatSTR": "LBAHF.LFACU.LBAGY.LMAJY.LBAGN.LBAGO.LBAGP.LBAEO.LHAAZ.LFADF.LMAGM.LBAEB.LBAEA.LBACD.LBADC.LHABU.LBABL.LBACX.LSAAV.LFACG.LHADR.LMADD.LBACP.LFAAV.LBACT.LHABR.LBACQ.LMACT.LHAAS.LFAAY.LSAAE.LHABD.LFAAX.LBAAR.LMACD.LFABX.LHACY.LMABT.LFAAW.LFABW.LMABO.LFAAP.LMAAZ.LHAAC.LHAAE.LBAAB.",
    },
]

def Log(logtype, info):
    raw_logtime = datetime.now()
    formatted_logtime = raw_logtime.strftime("%d %H:%M:%S")
    
    error_log = open("error_logs.txt", "a", encoding="utf-8")
    found_log = open("found_logs.txt", "a", encoding="utf-8")
    other_log = open("other_logs.txt", "a", encoding="utf-8")
    
    if logtype == "ERROR":
        Service = info[0]
        Error = str(info[1])

        error_log.write(f"{formatted_logtime} - ERROR - Service - {Service} - ErrorMessage - {Error}" + "\\n")
        error_log.close()
    elif logtype == "FOUND":
        Cosmetic = info[0]
        Code = info[1]
        Region = info[2]
        Concat = info[3]

        found_log.write(f"{formatted_logtime} - FOUND - {Cosmetic} - IN ROOM - {Code, Region} - CONCAT IS - {Concat}" + "\\n")
        found_log.close()
        
    else:
        OtherInfo = info[0]
        other_log.write(f"{formatted_logtime} - OTHER - {OtherInfo}" + "\\n")
        other_log.close()

# The Function That Sends All Webhooks
def SendWebhook(content, embeds, url):
    data = {"content": content, "embeds": embeds}
    headers = {"Content-Type": "application/json"}

    try:
        response = requests.post(url, json=data, headers=headers)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        Log("ERROR", ["DISCORD", data])

    return data

# Sends Webhook to A Channel When It Finds A Specific Person
def ConcatWebhook(Person, Region, Code, Count, Actor, BoardPos):
    ConcatWebhookURL = random.choice(ConcatWebhookURLs)
    content = f"<@&{ConcatTracker_Ping}>"
    embeds = [{
        "title": f"🙏 Tracker Concat ✝️",
        "description": ".gg/seroxen - Only one way > god",
        "color": 0xFFD700,
        "fields": [
           {"name": "**✝️ Person ✝️**", "value": f"```{Person}```", "inline": False},
           {"name": "**📖 Code 📖**", "value": f"```{Code}```", "inline": True},
           {"name": "**✝️ Region ✝️**", "value": f"```{Region}```", "inline": True},
           {"name": "**👥 Players 👥**", "value": f"```{Count}```", "inline": False},
           {"name": "**✝️ Leaderboard Position ✝️**", "value": f"```{BoardPos}```", "inline": True},
           {"name": "**🎭 Actor Number 🎭**", "value": f"```{Actor}```", "inline": True},
           {"name": "**📟 Tracker Status**", "value": random.choice(["```🟢 Active```"]), "inline": True},
       ],
       "footer": {
           "text": "• ✝️ Remember, 'I can do all things through Christ who strengthens me. — Philippians 4:13 ✝️",
       },
       "timestamp": datetime.utcnow().isoformat(),
    }]
    SendWebhook(content, embeds, ConcatWebhookURL)
    
    print(f"Found: {Person} in code -> {Code}{Region} with -> {Count} players")

# Sends Webhook to A Channel For Rarer Cosmetics
def MainWebhook(Cosmetic, Region, Code, Count, Actor, Concat, BoardPos, NormalCosmetics, Role):
    PaidWebhookURL = random.choice(PaidWebhookURLs)
    ConcatLength = len(Concat)

    # Stops Webhook From Including The Value 'Concat', When Its Value Exceeds 1500 Characters
    if ConcatLength > 1500:
        ConcatValue = "Concat Is Too Long..."
    else:
        ConcatValue = Concat

    # Checks To See How Many '.' are in the Concat string
    NormalCosmetics += Concat.count(".")
    
    content = f"<@&{Role}>"
    embeds [
        "title": "Tracker",
        "description": "",
        "color": 0xFFD700,
        "fields": [
            {"name": "**✝️Found✝️**", "value": f"```{Cosmetic}```", "inline": False},
            {"name": "**😼Code😼**`", "value": f"```{Code}```", "inline": True},
            {"name": "**✝️Region✝️**", "value": f"```{Region}```", "inline": True},
            {"name": "**🔥Normal Cosmetics🔥**`", "value": f"```{NormalCosmetics}```", "inline": False},
            {"name": "**✝️Actor Number✝️**", "value": f"```{Actor}```", "inline": True},
            {"name": "**🔥Concat 🔥**", "value": f"```{ConcatValue}```", "inline": False},
            {"name": "**🌐 Server Status🌐**", "value": random.choice(["```🟡 Maintenance```,"]), "inline": True},
        ],
    "footer": {"text": "• [Discord](https://discord.gg/yxTqAuDatK) "},
    "timestamp": datetime.utcnow().isoformat(),
    "thumbnail": {"url": "https://media.discordapp.net/attachments/1283566171681067109/130354785741"
    }]

    # Send the webhook and log the result
    Webhook = SendWebhook(content, embeds, PaidWebhookURL)
    Log("FOUND", [Cosmetic, Code, Region, Concat])
    
    print(f"Found: {Cosmetic} in code -> {Code} {Region} with -> {Count} players")
    return Webhook

# Sends Webhook to A Channel For Basic Cosmetics
def BasicWebhook(Cosmetic, Region, Code, Count, Actor, Concat, BoardPos, NormalCosmetics):
    FreeWebhookURL = random.choice(FreeWebhookURLs)
    ConcatLength = len(Concat)

    # Stops Webhook From Including The Value 'Concat' when its value exceeds 1500 characters
    if ConcatLength > 1500:
        ConcatValue = "Concat Is Too Long..."
    else:
        ConcatValue = Concat

    # Count the number of '.' in the Concat string
    NormalCosmetics += Concat.count(".")

    content = f"<@&{FreeTracker_Ping}>"
    embeds = [{
        "title": "Tracker Basic",
        "description": "",
        "color": 0x077eed,
        "fields": [
            {"name": "**✝️Item✝️**", "value": f"```{Cosmetic}```", "inline": False},
            {"name": "**🔥Code🔥**", "value": f"```{Code}```", "inline": True},
            {"name": "**😼Region😼**", "value": f"```{Region}```", "inline": True},
            {"name": "**✝️Player Count✝️**", "value": f"```{Count}```", "inline": False},
            {"name": "**✝️Normal Cosmetics✝️**", "value": f"```{NormalCosmetics}```", "inline": False},
            {"name": "**🔥Actor Number🔥**", "value": f"```{Actor}```", "inline": True},
            {"name": "```🌐 Server Status🌐```", "value": random.choice(["```🟡 Maintenance```,"]), "inline": True},
        ],
    "footer": {"text": "• [Discord](https://discord.gg/yxTqAuDatK)"},
    "timestamp": datetime.utcnow().isoformat(),  # Adds current UTC time in ISO format
    "thumbnail": {"url": "https://media.discordapp.net/attachments/1283566171681067109/1303547857411899472/caption.gif?ex=672e214b&is=672ccfcb&hm=d9d8cd2083449459eaaa0803f20acd9dd40baa24da07a302b235660ea99a1781&=&width=621&height=559.png"}  # Adds an image on the left side
    }]

    # Send the webhook and log the result
    Webhook = SendWebhook(content, embeds, FreeWebhookURL)

    # Log the found information
    print(f"Found: {Cosmetic} in code -> {Code} {Region} with -> {Count} players")
    return Webhook

# Sends Webhook To A Channel On Start That Contains The Accounts Information
def StartAccountInfo():
    for SessionTicket in SessionTickets:
        AccountWebhookURL = random.choice(AccountWebhookURLs)
        
        headers = {"X-Authorization": SessionTicket}
        json = {'InfoRequestParameters': {'GetUserAccountInfo': True}}
        request = requests.post(url=f"https://63fdd.playfabapi.com/Client/GetPlayerCombinedInfo",json=json,headers=headers)
        
        requestjson = request.json()
        status_code = requestjson['code']
        if status_code == 200:
            Last_Login = requestjson['data']['InfoResultPayload']['AccountInfo']['TitleInfo']['LastLogin']
            Is_Banned = requestjson['data']['InfoResultPayload']['AccountInfo']['TitleInfo']['isBanned']
            Steam_Id = requestjson['data']['InfoResultPayload']['AccountInfo']['SteamInfo']['SteamId']
            Steam_Name = requestjson['data']['InfoResultPayload']['AccountInfo']['SteamInfo']['SteamName']
        else:
            Last_Login = "N/A"
            Is_Banned = "N/A"
            Steam_Id = "N/A"
            Steam_Name = "N/A"
     
        content = f"<@&1281445089284980797>"
        embeds = [{
        "title": f"Tracker Accounts 🌙",
        "description": "",
        "color": 0x00FF00,
        "fields": [ 
            {"name": "", "value": "", "inline": False},
            {"name": "📅 Event 📅", "value": "Tracker Has Started", "inline": False},  
            {"name": "🎟️ Session Ticket", "value": f"```{SessionTicket}```", "inline": False},    
            {"name": "🏷️ Steam Name🏷️", "value": f"```{Steam_Name}```", "inline": False},
            {"name": "🛑 Is Banned 🛑", "value": f"```{Is_Banned}```", "inline": False},
            {"name": "🕕 Last Login 🕕", "value": f"```{Last_Login}```", "inline": False},
        ],
        "footer": {"text": "tracker"}
    }]
        SendWebhook(content, embeds, AccountWebhookURL)
        
# Sends Webhook To A Channel On Start That Contains The Accounts Information
def DeadAccountInfo(SessionTicket):
    AccountWebhookURL = random.choice(AccountWebhookURLs)        
     
    content = f"<@&1281445089284980797>"
    embeds = [{
        "title": f"Tracker Accounts",
        "description": "",
        "color": 0xFF0000,
        "fields": [ 
            {"name": "", "value": "", "inline": False},
            {"name": "📅 Event 📅", "value": "An Account Has Died!", "inline": False},  
            {"name": "🎟️ Session Ticket", "value": f"```{SessionTicket}```", "inline": False},    
            {"name": "🏷️ Steam Name🏷️", "value": f"```N/A```", "inline": False},
            {"name": "🛑 Is Banned 🛑", "value": f"```N/A```", "inline": False},
            {"name": "🕕 Last Login 🕕", "value": f"```N/A```", "inline": False},
        ],
        "footer": {"text": "tracker"}
    }]
    SendWebhook(content, embeds, AccountWebhookURL)

# Sends Notification To The Devices That Have Been Added To The 'NotificationKey' Variable
def Notification():
        json = {
              'accountKey': NotificationKey,
              'title': 'tracker',
              'message': 'Update Session Tickets! tracker Has Run Out Of Tickets, Update Now To Continue Running.',
              'priority': 2,
              'link': 'youtube.com'
        }
        request = requests.post(url="https://alertzy.app/send",json=json)
        requestjson = request.json()

# Fetches The Information For Each Code
async def FetchCode(session, url, headers, json):
    async with session.post(url, json=json, headers=headers) as response:
        return await response.json(), response.status

# Process The Returned Information Given By 'FetchCode'
async def ProcessCode(session, Code, Region, Headers):
    if not SessionTickets:
        Notification()
        exit()
    # Define json
    headers = Headers
    groupid = Code + Region
    json = {"SharedGroupId": groupid}
    url = "https://63FDD.playfabapi.com/Client/GetSharedGroupData"
    try:
        requestjson, status_code = await FetchCode(session, url, headers, json)
        # If Post Request is Approved
        if status_code == 200:
            PlayerCount = len(requestjson['data']['Data'])
            response_data = requestjson['data']['Data']
            BoardPos = 0
            NormalCosmetics = 0
            # Checks Value For Each Account
            for Actor, Concat in response_data.items():
                
                BoardPos += 1
                items = str(Concat['Value'])
                
                for RareCosmetic in RareCosmetics: 
                    if RareCosmetic["CosmeticId"] in items:
                        Webhook = MainWebhook(RareCosmetic["CosmeticName"], Region, Code, PlayerCount, Actor, items, BoardPos, NormalCosmetics, PaidTracker_Ping)
                for BasicCosmetic in BasicCosmetics: 
                    if BasicCosmetic["CosmeticId"] in items:
                        Webhook = BasicWebhook(BasicCosmetic["CosmeticName"], Region, Code, PlayerCount, Actor, items, BoardPos, NormalCosmetics)
                for Concat in Concats: 
                    if Concat["ConcatSTR"] in items:
                        Webhook = ConcatWebhook(Concat["Person"], Region, Code, PlayerCount, Actor, BoardPos)

                if PlayerCount == 1:
                    BasicWebhook('👻 Alone Player 👻', Region, Code, PlayerCount, Actor, items, BoardPos, NormalCosmetics)
            else:
                print(f"Checked {Code} -> {Region} -> {status_code} | Empty")
        
        # Ratelimited
        elif status_code == 429:
            throttle_time = requestjson['retryAfterSeconds']
            await asyncio.sleep(throttle_time)  
        
        # Invalid Session Ticket
        elif status_code == 401:
            session_ticket = headers.get('X-Authorization')
            if not session_ticket in DeadTickets:
                SessionTickets.remove(session_ticket)
                DeadTickets.append(session_ticket)
                DeadAccountInfo(session_ticket)
                print(f"A Session Ticket Has Been Removed, Check The Logs On The Discord!!!")                  
            else:
                print(f"A Session Ticket Is Invalid, But Has Already Been Removed!!!")  
        
        # Banned Account
        elif status_code == 403:
            session_ticket = headers.get('X-Authorization')
            if not session_ticket in DeadTickets:
                SessionTickets.remove(session_ticket)
                DeadTickets.append(session_ticket)
                DeadAccountInfo(session_ticket)
                print(f"A Session Ticket Has Been Removed, Check The Logs On The Discord!!!")                  
            else:
                print(f"A Session Ticket Is Invalid, But Has Already Been Removed!!!")       

    # Error Proccesing Code
    except Exception as e:
        error = str(e)
        if "429 Client Error:" in error:
            Error = "Webhook Throttled"
            print(f"Error processing {Code} -> {Region}: {Error}")
        if "400 Client Error: Bad Request for url: " in error:
            Error = "Bad Request For Discord Webhook"
            json = Webhook
            Log("ERROR", ["DISCORD", json])
            print(f"Error processing {Code} -> {Region}: {Error}")
        else:
            Log("ERROR", ["CHECKINGCODE", error])
            print(f"Error processing {Code} -> {Region}: {e}")


# Allows Each Session Ticket To Have A Different Asynchronous Operation
async def ProcessTicket(session, SessionTicket):
    headers = {"X-Authorization": SessionTicket}
    tasks = []
    for Code in Codes:
        for Region in ['EU', 'USW', 'US']:
            tasks.append(ProcessCode(session, Code, Region, headers))
    await asyncio.gather(*tasks)

# Uses Asynchronous Operations To Speed Up Tracker
async def main():
    async with aiohttp.ClientSession() as session:
        while True:
            tasks = []
            for SessionTicket in SessionTickets:
                tasks.append(ProcessTicket(session, SessionTicket))
            await asyncio.gather(*tasks)

def Start():
    StartAccountInfo()
    
    content = " "
    embeds = [{
    "title": "Tracker",
    "description": "",
    "color": 0x808080,
    "fields": [
        {"name": "", "value": "", "inline": False},
        {"name": "🔢 Number Of Codes 🔢", "value": f"```{len(Codes)}```", "inline": False},
        {"name": "🔢 Number Of Session tickets 🔢", "value": f"```{len(SessionTickets)}```", "inline": False},
        {"name": "🧍‍♂️ Person Running 🧍‍♂️", "value": f"```PI-TRACKER```", "inline": False},
        {"name": "🧱 Build Number 🧱", "value": f"```V2.0```", "inline": False},
        ],
    }]
    
    print("✨ tracker Started... ✨")
    print("")
    print("Stats:")
    print(f"Codes: {Code_Num}")
    print(f"Session tickets: {SessionTicketNum}")
    print("")
    print(f"The script will until its ratelimited, then it will sleep for the exact throttle time.")
    print("")
    print("Starting in 3 seconds...")
    time.sleep(3)
    
    SendWebhook(content, embeds, StartWebhookURL)
    
    asyncio.run(main())

    if SteamTickets:
        for SteamTicket in SteamTickets:
            json = {"SteamTicket": SteamTicket, "CreateAccount": True, "TitleId": "63FDD"}
            request = requests.post(url="https://63FDD.playfabapi.com/Client/LoginWithSteam",json=json)
            
            request.raise_for_status()
            requestjson = request.json()
            
            if request.status_code == 200:
                SessionTicket = requestjson['data']['SessionTicket']
                SessionTickets.append(SessionTicket)
            else:
                pass
Start()
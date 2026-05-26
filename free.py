from flask import Flask, render_template_string, request, redirect, url_for, make_response
import datetime
import time
import json
import os
import random
import string
import urllib.request
import hashlib

app = Flask(__name__)

# Cross-platform persistent storage directory architecture path resolver
if os.name == 'nt':  # Local Windows PC text verification environment paths
    BASE_USER_DIR = os.path.join(
        os.path.expanduser("~"), "Desktop", "2g_storage")
else:  # Live production Linux container web server workspace nodes
    BASE_USER_DIR = "/tmp"

# Create structural database directory tree layout elements automatically if missing from disk
if not os.path.exists(BASE_USER_DIR):
    os.makedirs(BASE_USER_DIR, exist_ok=True)

KEYS_FILE = os.path.join(BASE_USER_DIR, "keys_db.json")
CHAT_LOG_FILE = os.path.join(BASE_USER_DIR, "chat_history.json")
SANCTIONS_FILE = os.path.join(BASE_USER_DIR, "sanctions_db.json")

# Core high-performance memory cache arrays
room_presence = {}
spam_tracker = {}
recent_sign_ins = []  # In-memory storage trace for administrative logging audit streams

# Permanent cloud replication bucket anchors targeting open-access key storage registries
CLOUD_KEYS_URL = "https://kvdb.io"


def generate_sha256_signature(input_string):
    """Produces unbreakable SHA-256 fingerprint identifiers for tracking device footprints."""
    return hashlib.sha256(input_string.encode('utf-8')).hexdigest()[:12]


def load_sanctions_db():
    """Loads internal rate-limiting penalty databases tracking blocks, suspensions, and hardware device bans."""
    if os.path.exists(SANCTIONS_FILE):
        try:
            with open(SANCTIONS_FILE, "r") as f:
                return json.load(f)
        except Exception:
            pass
    initial_db = {"blocked_creators": {},
                  "suspended_users": {}, "banned_hardware": []}
    with open(SANCTIONS_FILE, "w") as f:
        json.dump(initial_db, f, indent=4)
    return initial_db


def save_sanctions_db(data_dict):
    """Commits anti-fraud penalty tracking data straight to file disk layers instantly."""
    try:
        with open(SANCTIONS_FILE, "w") as f:
            json.dump(data_dict, f, indent=4)
    except Exception:
        pass


def is_spamming(user_agent):
    """Anti-Spam rate-limiting protection wall requiring a 2-second cooldown."""
    now = time.time()
    device_id = generate_sha256_signature(user_agent)
    if device_id in spam_tracker:
        if now - spam_tracker[device_id] < 2.0:
            spam_tracker[device_id] = now
            return True
    spam_tracker[device_id] = now
    return False


def save_keys_db(data_dict):
    """Backs up group key credentials to the cloud registry instantly."""
    try:
        with open(KEYS_FILE, 'w') as f:
            json.dump(data_dict, f, indent=4)
        req = urllib.request.Request(CLOUD_KEYS_URL, data=json.dumps(data_dict).encode('utf-8'),
                                     headers={'Content-Type': 'application/json'}, method='PUT')
        with urllib.request.urlopen(req) as r:
            pass
    except Exception:
        pass


def load_keys_db():
    """Self-healing decentralized key room database syncer."""
    if os.path.exists(KEYS_FILE):
        try:
            with open(KEYS_FILE, "r") as f:
                return json.load(f)
        except Exception:
            pass
    try:
        with urllib.request.urlopen(CLOUD_KEYS_URL) as r:
            cloud_data = json.loads(r.read().decode('utf-8'))
            with open(KEYS_FILE, 'w') as f:
                json.dump(cloud_data, f, indent=4)
            return cloud_data
    except Exception:
        if not os.path.exists(KEYS_FILE):
            with open(KEYS_FILE, 'w') as f:
                json.dump({}, f)
        return {}


def load_chat_history():
    """Loads past conversation lines from local text disk space."""
    if not os.path.exists(CHAT_LOG_FILE):
        initial_log = [{"user": "System", "phone": "000", "text": "Welcome to NIX CHATROOM.",
                        "time": "xx:xx", "is_system": True, "room_key": "GLOBAL"}]
        with open(CHAT_LOG_FILE, 'w') as f:
            json.dump(initial_log, f, indent=4)
        return initial_log
    try:
        with open(CHAT_LOG_FILE, "r") as f:
            return json.load(f)
    except Exception:
        return []


def append_to_chat_log(message_object):
    """Saves incoming messages onto local persistent disk and enforces a 20-message 2G memory limit."""
    global messages
    messages.append(message_object)

    room_groups = {}
    system_messages = []

    for m in messages:
        if m.get('is_system'):
            system_messages.append(m)
        else:
            rkey = m.get('room_key', 'GLOBAL')
            if rkey not in room_groups:
                room_groups[rkey] = []
            room_groups[rkey].append(m)

    optimized_messages = list(system_messages)
    for rkey, room_msgs in room_groups.items():
        if len(room_msgs) > 20:
            optimized_messages.extend(room_msgs[-20:])
        else:
            optimized_messages.extend(room_msgs)

    messages = optimized_messages

    try:
        with open(CHAT_LOG_FILE, "w") as f:
            json.dump(messages, f, indent=4)
    except Exception:
        pass


# Execute initial history database load sequences
messages = load_chat_history()


def encrypt_text(plaintext, key):
    """Lightweight ASCII math encryption algorithm tailored for 2G payload data."""
    if not key:
        return plaintext
    encrypted = []
    key_ints = [ord(c) for c in str(key)]
    for i, char in enumerate(plaintext):
        shift = key_ints[i % len(key_ints)]
        encrypted.append(chr(32 + (ord(char) - 32 + shift) % 95))
    return "".join(encrypted)


def decrypt_text(ciphertext, key):
    """Lightweight ASCII math decoding algorithm tailored for 2G payload data."""
    if not key:
        return ciphertext
    decrypted = []
    key_ints = [ord(c) for c in str(key)]
    for i, char in enumerate(ciphertext):
        shift = key_ints[i % len(key_ints)]
        decrypted.append(chr(32 + (ord(char) - 32 - shift) % 95))
    return "".join(decrypted)


# SCREEN ONE: User Sign-In (The Absolute Entrance Screen)
SIGNIN_TEMPLATE = """<!DOCTYPE html PUBLIC "-//WAPFORUM//DTD XHTML Mobile 1.0//EN" "http://wapforum.org">
<html xmlns="http://w3.org">
<head>
    <meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no" />
    <title>CHATROOM Sign In</title>
    <style type="text/css">
        body { background-color: #000; color: #FFF; font-family: monospace; font-size: 11px; margin: 5px; }
        .hdr { background-color: #FF0055; color: #000; font-weight: bold; text-align: center; padding: 2px; margin-bottom: 8px;}
        .form-sect { border: 1px dashed #333; padding: 5px; margin-bottom: 8px; background: #0A0A0A; }
        .lbl-title { color: #FFFF00; font-weight: bold; display: block; margin-bottom: 4px; border-bottom: 1px solid #222; padding-bottom: 2px;}
        .err { color: #FF0000; font-weight: bold; border: 1px dashed #FF0000; padding: 2px; margin-bottom: 5px; }
        .donation-msg { color: #FFFF00; font-size: 10px; font-weight: bold; text-align: center; margin: 8px 0; border: 1px dashed #FFFF00; padding: 4px; }
        .footer-info { border-top: 1px dashed #333; margin-top: 10px; padding-top: 5px; font-size: 9px; color: #AAA; text-align: center; }
        input[type="text"], input[type="tel"] { background: #000; color: #FFF; border: 1px solid #FF0055; font-size: 11px; width: 90%; padding: 2px; margin-bottom: 4px;}
        input[type="submit"] { background: #FF0055; color: #000; font-weight: bold; font-size: 11px; margin-top: 4px; border: none; padding: 2px 6px; width: 95%; }
    </style>
</head>
<body>
    <div class="hdr">CHATROOM SIGN-IN</div>

    {% if error_msg %}
    <div class="err">[!] {{ error_msg }}</div>
    {% endif %}

    <form action="/sign-in-action" method="post">
        <div class="form-sect">
            <span class="lbl-title">USER ACCOUNT IDENTIFICATION</span>
            Your Name/Handle:<br />
            <input type="text" name="username" maxlength="10" placeholder="e.g. Allan" required autocomplete="off" /><br />
            Your Phone Number:<br />
            <input type="tel" name="phone" maxlength="15" placeholder="e.g. 07..." required autocomplete="off" /><br />
            <input type="submit" value="REGISTER PROFILE IDENTITY" />
        </div>
    </form>

    <div class="donation-msg">
        see our terms of use at termsofnix.netlify.app|contact support @ 256 743398481
    </div>

    <div class="footer-info">
        Be aware of constant updates to improve security and speed.<br />
        With AEGIX Sentinel security. version 0.7<br />
        Nix OS Framework v0.1 | Suite v1.0
    </div>
</body>
</html>"""

# SCREEN TWO: Multi-Room Switching Directory with Dynamic Unread Badges
DIRECTORY_TEMPLATE = """<!DOCTYPE html PUBLIC "-//WAPFORUM//DTD XHTML Mobile 1.0//EN" "http://wapforum.org">
<html xmlns="http://w3.org">
<head>
    <meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no" />
    <title>NIX Directory</title>
    <style type="text/css">
        body { background-color: #000; color: #FFF; font-family: monospace; font-size: 11px; margin: 5px; }
        .hdr { background-color: #FF0055; color: #000; font-weight: bold; text-align: center; padding: 2px; margin-bottom: 8px;}
        .form-sect { border: 1px dashed #333; padding: 5px; margin-bottom: 8px; background: #0A0A0A; }
        .lbl-title { color: #FFFF00; font-weight: bold; display: block; margin-bottom: 4px; border-bottom: 1px solid #222; padding-bottom: 2px;}
        .room-link { display: block; color: #00FF00; font-weight: bold; text-decoration: underline; padding: 4px 2px; border-bottom: 1px dashed #222; }
        .badge-new { color: #FF0055; font-weight: bold; background-color: #1a0009; padding: 0px 2px; border: 1px solid #FF0055; font-size: 9px; }
        .badge-ok { color: #00FF00; font-size: 9px; }
        .err { color: #FF0000; font-weight: bold; border: 1px dashed #FF0000; padding: 2px; margin-bottom: 5px; }
        .donation-msg { color: #FFFF00; font-size: 10px; font-weight: bold; text-align: center; margin: 8px 0; border: 1px dashed #FFFF00; padding: 4px; }
        .nav-btn { display: inline-block; background: #00FF00; color: #000; padding: 2px 6px; font-weight: bold; text-decoration: none; margin-bottom: 4px; font-size: 10px; }
        input[type="text"], input[type="tel"], select { background: #000; color: #FFF; border: 1px solid #FF0055; font-size: 11px; width: 90%; padding: 2px; margin-bottom: 4px;}
        input[type="submit"] { background: #FF0055; color: #000; font-weight: bold; font-size: 11px; margin-top: 4px; border: none; padding: 2px 6px; }
    </style>
</head>
<body>
    <div class="hdr">CHATROOMS</div>

    {% if error_msg %}
    <div class="err">[!] {{ error_msg }}</div>
    {% endif %}

    <div style="margin-bottom: 6px;">
        <a href="/" class="nav-btn">[Update Directory Feed]</a>
    </div>

    <div style="font-size:10px; color:#888; margin-bottom:6px;">Logged in as: <strong>{{ current_user }}</strong></div>

    <div class="form-sect">
        <span class="lbl-title">SELECT AVAILABLE CHATROOMS</span>
        {% if available_rooms %}
            {% for rkey, rdata in available_rooms.items() %}
                <a href="/join-room-action/{{ rkey }}" class="room-link"> -->{{ rdata.admin_name }}'s room
                    {% if rkey in status_map %}
                        {% if status_map[rkey] == 'APPROVED' %}
                            <span class="badge-ok">[Verified]</span>
                            {% if unread_map and unread_map[rkey] and unread_map[rkey] > 0 %}
                                <span class="badge-new">({{ unread_map[rkey] }} New)</span>
                            {% endif %}
                        {% elif status_map[rkey] == 'PENDING' %}
                            <span style="color:#FFFF00; font-size:9px;">[Pending Approval]</span>
                        {% endif %}
                    {% else %}
                        <span style="color:#888; font-size:9px;">[Click to Request Entry]</span>
                    {% endif %}
                </a>
            {% endfor %}
        {% else %}
            <div style="color: #666; font-style: italic; padding: 4px 0;">No active rooms found. Create one down below!</div>
        {% endif %}
    </div>

    <div class="form-sect">
        <span class="lbl-title">OR CREATE A NEW CHATROOM</span>
        <form action="/create-room-action" method="post">
            Desired Key / Numerical ID:<br />
            <input type="tel" name="secret_key" maxlength="10" placeholder="e.g. 1234" required autocomplete="off" /><br />
            Select Room Allocation Type:<br />
            <select name="room_type">
                <option value="pair">Pair Room</option>
                <option value="group">Group Room </option>
            </select><br />
            <input type="submit" value="INITIALIZE ROOM" />
        </form>
    </div>

    <div class="donation-msg">
        Messages are S2R encrypted
    </div>
</body>
</html>"""

# SCREEN THREE: Privacy Gate Options Interface Screen Layout Block
APPROVAL_PENDING_TEMPLATE = """<!DOCTYPE html PUBLIC "-//WAPFORUM//DTD XHTML Mobile 1.0//EN" "http://wapforum.org">
<html xmlns="http://w3.org">
<head>
    <meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no" />
    <title>Approval Pending</title>
    <style type="text/css">
        body { background-color: #000; color: #FFF; font-family: monospace; font-size: 11px; margin: 5px; text-align: center; }
        .hdr { background-color: #FFFF00; color: #000; font-weight: bold; padding: 2px; margin-bottom: 12px; }
        .box { border: 1px dashed #FF0055; padding: 8px; background: #111; margin-bottom: 12px; line-height: 14px; text-align: left; }
        .donation-msg { color: #FFFF00; font-size: 10px; font-weight: bold; text-align: center; margin: 8px 0; border: 1px dashed #FFFF00; padding: 4px; }
        .btn { display: block; background: #00FF00; color: #000; font-weight: bold; border: none; padding: 5px; text-decoration: none; font-size: 11px; margin-bottom: 6px; width: 90%; margin-left: auto; margin-right: auto; text-align: center;}
        .btn-back { background: #FF0055; color: #000; }
    </style>
</head>
<body>
    <div class="hdr">TUNNEL BLOCK</div>
    <div class="box">
        Your access request status for this room is currently logged as
        <span style="color:#FFFF00;font-weight:bold;">[PENDING APPROVAL]</span>.<br /><br />
        The room owner must grant entry parameters before your connection link can decode message data payloads.
    </div>
    <a href="/" class="btn">[Reload Status]</a>
    <a href="/clear-room-cookie" class="btn btn-back">[Go Back to Directory]</a>

    <div class="donation-msg">
        see why at termsofnix.netlify.app
    </div>
</body>
</html>"""

# SCREEN THREE-B: FIXED SELF-HEALING OPTION TEMPLATE
# Prevents blank screen crashes entirely by offering an clear, direct data-wiping redirect checkout link.
DELETED_ROOM_TEMPLATE = """<!DOCTYPE html PUBLIC "-//WAPFORUM//DTD XHTML Mobile 1.0//EN" "http://wapforum.org">
<html xmlns="http://w3.org">
<head>
    <meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no" />
    <title>Room Closed</title>
    <style type="text/css">
body { background-color: #000000; color: #FFF; font-family: monospace; font-size: 11px;
margin: 5px; text-align: center; }
.hdr { background-color: #FF0055; color: #000000; font-weight: bold; padding: 2px;
margin-bottom: 12px; }
.notice-box { border: 1px dashed #FF0055; padding: 10px; background: #0F0205;
margin-bottom: 12px; line-height: 14px; text-align: left; color: #FFAAAA; }
.nav-lnk { display: block; background: #00FF00; color: #000000; font-weight: bold;
border: none; padding: 6px; text-decoration: none; font-size: 11px; width: 90%; margin: 0
auto; text-align: center; border-radius: 2px; box-shadow: 0 0 5px #00FF00; }
.donation-msg { color: #FFFF00; font-size: 10px; font-weight: bold; text-align: center;
margin: 8px 0; border: 1px dashed #FFFF00; padding: 4px; }
 [ROOM UNAVAILABLE]
This specific chatroom has been completely closed, purged, or deleted from the server matrix vault registries.
You have been disconnected from the session tunnel pipeline.
[ CLICK HERE TO CREATE A NEW ROOM]
see why at termsofnix.netlify.app
"""
# SCREEN FOUR: Secure Main Room Terminal Interface (Static Core Navigation Architecture)
CHAT_TEMPLATE = """<!DOCTYPE html PUBLIC "-//WAPFORUM//DTD XHTML Mobile 1.0//EN" "http://wapforum.org">
<html xmlns="http://w3.org">
<head>
    <meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no" />
    <title>NIX Chatroom</title>
    <style type="text/css">
        body { background-color: #000000; color: #FFFFFF; font-family: monospace; font-size: 11px; margin: 3px; }
        .hdr { background-color: #FF0055; color: #000000; font-weight: bold; text-align: center; padding: 2px; }
        .status-box { background-color: #111; border: 1px solid #FF0055; padding: 3px; font-size: 10px; margin-bottom: 4px; color: #FFFF00; text-align: center; }
        .admin-box { background-color: #0c0800; border: 1px solid #FFFF00; padding: 4px; font-size: 10px; margin-bottom: 5px; color: #FFF; line-height: 14px; }
        .msg-box { border-bottom: 1px dashed #111; padding: 3px 0px; line-height: 13px; word-wrap: break-word; overflow-wrap: break-word; }
        .usr { color: #00FF00; font-weight: bold; }
        .me { color: #FFFF00; font-weight: bold; }
        .phn { color: #00FFFF; font-size: 10px; }
        .tm { color: #666666; font-size: 9px; }
        .alert-text { color: #FF0055; font-weight: bold; font-style: italic; background-color: #0c0004; padding: 1px; }
        .form-sect { background-color: #111; padding: 4px; border: 1px solid #222; margin-top: 5px; }
        .nav-btn { display: inline-block; background: #00FF00; color: #000; padding: 2px 6px; font-weight: bold; text-decoration: none; margin-bottom: 4px; font-size: 10px; margin-right: 4px; }
        .nav-back { background: #FF0055; }
        .donation-msg { color: #FFFF00; font-size: 10px; font-weight: bold; text-align: center; margin: 6px 0; border: 1px dashed #FFFF00; padding: 4px; }
        input[type="text"] { background: #000; color: #FFF; border: 1px solid #555; font-size: 11px; width: 90%; padding: 2px; }
        input[type="submit"] { background: #FF0055; color: #000; font-weight: bold; font-size: 11px; margin-top: 4px; border: none; padding: 2px 6px; }
        .ftr { text-align: center; font-size: 9px; color: #666; margin-top: 6px; border-top: 1px dashed #333; padding-top: 4px; }
    </style>
</head>
<body>

    <div class="hdr">
        CHATROOM
    </div>

    <div class="status-box">
        <strong>[ROOM CODE KEY]</strong> {{ current_room_key }}
    </div>

    <!-- ACTION CONTROLS LINK SYSTEM -->
    <div style="margin-bottom: 6px; margin-top: 4px;">
        <a href="/" class="nav-btn">[1. Check New Messages / Requests]</a>
        <a href="/clear-room-cookie" class="nav-btn nav-back">[2. Exit to Rooms Menu]</a>
    </div>

    <!-- ROOM OWNER APPROVAL BLOCK UTILITY BLOCK -->
    {% if is_room_admin and pending_applicants %}
    <div class="admin-box">
        <strong style="color:#FFFF00;">[ROOM ADMIN: Pending Entry Requests]</strong><br />
        {% for applicant in pending_applicants %}
            • Phone: {{ applicant }}
            <a href="/room-admin-action/allow/{{ applicant }}" style="color:#00FF00; font-weight:bold; text-decoration:underline;">[Allow]</a>
            <a href="/room-admin-action/deny/{{ applicant }}" style="color:#FF0000; font-weight:bold; text-decoration:underline;">[Block]</a><br />
        {% endfor %}
    </div>
    {% endif %}

    <!-- STATIC MESSAGE DECK VIEWPORT CONTEXT LOOP -->
    <div style="background:#050505; border:1px solid #222; padding:3px; min-height:100px;">
        {% for m in decrypted_messages %}
        <div class="msg-box">
            {% if m.is_alert or m.is_system %}
                <span class="tm">[{{ m.time }}]</span> <span class="alert-text">{{ m.text }}</span>
            {% else %}
                <span class="tm">[{{ m.time }}]</span>
                <span class="{% if m.phone == current_phone %}me{% else %}usr{% endif %}">{{ m.user }}</span>
                {% if m.phone != "000" %}<span class="phn">({{ m.phone }}):</span>{% else %}:{% endif %}
                {{ m.text }}
            {% endif %}
        </div>
        {% endfor %}
    </div>

    <!-- DATA SUBMISSION TRANSMISSION ENTRY BOX -->
    <div class="form-sect">
        <form action="/send" method="post">
            Enter message:<br />
            <input type="text" name="message" maxlength="50" autocomplete="off" required /><br />
            <input type="submit" value="[SEND]" />
        </form>
    </div>

    <div class="donation-msg">
        
    </div>
</body>
</html>"""


@app.route('/')
def index():
    user_agent = request.headers.get('User-Agent', 'Unknown-Device').strip()
    username = request.cookies.get('username')
    phone = request.cookies.get('phone')
    secret_key = request.cookies.get('secret_key')

    # DEVICE SECURITY PROTECTION LAYER: Cross-reference hardware fingerprints
    sanctions_db = load_sanctions_db()
    device_signature = generate_sha256_signature(user_agent)

    if device_signature in sanctions_db.get("banned_hardware", []):
        err_block = make_response(render_template_string(
            SIGNIN_TEMPLATE, error_msg="Security Violation: This hardware terminal fingerprint signature is permanently banned from accessing our platform network systems nodes."))
        err_block.headers['Content-Type'] = 'text/html; charset=utf-8'
        return err_block

    # STEP 1: INITIAL IDENTITY SIGN-IN WALL
    if not username or not phone:
        signin_resp = make_response(render_template_string(
            SIGNIN_TEMPLATE, error_msg=request.args.get('error')))
        signin_resp.headers['Content-Type'] = 'text/html; charset=utf-8'
        return signin_resp

    # DYNAMIC TIME-BASED COOLDOWN EVALUATOR FOR SUSPENDED PROFILES
    if phone in sanctions_db.get("suspended_users", {}):
        expiry_timestamp = sanctions_db["suspended_users"][phone]
        if time.time() < expiry_timestamp:
            remaining_hours = int((expiry_timestamp - time.time()) / 3600)
            remaining_minutes = int(
                ((expiry_timestamp - time.time()) % 3600) / 60)
            susp_resp = make_response(render_template_string(
                SIGNIN_TEMPLATE, error_msg=f"Access Suspended: Your profile handle is locked for a 1-week defensive cooling penalty window. Remaining lockout duration: {remaining_hours} hours, {remaining_minutes} minutes."))
            susp_resp.headers['Content-Type'] = 'text/html; charset=utf-8'
            return susp_resp
        else:
            sanctions_db["suspended_users"].pop(phone, None)
            if phone in sanctions_db.get("blocked_creators", {}):
                sanctions_db["blocked_creators"][phone] = 0
            save_sanctions_db(sanctions_db)

    keys_db = load_keys_db()

    # STEP 2: REJECT PURGED ACCESSED ROOM BOUNDS
    if secret_key and secret_key not in keys_db:
        eviction_resp = make_response(
            render_template_string(DELETED_ROOM_TEMPLATE))
        eviction_resp.headers['Content-Type'] = 'text/html; charset=utf-8'
        return eviction_resp

    # STEP 3: DYNAMIC RE-AUTHENTICATED DIRECTORY CHANNELS DECK
    if not secret_key:
        status_map = {}
        unread_map = {}

        for rkey, rdata in keys_db.items():
            allowed_list = rdata.get("allowed_users", [])
            pending_list = rdata.get("pending_users", [])
            admin_phone = rdata.get("admin")

            if phone == admin_phone or phone in allowed_list:
                status_map[rkey] = 'APPROVED'

                room_msgs = [m for m in messages if not m.get(
                    'is_system') and m.get('room_key') == rkey]
                last_seen_cookie = request.cookies.get(f'last_seen_ts_{rkey}')

                if last_seen_cookie:
                    try:
                        cutoff_ts = float(last_seen_cookie)
                        unread_count = sum(1 for m in room_msgs if m.get(
                            'timestamp', 0) > cutoff_ts)
                    except ValueError:
                        unread_count = 0
                else:
                    unread_count = len(room_msgs)
                unread_map[rkey] = unread_count

            elif phone in pending_list:
                status_map[rkey] = 'PENDING'

        dir_resp = make_response(render_template_string(
            DIRECTORY_TEMPLATE, current_user=username, available_rooms=keys_db,
            status_map=status_map, unread_map=unread_map, error_msg=request.args.get(
                'error')
        ))
        dir_resp.headers['Content-Type'] = 'text/html; charset=utf-8'
        return dir_resp

    now_ts = time.time()

    # STEP 4: VERIFY ACCESSED ROOM CREATOR PRIVACY CHECKPOINTS
    if secret_key in keys_db:
        allowed_list = keys_db[secret_key].get("allowed_users", [])
        if phone != keys_db[secret_key].get("admin") and phone not in allowed_list:
            pending_resp = make_response(render_template_string(
                APPROVAL_PENDING_TEMPLATE, secret_key=secret_key))
            pending_resp.headers['Content-Type'] = 'text/html; charset=utf-8'
            return pending_resp

    # STEP 5: CREATOR UTILITY MARKERS
    is_room_admin = False
    pending_applicants = []
    if phone == keys_db[secret_key].get("admin"):
        is_room_admin = True
        pending_applicants = keys_db[secret_key].get("pending_users", [])

    # STEP 6: SYNC HANDSET TRACKING INFORMATION INTO MONITOR MEMORY PIPELINE
    if secret_key not in room_presence:
        room_presence[secret_key] = {}

    current_time_str = datetime.datetime.now().strftime("%H:%M")

    if phone not in room_presence[secret_key]:
        append_to_chat_log({
            "user": "SYSTEM_ALERT", "phone": "000",
            "text": f"--> {username} connected to room.",
            "time": current_time_str,
            "room_key": secret_key,
            "is_alert": True,
            "timestamp": now_ts
        })

    room_presence[secret_key][phone] = {
        "name": username,
        "last_seen": now_ts,
        "device": user_agent
    }

    for peer_phone, peer_data in list(room_presence[secret_key].items()):
        if peer_phone != phone:
            if now_ts - peer_data["last_seen"] > 60:
                append_to_chat_log({
                    "user": "SYSTEM_ALERT",
                    "phone": "000",
                    "text": f"<-- {peer_data['name']} went offline.",
                    "time": current_time_str,
                    "room_key": secret_key,
                    "is_alert": True
                })
                room_presence[secret_key].pop(peer_phone, None)

    # =======================================================================
    # OUTPUT CONTEXT ARRAY AND COMPUTE TS COOKIE VALUES FOR TRACKING DELTA TILES
    # =======================================================================
    decrypted_stream = []
    for m in messages:
        if m.get('is_system') or (m.get('room_key') == secret_key):
            if m.get('is_system') or m.get('is_alert'):
                decrypted_stream.append(m)
            else:
                decrypted_text = decrypt_text(m['text'], secret_key)
                decrypted_stream.append({
                    "user": m['user'],
                    "phone": m['phone'],
                    "text": decrypted_text,
                    "time": m['time']
                })

    response = make_response(render_template_string(
        CHAT_TEMPLATE,
        current_room_key=secret_key,
        current_phone=phone,
        is_room_admin=is_room_admin,
        pending_applicants=pending_applicants,
        decrypted_messages=decrypted_stream[-8:]
    ))

    response.headers['Content-Type'] = 'text/html; charset=utf-8'
    response.set_cookie(f'last_seen_ts_{secret_key}', str(
        now_ts), max_age=31536000, path='/')
    return response


@app.route('/sign-in-action', methods=['POST'])
def sign_in_action():
    user_agent = request.headers.get('User-Agent', 'Unknown-Device').strip()
    if is_spamming(user_agent):
        resp = make_response(redirect(
            url_for('index', error="Spam Detected: Please slow down! Wait 2 seconds.")))
        resp.headers['Content-Type'] = 'text/html; charset=utf-8'
        return resp

    username = request.form.get('username', 'User').strip()[:8]
    phone = request.form.get('phone', '').strip()[:15]

    if phone.startswith('+256'):
        phone = '0' + phone[4:]
    elif phone.startswith('256'):
        phone = '0' + phone[3:]

    if not username or not phone:
        resp = make_response(redirect(url_for(
            'index', error="Error: Both fields are required for sign-in identification.")))
        resp.headers['Content-Type'] = 'text/html; charset=utf-8'
        return resp

    # ANTI-FRAUD SECURITY LAYER: Check if this hardware device fingerprint is completely banned
    sanctions_db = load_sanctions_db()
    device_signature = generate_sha256_signature(user_agent)

    if device_signature in sanctions_db.get("banned_hardware", []):
        resp = make_response(redirect(url_for(
            'index', error="Hardware Banned: Access from this terminal device footprint is blocked.")))
        resp.headers['Content-Type'] = 'text/html; charset=utf-8'
        return resp

    # ADVANCED LOG MONITORING: Log this login event instantly into memory for your portal to audit
    current_time_str = datetime.datetime.now().strftime("%H:%M:%S")
    recent_sign_ins.insert(0, {
        "name": username,
        "phone": phone,
        "time": current_time_str,
        "device": user_agent
    })

    # Enforce memory buffer cap (Keep last 30 sign-ins to avoid memory bloating)
    if len(recent_sign_ins) > 30:
        recent_sign_ins.pop()

    response = make_response(redirect(url_for('index')))
    response.headers['Content-Type'] = 'text/html; charset=utf-8'
    response.set_cookie('username', username, max_age=31536000, path='/')
    response.set_cookie('phone', phone, max_age=31536000, path='/')
    return response


@app.route('/join-room-action/<secret_key>')
def join_room_action(secret_key):
    username = request.cookies.get('username')
    phone = request.cookies.get('phone')
    if not username or not phone:
        resp = make_response(redirect(url_for('index')))
        resp.headers['Content-Type'] = 'text/html; charset=utf-8'
        return resp

    secret_key = secret_key.strip()[:10]
    keys_db = load_keys_db()

    if secret_key in keys_db:
        room = keys_db[secret_key]
        room_type = room.get('room_type', 'group')
        admin_phone = room.get('admin')
        allowed_list = room.get('allowed_users', [])
        pending_list = room.get('pending_users', [])

        if phone == admin_phone or phone in allowed_list:
            response = make_response(redirect(url_for('index')))
            response.headers['Content-Type'] = 'text/html; charset=utf-8'
            response.set_cookie('secret_key', secret_key,
                                max_age=31536000, path='/')
            return response

        total_slots_occupied = len(allowed_list) + 1

        if phone not in pending_list:
            if room_type == 'pair' and total_slots_occupied >= 2:
                resp = make_response(redirect(url_for(
                    'index', error="Join Blocked: This private room is strictly capped at 2 people max!")))
                resp.headers['Content-Type'] = 'text/html; charset=utf-8'
                return resp

            if room_type == 'group' and total_slots_occupied >= 20:
                resp = make_response(redirect(url_for(
                    'index', error="Join Blocked: This room group is full! Strict cap of 20 users reached.")))
                resp.headers['Content-Type'] = 'text/html; charset=utf-8'
                return resp

            pending_list.append(phone)
            keys_db[secret_key]['pending_users'] = pending_list
            save_keys_db(keys_db)

    response = make_response(redirect(url_for('index')))
    response.headers['Content-Type'] = 'text/html; charset=utf-8'
    response.set_cookie('secret_key', secret_key, max_age=31536000, path='/')
    return response


@app.route('/create-room-action', methods=['POST'])
def create_room_action():
    user_agent = request.headers.get('User-Agent', 'Unknown-Device').strip()
    if is_spamming(user_agent):
        resp = make_response(
            redirect(url_for('index', error="Spam Detected: Slow down! Wait 2s.")))
        resp.headers['Content-Type'] = 'text/html; charset=utf-8'
        return resp

    username = request.cookies.get('username', 'User')
    phone = request.cookies.get('phone')
    secret_key = request.form.get('secret_key', '').strip()[:10]
    room_type = request.form.get('room_type', 'group').strip()

    if not phone or not secret_key:
        resp = make_response(redirect(url_for('index')))
        resp.headers['Content-Type'] = 'text/html; charset=utf-8'
        return resp

    sanctions_db = load_sanctions_db()
    device_signature = generate_sha256_signature(user_agent)

    # RE-VERIFY DEVICE TERMINAL IS NOT PERMANENTLY BANNED
    if device_signature in sanctions_db.get("banned_hardware", []):
        resp = make_response(redirect(url_for(
            'index', error="Security Block: This device terminal is permanently banned.")))
        resp.headers['Content-Type'] = 'text/html; charset=utf-8'
        return resp

    # =======================================================================
    # ADVANCED DEFENSIVE RATE-LIMITING ENGINE (ANTI-FRAUD QUOTA BLOCKER)
    # =======================================================================
    current_creation_count = sanctions_db.get(
        "blocked_creators", {}).get(phone, 0)

    # LEVEL 3: HARD PERMANENT BAN
    if current_creation_count >= 52:
        if device_signature not in sanctions_db["banned_hardware"]:
            sanctions_db["banned_hardware"].append(device_signature)
        sanctions_db["suspended_users"].pop(phone, None)
        save_sanctions_db(sanctions_db)
        resp = make_response(redirect(url_for(
            'index', error="Security Violation: Exploit flagged. This hardware terminal is permanently banned.")))
        resp.headers['Content-Type'] = 'text/html; charset=utf-8'
        return resp

    # LEVEL 2: 1-WEEK SUSPENSION
    elif current_creation_count == 51:
        one_week_lockout_ts = time.time() + (7 * 24 * 3600)
        sanctions_db["suspended_users"][phone] = one_week_lockout_ts
        sanctions_db["blocked_creators"][phone] = 52
        save_sanctions_db(sanctions_db)
        resp = make_response(redirect(url_for(
            'index', error="Access Suspended: Exploit attempts flagged. Profile suspended for 1 week.")))
        resp.headers['Content-Type'] = 'text/html; charset=utf-8'
        return resp

    # LEVEL 1: OVER-QUOTA ROOM GENERATION BLOCK
    elif current_creation_count == 50:
        sanctions_db["blocked_creators"][phone] = 51
        save_sanctions_db(sanctions_db)
        resp = make_response(redirect(url_for(
            'index', error="Key error: Room creation limit reached. Profile is blocked from making more rooms.")))
        resp.headers['Content-Type'] = 'text/html; charset=utf-8'
        return resp
    # =======================================================================

    keys_db = load_keys_db()

    # COLLISION PASSTHROUGH CHECK
    if secret_key in keys_db:
        resp = make_response(redirect(
            url_for('index', error="Cant use key, Create a new one.")))
        resp.headers['Content-Type'] = 'text/html; charset=utf-8'
        return resp

    # Increment creation counters safely
    if phone not in sanctions_db["blocked_creators"]:
        sanctions_db["blocked_creators"][phone] = 0
    sanctions_db["blocked_creators"][phone] += 1
    save_sanctions_db(sanctions_db)

    # Save room properties inside cloud indexes
    keys_db[secret_key] = {
        "admin": phone,
        "admin_name": username,
        "room_type": room_type,
        "allowed_users": [],
        "pending_users": []
    }
    save_keys_db(keys_db)

    response = make_response(redirect(url_for('index')))
    response.headers['Content-Type'] = 'text/html; charset=utf-8'
    response.set_cookie('secret_key', secret_key, max_age=31536000, path='/')
    return response


@app.route('/send', methods=['POST'])
def send():
    user_agent = request.headers.get('User-Agent', 'Unknown-Device').strip()
    if is_spamming(user_agent):
        resp = make_response(redirect(url_for('index')))
        resp.headers['Content-Type'] = 'text/html; charset=utf-8'
        return resp

    username = request.cookies.get('username', 'Anonymous')
    phone = request.cookies.get('phone', '000')
    secret_key = request.cookies.get('secret_key', '')

    keys_db = load_keys_db()
    if not secret_key or secret_key not in keys_db:
        resp = make_response(render_template_string(DELETED_ROOM_TEMPLATE))
        resp.headers['Content-Type'] = 'text/html; charset=utf-8'
        return resp

    message_text = request.form.get('message', '').strip()[:50]

    if message_text:
        now = datetime.datetime.now().strftime("%H:%M")
        now_ts = time.time()
        encrypted_payload = encrypt_text(message_text, secret_key)

        append_to_chat_log({
            "user": username,
            "phone": phone,
            "text": encrypted_payload,
            "time": now,
            "room_key": secret_key,
            "timestamp": now_ts
        })
    response = make_response(redirect(url_for('index')))
    response.headers['Content-Type'] = 'text/html; charset=utf-8'
    return response


@app.route('/clear-room-cookie')
def clear_room_cookie():
    """Drops the active room passcode cookie so the user goes back to the directory list."""
    response = make_response(redirect(url_for('index')))
    response.headers['Content-Type'] = 'text/html; charset=utf-8'
    response.set_cookie('secret_key', '', max_age=0, path='/')
    return response


@app.route('/logout')
def logout():
    """Drops all account cookies completely out of the feature phone browser cache."""
    phone = request.cookies.get('phone')
    secret_key = request.cookies.get('secret_key')
    username = request.cookies.get('username', 'User')
    current_time_str = datetime.datetime.now().strftime("%H:%M")

    if secret_key in room_presence and phone in room_presence[secret_key]:
        room_presence[secret_key].pop(phone, None)
        append_to_chat_log({
            "user": "SYSTEM_ALERT", "phone": "000",
            "text": f"<-- {username} logged out.",
            "time": current_time_str, "room_key": secret_key, "is_alert": True
        })

    response = make_response(redirect(url_for('index')))
    response.headers['Content-Type'] = 'text/html; charset=utf-8'
    response.set_cookie('username', '', max_age=0, path='/')
    response.set_cookie('phone', '', max_age=0, path='/')
    response.set_cookie('secret_key', '', max_age=0, path='/')
    return response


# DECENTRALIZED ROOM CREATOR APPROVAL ACTIONS: Called strictly by the specific room owner
@app.route('/room-admin-action/<action>/<target_phone>')
def room_admin_action(action, target_phone):
    phone = request.cookies.get('phone')
    secret_key = request.cookies.get('secret_key')

    if not phone or not secret_key:
        resp = make_response(redirect(url_for('index')))
        resp.headers['Content-Type'] = 'text/html; charset=utf-8'
        return resp

    if target_phone.startswith('+256'):
        target_phone = '0' + target_phone[4:]
    elif target_phone.startswith('256'):
        target_phone = '0' + target_phone[3:]

    keys_db = load_keys_db()

    # SECURITY POLICY GUARD CHANNELS: Verify current requester is the true owner admin creator
    if secret_key not in keys_db or phone != keys_db[secret_key].get("admin"):
        err_resp = make_response(
            "Unauthorized Action: You are not the admin creator of this room key!", 403)
        err_resp.headers['Content-Type'] = 'text/plain; charset=utf-8'
        return err_resp

    room = keys_db[secret_key]
    room_type = room.get('room_type', 'group')
    pending_list = room.get("pending_users", [])
    allowed_list = room.get("allowed_users", [])

    if target_phone in pending_list:
        pending_list.remove(target_phone)

    if action == "allow":
        total_slots_occupied = len(allowed_list) + 1

        # DOUBLE ENFORCE STRICT CAP LIMITS DURING THE APPROVAL STAGE OVER KEYPADS
        if room_type == 'pair' and total_slots_occupied >= 2:
            fail_resp = make_response(
                "Approval Aborted: This strict 2-people room is completely filled!", 400)
            fail_resp.headers['Content-Type'] = 'text/plain; charset=utf-8'
            return fail_resp
        if room_type == 'group' and total_slots_occupied >= 20:
            fail_resp = make_response(
                "Approval Aborted: This room capacity is capped at 20 users!", 400)
            fail_resp.headers['Content-Type'] = 'text/plain; charset=utf-8'
            return fail_resp

        if target_phone not in allowed_list:
            allowed_list.append(target_phone)
            current_time_str = datetime.datetime.now().strftime("%H:%M")
            append_to_chat_log({
                "user": "SYSTEM_ALERT", "phone": "000",
                "text": f"[Tunnel Notice]: {target_phone} was approved by Admin.",
                "time": current_time_str, "room_key": secret_key, "is_alert": True,
                "timestamp": time.time()
            })
    elif action == "deny":
        if target_phone in allowed_list:
            allowed_list.remove(target_phone)

    keys_db[secret_key]["pending_users"] = pending_list
    keys_db[secret_key]["allowed_users"] = allowed_list
    save_keys_db(keys_db)

    response = make_response(redirect(url_for('index')))
    response.headers['Content-Type'] = 'text/html; charset=utf-8'
    return response


# DYNAMIC MONITOR PANEL ENDPOINT: Serves live room data maps directly onto your HTML console interface
@app.route('/secret-admin-get-users/<password>')
def secret_admin_get_users(password):
    if password != "Kampala2026":
        err_resp = make_response("Unauthorized Access Denied!", 403)
        err_resp.headers['Content-Type'] = 'text/plain; charset=utf-8'
        return err_resp

    keys_db = load_keys_db()
    response = make_response(json.dumps(keys_db, indent=4))
    response.headers['Content-Type'] = 'application/json; charset=utf-8'
    return response


# RE-BRIDGE TRAFFIC TELEMETRY ENDPOINT: Feeds network profiles straight to your portal cards
@app.route('/secret-admin-get-activity/<password>')
def secret_admin_get_activity(password):
    if password != "Kampala2026":
        err_resp = make_response("Unauthorized Access Denied!", 403)
        err_resp.headers['Content-Type'] = 'text/plain; charset=utf-8'
        return err_resp

    active_snapshots = {}
    for rkey, peers in room_presence.items():
        active_snapshots[rkey] = {}
        for phone, data in peers.items():
            active_snapshots[rkey][phone] = {
                "name": data.get("name", "User"),
                "device": data.get("device", "Unknown Handset Device Component Profile")
            }

    response = make_response(json.dumps(active_snapshots, indent=4))
    response.headers['Content-Type'] = 'application/json; charset=utf-8'
    return response


# NEW SECURITY LOG TELEMETRY ENCODING PIPELINE: Streams fresh profile sign-in audits to dashboard logs
@app.route('/secret-admin-get-signins/<password>')
def secret_admin_get_signins(password):
    if password != "Kampala2026":
        err_resp = make_response("Unauthorized Access Denied!", 403)
        err_resp.headers['Content-Type'] = 'text/plain; charset=utf-8'
        return err_resp

    response = make_response(json.dumps(recent_sign_ins, indent=4))
    response.headers['Content-Type'] = 'application/json; charset=utf-8'
    return response


# NEW SECURITY DEFENSIVE REMEDIAL GATEWAY: Flushes and unbans access parameters inside fractions of a second
@app.route('/secret-admin-lift-sanctions/<password>/<target_phone>')
def secret_admin_lift_sanctions(password, target_phone):
    if password != "Kampala2026":
        err_resp = make_response("Unauthorized Access Denied!", 403)
        err_resp.headers['Content-Type'] = 'text/plain; charset=utf-8'
        return err_resp

    if target_phone.startswith('+256'):
        target_phone = '0' + target_phone[4:]
    elif target_phone.startswith('256'):
        target_phone = '0' + target_phone[3:]

    sanctions_db = load_sanctions_db()

    # Fully flush rate-limiting counters back down to zero metrics layers
    if target_phone in sanctions_db.get("blocked_creators", {}):
        sanctions_db["blocked_creators"][target_phone] = 0
    if target_phone in sanctions_db.get("suspended_users", {}):
        sanctions_db["suspended_users"].pop(target_phone, None)

    # Wipe the database trackers completely clear for access restoration
    save_sanctions_db(sanctions_db)
    response = make_response(
        f"[✓] Success: All security locks, counts and blocks removed for account handle: {target_phone}.")
    response.headers['Content-Type'] = 'text/plain; charset=utf-8'
    return response


# NEW OPERATIONAL PIPELINE: Quietly wipes a user account completely out of all database definitions
@app.route('/secret-admin-delete-account/<password>/<target_phone>')
def secret_admin_delete_account(password, target_phone):
    if password != "Kampala2026":
        err_resp = make_response("Unauthorized Access Denied!", 403)
        err_resp.headers['Content-Type'] = 'text/plain; charset=utf-8'
        return err_resp

    if target_phone.startswith('+256'):
        target_phone = '0' + target_phone[4:]
    elif target_phone.startswith('256'):
        target_phone = '0' + target_phone[3:]

    sanctions_db = load_sanctions_db()

    # 1. Clear out all anti-fraud tracking metrics counters for this number
    if target_phone in sanctions_db.get("blocked_creators", {}):
        sanctions_db["blocked_creators"].pop(target_phone, None)

    # 2. Lift any active 1-week suspensions structural logs
    if target_phone in sanctions_db.get("suspended_users", {}):
        sanctions_db["suspended_users"].pop(target_phone, None)

    # Commit changes cleanly onto sanctions file database layout paths
    save_sanctions_db(sanctions_db)

    # 3. Purge all private chat rooms initialized by this specific user handle profile
    keys_db = load_keys_db()
    corrupted_rooms = [rkey for rkey, rdata in keys_db.items(
    ) if rdata.get("admin") == target_phone]

    for rkey in corrupted_rooms:
        keys_db.pop(rkey, None)

    # Sync the room wipeout immediately to the cloud keys vault index
    save_keys_db(keys_db)
    response = make_response(
        f"[✓] Success: Account profile history records and owned room allocations completely deleted for phone number: {target_phone}.")
    response.headers['Content-Type'] = 'text/plain; charset=utf-8'
    return response


# DYNAMIC OVERRIDE API: Erase or unlock room footprints cleanly across network bounds
@app.route('/secret-admin-manage-rooms/<password>/<action>/<secret_key>')
def secret_admin_manage_rooms(password, action, secret_key):
    if password != "Kampala2026":
        err_resp = make_response("Unauthorized Access Denied!", 403)
        err_resp.headers['Content-Type'] = 'text/plain; charset=utf-8'
        return err_resp

    keys_db = load_keys_db()
    if secret_key in keys_db:
        if action == "delete":

            keys_db.pop(secret_key, None)
            save_keys_db(keys_db)
            success_resp = make_response(
                f"[✓] Success: Completely purged secret key room '{secret_key}'.")
            success_resp.headers['Content-Type'] = 'text/plain; charset=utf-8'
            return success_resp

        elif action == "unlock":
            keys_db[secret_key]["allowed_users"] = []
            keys_db[secret_key]["pending_users"] = []
            save_keys_db(keys_db)
            success_resp = make_response(
                f"[✓] Success: Flushed permission tables for room '{secret_key}'.")
            success_resp.headers['Content-Type'] = 'text/plain; charset=utf-8'
            return success_resp

    not_found_resp = make_response(
        "[X] Error: Target room passcode not found.", 404)
    not_found_resp.headers['Content-Type'] = 'text/plain; charset=utf-8'
    return not_found_resp


@app.after_request
def add_cors_headers(response):
    """Enforces wide-open cross-origin permissive sharing rules to link up with separate sites like Netlify."""
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Headers'] = 'Content-Type,Authorization'
    response.headers['Access-Control-Allow-Methods'] = 'GET,PUT,POST,DELETE,OPTIONS'
    return response


def def_generate_secure_token(length=6):
    chars = string.ascii_uppercase + string.digits
    return ''.join(random.choice(chars) for _ in range(length))


# FIXED: Re-injected full system double-underscores to trigger deployment boots
if __name__ == '__main__':
    # Initialise deployment system core loop natively without debugging flags over waitress environments
    app.run(host='0.0.0.0', port=5000, debug=False)

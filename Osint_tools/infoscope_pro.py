import streamlit as st
import requests
import folium
from streamlit_folium import st_folium
import socket
import phonenumbers
from phonenumbers import geocoder, carrier, timezone as ph_timezone
import datetime
import re
import math
from collections import Counter
import dns.resolver
import whois
import json
from PIL import Image
from PIL.ExifTags import TAGS, GPSTAGS
import hashlib
import os
from html import escape
from email.utils import parseaddr

# ─────────────────────────────────────────────
# PAGE CONFIG
# ─────────────────────────────────────────────
st.set_page_config(
    page_title="InfoScope Pro",
    page_icon="🕵️",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ─────────────────────────────────────────────
# STYLES
# ─────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Share+Tech+Mono&family=Orbitron:wght@400;700;900&family=Syne:wght@400;600;800&display=swap');

html, body, [class*="css"] {
    font-family: 'Syne', sans-serif;
    background-color: #04090f;
    color: #b8cfe0;
}
.stApp {
    background: radial-gradient(ellipse at 20% 10%, #051020 0%, #04090f 60%);
}
::-webkit-scrollbar { width: 4px; }
::-webkit-scrollbar-thumb { background: #1a4060; border-radius: 2px; }
#MainMenu, footer, header { visibility: hidden; }
[data-testid="stSidebar"] { display: none; }
.block-container { padding: 1.5rem 2rem 2rem 2rem !important; max-width: 100% !important; }

/* NAV */
.topnav {
    display: flex; align-items: center; justify-content: space-between;
    padding: 14px 28px;
    background: rgba(5,16,32,0.97);
    border-bottom: 1px solid #0e2a44;
    margin: -1.5rem -2rem 2rem -2rem;
}
.logo { font-family:'Orbitron',sans-serif; font-weight:900; font-size:1.3rem; color:#e8f4ff; letter-spacing:.06em; }
.logo span { color:#1e88e5; }
.nav-badge {
    display:inline-flex; align-items:center; gap:6px;
    background:rgba(0,180,80,.12); border:1px solid rgba(0,180,80,.3);
    border-radius:20px; padding:4px 14px;
    font-family:'Share Tech Mono',monospace; font-size:.72rem; color:#00cc66; letter-spacing:.1em;
}
.nav-dot { width:6px;height:6px;border-radius:50%;background:#00cc66;box-shadow:0 0 6px #00cc66;animation:pulse 2s infinite; }
@keyframes pulse { 0%,100%{opacity:1}50%{opacity:.4} }
.nav-time { font-family:'Share Tech Mono',monospace; font-size:.76rem; color:#2a6a9a; }

/* STATS */
.stat-card {
    background:linear-gradient(135deg,#071422,#050e1c);
    border:1px solid #0e2a44; border-radius:10px; padding:16px; text-align:center; position:relative; overflow:hidden;
}
.stat-card::after { content:'';position:absolute;bottom:0;left:0;right:0;height:2px;background:linear-gradient(90deg,transparent,#1e6aaa,transparent); }
.stat-num { font-family:'Orbitron',monospace; font-size:1.7rem; font-weight:700; color:#4ab8f8; }
.stat-lbl { font-family:'Share Tech Mono',monospace; font-size:.65rem; letter-spacing:.15em; color:#2a5a80; text-transform:uppercase; margin-top:4px; }

/* MODULE CARD */
.mod-card {
    background:linear-gradient(145deg,#071422,#04090f);
    border:1px solid #0e2a44; border-radius:12px; padding:20px; position:relative; overflow:hidden;
}
.mod-card::before { content:'';position:absolute;top:0;left:0;right:0;height:2px;background:linear-gradient(90deg,transparent,#1e88e5,transparent);opacity:.6; }
.mod-icon { font-size:1.7rem; margin-bottom:8px; display:block; }
.mod-title { font-family:'Orbitron',sans-serif; font-size:.8rem; font-weight:700; color:#5aaae8; letter-spacing:.1em; text-transform:uppercase; margin-bottom:14px; }

/* SECTION LABEL */
.sec-head {
    font-family:'Orbitron',sans-serif; font-size:.65rem; font-weight:700; color:#1e6aaa;
    letter-spacing:.2em; text-transform:uppercase;
    border-left:3px solid #1a5580; padding-left:10px; margin:18px 0 10px 0;
}

/* RESULT ROW */
.res-row {
    display:flex; align-items:flex-start; gap:10px; padding:8px 12px;
    border-radius:6px; background:rgba(10,30,60,.5); border:1px solid #0b2040;
    margin-bottom:6px; font-family:'Share Tech Mono',monospace; font-size:.81rem;
}
.res-label { color:#2a6a9a; min-width:140px; font-size:.73rem; letter-spacing:.04em; flex-shrink:0; }
.res-val { color:#c8e0f8; word-break:break-all; }
.res-val.good { color:#00cc66; }
.res-val.warn { color:#f0a030; }
.res-val.bad  { color:#f05050; }

/* DATA TABLE */
.data-table { width:100%; border-collapse:collapse; font-family:'Share Tech Mono',monospace; font-size:.78rem; margin-top:6px; }
.data-table th { background:#071828; color:#1e6aaa; padding:8px 10px; text-align:left; letter-spacing:.1em; font-size:.68rem; border-bottom:1px solid #0e2a44; }
.data-table td { padding:8px 10px; border-bottom:1px solid #071828; color:#b0cce0; vertical-align:top; }
.data-table tr:last-child td { border-bottom:none; }
.data-table tr:hover td { background:rgba(14,42,70,.4); }

/* DIVIDER */
.vdiv { border:none; border-top:1px solid #0a2030; margin:18px 0; }

/* EMPTY STATE */
.empty-state {
    text-align:center; padding:40px 20px;
    font-family:'Share Tech Mono',monospace; font-size:.8rem; color:#1a4a68;
    border:1px dashed #0a2030; border-radius:10px; margin-top:10px;
}

/* INPUTS */
.stTextInput > div > div > input {
    background:#060f1e !important; border:1px solid #0e2a44 !important;
    border-radius:7px !important; color:#c8e0f8 !important;
    font-family:'Share Tech Mono',monospace !important; font-size:.9rem !important; padding:11px 14px !important;
}
.stTextInput > div > div > input:focus { border-color:#1e6aaa !important; box-shadow:0 0 0 3px rgba(30,106,170,.15) !important; }
.stTextInput > div > div > input::placeholder { color:#1e4a68 !important; }

/* BUTTONS */
.stButton > button {
    background:linear-gradient(135deg,#0c2e54,#1a5a9a) !important;
    color:#d8eeff !important; border:1px solid #1e6aaa !important;
    border-radius:7px !important; font-family:'Orbitron',sans-serif !important;
    font-weight:700 !important; font-size:.68rem !important; letter-spacing:.12em !important;
    padding:10px 18px !important; text-transform:uppercase !important; width:100% !important;
}
.stButton > button:hover { background:linear-gradient(135deg,#1a5a9a,#2a80d0) !important; box-shadow:0 0 20px rgba(30,136,229,.35) !important; }

/* TABS */
[data-baseweb="tab-list"] { background:transparent !important; gap:4px !important; border-bottom:1px solid #0e2a44 !important; margin-bottom:20px !important; flex-wrap:wrap !important; }
[data-baseweb="tab"] { font-family:'Orbitron',sans-serif !important; font-size:.62rem !important; font-weight:700 !important; letter-spacing:.12em !important; color:#2a6a9a !important; background:transparent !important; border:none !important; padding:10px 14px !important; border-radius:6px 6px 0 0 !important; }
[aria-selected="true"][data-baseweb="tab"] { color:#5aaae8 !important; background:rgba(14,42,70,.6) !important; border-bottom:2px solid #1e88e5 !important; }

/* ALERTS */
[data-testid="stAlert"] { border-radius:7px !important; font-family:'Share Tech Mono',monospace !important; font-size:.8rem !important; }

/* MAP */
[data-testid="stIframe"] { border-radius:10px !important; border:1px solid #0e2a44 !important; overflow:hidden !important; }

/* SPINNER */
.stSpinner > div { border-top-color:#1e88e5 !important; }

/* ANALYST PANELS */
.intel-banner {
    background: linear-gradient(135deg, rgba(15,35,60,.88), rgba(5,14,28,.92));
    border: 1px solid rgba(55,130,195,.35);
    border-radius: 14px;
    padding: 16px 18px;
    margin: 4px 0 16px 0;
    box-shadow: 0 14px 30px rgba(0,0,0,.18);
}
.intel-banner-title {
    font-family:'Orbitron',sans-serif;
    font-size:.78rem;
    letter-spacing:.14em;
    text-transform:uppercase;
    color:#8fd6ff;
    margin-bottom:8px;
}
.intel-banner-copy {
    font-family:'Share Tech Mono',monospace;
    font-size:.74rem;
    line-height:1.7;
    color:#a8c9df;
}
.mini-grid {
    display:grid;
    grid-template-columns:repeat(3, minmax(0, 1fr));
    gap:10px;
    margin:10px 0 14px 0;
}
.mini-card {
    background:rgba(6,15,30,.9);
    border:1px solid #10304f;
    border-radius:10px;
    padding:12px;
}
.mini-k {
    font-family:'Share Tech Mono',monospace;
    font-size:.62rem;
    letter-spacing:.14em;
    color:#42769b;
    text-transform:uppercase;
    margin-bottom:5px;
}
.mini-v {
    font-family:'Orbitron',sans-serif;
    font-size:.92rem;
    color:#d7eeff;
}
@media (max-width: 900px) {
    .mini-grid {
        grid-template-columns:1fr;
    }
}
</style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────
# SESSION STATE
# ─────────────────────────────────────────────
for k, v in [("log", []), ("q_count", 0)]:
    if k not in st.session_state:
        st.session_state[k] = v

def add_log(mod, query):
    now = datetime.datetime.now().strftime("%H:%M:%S")
    st.session_state.log.insert(0, {"t": now, "m": mod, "q": query})
    st.session_state.log = st.session_state.log[:30]
    st.session_state.q_count += 1

# ─────────────────────────────────────────────
# UI HELPERS
# ─────────────────────────────────────────────
def row(icon, label, value, cls=""):
    st.markdown(f"""<div class='res-row'>
        <span class='res-label'>{icon} {label}</span>
        <span class='res-val {cls}'>{value}</span>
    </div>""", unsafe_allow_html=True)

def section(title):
    st.markdown(f"<div class='sec-head'>{title}</div>", unsafe_allow_html=True)

def table(headers, rows):
    th = "".join(f"<th>{escape(str(h))}</th>" for h in headers)
    trs = ""
    for r in rows:
        trs += "<tr>" + "".join(f"<td>{c}</td>" for c in r) + "</tr>"
    st.markdown(
        f"<table class='data-table'><thead><tr>{th}</tr></thead><tbody>{trs}</tbody></table>",
        unsafe_allow_html=True
    )

def intel_banner(title, copy_text):
    st.markdown(
        f"""
        <div class='intel-banner'>
            <div class='intel-banner-title'>{escape(title)}</div>
            <div class='intel-banner-copy'>{escape(copy_text)}</div>
        </div>
        """,
        unsafe_allow_html=True
    )

def mini_stats(items):
    cards = []
    for label, value in items:
        cards.append(
            f"<div class='mini-card'><div class='mini-k'>{escape(str(label))}</div><div class='mini-v'>{escape(str(value))}</div></div>"
        )
    st.markdown(f"<div class='mini-grid'>{''.join(cards)}</div>", unsafe_allow_html=True)

def clean_exif_value(value):
    try:
        if isinstance(value, bytes):
            decoded = value.decode("utf-8", errors="ignore").strip("\x00").strip()
            return decoded if decoded else repr(value)
        if isinstance(value, tuple):
            return ", ".join(str(v) for v in value)
        return str(value)
    except Exception:
        return str(value)

def is_useful_metadata_field(key, value):
    ignored_fields = {
        "MakerNote",
        "UserComment",
        "ComponentsConfiguration",
        "PrintImageMatching",
        "GPSInfo"
    }
    if key in ignored_fields:
        return False
    cleaned = clean_exif_value(value).strip()
    if not cleaned:
        return False
    if cleaned in {"0", "0.0", "None", "b''"}:
        return False
    return True

# ─────────────────────────────────────────────
# VALIDATORS
# ─────────────────────────────────────────────
def valid_ip(ip):
    parts = ip.strip().split(".")
    if len(parts) != 4:
        return False
    return all(p.isdigit() and 0 <= int(p) <= 255 for p in parts)

def valid_email(email):
    email = (email or "").strip().lower()
    _, parsed = parseaddr(email)
    if not parsed:
        return False
    pattern = r'^[a-z0-9._%+\-]+@[a-z0-9.\-]+\.[a-z]{2,}$'
    return bool(re.fullmatch(pattern, parsed))

# ─────────────────────────────────────────────
# DATA FETCHERS
# ─────────────────────────────────────────────
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/120 Safari/537.36"
}

def extract_metadata(image_file):
    try:
        image = Image.open(image_file)
        exif_data = image._getexif()
        if not exif_data:
            return None, None

        metadata = {}
        gps_data = {}

        for tag, value in exif_data.items():
            decoded = TAGS.get(tag, tag)
            metadata[decoded] = value

        if "GPSInfo" in metadata:
            for key in metadata["GPSInfo"]:
                decoded = GPSTAGS.get(key, key)
                gps_data[decoded] = metadata["GPSInfo"][key]

        return metadata, gps_data
    except Exception:
        return None, None

def fetch_ip_data(ip):
    fields = "status,message,country,countryCode,region,regionName,city,zip,lat,lon,timezone,offset,isp,org,as,asname,mobile,proxy,hosting,query"
    r = requests.get(f"http://ip-api.com/json/{ip}?fields={fields}", timeout=10)
    return r.json()

def fetch_whois_domain(domain):
    try:
        return whois.whois(domain)
    except Exception:
        return None

def fetch_dns_records(domain):
    records = {}
    for rtype in ["A", "MX", "NS", "TXT", "AAAA", "CNAME"]:
        try:
            answers = dns.resolver.resolve(domain, rtype, lifetime=4)
            records[rtype] = [str(r) for r in answers]
        except Exception:
            records[rtype] = []
    return records

def fetch_reverse_ip(ip):
    try:
        r = requests.get(f"https://api.hackertarget.com/reverseiplookup/?q={ip}", timeout=8, headers=HEADERS)
        if "error" not in r.text.lower() and r.text.strip():
            domains = [d.strip() for d in r.text.strip().split("\n") if d.strip()]
            return domains[:20]
    except Exception:
        pass
    return []

def fetch_http_headers(domain):
    results = {}
    for scheme in ["https", "http"]:
        try:
            r = requests.head(f"{scheme}://{domain}", timeout=6, allow_redirects=True, headers=HEADERS)
            results["Status Code"] = str(r.status_code)
            results["Server"] = r.headers.get("Server", "Not disclosed")
            results["X-Powered-By"] = r.headers.get("X-Powered-By", "Not disclosed")
            results["Content-Type"] = r.headers.get("Content-Type", "N/A")
            results["Strict-Transport-Security"] = r.headers.get("Strict-Transport-Security", "❌ Not set")
            results["X-Frame-Options"] = r.headers.get("X-Frame-Options", "❌ Not set")
            results["X-Content-Type-Options"] = r.headers.get("X-Content-Type-Options", "❌ Not set")
            results["Content-Security-Policy"] = r.headers.get("Content-Security-Policy", "❌ Not set")
            results["Final URL"] = r.url
            break
        except Exception:
            continue
    return results

def fetch_ssl_info(domain):
    try:
        r = requests.get(f"https://crt.sh/?q={domain}&output=json", timeout=8)
        certs = r.json()
        if certs:
            latest = certs[0]
            return {
                "Common Name": latest.get("common_name", "N/A"),
                "Issuer": latest.get("issuer_name", "N/A"),
                "Not Before": latest.get("not_before", "N/A"),
                "Not After": latest.get("not_after", "N/A"),
                "Total Certs Found": len(certs),
            }
    except Exception:
        pass
    return {}

def fetch_subdomains(domain):
    try:
        r = requests.get(f"https://crt.sh/?q=%.{domain}&output=json", timeout=10)
        data = r.json()
        subs = set()
        for entry in data:
            name = entry.get("name_value", "")
            for s in name.split("\n"):
                s = s.strip().lstrip("*.")
                if domain in s and s != domain:
                    subs.add(s)
        return sorted(list(subs))[:30]
    except Exception:
        return []

def fetch_ip_reputation(ip):
    results = {}
    try:
        requests.get(f"https://api.ipqualityscore.com/api/json/ip/YOUR_KEY/{ip}", timeout=6)
    except Exception:
        pass
    try:
        requests.get(
            f"https://www.virustotal.com/api/v3/ip_addresses/{ip}",
            headers={"x-apikey": ""},
            timeout=5
        )
    except Exception:
        pass
    return results

def check_email_disposable(domain):
    disposable = [
        "mailinator.com","guerrillamail.com","10minutemail.com","tempmail.com",
        "throwam.com","yopmail.com","maildrop.cc","sharklasers.com","guerrillamailblock.com",
        "grr.la","guerrillamail.info","guerrillamail.biz","guerrillamail.de","guerrillamail.net",
        "guerrillamail.org","spam4.me","trashmail.com","trashmail.at","trashmail.io",
        "fakeinbox.com","dispostable.com","mailnull.com","spamgourmet.com"
    ]
    return domain.lower() in disposable

def fetch_email_breach_count(email):
    try:
        r = requests.get(
            f"https://haveibeenpwned.com/api/v3/breachedaccount/{email}",
            headers={**HEADERS, "hibp-api-key": ""},
            timeout=6
        )
        if r.status_code == 200:
            return len(r.json()), r.json()
        elif r.status_code == 404:
            return 0, []
    except Exception:
        pass
    return None, []

def gravatar_url(email):
    h = hashlib.md5(email.strip().lower().encode()).hexdigest()
    return f"https://www.gravatar.com/avatar/{h}?d=404&s=80", f"https://www.gravatar.com/{h}"

def fetch_open_ports(ip):
    common_ports = {
        21: "FTP", 22: "SSH", 23: "Telnet", 25: "SMTP",
        53: "DNS", 80: "HTTP", 110: "POP3", 143: "IMAP",
        443: "HTTPS", 445: "SMB", 3306: "MySQL",
        3389: "RDP", 5432: "PostgreSQL", 6379: "Redis",
        8080: "HTTP-Alt", 8443: "HTTPS-Alt", 27017: "MongoDB"
    }
    open_ports = []
    for port, service in common_ports.items():
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(0.5)
            result = sock.connect_ex((ip, port))
            if result == 0:
                open_ports.append((port, service, "OPEN"))
            sock.close()
        except Exception:
            pass
    return open_ports

# ─────────────────────────────────────────────
# IMAGE HELPERS
# ─────────────────────────────────────────────
def generate_hashes(file_bytes):
    return {
        "MD5": hashlib.md5(file_bytes).hexdigest(),
        "SHA1": hashlib.sha1(file_bytes).hexdigest(),
        "SHA256": hashlib.sha256(file_bytes).hexdigest()
    }

def extract_strings(file_bytes):
    try:
        text = file_bytes.decode(errors="ignore")

        found = []

        # URLs
        urls = re.findall(r'https?://[^\s"\'>]+', text)
        found.extend(urls)

        # # Emails
        # emails = re.findall(r'[A-Za-z0-9._%+\-]+@[A-Za-z0-9.\-]+\.[A-Za-z]{2,}', text)
        # found.extend(emails)

        # Phone-like patterns
        phones = re.findall(r'\+?\d[\d\-\s()]{7,}\d', text)
        found.extend(phones)

        # Social handles
        handles = re.findall(r'@[A-Za-z0-9._]{3,}', text)
        found.extend(handles)

        # Clean duplicates
        clean = []
        seen = set()

        for item in found:
            item = item.strip()
            if item and item not in seen:
                seen.add(item)
                clean.append(item)

        return clean[:20]
    except Exception:
        return []

def detect_stego(file_bytes):
    byte_counts = Counter(file_bytes)
    total = len(file_bytes)

    entropy = 0
    for count in byte_counts.values():
        p = count / total
        entropy -= p * math.log2(p)

    if entropy > 7.9:
        return f"⚠️ Very high entropy ({entropy:.2f}) — Possible encrypted/packed data"
    elif entropy > 7.5:
        return f"⚠️ High entropy ({entropy:.2f}) — Normal for compressed images (JPEG/PNG)"
    elif entropy > 6.5:
        return f"🟡 Moderate entropy ({entropy:.2f}) — Likely normal image"
    else:
        return f"🟢 Low entropy ({entropy:.2f}) — Unusual (check manually)"

def exif_coord_to_decimal(coord, ref):
    try:
        def to_float(x):
            if isinstance(x, tuple) and len(x) == 2:
                num, den = x
                return float(num) / float(den) if den else 0.0
            return float(x)

        degrees = to_float(coord[0])
        minutes = to_float(coord[1])
        seconds = to_float(coord[2])

        decimal = degrees + (minutes / 60.0) + (seconds / 3600.0)

        if ref in ["S", "W"]:
            decimal = -decimal

        return decimal
    except Exception:
        return None

def extract_gps_coordinates(gps_data):
    try:
        lat = gps_data.get("GPSLatitude")
        lat_ref = gps_data.get("GPSLatitudeRef")
        lon = gps_data.get("GPSLongitude")
        lon_ref = gps_data.get("GPSLongitudeRef")

        if not lat or not lat_ref or not lon or not lon_ref:
            return None, None

        if isinstance(lat_ref, bytes):
            lat_ref = lat_ref.decode(errors="ignore")
        if isinstance(lon_ref, bytes):
            lon_ref = lon_ref.decode(errors="ignore")

        latitude = exif_coord_to_decimal(lat, lat_ref)
        longitude = exif_coord_to_decimal(lon, lon_ref)

        return latitude, longitude
    except Exception:
        return None, None

def google_maps_link(lat, lon):
    return f"https://www.google.com/maps?q={lat},{lon}"

# ─────────────────────────────────────────────
# TOP NAV
# ─────────────────────────────────────────────
now_str = datetime.datetime.now().strftime("%Y-%m-%d  %H:%M:%S")
st.markdown(f"""
<div class='topnav'>
    <div class='logo'>INFO<span>SCOPE</span> PRO</div>
    <div class='nav-badge'><div class='nav-dot'></div>SYSTEM ONLINE</div>
    <div class='nav-time'>{now_str}</div>
</div>""", unsafe_allow_html=True)

# ─────────────────────────────────────────────
# STATS
# ─────────────────────────────────────────────
s1, s2, s3, s4 = st.columns(4)
with s1:
    st.markdown(f"<div class='stat-card'><div class='stat-num'>{st.session_state.q_count}</div><div class='stat-lbl'>Queries Run</div></div>", unsafe_allow_html=True)
with s2:
    st.markdown("<div class='stat-card'><div class='stat-num'>3</div><div class='stat-lbl'>Active Modules</div></div>", unsafe_allow_html=True)
with s3:
    st.markdown("<div class='stat-card'><div class='stat-num'>10+</div><div class='stat-lbl'>Data Sources</div></div>", unsafe_allow_html=True)
with s4:
    st.markdown(f"<div class='stat-card'><div class='stat-num'>{len(st.session_state.log)}</div><div class='stat-lbl'>Log Entries</div></div>", unsafe_allow_html=True)

st.markdown("<hr class='vdiv'>", unsafe_allow_html=True)

# ─────────────────────────────────────────────
# TABS
# ─────────────────────────────────────────────
tab1, tab3, tab4, tab5 = st.tabs([
    "👤  NAME INTELLIGENCE",
    #"📧  EMAIL INTELLIGENCE",
    "🌐  IP INTELLIGENCE",
    "🖼️  IMAGE METADATA",
    "📋  ACTIVITY LOG"
])

# ══════════════════════════════════════════════
# TAB 1 — NAME INTELLIGENCE (ADVANCED)
# ══════════════════════════════════════════════
with tab1:
    L, R = st.columns([1, 1.8], gap="large")

    # ───────── LEFT PANEL ─────────
    with L:
        st.markdown("<div class='mod-card'>", unsafe_allow_html=True)
        st.markdown("<span class='mod-icon'>👤</span><div class='mod-title'>Name Intelligence</div>", unsafe_allow_html=True)

        name_in = st.text_input("Full Name", key="name_in")
        name_city = st.text_input("City (optional)", key="name_city")
        name_cntry = st.text_input("Country (optional)", key="name_cntry")

        run_name = st.button("🔍 ANALYZE NAME", key="btn_name")

        st.markdown("</div>", unsafe_allow_html=True)

    # ───────── RIGHT PANEL ─────────
    with R:
        if run_name:
            if not name_in.strip():
                st.error("❌ Enter a name.")
            else:
                add_log("Name Intel", name_in.strip())

                parts = name_in.strip().split()
                fname = parts[0]
                lname = parts[-1] if len(parts) > 1 else ""

                fn, ln = fname.lower(), lname.lower()

                # ───────── BASIC INFO ─────────
                section("PARSED INFORMATION")
                row("🔤", "Full Name", name_in.strip())
                row("🔤", "First Name", fname)
                row("🔤", "Last Name", lname or "—")
                row("📏", "Word Count", f"{len(parts)}")

                conf = ("HIGH", "good") if len(parts) >= 2 else ("LOW — use full name", "warn")
                row("📊", "Confidence", conf[0], conf[1])

                # ───────── USERNAME GENERATION ─────────
                section("GENERATED USERNAMES")

                def generate_usernames(fn, ln):
                    usernames = set()
                    if ln:
                        usernames.update([
                            fn + ln,
                            fn + "." + ln,
                            fn + "_" + ln,
                            fn + "-" + ln,
                            fn + ln + "123",
                            fn + ln + "99",
                            fn[0] + ln,
                            ln + fn
                        ])
                    else:
                        usernames.update([
                            fn,
                            fn + "123",
                            fn + "_official",
                            fn + "99"
                        ])
                    return list(usernames)

                usernames = generate_usernames(fn, ln)

                table(["#", "Username"], [(str(i+1), u) for i, u in enumerate(usernames)])

                # ───────── CONFIDENCE FUNCTION ─────────
                def get_confidence(platform):
                    if platform in ["GitHub", "Reddit"]:
                        return "HIGH"
                    elif platform in ["Twitter/X", "Instagram", "LinkedIn", "Pinterest"]:
                        return "MEDIUM"
                    else:
                        return "LOW"

                # ───────── PLATFORM CHECK ─────────
                section("ADVANCED USERNAME INTELLIGENCE")

                platforms = {
                    "GitHub":    "https://github.com/{u}",
                    "Twitter/X": "https://x.com/{u}",
                    "Instagram": "https://www.instagram.com/{u}/",
                    "LinkedIn":  "https://www.linkedin.com/in/{u}",
                    "Reddit":    "https://www.reddit.com/user/{u}",
                    "Pinterest": "https://www.pinterest.com/{u}/",
                }

                results = []

                with st.spinner("Running OSINT scan..."):
                    for username in usernames:
                        for platform, url_tpl in platforms.items():
                            url = url_tpl.replace("{u}", username)

                            try:
                                resp = requests.get(url, timeout=5, headers=HEADERS)
                                text = resp.text.lower()

                                if resp.status_code == 200:

                                    if platform == "Instagram" and "sorry, this page isn't available" in text:
                                        status = "⚪ NOT FOUND"

                                    elif platform == "Twitter/X" and "account doesn" in text:
                                        status = "⚪ NOT FOUND"

                                    elif platform == "Reddit" and "nobody on reddit goes by that name" in text:
                                        status = "⚪ NOT FOUND"

                                    elif platform == "LinkedIn":
                                        if "profile not found" in text:
                                            status = "⚪ NOT FOUND"
                                        elif "login" in text:
                                            status = "🟡 LOGIN REQUIRED"
                                        else:
                                            status = "🟢 FOUND"

                                    elif "not found" in text:
                                        status = "⚪ NOT FOUND"

                                    else:
                                        status = "🟢 FOUND"

                                elif resp.status_code == 404:
                                    status = "⚪ NOT FOUND"

                                elif resp.status_code == 403:
                                    status = "🟡 RESTRICTED"

                                else:
                                    status = "🟡 UNKNOWN"

                            except:
                                status = "🔴 ERROR"

                            confidence = get_confidence(platform)

                            if status == "🟢 FOUND":
                                results.append((platform, username, status, confidence, url))

                # ───────── DISPLAY RESULTS ─────────
                if results:
                    table(
                        ["Platform", "Username", "Status", "Confidence", "URL"],
                        [(p, u, s, c, f'<a href="{url}" target="_blank" style="color:#2a7ab8">{url[:45]}...</a>')
                         for p, u, s, c, url in results]
                    )
                else:
                    row("📭", "Result", "No strong matches found", "warn")

                st.success("✅ Advanced username analysis complete.")

        else:
            st.markdown("<div class='empty-state'>// Enter a name to begin OSINT analysis</div>", unsafe_allow_html=True)
# # ══════════════════════════════════════════════
# # TAB 2 — EMAIL INTELLIGENCE
# # ══════════════════════════════════════════════
# with tab2:
#     L, R = st.columns([1, 1.8], gap="large")

#     with L:
#         st.markdown("<div class='mod-card'>", unsafe_allow_html=True)
#         st.markdown("<span class='mod-icon'>📧</span><div class='mod-title'>Email Intelligence</div>", unsafe_allow_html=True)
#         email = st.text_input("Email Address", placeholder="e.g. user@example.com", key="email_in").strip().lower()
#         run_email = st.button("🔍 ANALYZE EMAIL", key="btn_email")
#         st.markdown("</div>", unsafe_allow_html=True)

#     with R:
#         if run_email:
#             if not email:
#                 st.error("❌ Enter an email address.")
#             elif not valid_email(email):
#                 st.error(f"❌ Invalid email format: {repr(email)}")
#             else:
#                 add_log("Email Intel", email)
#                 local, domain = email.split("@", 1)

#                 intel_banner(
#                     "Email Identity Review",
#                     "This view shows address structure, provider clues, mail-routing records, public profile indicators, and domain intelligence."
#                 )

#                 mini_stats([
#                     ("Address", email),
#                     ("Username", local),
#                     ("Domain", domain),
#                 ])

#                 section("BASIC INFORMATION")
#                 row("📧", "Email", email)
#                 row("👤", "Username Part", local)
#                 row("🌐", "Domain", domain)

#                 providers = {
#                     "gmail.com": "Google Gmail",
#                     "yahoo.com": "Yahoo Mail",
#                     "outlook.com": "Microsoft Outlook",
#                     "hotmail.com": "Microsoft Hotmail",
#                     "live.com": "Microsoft Live",
#                     "icloud.com": "Apple iCloud Mail",
#                     "proton.me": "Proton Mail",
#                     "protonmail.com": "Proton Mail",
#                     "zoho.com": "Zoho Mail",
#                 }
#                 provider = providers.get(domain.lower(), f"Custom / Organization domain ({domain})")
#                 row("🏢", "Provider", provider)

#                 disposable = check_email_disposable(domain)
#                 row("🗑️", "Disposable", "Yes" if disposable else "No", "warn" if disposable else "good")

#                 section("DNS RECORDS")
#                 with st.spinner("Resolving domain DNS..."):
#                     dns_recs = fetch_dns_records(domain)

#                 dns_rows = []
#                 for rtype, vals in dns_recs.items():
#                     if vals:
#                         for v in vals:
#                             dns_rows.append((rtype, v))
#                     else:
#                         dns_rows.append((rtype, "—"))
#                 table(["Record Type", "Value"], dns_rows)

#                 section("DOMAIN HOST INFORMATION")
#                 try:
#                     ip_addr = socket.gethostbyname(domain)
#                     row("🧭", "Domain IP", ip_addr)
#                     try:
#                         hostname = socket.gethostbyaddr(ip_addr)[0]
#                         row("🔁", "Reverse DNS", hostname)
#                     except Exception:
#                         row("🔁", "Reverse DNS", "Not available", "warn")

#                     geo = fetch_ip_data(ip_addr)
#                     if geo.get("status") == "success":
#                         row("🌍", "Hosted In", f"{geo.get('city','?')}, {geo.get('country','?')}")
#                         row("📡", "Hosting ISP", geo.get("isp", "N/A"))
#                         row("🏭", "Hosting / DC", "Yes" if geo.get("hosting") else "No", "warn" if geo.get("hosting") else "good")
#                 except Exception as e:
#                     row("❌", "DNS Resolution", f"Failed: {e}", "bad")

#                 section("GRAVATAR CHECK")
#                 grav_img, grav_url = gravatar_url(email)
#                 try:
#                     gr = requests.get(grav_img, timeout=5)
#                     if gr.status_code == 200:
#                         row("🖼️", "Gravatar", "Profile image found", "good")
#                         st.image(grav_img, width=80)
#                     else:
#                         row("🖼️", "Gravatar", "No public Gravatar found", "warn")
#                 except Exception:
#                     row("🖼️", "Gravatar", "Could not check", "warn")

#                 section("BREACH CHECK")
#                 with st.spinner("Checking public breach signal..."):
#                     breach_count, breaches = fetch_email_breach_count(email)

#                 if breach_count is None:
#                     row("⚠️", "Breach Status", "Check unavailable / API not configured", "warn")
#                 elif breach_count == 0:
#                     row("✅", "Breach Status", "No public breach found", "good")
#                 else:
#                     row("🚨", "Breaches Found", str(breach_count), "bad")
#                     rows = []
#                     for b in breaches[:10]:
#                         rows.append((
#                             b.get("Name", "N/A"),
#                             b.get("Domain", "N/A"),
#                             str(b.get("BreachDate", "N/A"))
#                         ))
#                     if rows:
#                         table(["Breach", "Domain", "Date"], rows)

#                 st.success("✅ Email analysis complete.")
#         else:
#             st.markdown("<div class='empty-state'>// Enter an email address to begin analysis</div>", unsafe_allow_html=True)

# ══════════════════════════════════════════════
# TAB 3 — IP INTELLIGENCE
# ══════════════════════════════════════════════
with tab3:
    L, R = st.columns([1, 1.8], gap="large")
    with L:
        st.markdown("<div class='mod-card'>", unsafe_allow_html=True)
        st.markdown("<span class='mod-icon'>🌐</span><div class='mod-title'>IP Intelligence</div>", unsafe_allow_html=True)
        ip_in = st.text_input("IP Address", placeholder="e.g. 8.8.8.8", key="ip_in")
        run_ip = st.button("🔍 ANALYZE IP", key="btn_ip")
        st.markdown("</div>", unsafe_allow_html=True)

    with R:
        ip_val = st.session_state.get("ip_in", ip_in).strip()
        if run_ip:
            if not ip_val:
                st.error("❌ Enter an IP address.")
            elif not valid_ip(ip_val):
                st.error("❌ Invalid format. Example: 8.8.8.8")
            else:
                with st.spinner("Fetching geolocation..."):
                    data = fetch_ip_data(ip_val)

                if data.get("status") != "success":
                    st.error(f"❌ {data.get('message','Lookup failed')}. Private/reserved IPs cannot be geolocated.")
                else:
                    add_log("IP Intel", ip_val)

                    section("GEOLOCATION")
                    row("🌍", "Country", f"{data.get('country','N/A')} ({data.get('countryCode','N/A')})")
                    row("🏙", "City", data.get("city") or "N/A")
                    row("🗺", "Region", data.get("regionName") or "N/A")
                    row("📮", "ZIP Code", data.get("zip") or "N/A")
                    row("📍", "Coordinates", f"{data.get('lat','?')}°, {data.get('lon','?')}°")
                    row("🕒", "Timezone", data.get("timezone","N/A"))
                    off = data.get("offset", 0) // 3600
                    row("⏱", "UTC Offset", f"UTC{'+' if off >= 0 else ''}{off}")

                    section("NETWORK INFORMATION")
                    row("📡", "ISP", data.get("isp","N/A"))
                    row("🏢", "Organization", data.get("org","N/A"))
                    row("🔗", "AS Number", data.get("as","N/A"))
                    row("🏷", "AS Name", data.get("asname","N/A"))

                    section("RISK & FLAG ANALYSIS")
                    row("📱", "Mobile Network", "⚠️ Yes" if data.get("mobile") else "No", "warn" if data.get("mobile") else "good")
                    row("🛡", "Proxy / VPN", "⚠️ Detected" if data.get("proxy") else "Clean", "warn" if data.get("proxy") else "good")
                    row("🏭", "Hosting / DC", "⚠️ Yes" if data.get("hosting") else "No", "warn" if data.get("hosting") else "good")

                    section("REVERSE IP LOOKUP")
                    with st.spinner("Checking domains on this IP..."):
                        rev_domains = fetch_reverse_ip(ip_val)
                    if rev_domains:
                        row("🌐", "Domains Found", f"{len(rev_domains)} domain(s) on this IP")
                        table(["#", "Domain"], [(str(i+1), d) for i, d in enumerate(rev_domains)])
                    else:
                        row("🌐", "Reverse IP", "No domains found or not accessible")

                    section("OPEN PORT SCAN (Common Ports)")
                    st.markdown("""<div style='font-family:Share Tech Mono,monospace;font-size:.72rem;
                        color:#f0a030;margin-bottom:8px;'>
                        ⚠️ Scanning common ports — this may take 10–20 seconds...</div>""",
                        unsafe_allow_html=True)
                    with st.spinner("Scanning ports..."):
                        open_ports = fetch_open_ports(ip_val)
                    if open_ports:
                        table(["Port", "Service", "Status"],
                              [(str(p), s, "🟢 OPEN") for p, s, _ in open_ports])
                    else:
                        row("🔒", "Open Ports", "No common open ports found", "good")

                    section("LOCATION MAP")
                    lat, lon = data["lat"], data["lon"]
                    m = folium.Map(location=[lat, lon], zoom_start=10, tiles="CartoDB dark_matter")
                    folium.CircleMarker(
                        [lat, lon], radius=14,
                        color="#1e88e5", fill=True, fill_color="#4ab8f8", fill_opacity=.7,
                        tooltip=f"{ip_val} → {data.get('city')}, {data.get('country')}"
                    ).add_to(m)
                    folium.Marker(
                        [lat, lon],
                        popup=f"<b>{ip_val}</b><br>{data.get('city')}, {data.get('country')}<br>{data.get('isp')}",
                        icon=folium.Icon(color="blue", icon="info-sign")
                    ).add_to(m)
                    st_folium(m, width=None, height=300, returned_objects=[])

                    st.success("✅ IP analysis complete.")
        else:
            st.markdown("<div class='empty-state'>// Enter an IP address to begin deep analysis</div>", unsafe_allow_html=True)

# ══════════════════════════════════════════════
# TAB 4 — IMAGE METADATA
# ══════════════════════════════════════════════
with tab4:
    L, R = st.columns([1, 1.8], gap="large")

    with L:
        st.markdown("<div class='mod-card'>", unsafe_allow_html=True)
        st.markdown("<span class='mod-icon'>🖼️</span><div class='mod-title'>Image Metadata</div>", unsafe_allow_html=True)
        uploaded_file = st.file_uploader("Upload Image", type=["jpg", "jpeg", "png"])
        run_meta = st.button("🔍 EXTRACT METADATA", key="btn_meta")
        st.markdown("</div>", unsafe_allow_html=True)

    with R:
        if run_meta:
            if not uploaded_file:
                st.error("❌ Upload an image file.")
            else:
                add_log("Metadata", uploaded_file.name)

                file_bytes = uploaded_file.read()

                # ───────── FILE INFO ─────────
                section("FILE INFORMATION")
                row("📄", "Filename", uploaded_file.name)
                row("📦", "File Size", f"{len(file_bytes)//1024} KB")
                row("🧾", "File Type", uploaded_file.type)

                # ───────── HASHES ─────────
                section("FORENSIC HASHES")
                hashes = generate_hashes(file_bytes)
                for k, v in hashes.items():
                    row("🔑", k, v)

                uploaded_file.seek(0)
                metadata, gps_data = extract_metadata(uploaded_file)

                # ───────── EXIF ─────────
                section("EXIF METADATA")
                if metadata:
                    cleaned_rows = []
                    for k, v in metadata.items():
                        if is_useful_metadata_field(k, v):
                            cleaned_rows.append((k, clean_exif_value(v)))

                    if cleaned_rows:
                        table(["Field", "Value"], cleaned_rows[:30])
                    else:
                        row("⚠️", "Status", "EXIF exists but not useful", "warn")
                else:
                    row("⚠️", "Status", "No EXIF metadata found", "warn")

                # ───────── GPS ─────────
                section("GPS INFORMATION")
                if gps_data:
                    lat, lon = extract_gps_coordinates(gps_data)

                    if lat is not None and lon is not None:
                        row("📍", "Latitude", f"{lat:.6f}", "good")
                        row("📍", "Longitude", f"{lon:.6f}", "good")

                        maps_url = google_maps_link(lat, lon)
                        st.markdown(
                            f"""<div class='res-row'>
                                <span class='res-label'>🗺 Google Maps</span>
                                <span class='res-val good'>
                                    <a href="{maps_url}" target="_blank" style="color:#4ab8f8;">
                                        Open Location
                                    </a>
                                </span>
                            </div>""",
                            unsafe_allow_html=True
                        )
                    else:
                        row("⚠️", "GPS Status", "No usable coordinates found", "warn")
                else:
                    row("❌", "GPS Data", "Not Available", "warn")

                # ───────── STEGO ─────────
                section("STEGO ANALYSIS")
                row("🧠", "Result", detect_stego(file_bytes))

                st.success("✅ Metadata analysis complete.")
        else:
            st.markdown("<div class='empty-state'>// Upload image to extract metadata</div>", unsafe_allow_html=True)

# ══════════════════════════════════════════════
# TAB 5 — ACTIVITY LOG
# ══════════════════════════════════════════════
with tab5:
    hc, bc = st.columns([4,1])
    with hc:
        section("SESSION ACTIVITY LOG")
    with bc:
        if st.button("🗑 CLEAR", key="clear_log"):
            st.session_state.log = []
            st.session_state.q_count = 0
            st.rerun()

    if st.session_state.log:
        st.markdown("""<div style='background:#060f1e;border:1px solid #0a2030;border-radius:10px;padding:16px 20px;'>
        <div style='display:grid;grid-template-columns:80px 120px 1fr;gap:8px;
            font-family:Share Tech Mono,monospace;font-size:.66rem;color:#1a4a68;
            letter-spacing:.1em;border-bottom:1px solid #0a2030;padding-bottom:8px;margin-bottom:6px;'>
            <span>TIME</span><span>MODULE</span><span>QUERY</span>
        </div>""", unsafe_allow_html=True)
        for e in st.session_state.log:
            st.markdown(f"""<div style='display:flex;gap:10px;padding:7px 0;border-bottom:1px solid #071828;
                font-family:Share Tech Mono,monospace;font-size:.76rem;'>
                <span style='color:#1e5a84;min-width:80px;'>{e['t']}</span>
                <span style='color:#1e88e5;min-width:120px;'>[{e['m']}]</span>
                <span style='color:#7aaccc;'>{e['q']}</span>
            </div>""", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)
    else:
        st.markdown("<div class='empty-state'>// No activity yet. Run any module to populate log.</div>", unsafe_allow_html=True)

# ─────────────────────────────────────────────
# FOOTER
# ─────────────────────────────────────────────
st.markdown("""
<div style='border-top:1px solid #0a2030;margin-top:32px;padding-top:14px;
    text-align:center;font-family:Share Tech Mono,monospace;font-size:.66rem;
    color:#0e2a44;letter-spacing:.1em;'>
    INFOSCOPE PRO &nbsp;//&nbsp; SELF-CONTAINED OSINT PLATFORM &nbsp;//&nbsp; FOR AUTHORIZED RESEARCH USE ONLY
</div>""", unsafe_allow_html=True)
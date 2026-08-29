import json
import torch
import torch.nn as nn
import streamlit as st
from PIL import Image
from torchvision import models, transforms
# ==========================================
# 1. PAGE CONFIGURATION
# ==========================================
st.set_page_config(
    page_title="PlantCare AI — Plant Disease Detection",
    page_icon="🌿",
    layout="centered"
)
# ==========================================
# SESSION STATE (for "Scan Another Leaf")
# ==========================================
if "reset_counter" not in st.session_state:
    st.session_state.reset_counter = 0
if "scan_active" not in st.session_state:
    st.session_state.scan_active = False
# ==========================================
# GLOBAL STYLE — SUPER 3D NATURE + GLASSMORPHISM
# ==========================================
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Sora:wght@400;600;700;800&family=Manrope:wght@400;500;600;700&display=swap');
:root {
    --leaf: #5eead4;
    --leaf-bright: #7bf1a8;
    --leaf-deep: #2fae65;
    --gold: #e0b25e;
    --ice: #7dd3fc;
    --glass: rgba(20, 58, 38, 0.40);
    --glass-strong: rgba(24, 68, 44, 0.55);
    --glass-border: rgba(140, 255, 180, 0.18);
    --text-soft: #cfe9d6;
    --text-dim: #93b8a0;
}
html, body, [class*="css"] {
    font-family: 'Manrope', sans-serif;
}
/* ---------- App background: layered depth + botanical dots ---------- */
.stApp {
    background-color: #050f0a;
    background-image:
        radial-gradient(circle at 12% 8%, rgba(94, 234, 212, 0.10) 0%, transparent 38%),
        radial-gradient(circle at 88% 15%, rgba(224, 178, 94, 0.07) 0%, transparent 32%),
        radial-gradient(circle at 50% 100%, rgba(47, 174, 101, 0.14) 0%, transparent 45%),
        radial-gradient(rgba(140, 255, 180, 0.10) 1px, transparent 1.4px),
        linear-gradient(160deg, #04100a 0%, #0a2417 45%, #0d2a1c 75%, #081a12 100%);
    background-size: auto, auto, auto, 26px 26px, auto;
    background-position: 0 0, 0 0, 0 0, 0 0, 0 0;
}
.block-container {
    padding-top: 2rem;
    max-width: 780px;
}
/* ---------- Floating Leaf Particles ---------- */
.leaf-particle {
    position: fixed;
    pointer-events: none;
    z-index: 0;
    opacity: 0.12;
    font-size: 18px;
    animation: leafFloat linear infinite;
}
@keyframes leafFloat {
    0% {
        transform: translateY(110vh) rotate(0deg) scale(0.8);
        opacity: 0;
    }
    10% { opacity: 0.12; }
    90% { opacity: 0.12; }
    100% {
        transform: translateY(-10vh) rotate(360deg) scale(1.1);
        opacity: 0;
    }
}
/* ---------- Hero ---------- */
.hero-wrap {
    text-align: center;
    padding: 6px 0 18px 0;
}
.hero-badge {
    display: inline-block;
    font-family: 'Sora', sans-serif;
    font-size: 11.5px;
    font-weight: 700;
    letter-spacing: 1.6px;
    color: var(--leaf-bright);
    background: rgba(94, 234, 212, 0.08);
    border: 1px solid rgba(94, 234, 212, 0.35);
    padding: 6px 16px;
    border-radius: 999px;
    box-shadow: 0 0 18px rgba(94, 234, 212, 0.15);
    margin-bottom: 18px;
    animation: badgePulse 3s ease-in-out infinite;
}
@keyframes badgePulse {
    0%, 100% { box-shadow: 0 0 18px rgba(94, 234, 212, 0.15); }
    50% { box-shadow: 0 0 30px rgba(94, 234, 212, 0.28); }
}
.hero-orb {
    width: 84px;
    height: 84px;
    margin: 0 auto 16px auto;
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 36px;
    background: radial-gradient(circle at 35% 30%, rgba(123, 241, 168, 0.55), rgba(21, 60, 40, 0.65) 70%);
    border: 1px solid rgba(140, 255, 180, 0.30);
    box-shadow:
        0 0 0 1px rgba(255,255,255,0.03) inset,
        0 12px 30px rgba(0,0,0,0.35),
        0 0 40px rgba(94, 234, 212, 0.20);
    animation: orbFloat 4s ease-in-out infinite;
}
@keyframes orbFloat {
    0%, 100% { transform: translateY(0); }
    50% { transform: translateY(-8px); }
}
.main-title {
    font-family: 'Sora', sans-serif;
    font-weight: 800;
    font-size: 42px;
    letter-spacing: -0.5px;
    background: linear-gradient(180deg, #f2fff5 10%, #a9e8bc 100%);
    -webkit-background-clip: text;
    background-clip: text;
    color: transparent;
    margin-bottom: 6px;
}
.subtitle {
    color: var(--text-soft);
    font-size: 16.5px;
    max-width: 480px;
    margin: 0 auto 4px auto;
    line-height: 1.5;
}
.hero-hint {
    color: var(--text-dim);
    font-size: 13.5px;
    margin-top: 10px;
}
/* ---------- Stats Row ---------- */
.stats-row {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 12px;
    margin: 20px 0;
}
.stat-card {
    background: var(--glass);
    backdrop-filter: blur(8px);
    border: 1px solid var(--glass-border);
    border-radius: 16px;
    padding: 18px 14px;
    text-align: center;
}
.stat-value {
    font-family: 'Sora', sans-serif;
    font-weight: 800;
    font-size: 22px;
    color: var(--leaf);
    margin-bottom: 4px;
}
.stat-label {
    font-size: 10.5px;
    font-weight: 600;
    letter-spacing: 1px;
    color: var(--text-dim);
    text-transform: uppercase;
}
/* ---------- Glass / nature cards ---------- */
.nature-card {
    background: var(--glass);
    backdrop-filter: blur(6px);
    border: 1px solid var(--glass-border);
    border-radius: 20px;
    padding: 24px 26px;
    margin: 16px 0;
    box-shadow: 0 10px 30px rgba(0,0,0,0.30);
    transition: transform 0.2s ease, box-shadow 0.2s ease;
}
.nature-card:hover {
    transform: translateY(-2px);
    box-shadow: 0 14px 36px rgba(0,0,0,0.38);
}
.section-heading {
    font-family: 'Sora', sans-serif;
    font-weight: 700;
    font-size: 19px;
    color: #eafff0;
    margin: 22px 0 4px 0;
}
/* ---------- Upload / camera widgets as elevated 3D card ---------- */
div[data-testid="stFileUploader"],
div[data-testid="stCameraInput"] {
    background: var(--glass-strong);
    border: 1.5px dashed rgba(140, 255, 180, 0.35);
    border-radius: 20px;
    padding: 14px;
    box-shadow: 0 10px 28px rgba(0,0,0,0.30), 0 0 26px rgba(94, 234, 212, 0.06);
}
div[data-testid="stFileUploaderDropzone"] {
    background: transparent;
}
/* Image-source selector as a pill toggle */
div[role="radiogroup"] {
    background: rgba(20, 58, 38, 0.35);
    border: 1px solid var(--glass-border);
    padding: 8px 14px;
    border-radius: 14px;
}
/* ---------- Buttons ---------- */
.stButton > button {
    border-radius: 14px;
    font-weight: 700;
    font-family: 'Manrope', sans-serif;
    padding: 11px 28px;
    border: 1px solid rgba(140, 255, 180, 0.30);
    transition: transform 0.15s ease, box-shadow 0.15s ease;
}
.stButton > button[kind="primary"] {
    background: linear-gradient(135deg, #34d399, #16a06a);
    color: #04150c;
    box-shadow: 0 8px 24px rgba(52, 211, 153, 0.30);
}
.stButton > button:hover {
    transform: translateY(-1px);
    box-shadow: 0 10px 26px rgba(94, 234, 212, 0.20);
}
/* ---------- Preview image card ---------- */
.preview-card-label {
    font-size: 13px;
    letter-spacing: 0.5px;
    color: var(--text-dim);
    margin: 18px 0 6px 2px;
}
div[data-testid="stImage"] img {
    border-radius: 18px;
    border: 1px solid var(--glass-border);
    box-shadow: 0 12px 30px rgba(0,0,0,0.35);
}
/* ---------- Scanning animation ---------- */
.scan-container {
    text-align: center;
    padding: 40px 0;
}
.scan-ring {
    width: 100px;
    height: 100px;
    border-radius: 50%;
    border: 3px solid rgba(94, 234, 212, 0.2);
    border-top-color: var(--leaf-bright);
    animation: scanSpin 1s linear infinite;
    margin: 0 auto 16px auto;
    position: relative;
}
.scan-ring::after {
    content: '🔬';
    position: absolute;
    top: 50%;
    left: 50%;
    transform: translate(-50%, -50%);
    font-size: 30px;
}
.scan-pulse {
    width: 100px;
    height: 100px;
    border-radius: 50%;
    position: absolute;
    top: 50%;
    left: 50%;
    transform: translate(-50%, -50%);
    border: 2px solid rgba(94, 234, 212, 0.15);
    animation: scanPulse 1.5s ease-in-out infinite;
}
.scan-text {
    font-family: 'Sora', sans-serif;
    font-weight: 600;
    font-size: 15px;
    color: var(--leaf);
    margin-top: 8px;
}
@keyframes scanSpin {
    to { transform: rotate(360deg); }
}
@keyframes scanPulse {
    0% { width: 80px; height: 80px; opacity: 0.6; }
    100% { width: 160px; height: 160px; opacity: 0; }
}
/* ---------- Result card ---------- */
.result-card {
    background: linear-gradient(160deg, rgba(24, 68, 44, 0.55), rgba(14, 40, 27, 0.55));
    border: 1px solid var(--glass-border);
    border-radius: 22px;
    padding: 28px 28px 24px 28px;
    margin: 18px 0;
    box-shadow: 0 16px 40px rgba(0,0,0,0.35);
    animation: resultReveal 0.5s ease-out;
}
@keyframes resultReveal {
    from { opacity: 0; transform: translateY(20px) scale(0.97); }
    to { opacity: 1; transform: translateY(0) scale(1); }
}
.result-card.conf-high { box-shadow: 0 16px 40px rgba(0,0,0,0.35), 0 0 34px rgba(52, 211, 153, 0.18); }
.result-card.conf-medium { box-shadow: 0 16px 40px rgba(0,0,0,0.35), 0 0 34px rgba(224, 178, 94, 0.16); }
.result-card.conf-low { box-shadow: 0 16px 40px rgba(0,0,0,0.35), 0 0 34px rgba(125, 211, 252, 0.14); }
.result-eyebrow {
    font-size: 12.5px;
    font-weight: 700;
    letter-spacing: 1.4px;
    color: var(--text-dim);
    margin-bottom: 10px;
}
.result-plant {
    font-family: 'Sora', sans-serif;
    font-size: 26px;
    font-weight: 700;
    color: #f2fff5;
}
.result-disease {
    font-size: 18px;
    font-weight: 600;
    color: var(--gold);
    margin: 4px 0 18px 0;
}
.result-disease.result-healthy {
    color: var(--leaf-bright);
}
.confidence-block { margin-top: 6px; }
.confidence-label {
    font-size: 12px;
    letter-spacing: 1.2px;
    color: var(--text-dim);
    margin-bottom: 6px;
}
.confidence-row {
    display: flex;
    align-items: baseline;
    justify-content: space-between;
    margin-bottom: 8px;
}
.confidence-value {
    font-family: 'Sora', sans-serif;
    font-size: 30px;
    font-weight: 800;
}
.confidence-value.conf-high { color: var(--leaf-bright); }
.confidence-value.conf-medium { color: var(--gold); }
.confidence-value.conf-low { color: var(--ice); }
.confidence-tag {
    font-size: 11.5px;
    font-weight: 700;
    letter-spacing: 1px;
    padding: 5px 12px;
    border-radius: 999px;
}
.confidence-tag.conf-high { color: #04150c; background: var(--leaf-bright); }
.confidence-tag.conf-medium { color: #241705; background: var(--gold); }
.confidence-tag.conf-low { color: #04202b; background: var(--ice); }
.confidence-track {
    width: 100%;
    height: 12px;
    border-radius: 999px;
    background: rgba(255,255,255,0.06);
    overflow: hidden;
    border: 1px solid rgba(255,255,255,0.05);
}
.confidence-fill {
    height: 100%;
    border-radius: 999px;
    transition: width 0.8s cubic-bezier(0.22, 1, 0.36, 1);
}
.confidence-fill.conf-high { background: linear-gradient(90deg, #2fae65, #7bf1a8); }
.confidence-fill.conf-medium { background: linear-gradient(90deg, #b6822f, #e0b25e); }
.confidence-fill.conf-low { background: linear-gradient(90deg, #2d84a8, #7dd3fc); }
/* ---------- Remedy cards ---------- */
.remedy-card {
    padding-top: 20px;
    animation: resultReveal 0.6s ease-out;
}
.remedy-title {
    font-family: 'Sora', sans-serif;
    font-size: 17px;
    font-weight: 700;
    color: #eafff0;
    margin-bottom: 14px;
}
.remedy-item {
    font-size: 14.5px;
    color: var(--text-soft);
    padding: 10px 4px;
    border-bottom: 1px solid rgba(255,255,255,0.05);
    display: flex;
    align-items: flex-start;
    gap: 10px;
}
.remedy-item:last-child { border-bottom: none; }
.remedy-num {
    min-width: 24px;
    height: 24px;
    border-radius: 8px;
    background: rgba(94, 234, 212, 0.12);
    color: var(--leaf);
    font-size: 12px;
    font-weight: 700;
    display: flex;
    align-items: center;
    justify-content: center;
    flex-shrink: 0;
    margin-top: 1px;
}
/* ---------- Low confidence warning ---------- */
.low-conf-warning {
    background: rgba(125, 211, 252, 0.10);
    border: 1px solid rgba(125, 211, 252, 0.30);
    border-radius: 14px;
    padding: 14px 18px;
    margin-bottom: 16px;
    color: var(--ice);
    font-size: 14px;
    display: flex;
    align-items: center;
    gap: 10px;
}
/* ---------- Disclaimer ---------- */
.disclaimer {
    font-size: 12px;
    color: var(--text-dim);
    text-align: center;
    margin: 18px 0 6px 0;
    line-height: 1.5;
}
.disclaimer-label {
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 6px;
    margin-bottom: 4px;
    font-weight: 700;
    font-size: 11px;
    letter-spacing: 1px;
    color: var(--text-dim);
}
/* ---------- Footer ---------- */
.footer {
    text-align: center;
    padding: 28px 0 40px 0;
    border-top: 1px solid rgba(140, 255, 180, 0.08);
    margin-top: 30px;
}
.footer-text {
    font-size: 12px;
    color: var(--text-dim);
}
.footer-brand {
    font-family: 'Sora', sans-serif;
    font-weight: 700;
    color: var(--leaf);
}
/* ---------- Sidebar ---------- */
section[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #0a2115, #061309);
    border-right: 1px solid rgba(140, 255, 180, 0.08);
}
.sidebar-logo {
    font-family: 'Sora', sans-serif;
    font-weight: 700;
    font-size: 19px;
    color: #eafff0;
    margin-bottom: 2px;
}
.sidebar-tag {
    font-size: 12px;
    color: var(--text-dim);
    margin-bottom: 18px;
}
/* Alerts */
div[data-testid="stAlert"] {
    border-radius: 15px;
}
/* ---------- Responsive ---------- */
@media (max-width: 768px) {
    .main-title { font-size: 32px; }
    .subtitle { font-size: 15px; }
    .result-plant { font-size: 22px; }
    .confidence-value { font-size: 26px; }
    .stats-row { grid-template-columns: 1fr; }
}
@media (max-width: 480px) {
    .block-container { padding-left: 1rem; padding-right: 1rem; }
    .main-title { font-size: 27px; }
    .nature-card, .result-card { padding: 18px 18px; }
}
</style>
""", unsafe_allow_html=True)
# ==========================================
# FLOATING LEAF PARTICLES
# ==========================================
LEAF_PARTICLES = ['🌿', '🍃', '🌱', '☘️', '🌾', '🍀']
particle_html = '<div style="position:fixed;top:0;left:0;width:100%;height:100%;pointer-events:none;z-index:0;overflow:hidden;">'
import random
random.seed(42)
for i in range(10):
    emoji = LEAF_PARTICLES[i % len(LEAF_PARTICLES)]
    left = random.randint(3, 94)
    duration = random.randint(12, 28)
    delay = random.randint(0, 15)
    size = random.randint(14, 24)
    particle_html += (
        f'<div class="leaf-particle" style="'
        f'left:{left}%;'
        f'animation-duration:{duration}s;'
        f'animation-delay:{delay}s;'
        f'font-size:{size}px;'
        f'">{emoji}</div>'
    )
particle_html += '</div>'
st.markdown(particle_html, unsafe_allow_html=True)
# ==========================================
# 2. HERO SECTION
# ==========================================
st.markdown("""
<div class="hero-wrap">
    <div class="hero-badge">AI-POWERED AGRICULTURE</div>
    <div class="hero-orb">🌱</div>
    <div class="main-title">AI Plant Doctor</div>
    <div class="subtitle">Upload a leaf image and let AI identify potential plant diseases in seconds.</div>
</div>
""", unsafe_allow_html=True)
# ==========================================
# LANGUAGE SELECTION + SIDEBAR
# ==========================================
st.sidebar.markdown(
    '<div class="sidebar-logo">🌿 PlantCare AI</div>'
    '<div class="sidebar-tag">AI Plant Doctor</div>',
    unsafe_allow_html=True
)
language = st.sidebar.selectbox(
    "🌐 Language / భాష",
    ["English", "తెలుగు"]
)
st.sidebar.markdown("---")
st.sidebar.header("🌿 About")
st.sidebar.write(
    "PlantCare AI identifies plant leaf diseases from a photo "
    "and suggests simple management steps, in English or Telugu."
)
st.sidebar.write(
    "Upload a clear photo of a single leaf for the best result."
)
# ==========================================
# STATS ROW
# ==========================================
stats_html = '<div class="stats-row">'
stats_html += '<div class="stat-card"><div class="stat-value">25K+</div><div class="stat-label">Images Trained</div></div>'
stats_html += '<div class="stat-card"><div class="stat-value">38</div><div class="stat-label">Disease Classes</div></div>'
stats_html += '<div class="stat-card"><div class="stat-value">96%+</div><div class="stat-label">Accuracy</div></div>'
stats_html += '</div>'
st.markdown(stats_html, unsafe_allow_html=True)
# ==========================================
# 3. LOAD CLASS NAMES
# ==========================================
with open("dataset_split.json", "r") as f:
    split_data = json.load(f)
class_names = split_data["classes"]
NUM_CLASSES = len(class_names)
# ==========================================
# 4. DEVICE
# ==========================================
device = torch.device(
    "cuda" if torch.cuda.is_available() else "cpu"
)
# ==========================================
# 5. IMAGE TRANSFORMATION
# ==========================================
transform = transforms.Compose([
    transforms.Resize((224, 224)),
    transforms.ToTensor(),
    transforms.Normalize(
        mean=[0.485, 0.456, 0.406],
        std=[0.229, 0.224, 0.225]
    )
])
# ==========================================
# 6. LOAD MOBILE NET V2
# ==========================================
@st.cache_resource
def load_model():
    model = models.mobilenet_v2(weights=None)
    # Replace original classifier
    model.classifier[1] = nn.Linear(
        model.last_channel,
        NUM_CLASSES
    )
    # Load our trained model
    checkpoint = torch.load(
        "best_model.pth",
        map_location=device
    )
    # Handle either a raw state_dict or a checkpoint dictionary
    if isinstance(checkpoint, dict) and "model_state_dict" in checkpoint:
        model.load_state_dict(checkpoint["model_state_dict"])
    else:
        model.load_state_dict(checkpoint)
    model = model.to(device)
    model.eval()
    return model
# ==========================================
# 7. LOAD MODEL (quiet — no technical banner)
# ==========================================
with st.spinner(
    "AI మోడల్‌ను లోడ్ చేస్తోంది..." if language == "తెలుగు" else "Waking up the AI plant doctor..."
):
    model = load_model()
# ==========================================
# 8. IMAGE INPUT — CAMERA OR UPLOAD
# ==========================================
st.markdown(
    f'<div class="section-heading">📸 '
    f'{"ఆకు ఫోటోను జోడించండి" if language == "తెలుగు" else "Add a leaf photo"}'
    f'</div>',
    unsafe_allow_html=True
)
st.markdown(
    f'<div class="hero-hint" style="margin-top:-4px;margin-bottom:10px;">'
    f'{"ఉత్తమ ఫలితాల కోసం, ఒకే ఆకు యొక్క స్పష్టమైన ఫోటోను ఉపయోగించండి." if language == "తెలుగు" else "For best results, use a clear image of a single leaf."}'
    f'</div>',
    unsafe_allow_html=True
)
input_method = st.radio(
    "Image source",
    ["📷 Capture Photo", "📁 Upload Image"],
    horizontal=True,
    label_visibility="collapsed"
)
uploaded_file = None
reset_key = st.session_state.reset_counter
if input_method == "📷 Capture Photo":
    camera_photo = st.camera_input(
        "Point your camera at a clear leaf and take a photo",
        key=f"leaf_camera_{reset_key}"
    )
    if camera_photo is not None:
        uploaded_file = camera_photo
else:
    uploaded_file = st.file_uploader(
        "📁 Choose a leaf image (JPG / PNG)",
        type=["jpg", "jpeg", "png"],
        key=f"leaf_uploader_{reset_key}"
    )
# ==========================================
# 🌿 DISEASE REMEDY DATABASE
# ==========================================
REMEDIES = {
    "Apple___Apple_scab": {
        "English": {
            "name": "Apple Scab",
            "remedy": [
                "Remove and destroy fallen infected leaves.",
                "Prune the tree to improve air circulation.",
                "Avoid prolonged leaf wetness.",
                "Use disease-resistant varieties where available.",
                "Use fungicides only according to locally approved labels."
            ]
        },
        "తెలుగు": {
            "name": "ఆపిల్ స్కాబ్",
            "remedy": [
                "వ్యాధి సోకిన పడిపోయిన ఆకులను తొలగించండి.",
                "గాలి ప్రసరణ మెరుగుపడేలా కొమ్మలను కత్తిరించండి.",
                "ఆకులు ఎక్కువసేపు తడిగా ఉండకుండా చూడండి.",
                "సాధ్యమైనప్పుడు వ్యాధి నిరోధక రకాలను ఎంచుకోండి.",
                "స్థానికంగా అనుమతించబడిన మందులను లేబుల్ సూచనల ప్రకారం మాత్రమే వాడండి."
            ]
        }
    },
    "Apple___Black_rot": {
        "English": {
            "name": "Apple Black Rot",
            "remedy": [
                "Remove infected fruit and mummified fruit.",
                "Prune dead branches and cankers.",
                "Remove pruned infected material from the orchard.",
                "Improve tree air circulation.",
                "Avoid injuries to fruit and branches."
            ]
        },
        "తెలుగు": {
            "name": "ఆపిల్ బ్లాక్ రాట్",
            "remedy": [
                "వ్యాధి సోకిన పండ్లు మరియు ఎండిపోయిన పండ్లను తొలగించండి.",
                "చనిపోయిన కొమ్మలు మరియు క్యాంకర్లను కత్తిరించండి.",
                "కత్తిరించిన వ్యాధిగ్రస్త భాగాలను తోట నుండి తొలగించండి.",
                "చెట్టులో గాలి ప్రసరణను మెరుగుపరచండి.",
                "పండ్లు మరియు కొమ్మలకు గాయాలు కాకుండా జాగ్రత్త వహించండి."
            ]
        }
    },
    "Apple___Cedar_apple_rust": {
        "English": {
            "name": "Cedar Apple Rust",
            "remedy": [
                "Use resistant apple varieties where available.",
                "Monitor nearby cedar or juniper hosts.",
                "Remove infected plant material where appropriate.",
                "Improve orchard sanitation.",
                "Follow local disease-management recommendations."
            ]
        },
        "తెలుగు": {
            "name": "సీడార్ ఆపిల్ రస్ట్",
            "remedy": [
                "సాధ్యమైనప్పుడు వ్యాధి నిరోధక ఆపిల్ రకాలను ఎంచుకోండి.",
                "దగ్గరలో ఉన్న సీడార్ లేదా జునిపర్ మొక్కలను పరిశీలించండి.",
                "అవసరమైన చోట వ్యాధిగ్రస్త భాగాలను తొలగించండి.",
                "తోట పరిశుభ్రతను మెరుగుపరచండి.",
                "స్థానిక వ్యవసాయ నిపుణుల సూచనలను పాటించండి."
            ]
        }
    },
    "Cherry_(including_sour)___Powdery_mildew": {
        "English": {
            "name": "Cherry Powdery Mildew",
            "remedy": [
                "Remove heavily infected leaves or shoots.",
                "Improve air circulation around the plant.",
                "Avoid excessive nitrogen fertilizer.",
                "Keep the canopy open through proper pruning.",
                "Use approved fungicides only when necessary."
            ]
        },
        "తెలుగు": {
            "name": "చెర్రీ పౌడరీ మిల్డ్యూ",
            "remedy": [
                "తీవ్రంగా వ్యాధి సోకిన ఆకులు లేదా కొమ్మలను తొలగించండి.",
                "మొక్క చుట్టూ గాలి ప్రసరణను మెరుగుపరచండి.",
                "అధిక నైట్రోజన్ ఎరువులను నివారించండి.",
                "సరైన కత్తిరింపుతో చెట్టు లోపలి భాగాన్ని తెరిచి ఉంచండి.",
                "అవసరమైనప్పుడు మాత్రమే అనుమతించబడిన శిలీంద్రనాశకాలను వాడండి."
            ]
        }
    },
    "Corn_(maize)___Cercospora_leaf_spot Gray_leaf_spot": {
        "English": {
            "name": "Corn Gray Leaf Spot",
            "remedy": [
                "Use resistant hybrids where available.",
                "Rotate crops where practical.",
                "Manage infected crop residue.",
                "Scout fields regularly.",
                "Use locally recommended fungicide programs when necessary."
            ]
        },
        "తెలుగు": {
            "name": "మొక్కజొన్న గ్రే లీఫ్ స్పాట్",
            "remedy": [
                "సాధ్యమైనప్పుడు వ్యాధి నిరోధక హైబ్రిడ్లను ఉపయోగించండి.",
                "సాధ్యమైన చోట పంట మార్పిడి చేయండి.",
                "వ్యాధిగ్రస్త పంట అవశేషాలను సరిగ్గా నిర్వహించండి.",
                "పొలాన్ని క్రమం తప్పకుండా పరిశీలించండి.",
                "అవసరమైనప్పుడు స్థానిక సిఫార్సుల ప్రకారం మందులను ఉపయోగించండి."
            ]
        }
    },
    "Corn_(maize)___Common_rust": {
        "English": {
            "name": "Corn Common Rust",
            "remedy": [
                "Use resistant corn hybrids.",
                "Monitor young leaves regularly.",
                "Maintain good crop management.",
                "Consider treatment only when disease pressure justifies it.",
                "Follow local agricultural recommendations."
            ]
        },
        "తెలుగు": {
            "name": "మొక్కజొన్న కామన్ రస్ట్",
            "remedy": [
                "వ్యాధి నిరోధక మొక్కజొన్న హైబ్రిడ్లను ఉపయోగించండి.",
                "చిన్న ఆకులను క్రమం తప్పకుండా పరిశీలించండి.",
                "పంటను సక్రమంగా నిర్వహించండి.",
                "వ్యాధి తీవ్రత ఎక్కువగా ఉన్నప్పుడు మాత్రమే చికిత్సను పరిగణించండి.",
                "స్థానిక వ్యవసాయ సిఫార్సులను పాటించండి."
            ]
        }
    },
    "Corn_(maize)___Northern_Leaf_Blight": {
        "English": {
            "name": "Corn Northern Leaf Blight",
            "remedy": [
                "Use resistant hybrids.",
                "Rotate crops where practical.",
                "Manage infected crop debris.",
                "Scout fields for early symptoms.",
                "Use fungicides only when recommended for the crop and situation."
            ]
        },
        "తెలుగు": {
            "name": "మొక్కజొన్న నార్తర్న్ లీఫ్ బ్లైట్",
            "remedy": [
                "వ్యాధి నిరోధక హైబ్రిడ్లను ఉపయోగించండి.",
                "సాధ్యమైన చోట పంట మార్పిడి చేయండి.",
                "వ్యాధిగ్రస్త పంట అవశేషాలను నిర్వహించండి.",
                "ప్రారంభ లక్షణాల కోసం పొలాన్ని పరిశీలించండి.",
                "పంట మరియు పరిస్థితికి సిఫార్సు చేసినప్పుడు మాత్రమే మందులను వాడండి."
            ]
        }
    },
    "Grape___Black_rot": {
        "English": {
            "name": "Grape Black Rot",
            "remedy": [
                "Remove infected berries and mummified fruit.",
                "Remove infected prunings.",
                "Improve air circulation around the fruit zone.",
                "Use resistant varieties where available.",
                "Begin disease protection early when conditions favor infection."
            ]
        },
        "తెలుగు": {
            "name": "ద్రాక్ష బ్లాక్ రాట్",
            "remedy": [
                "వ్యాధి సోకిన ద్రాక్ష గుత్తులు మరియు ఎండిపోయిన పండ్లను తొలగించండి.",
                "వ్యాధిగ్రస్త కత్తిరింపు భాగాలను తొలగించండి.",
                "పండ్ల చుట్టూ గాలి ప్రసరణను మెరుగుపరచండి.",
                "సాధ్యమైనప్పుడు వ్యాధి నిరోధక రకాలను ఎంచుకోండి.",
                "వ్యాధికి అనుకూల పరిస్థితులు ఉన్నప్పుడు ముందుగానే రక్షణ చర్యలు తీసుకోండి."
            ]
        }
    },
    "Grape___Leaf_blight_(Isariopsis_Leaf_Spot)": {
        "English": {
            "name": "Grape Leaf Blight",
            "remedy": [
                "Remove severely infected leaves.",
                "Remove infected plant debris.",
                "Improve canopy ventilation.",
                "Avoid prolonged leaf wetness.",
                "Follow local grape disease-management recommendations."
            ]
        },
        "తెలుగు": {
            "name": "ద్రాక్ష లీఫ్ బ్లైట్",
            "remedy": [
                "తీవ్రంగా వ్యాధి సోకిన ఆకులను తొలగించండి.",
                "వ్యాధిగ్రస్త మొక్కల అవశేషాలను తొలగించండి.",
                "మొక్కల మధ్య గాలి ప్రసరణను మెరుగుపరచండి.",
                "ఆకులు ఎక్కువసేపు తడిగా ఉండకుండా చూడండి.",
                "స్థానిక ద్రాక్ష వ్యాధి నిర్వహణ సూచనలను పాటించండి."
            ]
        }
    },
    "Orange___Haunglongbing_(Citrus_greening)": {
        "English": {
            "name": "Citrus Greening (HLB)",
            "remedy": [
                "There is currently no cure that eliminates HLB.",
                "Use healthy, certified planting material.",
                "Monitor and manage the Asian citrus psyllid.",
                "Have suspected trees professionally confirmed.",
                "Follow local citrus quarantine and removal guidance."
            ]
        },
        "తెలుగు": {
            "name": "సిట్రస్ గ్రీనింగ్ (HLB)",
            "remedy": [
                "HLB ను పూర్తిగా నయం చేసే చికిత్స ప్రస్తుతం లేదు.",
                "ఆరోగ్యకరమైన ధృవీకరించబడిన నాట్లను ఉపయోగించండి.",
                "ఆసియన్ సిట్రస్ సైలిడ్ పురుగును పర్యవేక్షించి నియంత్రించండి.",
                "అనుమానాస్పద చెట్లను నిపుణులతో నిర్ధారించండి.",
                "స్థానిక సిట్రస్ క్వారంటైన్ మరియు తొలగింపు సూచనలను పాటించండి."
            ]
        }
    },
    "Peach___Bacterial_spot": {
        "English": {
            "name": "Peach Bacterial Spot",
            "remedy": [
                "Use disease-resistant varieties where available.",
                "Remove severely affected plant material.",
                "Avoid working with plants when foliage is wet.",
                "Improve orchard sanitation.",
                "Follow locally approved bacterial-disease management practices."
            ]
        },
        "తెలుగు": {
            "name": "పీచ్ బ్యాక్టీరియల్ స్పాట్",
            "remedy": [
                "సాధ్యమైనప్పుడు వ్యాధి నిరోధక రకాలను ఉపయోగించండి.",
                "తీవ్రంగా ప్రభావితమైన మొక్క భాగాలను తొలగించండి.",
                "ఆకులు తడిగా ఉన్నప్పుడు మొక్కలను నిర్వహించకుండా ఉండండి.",
                "తోట పరిశుభ్రతను మెరుగుపరచండి.",
                "స్థానికంగా అనుమతించబడిన బ్యాక్టీరియా వ్యాధి నిర్వహణ పద్ధతులను పాటించండి."
            ]
        }
    },
    "Pepper,_bell___Bacterial_spot": {
        "English": {
            "name": "Pepper Bacterial Spot",
            "remedy": [
                "Use certified disease-free seed or transplants.",
                "Remove severely infected plants.",
                "Avoid overhead irrigation.",
                "Sanitize tools after working with infected plants.",
                "Rotate crops where practical."
            ]
        },
        "తెలుగు": {
            "name": "మిరప బ్యాక్టీరియల్ స్పాట్",
            "remedy": [
                "వ్యాధి రహిత ధృవీకరించబడిన విత్తనాలు లేదా నాట్లను ఉపయోగించండి.",
                "తీవ్రంగా వ్యాధి సోకిన మొక్కలను తొలగించండి.",
                "పై నుంచి నీరు పోయడాన్ని నివారించండి.",
                "వ్యాధిగ్రస్త మొక్కల తర్వాత పనిముట్లను శుభ్రపరచండి.",
                "సాధ్యమైనప్పుడు పంట మార్పిడి చేయండి."
            ]
        }
    },
    "Potato___Early_blight": {
        "English": {
            "name": "Potato Early Blight",
            "remedy": [
                "Remove severely infected leaves.",
                "Maintain adequate plant nutrition.",
                "Avoid prolonged leaf wetness.",
                "Remove crop debris after harvest.",
                "Use resistant varieties and approved disease-management products where appropriate."
            ]
        },
        "తెలుగు": {
            "name": "బంగాళాదుంప ఎర్లీ బ్లైట్",
            "remedy": [
                "తీవ్రంగా వ్యాధి సోకిన ఆకులను తొలగించండి.",
                "మొక్కకు సరైన పోషకాలను అందించండి.",
                "ఆకులు ఎక్కువసేపు తడిగా ఉండకుండా చూడండి.",
                "కోత తర్వాత పంట అవశేషాలను తొలగించండి.",
                "సాధ్యమైనప్పుడు నిరోధక రకాలు మరియు అనుమతించబడిన నిర్వహణ ఉత్పత్తులను ఉపయోగించండి."
            ]
        }
    },
    "Potato___Late_blight": {
        "English": {
            "name": "Potato Late Blight",
            "remedy": [
                "Scout the crop regularly for new symptoms.",
                "Remove or destroy infected plants when practical.",
                "Keep foliage as dry as possible.",
                "Improve spacing and air circulation.",
                "Use locally recommended late-blight products according to the label."
            ]
        },
        "తెలుగు": {
            "name": "బంగాళాదుంప లేట్ బ్లైట్",
            "remedy": [
                "కొత్త లక్షణాల కోసం పొలాన్ని క్రమం తప్పకుండా పరిశీలించండి.",
                "సాధ్యమైనప్పుడు వ్యాధి సోకిన మొక్కలను తొలగించండి.",
                "ఆకులు వీలైనంత పొడిగా ఉండేలా చూడండి.",
                "మొక్కల మధ్య సరైన దూరం మరియు గాలి ప్రసరణ కల్పించండి.",
                "స్థానికంగా సిఫార్సు చేసిన లేట్ బ్లైట్ మందులను లేబుల్ ప్రకారం ఉపయోగించండి."
            ]
        }
    },
    "Squash___Powdery_mildew": {
        "English": {
            "name": "Squash Powdery Mildew",
            "remedy": [
                "Remove severely infected leaves.",
                "Improve air circulation.",
                "Avoid overcrowding.",
                "Water at the soil level when practical.",
                "Use resistant varieties where available."
            ]
        },
        "తెలుగు": {
            "name": "స్క్వాష్ పౌడరీ మిల్డ్యూ",
            "remedy": [
                "తీవ్రంగా వ్యాధి సోకిన ఆకులను తొలగించండి.",
                "గాలి ప్రసరణను మెరుగుపరచండి.",
                "మొక్కలను అధికంగా దగ్గరగా నాటవద్దు.",
                "సాధ్యమైనప్పుడు నేల దగ్గర నీరు పెట్టండి.",
                "సాధ్యమైనప్పుడు వ్యాధి నిరోధక రకాలను ఉపయోగించండి."
            ]
        }
    },
    "Strawberry___Leaf_scorch": {
        "English": {
            "name": "Strawberry Leaf Scorch",
            "remedy": [
                "Remove severely infected leaves.",
                "Improve air circulation.",
                "Avoid overhead watering.",
                "Remove infected plant debris.",
                "Maintain good field sanitation."
            ]
        },
        "తెలుగు": {
            "name": "స్ట్రాబెర్రీ లీఫ్ స్కార్చ్",
            "remedy": [
                "తీవ్రంగా వ్యాధి సోకిన ఆకులను తొలగించండి.",
                "గాలి ప్రసరణను మెరుగుపరచండి.",
                "పై నుంచి నీరు పోయడాన్ని నివారించండి.",
                "వ్యాధిగ్రస్త మొక్కల అవశేషాలను తొలగించండి.",
                "పొలం పరిశుభ్రతను పాటించండి."
            ]
        }
    },
    "Tomato___Bacterial_spot": {
        "English": {
            "name": "Tomato Bacterial Spot",
            "remedy": [
                "Use disease-free seed and transplants.",
                "Avoid working with wet plants.",
                "Avoid overhead irrigation.",
                "Remove severely infected plants.",
                "Sanitize tools and rotate crops."
            ]
        },
        "తెలుగు": {
            "name": "టమాటా బ్యాక్టీరియల్ స్పాట్",
            "remedy": [
                "వ్యాధి రహిత విత్తనాలు మరియు నాట్లను ఉపయోగించండి.",
                "మొక్కలు తడిగా ఉన్నప్పుడు వాటిని నిర్వహించవద్దు.",
                "పై నుంచి నీరు పోయడాన్ని నివారించండి.",
                "తీవ్రంగా వ్యాధి సోకిన మొక్కలను తొలగించండి.",
                "పనిముట్లను శుభ్రపరచి పంట మార్పిడి చేయండి."
            ]
        }
    },
    "Tomato___Early_blight": {
        "English": {
            "name": "Tomato Early Blight",
            "remedy": [
                "Remove infected lower leaves.",
                "Mulch around plants to reduce soil splash.",
                "Water at the base of plants.",
                "Remove plant debris after harvest.",
                "Maintain good plant nutrition."
            ]
        },
        "తెలుగు": {
            "name": "టమాటా ఎర్లీ బ్లైట్",
            "remedy": [
                "వ్యాధి సోకిన దిగువ ఆకులను తొలగించండి.",
                "నేల నుంచి ఆకులపై మట్టి చిమ్మకుండా మల్చింగ్ చేయండి.",
                "మొక్క అడుగు భాగంలో నీరు పెట్టండి.",
                "కోత తర్వాత మొక్కల అవశేషాలను తొలగించండి.",
                "మొక్కకు సరైన పోషకాలను అందించండి."
            ]
        }
    },
    "Tomato___Late_blight": {
        "English": {
            "name": "Tomato Late Blight",
            "remedy": [
                "Scout plants frequently.",
                "Remove infected plants or leaves promptly.",
                "Keep foliage dry.",
                "Improve air circulation.",
                "Use locally recommended disease-management products when appropriate."
            ]
        },
        "తెలుగు": {
            "name": "టమాటా లేట్ బ్లైట్",
            "remedy": [
                "మొక్కలను తరచుగా పరిశీలించండి.",
                "వ్యాధి సోకిన ఆకులు లేదా మొక్కలను వెంటనే తొలగించండి.",
                "ఆకులు పొడిగా ఉండేలా చూడండి.",
                "గాలి ప్రసరణను మెరుగుపరచండి.",
                "అవసరమైనప్పుడు స్థానికంగా సిఫార్సు చేసిన వ్యాధి నిర్వహణ ఉత్పత్తులను ఉపయోగించండి."
            ]
        }
    },
    "Tomato___Leaf_Mold": {
        "English": {
            "name": "Tomato Leaf Mold",
            "remedy": [
                "Reduce humidity around plants.",
                "Improve ventilation.",
                "Avoid wetting leaves during irrigation.",
                "Remove infected leaves.",
                "Clean plant debris after harvest."
            ]
        },
        "తెలుగు": {
            "name": "టమాటా లీఫ్ మోల్డ్",
            "remedy": [
                "మొక్కల చుట్టూ అధిక తేమను తగ్గించండి.",
                "గాలి ప్రసరణను మెరుగుపరచండి.",
                "నీరు పెట్టేటప్పుడు ఆకులను తడపకుండా ఉండండి.",
                "వ్యాధి సోకిన ఆకులను తొలగించండి.",
                "కోత తర్వాత మొక్కల అవశేషాలను శుభ్రం చేయండి."
            ]
        }
    },
    "Tomato___Septoria_leaf_spot": {
        "English": {
            "name": "Tomato Septoria Leaf Spot",
            "remedy": [
                "Remove infected lower leaves.",
                "Avoid overhead watering.",
                "Use mulch to reduce soil splash.",
                "Improve plant spacing.",
                "Remove infected debris after harvest."
            ]
        },
        "తెలుగు": {
            "name": "టమాటా సెప్టోరియా లీఫ్ స్పాట్",
            "remedy": [
                "వ్యాధి సోకిన దిగువ ఆకులను తొలగించండి.",
                "పై నుంచి నీరు పోయడాన్ని నివారించండి.",
                "నేల చిమ్మకుండా మల్చింగ్ చేయండి.",
                "మొక్కల మధ్య సరైన దూరం ఉంచండి.",
                "కోత తర్వాత వ్యాధిగ్రస్త అవశేషాలను తొలగించండి."
            ]
        }
    },
    "Tomato___Spider_mites Two-spotted_spider_mite": {
        "English": {
            "name": "Two-Spotted Spider Mite",
            "remedy": [
                "Inspect the underside of leaves.",
                "Reduce plant stress by providing adequate water.",
                "Use a strong water spray where appropriate.",
                "Protect beneficial predatory insects.",
                "Use an approved miticide only when necessary."
            ]
        },
        "తెలుగు": {
            "name": "టూ-స్పాటెడ్ స్పైడర్ మైట్",
            "remedy": [
                "ఆకుల దిగువ భాగాన్ని పరిశీలించండి.",
                "సరైన నీరు అందించి మొక్క ఒత్తిడిని తగ్గించండి.",
                "అవసరమైనప్పుడు నీటి స్ప్రేతో పురుగులను తొలగించండి.",
                "ప్రయోజనకరమైన సహజ శత్రు పురుగులను రక్షించండి.",
                "అవసరమైనప్పుడు మాత్రమే అనుమతించబడిన మైటిసైడ్‌ను ఉపయోగించండి."
            ]
        }
    },
    "Tomato___Target_Spot": {
        "English": {
            "name": "Tomato Target Spot",
            "remedy": [
                "Remove severely infected leaves.",
                "Improve air circulation.",
                "Avoid prolonged leaf wetness.",
                "Remove plant debris.",
                "Use locally recommended disease-management practices."
            ]
        },
        "తెలుగు": {
            "name": "టమాటా టార్గెట్ స్పాట్",
            "remedy": [
                "తీవ్రంగా వ్యాధి సోకిన ఆకులను తొలగించండి.",
                "గాలి ప్రసరణను మెరుగుపరచండి.",
                "ఆకులు ఎక్కువసేపు తడిగా ఉండకుండా చూడండి.",
                "మొక్కల అవశేషాలను తొలగించండి.",
                "స్థానికంగా సిఫార్సు చేసిన వ్యాధి నిర్వహణ పద్ధతులను పాటించండి."
            ]
        }
    },
    "Tomato___Tomato_Yellow_Leaf_Curl_Virus": {
        "English": {
            "name": "Tomato Yellow Leaf Curl Virus",
            "remedy": [
                "There is no cure for an infected plant.",
                "Remove suspected infected plants.",
                "Control whitefly populations to reduce spread.",
                "Use resistant varieties where available.",
                "Start with healthy transplants."
            ]
        },
        "తెలుగు": {
            "name": "టమాటా ఎల్లో లీఫ్ కర్ల్ వైరస్",
            "remedy": [
                "వ్యాధి సోకిన మొక్కకు పూర్తిగా నయం చేసే చికిత్స లేదు.",
                "అనుమానాస్పద వ్యాధి సోకిన మొక్కలను తొలగించండి.",
                "వ్యాధి వ్యాప్తిని తగ్గించడానికి వైట్‌ఫ్లై పురుగులను నియంత్రించండి.",
                "సాధ్యమైనప్పుడు నిరోధక రకాలను ఉపయోగించండి.",
                "ఆరోగ్యకరమైన నాట్లతో సాగు ప్రారంభించండి."
            ]
        }
    },
    "Tomato___Tomato_mosaic_virus": {
        "English": {
            "name": "Tomato Mosaic Virus",
            "remedy": [
                "There is no cure for an infected plant.",
                "Remove suspected infected plants.",
                "Sanitize hands and tools.",
                "Use disease-free seed and transplants.",
                "Avoid tobacco contamination around tomato plants."
            ]
        },
        "తెలుగు": {
            "name": "టమాటా మోసాయిక్ వైరస్",
            "remedy": [
                "వ్యాధి సోకిన మొక్కకు పూర్తిగా నయం చేసే చికిత్స లేదు.",
                "అనుమానాస్పద వ్యాధి సోకిన మొక్కలను తొలగించండి.",
                "చేతులు మరియు పనిముట్లను శుభ్రపరచండి.",
                "వ్యాధి రహిత విత్తనాలు మరియు నాట్లను ఉపయోగించండి.",
                "టమాటా మొక్కల దగ్గర పొగాకు కలుషితాన్ని నివారించండి."
            ]
        }
    }
}
# ==========================================
# 9. PREDICTION + RESULT DISPLAY
# ==========================================
if uploaded_file is not None:
    # Open uploaded image
    image = Image.open(uploaded_file).convert("RGB")
    # Show uploaded image inside a premium 3D card
    st.markdown(
        f'<div class="preview-card-label">🖼️ '
        f'{"మీ ఆకు ఫోటో" if language == "తెలుగు" else "Your leaf photo"}'
        f'</div>',
        unsafe_allow_html=True
    )
    st.image(
        image,
        width="stretch"
    )
    detect_clicked = st.button(
        "🔬 " + ("వ్యాధిని గుర్తించండి" if language == "తెలుగు" else "Detect Disease"),
        type="primary",
        width="stretch"
    )
    if detect_clicked:
        # Show scanning animation
        scan_html = """
        <div class="scan-container">
            <div style="position:relative;width:100px;height:100px;margin:0 auto;">
                <div class="scan-ring"></div>
                <div class="scan-pulse"></div>
            </div>
            <div class="scan-text">{}</div>
        </div>
        """.format(
            "AI ఆకును విశ్లేషిస్తోంది..." if language == "తెలుగు"
            else "AI is analyzing your leaf..."
        )
        scan_placeholder = st.empty()
        scan_placeholder.markdown(scan_html, unsafe_allow_html=True)
        # Transform image
        image_tensor = transform(image)
        # Add batch dimension
        image_tensor = image_tensor.unsqueeze(0).to(device)
        # Make prediction
        with torch.no_grad():
            outputs = model(image_tensor)
            probabilities = torch.softmax(outputs, dim=1)
            confidence, predicted_index = torch.max(
                probabilities, dim=1
            )
        # Clear scanning animation
        scan_placeholder.empty()
        # Get prediction
        predicted_class = class_names[predicted_index.item()]
        confidence_percentage = confidence.item() * 100
        # Split dataset class name into plant + condition for display only
        # (the raw predicted_class / class_names values are never changed)
        plant_part, _, condition_part = predicted_class.partition("___")
        plant_display = plant_part.replace("_", " ").strip()
        condition_display = condition_part.replace("_", " ").strip()
        is_healthy = "healthy" in condition_part.lower()
        LOW_CONFIDENCE_THRESHOLD = 50
        HIGH_CONFIDENCE_THRESHOLD = 85
        if confidence_percentage >= HIGH_CONFIDENCE_THRESHOLD:
            level_class = "conf-high"
            level_label = "అధిక నమ్మకం" if language == "తెలుగు" else "HIGH CONFIDENCE"
        elif confidence_percentage >= LOW_CONFIDENCE_THRESHOLD:
            level_class = "conf-medium"
            level_label = "మధ్యస్థ నమ్మకం" if language == "తెలుగు" else "MODERATE CONFIDENCE"
        else:
            level_class = "conf-low"
            level_label = "తక్కువ నమ్మకం" if language == "తెలుగు" else "LOW CONFIDENCE"
        fill_width = min(max(confidence_percentage, 0), 100)
        # ==========================================
        # 🌿 AI DIAGNOSIS CARD
        # ==========================================
        if confidence_percentage < LOW_CONFIDENCE_THRESHOLD:
            low_warning = (
                "⚠️ AI ఖచ్చితంగా చెప్పలేకపోతోంది. దయచేసి స్పష్టమైన, "
                "దగ్గరి ఆకు ఫోటోతో మళ్ళీ ప్రయత్నించండి."
                if language == "తెలుగు" else
                "⚠️ The AI isn't confident about this image. "
                "Try a clearer, closer photo of a single leaf."
            )
            st.markdown(
                f'<div class="low-conf-warning">{low_warning}</div>',
                unsafe_allow_html=True
            )
            st.markdown(f"""
<div class="result-card {level_class}">
    <div class="result-eyebrow">🌿 {"AI నిర్ధారణ" if language == "తెలుగు" else "AI DIAGNOSIS"}</div>
    <div class="confidence-block">
        <div class="confidence-row">
            <span class="confidence-value {level_class}">{confidence_percentage:.1f}%</span>
            <span class="confidence-tag {level_class}">{level_label}</span>
        </div>
        <div class="confidence-track">
            <div class="confidence-fill {level_class}" style="width:{fill_width:.1f}%;"></div>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)
        else:
            eyebrow = "🌿 " + ("AI నిర్ధారణ" if language == "తెలుగు" else "AI DIAGNOSIS")
            if is_healthy:
                condition_line = "✅ " + ("ఆరోగ్యంగా ఉంది" if language == "తెలుగు" else "Healthy")
                condition_css_class = "result-disease result-healthy"
            else:
                condition_line = f"⚠️ {condition_display}"
                condition_css_class = "result-disease"
            st.markdown(f"""
<div class="result-card {level_class}">
    <div class="result-eyebrow">{eyebrow}</div>
    <div class="result-plant">🍃 {plant_display}</div>
    <div class="{condition_css_class}">{condition_line}</div>
    <div class="confidence-block">
        <div class="confidence-label">{"AI నమ్మకం" if language == "తెలుగు" else "AI CONFIDENCE"}</div>
        <div class="confidence-row">
            <span class="confidence-value {level_class}">{confidence_percentage:.1f}%</span>
            <span class="confidence-tag {level_class}">{level_label}</span>
        </div>
        <div class="confidence-track">
            <div class="confidence-fill {level_class}" style="width:{fill_width:.1f}%;"></div>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)
        # ==========================================
        # 💊 REMEDY / MANAGEMENT
        # ==========================================
        if confidence_percentage >= LOW_CONFIDENCE_THRESHOLD and not is_healthy:
            st.markdown(
                f'<div class="section-heading">💊 '
                f'{"సిఫార్సు చేసిన నిర్వహణ" if language == "తెలుగు" else "Recommended Management"}'
                f'</div>',
                unsafe_allow_html=True
            )
            if predicted_class in REMEDIES:
                disease_data = REMEDIES[predicted_class][language]
                remedy_html = (
                    f'<div class="nature-card remedy-card">'
                    f'<div class="remedy-title">🌱 {disease_data["name"]}</div>'
                )
                for i, remedy in enumerate(disease_data["remedy"], 1):
                    remedy_html += (
                        f'<div class="remedy-item">'
                        f'<span class="remedy-num">{i}</span>'
                        f'<span>{remedy}</span>'
                        f'</div>'
                    )
                remedy_html += '</div>'
                st.markdown(remedy_html, unsafe_allow_html=True)
            else:
                if language == "తెలుగు":
                    st.info("🌱 ఈ వ్యాధికి నిర్వహణ సమాచారం త్వరలో జోడించబడుతుంది.")
                else:
                    st.info("🌱 General management information for this class will be added soon.")
        elif is_healthy and confidence_percentage >= LOW_CONFIDENCE_THRESHOLD:
            if language == "తెలుగు":
                st.markdown(
                    '<div class="nature-card remedy-card">'
                    '<div class="remedy-title">✅ మీ మొక్క ఆరోగ్యంగా కనిపిస్తోంది!</div>'
                    '<div class="remedy-item"><span class="remedy-num">🌿</span><span>సాధారణ నీటిపారుదల మరియు పోషణను కొనసాగించండి.</span></div>'
                    '<div class="remedy-item"><span class="remedy-num">🔍</span><span>వ్యాధి సంకేతాల కోసం ఆకులను క్రమం తప్పకుండా పరిశీలించండి.</span></div>'
                    '</div>',
                    unsafe_allow_html=True
                )
            else:
                st.markdown(
                    '<div class="nature-card remedy-card">'
                    '<div class="remedy-title">✅ Your plant looks healthy!</div>'
                    '<div class="remedy-item"><span class="remedy-num">🌿</span><span>Keep up regular watering and nutrition.</span></div>'
                    '<div class="remedy-item"><span class="remedy-num">🔍</span><span>Check leaves periodically for early signs of disease.</span></div>'
                    '</div>',
                    unsafe_allow_html=True
                )
        # ==========================================
        # 🛡️ DISCLAIMER
        # ==========================================
        disclaimer_text = (
            "AI ఫలితాలు సమాచార ప్రయోజనాల కోసం మాత్రమే. నిర్ధారణ అనుమానంగా ఉన్నప్పుడు లేదా "
            "పంట తీవ్రంగా దెబ్బతిన్నప్పుడు వ్యవసాయ నిపుణుడిని సంప్రదించండి."
            if language == "తెలుగు" else
            "AI results are informational and should be confirmed by an agricultural "
            "expert when the diagnosis is uncertain or the crop is severely affected."
        )
        st.markdown(
            f'<div class="disclaimer">'
            f'<div class="disclaimer-label">ℹ️ DISCLAIMER</div>'
            f'{disclaimer_text}</div>',
            unsafe_allow_html=True
        )
        # ==========================================
        # 🔄 SCAN ANOTHER LEAF
        # ==========================================
        scan_again_label = "🔄 " + (
            "మరో ఆకును పరిశీలించండి" if language == "తెలుగు" else "Scan Another Leaf"
        )
        if st.button(scan_again_label, width="stretch"):
            st.session_state.reset_counter += 1
            st.rerun()
# ==========================================
# EMPTY STATE (no image uploaded yet)
# ==========================================
if uploaded_file is None:
    empty_html = """
    <div class="nature-card" style="text-align:center;padding:40px 28px;">
        <div style="font-size:40px;margin-bottom:12px;opacity:0.5;">🍃</div>
        <p style="color:var(--text-dim);font-size:14px;margin:0;">
            {}
        </p>
    </div>
    """.format(
        "📸 ప్రారంభించడానికి ఆకు ఫోటోను అప్‌లోడ్ చేయండి"
        if language == "తెలుగు"
        else "📸 Upload a leaf photo to get started"
    )
    st.markdown(empty_html, unsafe_allow_html=True)
# ==========================================
# FOOTER
# ==========================================
st.markdown("""
<div class="footer">
    <span class="footer-text">
        🌿 Built with <span class="footer-brand">PlantCare AI</span> — Smart Agriculture
    </span>
</div>
""", unsafe_allow_html=True)

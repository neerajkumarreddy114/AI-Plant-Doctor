
from remedies import REMEDIES
st.write(
    f"**Predicted class:** `{predicted_class}`"
)

# ==========================================
# PLANT DISEASE REMEDY / MANAGEMENT DATABASE
# ==========================================

REMEDIES = {

    "Apple___Apple_scab": {
        "crop": "Apple",
        "disease": "Apple Scab",
        "management": "Remove and destroy infected fallen leaves and fruit. Improve orchard sanitation and maintain good airflow through appropriate pruning.",
        "telugu": "ఆపిల్ స్కాబ్: సోకిన ఆకులు మరియు పండ్లను తొలగించి నాశనం చేయాలి. తోటలో పరిశుభ్రత మరియు మంచి గాలి ప్రసరణను పాటించాలి."
    },

    "Apple___Black_rot": {
        "crop": "Apple",
        "disease": "Black Rot",
        "management": "Remove infected fruit, leaves and dead wood. Maintain orchard sanitation and prune affected branches appropriately.",
        "telugu": "బ్లాక్ రాట్: సోకిన పండ్లు, ఆకులు మరియు ఎండిన కొమ్మలను తొలగించాలి. తోటలో పరిశుభ్రత పాటించాలి."
    },

    "Apple___Cedar_apple_rust": {
        "crop": "Apple",
        "disease": "Cedar Apple Rust",
        "management": "Remove heavily infected plant material where practical and maintain good orchard sanitation and airflow.",
        "telugu": "సీడార్ ఆపిల్ రస్ట్: తీవ్రంగా సోకిన భాగాలను తొలగించి, తోటలో పరిశుభ్రత మరియు గాలి ప్రసరణను మెరుగుపరచాలి."
    },

    "Apple___healthy": {
        "crop": "Apple",
        "disease": "Healthy",
        "management": "No disease symptoms detected. Continue regular monitoring, sanitation and good crop-management practices.",
        "telugu": "ఆరోగ్యకరమైన ఆపిల్: వ్యాధి లక్షణాలు కనిపించలేదు. క్రమం తప్పకుండా పంటను పరిశీలిస్తూ మంచి పంట నిర్వహణ పద్ధతులను పాటించాలి."
    },

    "Blueberry___healthy": {
        "crop": "Blueberry",
        "disease": "Healthy",
        "management": "No disease symptoms detected. Continue regular monitoring and good crop-management practices.",
        "telugu": "ఆరోగ్యకరమైన బ్లూబెర్రీ: వ్యాధి లక్షణాలు కనిపించలేదు. పంటను క్రమం తప్పకుండా పరిశీలించాలి."
    },

    "Cherry_(including_sour)___Powdery_mildew": {
        "crop": "Cherry",
        "disease": "Powdery Mildew",
        "management": "Improve airflow and sunlight penetration through appropriate canopy management. Remove severely affected plant material where practical.",
        "telugu": "పౌడరీ మిల్డ్యూ: మొక్కలో గాలి ప్రసరణ మరియు సూర్యకాంతి అందేలా నిర్వహణ చేయాలి. తీవ్రంగా సోకిన భాగాలను తొలగించాలి."
    },

    "Cherry_(including_sour)___healthy": {
        "crop": "Cherry",
        "disease": "Healthy",
        "management": "No disease symptoms detected. Continue regular monitoring and sanitation.",
        "telugu": "ఆరోగ్యకరమైన చెర్రీ: వ్యాధి లక్షణాలు కనిపించలేదు. క్రమం తప్పకుండా పంటను పరిశీలించాలి."
    },

    "Corn_(maize)___Cercospora_leaf_spot Gray_leaf_spot": {
        "crop": "Corn",
        "disease": "Cercospora Leaf Spot / Gray Leaf Spot",
        "management": "Use crop rotation where appropriate, manage crop residue and maintain good field sanitation. Monitor fields regularly.",
        "telugu": "మొక్కజొన్న గ్రే లీఫ్ స్పాట్: పంట మార్పిడి మరియు పొల పరిశుభ్రత పాటించాలి. పంటను క్రమం తప్పకుండా పరిశీలించాలి."
    },

    "Corn_(maize)___Common_rust_": {
        "crop": "Corn",
        "disease": "Common Rust",
        "management": "Monitor plants regularly and use suitable resistant varieties where available. Maintain good crop-management practices.",
        "telugu": "మొక్కజొన్న కామన్ రస్ట్: పంటను క్రమం తప్పకుండా పరిశీలించాలి. అందుబాటులో ఉంటే నిరోధక రకాలను ఉపయోగించాలి."
    },

    "Corn_(maize)___Northern_Leaf_Blight": {
        "crop": "Corn",
        "disease": "Northern Leaf Blight",
        "management": "Use resistant varieties where available, rotate crops and manage infected crop residue appropriately.",
        "telugu": "మొక్కజొన్న నార్తర్న్ లీఫ్ బ్లైట్: నిరోధక రకాలను ఉపయోగించడం, పంట మార్పిడి మరియు సోకిన అవశేషాల నిర్వహణ చేయాలి."
    },

    "Corn_(maize)___healthy": {
        "crop": "Corn",
        "disease": "Healthy",
        "management": "No disease symptoms detected. Continue regular monitoring and good crop-management practices.",
        "telugu": "ఆరోగ్యకరమైన మొక్కజొన్న: వ్యాధి లక్షణాలు కనిపించలేదు."
    },

    "Grape___Black_rot": {
        "crop": "Grape",
        "disease": "Black Rot",
        "management": "Remove infected berries and plant material and maintain vineyard sanitation. Improve canopy airflow where practical.",
        "telugu": "ద్రాక్ష బ్లాక్ రాట్: సోకిన పండ్లు మరియు మొక్క భాగాలను తొలగించాలి. ద్రాక్ష తోటలో పరిశుభ్రత మరియు గాలి ప్రసరణను మెరుగుపరచాలి."
    },

    "Grape___Esca_(Black_Measles)": {
        "crop": "Grape",
        "disease": "Esca / Black Measles",
        "management": "Remove severely affected plant material where appropriate and maintain vineyard sanitation. Monitor affected vines carefully.",
        "telugu": "ద్రాక్ష ఎస్కా: తీవ్రంగా ప్రభావితమైన మొక్క భాగాలను తొలగించి తోట పరిశుభ్రతను పాటించాలి."
    },

    "Grape___Leaf_blight_(Isariopsis_Leaf_Spot)": {
        "crop": "Grape",
        "disease": "Leaf Blight",
        "management": "Remove affected leaves and maintain good canopy airflow and vineyard sanitation.",
        "telugu": "ద్రాక్ష లీఫ్ బ్లైట్: సోకిన ఆకులను తొలగించి మంచి గాలి ప్రసరణ మరియు తోట పరిశుభ్రతను పాటించాలి."
    },

    "Grape___healthy": {
        "crop": "Grape",
        "disease": "Healthy",
        "management": "No disease symptoms detected. Continue monitoring and good vineyard-management practices.",
        "telugu": "ఆరోగ్యకరమైన ద్రాక్ష: వ్యాధి లక్షణాలు కనిపించలేదు."
    },

    "Orange___Haunglongbing_(Citrus_greening)": {
        "crop": "Orange",
        "disease": "Huanglongbing / Citrus Greening",
        "management": "Monitor trees regularly and manage the insect vector according to local agricultural guidance. Remove severely affected trees where recommended by local authorities.",
        "telugu": "సిట్రస్ గ్రీనింగ్: చెట్లను క్రమం తప్పకుండా పరిశీలించాలి. స్థానిక వ్యవసాయ నిపుణుల సూచనల ప్రకారం వ్యాధి వ్యాప్తి చేసే పురుగును నిర్వహించాలి."
    },

    "Peach___Bacterial_spot": {
        "crop": "Peach",
        "disease": "Bacterial Spot",
        "management": "Maintain good orchard sanitation, avoid unnecessary leaf wetness and use suitable resistant varieties where available.",
        "telugu": "పీచ్ బ్యాక్టీరియల్ స్పాట్: తోట పరిశుభ్రత పాటించాలి మరియు అందుబాటులో ఉంటే నిరోధక రకాలను ఉపయోగించాలి."
    },

    "Peach___healthy": {
        "crop": "Peach",
        "disease": "Healthy",
        "management": "No disease symptoms detected. Continue regular monitoring and good orchard management.",
        "telugu": "ఆరోగ్యకరమైన పీచ్: వ్యాధి లక్షణాలు కనిపించలేదు."
    },

    "Pepper,_bell___Bacterial_spot": {
        "crop": "Bell Pepper",
        "disease": "Bacterial Spot",
        "management": "Use clean planting material, maintain field sanitation and avoid working with wet plants where possible.",
        "telugu": "క్యాప్సికమ్ బ్యాక్టీరియల్ స్పాట్: ఆరోగ్యకరమైన నాట్లను ఉపయోగించి, పొల పరిశుభ్రత పాటించాలి."
    },

    "Pepper,_bell___healthy": {
        "crop": "Bell Pepper",
        "disease": "Healthy",
        "management": "No disease symptoms detected. Continue regular monitoring and good crop-management practices.",
        "telugu": "ఆరోగ్యకరమైన క్యాప్సికమ్: వ్యాధి లక్షణాలు కనిపించలేదు."
    },

    "Potato___Early_blight": {
        "crop": "Potato",
        "disease": "Early Blight",
        "management": "Remove heavily affected plant material where practical, maintain field sanitation and use crop rotation to reduce disease pressure.",
        "telugu": "బంగాళాదుంప ఎర్లీ బ్లైట్: సోకిన మొక్క భాగాలను తొలగించి, పొల పరిశుభ్రత మరియు పంట మార్పిడిని పాటించాలి."
    },

    "Potato___Late_blight": {
        "crop": "Potato",
        "disease": "Late Blight",
        "management": "Remove and properly manage infected plant material, avoid prolonged leaf wetness and monitor the crop frequently. Follow local agricultural recommendations for disease management.",
        "telugu": "బంగాళాదుంప లేట్ బ్లైట్: సోకిన మొక్క భాగాలను తొలగించి, ఆకులు ఎక్కువసేపు తడిగా ఉండకుండా చూడాలి. స్థానిక వ్యవసాయ నిపుణుల సూచనలు పాటించాలి."
    },

    "Potato___healthy": {
        "crop": "Potato",
        "disease": "Healthy",
        "management": "No disease symptoms detected. Continue regular monitoring and good crop-management practices.",
        "telugu": "ఆరోగ్యకరమైన బంగాళాదుంప: వ్యాధి లక్షణాలు కనిపించలేదు."
    },

    "Raspberry___healthy": {
        "crop": "Raspberry",
        "disease": "Healthy",
        "management": "No disease symptoms detected. Continue regular monitoring and good field sanitation.",
        "telugu": "ఆరోగ్యకరమైన రాస్ప్‌బెర్రీ: వ్యాధి లక్షణాలు కనిపించలేదు."
    },

    "Soybean___healthy": {
        "crop": "Soybean",
        "disease": "Healthy",
        "management": "No disease symptoms detected. Continue regular monitoring and good crop-management practices.",
        "telugu": "ఆరోగ్యకరమైన సోయాబీన్: వ్యాధి లక్షణాలు కనిపించలేదు."
    },

    "Squash___Powdery_mildew": {
        "crop": "Squash",
        "disease": "Powdery Mildew",
        "management": "Improve airflow around plants, avoid excessive humidity and remove severely affected plant material where practical.",
        "telugu": "స్క్వాష్ పౌడరీ మిల్డ్యూ: మొక్కల మధ్య గాలి ప్రసరణ మెరుగుపరచాలి మరియు తీవ్రంగా సోకిన భాగాలను తొలగించాలి."
    },

    "Strawberry___Leaf_scorch": {
        "crop": "Strawberry",
        "disease": "Leaf Scorch",
        "management": "Remove severely affected leaves, maintain good field sanitation and avoid conditions that promote prolonged leaf wetness.",
        "telugu": "స్ట్రాబెర్రీ లీఫ్ స్కార్చ్: తీవ్రంగా సోకిన ఆకులను తొలగించి పొల పరిశుభ్రత పాటించాలి."
    },

    "Strawberry___healthy": {
        "crop": "Strawberry",
        "disease": "Healthy",
        "management": "No disease symptoms detected. Continue regular monitoring and good crop-management practices.",
        "telugu": "ఆరోగ్యకరమైన స్ట్రాబెర్రీ: వ్యాధి లక్షణాలు కనిపించలేదు."
    },

    "Tomato___Bacterial_spot": {
        "crop": "Tomato",
        "disease": "Bacterial Spot",
        "management": "Use clean planting material, remove severely affected plant material and maintain good field sanitation.",
        "telugu": "టమాటో బ్యాక్టీరియల్ స్పాట్: ఆరోగ్యకరమైన నాట్లను ఉపయోగించి, సోకిన భాగాలను తొలగించి పొల పరిశుభ్రత పాటించాలి."
    },

    "Tomato___Early_blight": {
        "crop": "Tomato",
        "disease": "Early Blight",
        "management": "Remove affected leaves, maintain field sanitation and use crop rotation where appropriate.",
        "telugu": "టమాటో ఎర్లీ బ్లైట్: సోకిన ఆకులను తొలగించి, పొల పరిశుభ్రత మరియు పంట మార్పిడిని పాటించాలి."
    },

    "Tomato___Late_blight": {
        "crop": "Tomato",
        "disease": "Late Blight",
        "management": "Remove infected plant material, reduce prolonged leaf wetness and monitor the crop frequently. Follow local agricultural recommendations.",
        "telugu": "టమాటో లేట్ బ్లైట్: సోకిన మొక్క భాగాలను తొలగించి, ఆకులు ఎక్కువసేపు తడిగా ఉండకుండా చూడాలి."
    },

    "Tomato___Leaf_Mold": {
        "crop": "Tomato",
        "disease": "Leaf Mold",
        "management": "Improve ventilation and reduce excessive humidity around foliage. Remove severely affected leaves and maintain sanitation.",
        "telugu": "టమాటో లీఫ్ మోల్డ్: గాలి ప్రసరణ మెరుగుపరచి అధిక తేమను తగ్గించాలి. తీవ్రంగా సోకిన ఆకులను తొలగించాలి."
    },

    "Tomato___Septoria_leaf_spot": {
        "crop": "Tomato",
        "disease": "Septoria Leaf Spot",
        "management": "Remove affected leaves, maintain field sanitation and avoid unnecessary wetting of foliage.",
        "telugu": "టమాటో సెప్టోరియా లీఫ్ స్పాట్: సోకిన ఆకులను తొలగించి పొల పరిశుభ్రత పాటించాలి."
    },

    "Tomato___Spider_mites Two-spotted_spider_mite": {
        "crop": "Tomato",
        "disease": "Two-spotted Spider Mite",
        "management": "Regularly inspect the underside of leaves and manage mite populations using appropriate integrated pest-management practices. Protect beneficial organisms where possible.",
        "telugu": "టమాటో స్పైడర్ మైట్స్: ఆకుల దిగువ భాగాన్ని క్రమం తప్పకుండా పరిశీలించి, సమగ్ర పురుగు నిర్వహణ పద్ధతులను పాటించాలి."
    },

    "Tomato___Target_Spot": {
        "crop": "Tomato",
        "disease": "Target Spot",
        "management": "Remove affected plant material, maintain good field sanitation and improve airflow around plants.",
        "telugu": "టమాటో టార్గెట్ స్పాట్: సోకిన మొక్క భాగాలను తొలగించి, పొల పరిశుభ్రత మరియు మంచి గాలి ప్రసరణను పాటించాలి."
    },

    "Tomato___Tomato_Yellow_Leaf_Curl_Virus": {
        "crop": "Tomato",
        "disease": "Tomato Yellow Leaf Curl Virus",
        "management": "Monitor and manage the insect vector according to local agricultural guidance. Remove severely infected plants where recommended and control volunteer plants/weeds that may support the vector or virus.",
        "telugu": "టమాటో యెల్లో లీఫ్ కర్ల్ వైరస్: స్థానిక వ్యవసాయ సూచనల ప్రకారం వైరస్ వ్యాప్తి చేసే పురుగును నిర్వహించాలి. తీవ్రంగా సోకిన మొక్కలను సిఫార్సు చేసినప్పుడు తొలగించాలి."
    },

    "Tomato___Tomato_mosaic_virus": {
        "crop": "Tomato",
        "disease": "Tomato Mosaic Virus",
        "management": "Use clean planting material, remove infected plants where appropriate and maintain strict field hygiene to reduce mechanical spread.",
        "telugu": "టమాటో మోసాయిక్ వైరస్: ఆరోగ్యకరమైన నాట్లను ఉపయోగించి, సోకిన మొక్కలను తొలగించి పొల పరిశుభ్రత పాటించాలి."
    },

    "Tomato___healthy": {
        "crop": "Tomato",
        "disease": "Healthy",
        "management": "No disease symptoms detected. Continue regular monitoring and good crop-management practices.",
        "telugu": "ఆరోగ్యకరమైన టమాటో: వ్యాధి లక్షణాలు కనిపించలేదు."
    }
}
# ==========================================
# 11. RECOMMENDED MANAGEMENT
# ==========================================

remedy = REMEDIES.get(predicted_class)

if remedy:

    st.write("### 💊 Recommended Management")

    st.info(
        remedy["management"]
    )

    st.write("### 🇮🇳 తెలుగు సూచనలు")

    st.info(
        remedy["telugu"]
    )

else:

    st.warning(
        "Management information is not available for this class yet."
    )
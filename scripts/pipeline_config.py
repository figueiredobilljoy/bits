from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DATASETS_DIR = ROOT / "datasets"
PRODUCTION_FILE = DATASETS_DIR / "production" / "Horticulture.xlsx"
PRICE_DIR = DATASETS_DIR / "price"
PROCESSED_DIR = ROOT / "data" / "processed"

START_YEAR = 2001
END_YEAR = 2020

SELECTED_STATES = [
    "Uttar Pradesh",
    "Tamil Nadu",
    "Madhya Pradesh",
    "Maharashtra",
    "Gujarat",
    "West Bengal",
    "Karnataka",
    "Haryana",
    "Himachal Pradesh",
    "Odisha",
    "Kerala",
    "Punjab",
]

HORTICULTURE_CROPS = [
    "Banana",
    "Black pepper",
    "Coconut",
    "Coriander",
    "Dry Chillies",
    "Garlic",
    "Ginger",
    "Onion",
    "Potato",
    "Sweet potato",
    "Tapioca",
    "Turmeric",
]

STATE_ALIASES = {
    "Chattisgarh": "Chhattisgarh",
    "Uttrakhand": "Uttarakhand",
    "Pondicherry": "Puducherry",
    "Orissa": "Odisha",
}

CROP_ALIASES = {
    "Arhar": "Arhar",
    "Arhar/Tur": "Arhar",
    "Arhar (Tur/Red Gram)(Whole)": "Arhar",
    "Arhar Dal (Tur Dal)": "Arhar",
    "Red Gram": "Arhar",
    "Pegeon Pea (Arhar Fali)": "Arhar",
    "Bajra (Pearl Millet/Cumbu)": "Bajra",
    "Bengal Gram (Gram)(Whole)": "Bengal Gram",
    "Bengal Gram Dal (Chana Dal)": "Bengal Gram",
    "Black Gram (Urd Beans)(Whole)": "Black Gram",
    "Black Gram Dal (Urd Dal)": "Black Gram",
    "Black Pepper": "Black pepper",
    "Coriander (Leaves)": "Coriander",
    "Cotton(lint)": "Cotton",
    "Dry chillies": "Dry Chillies",
    "Green Gram (Moong)(Whole)": "Green Gram",
    "Green Gram Dal (Moong Dal)": "Green Gram",
    "Ginger (Green)": "Ginger",
    "Gram": "Bengal Gram",
    "Gram Raw (Chholia)": "Bengal Gram",
    "Gur (Jaggery)": "Gur",
    "Horse-gram": "Horse Gram",
    "Jowar (Sorghum)": "Jowar",
    "Kulthi (Horse Gram)": "Horse Gram",
    "Lentil (Masur)(Whole)": "Lentil",
    "Masoor": "Lentil",
    "Moong(Green Gram)": "Green Gram",
    "Mustard": "Mustard",
    "Ragi (Finger Millet)": "Ragi",
    "Rapeseed &Mustard": "Mustard",
    "Sesamum (Sesame,Gingelly,Til)": "Sesamum",
    "Turmeric (raw)": "Turmeric",
    "Urad": "Black Gram",
}

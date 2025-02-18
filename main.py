import streamlit as st
import pandas as pd
import re

# Mapping data directly in the code
SHAPE_MAPPING = {
    'RB': 'Round Brilliant Cut',
    'RD': 'Round Brilliant Cut',
    'BR': 'Round Brilliant Cut',
    'BRT': 'Round Brilliant Cut',
    'RBC': 'Round Brilliant Cut',
    'PR': 'Princess Cut',
    'PC': 'Princess Cut',
    'PRC': 'Princess Cut',
    'EM': 'Emerald Cut',
    'EC': 'Emerald Cut',
    'EMC': 'Emerald Cut',
    'AS': 'Asscher Cut',
    'ASC': 'Asscher Cut',
    'CU': 'Cushion Cut',
    'CUC': 'Cushion Cut',
    'CUSH': 'Cushion Cut',
    'MQ': 'Marquise Cut',
    'MQB': 'Marquise Cut',
    'MAR': 'Marquise Cut',
    'OV': 'Oval Cut',
    'OVC': 'Oval Cut',
    'PE': 'Pear Cut',
    'PS': 'Pear Cut',
    'PEC': 'Pear Cut',
    'HS': 'Heart Cut',
    'HT': 'Heart Cut',
    'HSC': 'Heart Cut',
    'RAD': 'Radiant Cut',
    'RC': 'Radiant Cut',
    'RDC': 'Radiant Cut'
}

CLARITY_MAPPING = {
    'FL': 'Flawless',
    'IF': 'Internally Flawless',
    'VVS1': 'Very Very Slightly Included 1',
    'VVS2': 'Very Very Slightly Included 2',
    'VS1': 'Very Slightly Included 1',
    'VS2': 'Very Slightly Included 2',
    'SI1': 'Slightly Included 1',
    'SI2': 'Slightly Included 2',
    'I1': 'Included 1',
    'I2': 'Included 2',
    'I3': 'Included 3'
}

# Sort clarity codes by length to avoid confusion (e.g., "SI2" vs "I2")
sorted_clarity_codes = sorted(CLARITY_MAPPING.keys(), key=len, reverse=True)

def extracting_clarity(description):
    """
    Extrait la clarté à partir de la description à l'aide des codes triés.
    """
    description = str(description).upper()
    for clarity_code in sorted_clarity_codes:
        if clarity_code in description:
            return CLARITY_MAPPING[clarity_code]
    return None

def extract_color(description):
    """
    Extrait la couleur à partir de la description en utilisant des codes connus.
    """
    description = str(description).upper()
    if "WH" in description:
        return "White"
    if "D/CUT" in description:
        description = description.replace("D/CUT", "")
    
    color_match = re.findall(r'(?<![A-Z0-9])(WHITE|D|E|F|G|H|I|J|K|L|M|EVS1)(?![A-Z0-9])', description)
    for match in color_match:
        if match == "WHITE":
            return "White"
        elif match == "EVS1":
            return "E"
        else:
            return match.capitalize()
    return "UNKNOWN"

def extract_shape(description):
    """
    Extrait la forme à partir de la description en se basant sur la mapping.
    """
    description = str(description).lower()
    for code, shape in SHAPE_MAPPING.items():
        if code.lower() in description:
            return shape.capitalize()
    if "round" in description:
        return "Round Brilliant Cut"
    return "N/A"

def extract_dimensions(description):
    """
    Extrait les dimensions à partir de la description.
    """
    if not isinstance(description, str):
        return None, None, None, None, None

    description = description.upper()

    # 1. Format "(x.xx - y.yy * z.zz)"
    paren_dash_match = re.search(r'\((\d+\.\d+)\s*-\s*(\d+\.\d+)\s*\*\s*(\d+\.\d+)\)', description)
    if paren_dash_match:
        length = float(paren_dash_match.group(1))
        width  = float(paren_dash_match.group(2))
        height = float(paren_dash_match.group(3))
        mm_range = f"{length}-{width}"
        return length, length, height, mm_range, None

    # 2. Format "(x.xx * y.yy * z.zz)"
    star_match = re.search(r'\((\d+\.\d+)\s*\*\s*(\d+\.\d+)\s*\*\s*(\d+\.\d+)\)', description)
    if star_match:
        length = float(star_match.group(1))
        width  = float(star_match.group(2))
        height = float(star_match.group(3))
        mm_range = f"{length}-{width}"
        return length, width, height, mm_range, None

    # 3. Format "D (min-max) H(min-max)"
    d_h_match = re.search(r'D\s*\(\s*(\d+\.\d+)\s*-\s*(\d+\.\d+)\s*\)\s*H\s*\(\s*(\d+\.\d+)\s*-\s*(\d+\.\d+)\s*\)', description)
    if d_h_match:
        d_min = float(d_h_match.group(1))
        d_max = float(d_h_match.group(2))
        h_min = float(d_h_match.group(3))
        h_max = float(d_h_match.group(4))
        mm_range = f"{d_min}-{d_max}"
        height_range = f"{h_min}-{h_max}"
        return d_min, d_min, height_range, mm_range, None

    # 4. Format "L(1.50-1.85)H(0.90-1.25)"
    lh_match = re.search(r'L\((\d+\.\d+)-(\d+\.\d+)\)H\((\d+\.\d+)-(\d+\.\d+)\)', description)
    if lh_match:
        l_min = float(lh_match.group(1))
        l_max = float(lh_match.group(2))
        h_min = float(lh_match.group(3))
        h_max = float(lh_match.group(4))
        mm_range = f"{l_min}-{l_max}"
        height_range = f"{h_min}-{h_max}"
        return l_min, l_min, height_range, mm_range, None

    # 5. Format pour diamant non rond
    pear_match = re.search(r'L\(\s*(\d+\.\d+)-(\d+\.\d+)\)\s*W\(\s*(\d+\.\d+)-(\d+\.\d+)\)\s*H\(\s*(\d+\.\d+)-(\d+\.\d+)\)', description)
    if pear_match:
        l_min = float(pear_match.group(1))
        l_max = float(pear_match.group(2))
        w_min = float(pear_match.group(3))
        w_max = float(pear_match.group(4))
        h_min = float(pear_match.group(5))
        h_max = float(pear_match.group(6))
        mm_range = f"{l_min}-{l_max}"
        height_range = f"{h_min}-{h_max}"
        return l_min, w_min, height_range, mm_range, None

    # 6. Format avec "DIA MM" et "HEIGHT MM"
    dia_match = re.search(r'DIA\s*MM\s*(\d+\.\d+)\s*-\s*(\d+\.\d+)', description)
    if dia_match:
        min_dia = float(dia_match.group(1))
        max_dia = float(dia_match.group(2))
        mm_range = f"{min_dia}-{max_dia}"
        height_match = re.search(r'HEIGHT\s*MM\s*(\d+\.\d+)\s*-\s*(\d+\.\d+)', description)
        if height_match:
            min_height = float(height_match.group(1))
            max_height = float(height_match.group(2))
            height_range = f"{min_height}-{max_height}"
        else:
            height_range = None
        return min_dia, min_dia, height_range, mm_range, None

    # 7. Autres formats
    slash_match = re.search(r'(\d+\.\d+)/(\d+\.\d+)/(\d+\.\d+)', description)
    if slash_match:
        return float(slash_match.group(1)), float(slash_match.group(2)), float(slash_match.group(3)), None, None
    x_match = re.search(r'(\d+\.\d+)X(\d+\.\d+)X(\d+\.\d+)', description)
    if x_match:
        return float(x_match.group(1)), float(x_match.group(2)), float(x_match.group(3)), None, None

    return None, None, None, None, None

def extract_pcs_carat(description):
    """
    Extrait la valeur PCS/Carat en gérant notamment les formats fractionnaires.
    """
    if not isinstance(description, str):
        return "N/A"
    description = description.upper()
    
    frac_match = re.search(r'(?:PCS/CTS|PCT/CT)\s*(\d+)/(\d+)', description)
    if frac_match:
        return frac_match.group(2)
        
    pc_cts_match = re.search(r'PC/?CTS\s*(\d+\.?\d*)', description)
    if pc_cts_match:
        return pc_cts_match.group(1)
    p_cts_match = re.search(r'P/CTS\s*(\d+\.?\d*)', description)
    if p_cts_match:
        return p_cts_match.group(1)
        
    return "N/A"

def parse_pcs_carat_weight(pcs_carat):
    """
    Convertit la valeur extraite de PCS/Carat en float.
    """
    if pcs_carat == "N/A" or not pcs_carat:
        return None
    try:
        return float(pcs_carat)
    except (ValueError, IndexError):
        return None

def extract_gia_number(description):
    """
    Extrait le numéro GIA depuis la description.
    """
    if not isinstance(description, str):
        return "UNKNOWN"
    gia_match = re.search(r'GIA[:\s]?[:]?\s*(\d{5,10})', description.upper())
    if gia_match:
        return gia_match.group(1)
    return "UNKNOWN"

# Streamlit App
st.title("Diamond Data Analysis")

# Upload the Trade+Search file
uploaded_file = st.file_uploader("Upload the Trade+Search file to analyze", type=["xlsx"])

if uploaded_file:
    # Chargement du fichier
    df = pd.read_excel(uploaded_file)

    if 'Description of the goods' not in df.columns:
        st.error("'Description of the goods' column not found in the uploaded file.")
        st.stop()

    # Création et remplissage des colonnes
    df['Shape'] = df['Description of the goods'].apply(extract_shape)
    df['Empty Column'] = ''
    df['Clarity'] = df['Description of the goods'].apply(extracting_clarity)
    df['Color'] = df['Description of the goods'].apply(extract_color)
    df['Certi Number'] = df['Description of the goods'].apply(extract_gia_number)
    
    dimensions_df = df['Description of the goods'].apply(
        lambda x: pd.Series(extract_dimensions(x), 
                              index=['Length', 'Width', 'Height', 'MM Range', 'Depth']))
    for col in dimensions_df.columns:
        df[col] = dimensions_df[col]

    df['PCS/Carat'] = df['Description of the goods'].apply(extract_pcs_carat)
    df['Pieces per Carat Weight'] = df['PCS/Carat'].apply(parse_pcs_carat_weight)

    df['Height'] = df['Height'].combine_first(df['Depth'])
    df.drop(columns=['Depth'], inplace=True)

    # Conversion de la colonne Height en chaîne pour éviter les erreurs Arrow
    df['Height'] = df['Height'].astype(str)

    column_order = ['Description of the goods', 'Shape', 'Empty Column', 'Clarity', 
                    'Color', 'Certi Number', 'Length', 'Width', 'Height', 'MM Range', 
                    'PCS/Carat', 'Pieces per Carat Weight']
    df = df[column_order]

    st.subheader("Processed Data")
    st.dataframe(df)

    output_file = "Processed_Trade.xlsx"
    df.to_excel(output_file, index=False)
    with open(output_file, "rb") as f:
        st.download_button("Download the processed file", f, file_name="Processed_Trade.xlsx")
else:
    st.info("Please upload the Trade+Search file to proceed.")
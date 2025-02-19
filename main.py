import streamlit as st
import pandas as pd
import re
from logotest import LOGO_BASE64

# Configuration de la page
st.set_page_config(
    page_title="VD Global - Diamond Analysis",
    page_icon="💎",
    layout="wide"
)

# Custom CSS
st.markdown("""
    <style>
    .main {
        padding: 0rem 5rem;
    }
    .header-container {
        display: flex;
        align-items: center;
        justify-content: center;
        gap: 0px;
        margin-bottom: 0;
    }
    .logo {
        width: 150px;
    }
    .title-text {
        margin: 0;
        font-size: 2.5em;
        color: white;
    }
    .subtitle-text {
        font-size: 1.2rem;
        color: #666;
        text-align: center;
        margin-top: 0;
    }
    </style>
""", unsafe_allow_html=True)

# Header avec logo et titre alignés
st.markdown(f"""
    <div class='header-container'>
        <img src='data:image/png;base64,{LOGO_BASE64}' class='logo'>
        <h1 class='title-text'>VD Global</h1>
    </div>
    <p class='subtitle-text'>Diamond Data Analysis Tool</p>
""", unsafe_allow_html=True)

# Mapping data
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

# Sort clarity codes by length
sorted_clarity_codes = ['FL', 'IF', 'VVS1', 'VVS2', 'VS1', 'VS2', 'SI1', 'SI2', 'I1', 'I2', 'I3']

def extracting_clarity(description):
    """
    Extrait la clarté à partir de la description.
    """
    description = str(description).upper()
    for clarity_code in sorted_clarity_codes:
        if clarity_code in description:
            return clarity_code
    return None

def extract_color(description):
    """
    Extrait la couleur à partir de la description.
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
    Extrait la forme à partir de la description.
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
        return length, width, height, mm_range, None

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

    # 7. Format pour cas comme "CPD MARQUISE /NON CERT /F /VVS2 /NC/5.4 /2.86 /1.68"
    if '/NC' in description:
        after_nc = description.split('/NC')[-1]
        slash_match = re.search(r'(\d+\.\d+)\s*/\s*(\d+\.\d+)\s*/\s*(\d+\.\d+)', after_nc)
        if slash_match:
            length = float(slash_match.group(1))
            width = float(slash_match.group(2))
            height = float(slash_match.group(3))
            mm_range = f"{length}-{width}"
            return length, width, height, mm_range, None

    # 8. Autres formats avec slash
    slash_match = re.search(r'(\d+\.\d+)\s*/\s*(\d+\.\d+)\s*/\s*(\d+\.\d+)', description)
    if slash_match:
        length = float(slash_match.group(1))
        width = float(slash_match.group(2))
        height = float(slash_match.group(3))
        mm_range = f"{length}-{width}"
        return length, width, height, mm_range, None

    x_match = re.search(r'(\d+\.\d+)X(\d+\.\d+)X(\d+\.\d+)', description)
    if x_match:
        length = float(x_match.group(1))
        width = float(x_match.group(2))
        height = float(x_match.group(3))
        mm_range = f"{length}-{width}"
        return length, width, height, mm_range, None

    return None, None, None, None, None

def extract_pcs_carat(description):
    """
    Extrait la valeur PCS/Carat.
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
    Convertit la valeur PCS/Carat en float.
    """
    if pcs_carat == "N/A" or not pcs_carat:
        return None
    try:
        return float(pcs_carat)
    except (ValueError, IndexError):
        return None

def extract_gia_number(description):
    """
    Extrait le numéro GIA.
    """
    if not isinstance(description, str):
        return "UNKNOWN"
    gia_match = re.search(r'GIA[:\s]?[:]?\s*(\d{5,10})', description.upper())
    if gia_match:
        return gia_match.group(1)
    return "UNKNOWN"

# Interface principale
st.markdown("""
    <div style='background-color: #2c3e50; color: white; padding: 2rem; border-radius: 0.5rem; margin: 2rem 0; box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);'>
        <h3 style='margin-bottom: 1rem; color: #3498db;'>Instructions</h3>
        <p style='color: #ecf0f1; margin-bottom: 0.5rem;'>1. Upload your Excel file using the button below</p>
        <p style='color: #ecf0f1; margin-bottom: 0.5rem;'>2. The tool will automatically process the data and extract key information</p>
        <p style='color: #ecf0f1; margin-bottom: 0.5rem;'>3. Review the processed data in the interactive table</p>
        <p style='color: #ecf0f1; margin-bottom: 0.5rem;'>4. Download the processed file for further use</p>
    </div>
""", unsafe_allow_html=True)

# File uploader with custom styling
col1, col2, col3 = st.columns([1,2,1])
with col2:
    st.markdown('<div class="uploadBox">', unsafe_allow_html=True)
    uploaded_file = st.file_uploader("📂 Upload File", type=["xlsx"])
    st.markdown('</div>', unsafe_allow_html=True)

if uploaded_file:
    with st.spinner('Processing data...'):
        # Chargement du fichier
        df = pd.read_excel(uploaded_file)

        if 'Description of the goods' not in df.columns:
            st.error("❌ 'Description of the goods' column not found in the uploaded file.")
            st.stop()

        # Création et remplissage des colonnes extraites de la description
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

        # Conversion de la colonne Height en chaîne
        df['Height'] = df['Height'].astype(str)

        # Nouvel ordre des colonnes incluant toutes les colonnes originales et extraites
        column_order = [
            'Date',
            'Description of the goods', 
            'Shape', 
            'Empty Column', 
            'Clarity', 
            'Color', 
            'Supplier',
            'Purchaser',
            'Total($)',
            'Unit Price($)',
            'Weight(KG)',
            'Quantity',
            'Unit',
            'Certi Number', 
            'Length', 
            'Width', 
            'Height', 
            'MM Range', 
            'PCS/Carat', 
            'Pieces per Carat Weight'
        ]
        
        # S'assurer que toutes les colonnes existent avant de les réorganiser
        existing_columns = [col for col in column_order if col in df.columns]
        df = df[existing_columns]

        # Le reste du code reste identique...
        # Affichage des statistiques
        st.markdown("""
            <div style='background-color: #2c3e50; color: white; padding: 1rem; border-radius: 0.5rem; margin: 2rem 0;'>
                <h3 style='margin-bottom: 1rem; color: #3498db;'>Data Summary</h3>
            </div>
        """, unsafe_allow_html=True)
        
        col1, col2, col3, col4, col5 = st.columns(5)
        with col1:
            st.metric("Total Entries", len(df))
        with col2:
            st.metric("Unique Shapes", df['Shape'].nunique())
        with col3:
            st.metric("Unique Colors", df['Color'].nunique())
        with col4:
            st.metric("Unique Clarities", df['Clarity'].nunique())
        with col5:
            st.metric("Unique Suppliers", df['Supplier'].nunique())

        # Affichage du DataFrame
        st.markdown("<h3 style='margin: 2rem 0;'>Processed Data</h3>", unsafe_allow_html=True)
        st.dataframe(df, width=1500, height=400)

        # Export button
        output_file = "Processed_Trade.xlsx"
        df.to_excel(output_file, index=False)
        with open(output_file, "rb") as f:
            st.download_button(
                "📥 Download Processed File",
                f,
                file_name="VD_Global_Processed_Trade.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            )

        # Affichage des graphiques
        st.markdown("<h3 style='margin: 2rem 0;'>Data Visualization</h3>", unsafe_allow_html=True)
        col1, col2, col3 = st.columns(3)
        
        with col1:
            shape_counts = df['Shape'].value_counts()
            st.bar_chart(shape_counts)
            st.markdown("<p style='text-align: center;'>Distribution of Shapes</p>", unsafe_allow_html=True)
            
        with col2:
            clarity_counts = df['Clarity'].value_counts()
            st.bar_chart(clarity_counts)
            st.markdown("<p style='text-align: center;'>Distribution of Clarity</p>", unsafe_allow_html=True)
            
        with col3:
            supplier_counts = df['Supplier'].value_counts()
            st.bar_chart(supplier_counts)
            st.markdown("<p style='text-align: center;'>Distribution of Suppliers</p>", unsafe_allow_html=True)

else:
    st.info("👆 Please upload your file to begin the analysis.")

# Footer
st.markdown("""
    <div style='text-align: center; padding: 2rem 0; margin-top: 3rem; border-top: 1px solid #eee;'>
        <p>VD Global Diamond Analysis Tool</p>
        <p style='color: #666; font-size: 0.8rem;'>© 2024 VD Global. All rights reserved.</p>
    </div>
""", unsafe_allow_html=True)
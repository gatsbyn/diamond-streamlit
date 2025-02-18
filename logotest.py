import base64

def convert_image_to_base64(image_path):
    with open(image_path, "rb") as image_file:
        encoded_string = base64.b64encode(image_file.read()).decode()
    return encoded_string

# Générer la chaîne base64
image_path = "assets/logovdglobal.png"
LOGO_BASE64 = convert_image_to_base64(image_path)
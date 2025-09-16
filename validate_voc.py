import os, xml.etree.ElementTree as ET
from PIL import Image

IMG_DIR = "../images"
ANN_DIR = "../annotations"
VALID_EXTS = (".jpg", ".jpeg", ".png")

def check_bbox(xmin, ymin, xmax, ymax, w, h):
    return 0 <= xmin < xmax <= w and 0 <= ymin < ymax <= h

imgs = {f for f in os.listdir(IMG_DIR) if f.lower().endswith(VALID_EXTS)}
xmls = {f for f in os.listdir(ANN_DIR) if f.lower().endswith(".xml")}

# name sets without ext
img_names = {os.path.splitext(f)[0] for f in imgs}
xml_names = {os.path.splitext(f)[0] for f in xmls}

missing_xml = img_names - xml_names
missing_img = xml_names - img_names
if missing_xml:
    print("Missing XML for:", sorted(missing_xml))
if missing_img:
    print("Missing image for:", sorted(missing_img))

ok = True
for name in sorted(img_names & xml_names):
    img_path = os.path.join(IMG_DIR, name + ".jpg")
    if not os.path.exists(img_path):
        # try other ext
        for ext in (".jpeg",".png"):
            if os.path.exists(os.path.join(IMG_DIR, name + ext)):
                img_path = os.path.join(IMG_DIR, name + ext)
                break
    w, h = Image.open(img_path).size

    root = ET.parse(os.path.join(ANN_DIR, name + ".xml")).getroot()
    for obj in root.findall("object"):
        bb = obj.find("bndbox")
        xmin = int(float(bb.find("xmin").text))
        ymin = int(float(bb.find("ymin").text))
        xmax = int(float(bb.find("xmax").text))
        ymax = int(float(bb.find("ymax").text))
        if not check_bbox(xmin, ymin, xmax, ymax, w, h):
            ok = False
            print(f"[BAD BBOX] {name}: ({xmin},{ymin},{xmax},{ymax}) not within 0..{w}x0..{h}")
print("Validation:", "OK" if ok and not missing_xml and not missing_img else "Issues found.")


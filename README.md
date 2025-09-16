# License Plate Dataset
This repository contains a curated set of license-plate images with corresponding bounding-box annotations in Pascal VOC format. Images are stored in images/ and annotations in annotations/, with one XML per image using the class label license_plate (filenames match exactly, e.g., img_0001.jpg ↔ img_0001.xml). The dataset was generated on license-plate detection robustness and can be used to train/evaluate LPD models or reproduce our experiments. See each XML’s <size> for image dimensions; all files are standard 8-bit RGB images. The dataset is used in our ICASSP 2026 paper, **“Towards Physical Domain Adversarial Attacks Against License Plate Detection.”**Please cite the paper if you use this dataset.

## Structure
- `images/`: license plate images (e.g., 300×300 JPEGs)
- `annotations/`: Pascal VOC XMLs (filenames match images)

## Annotation format (Pascal VOC)
Each XML contains one or more `<object>` entries with `<name>license_plate</name>` and `<bndbox>` (`xmin,ymin,xmax,ymax` in pixel coords).

## Usage example (Python)
```python
# Parse one Pascal VOC file
import xml.etree.ElementTree as ET
root = ET.parse('annotations/img_0001.xml').getroot()
for obj in root.findall('object'):
    name = obj.find('name').text
    bb = obj.find('bndbox')
    xmin = int(bb.find('xmin').text)
    ymin = int(bb.find('ymin').text)
    xmax = int(bb.find('xmax').text)
    ymax = int(bb.find('ymax').text)
    print(name, xmin, ymin, xmax, ymax)

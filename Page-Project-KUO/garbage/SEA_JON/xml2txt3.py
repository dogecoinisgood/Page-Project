import xml.etree.ElementTree as ET
import os

def convert_to_yolov5(xml_path, output_folder):
    tree = ET.parse(xml_path)
    root = tree.getroot()

    for image in root.findall('.//image'):
        image_name = image.get('name')
        image_width = int(image.get('width'))
        image_height = int(image.get('height'))

        txt_filename = image_name.replace('.jpg', '.txt').replace('.JPG', '.txt')
        txt_path = os.path.join(output_folder, txt_filename)

        with open(txt_path, 'w') as output_file:
            for polygon in image.findall('.//polygon'):
                label = int(polygon.get('label').split('_')[1]) - 1  # 將"WASTE_X"映射為0到44
                points = polygon.get('points').split(';')
                x1, y1 = map(float, points[0].split(','))
                x2, y2 = map(float, points[2].split(','))

                x_center = (x1 + x2) / 2 / image_width
                y_center = (y1 + y2) / 2 / image_height
                width = abs(x2 - x1) / image_width
                height = abs(y2 - y1) / image_height

                output_line = f'{label} {x_center} {y_center} {width} {height}\n'
                output_file.write(output_line)

xml_path = '/Users/jonlee/Downloads/xml2txt/dataset_10000_update_0912.xml'
output_folder = '/Users/jonlee/Downloads/xml2txt/'

# 確保輸出資料夾存在
os.makedirs(output_folder, exist_ok=True)

# 呼叫函數進行轉換
convert_to_yolov5(xml_path, output_folder)

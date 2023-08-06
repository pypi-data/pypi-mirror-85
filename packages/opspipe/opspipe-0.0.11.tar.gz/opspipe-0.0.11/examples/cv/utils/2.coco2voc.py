'''
转换比赛数据
json - labelImg标注xml
为imgaug数据扩展做准备
'''
import json,os,math

def mkdir(path):
    # 去除首位空格
    path = path.strip()
    # 去除尾部 \ 符号
    path = path.rstrip("\\")
    # 判断路径是否存在
    # 存在     True
    # 不存在   False
    isExists = os.path.exists(path)
    # 判断结果
    if not isExists:
        # 如果不存在则创建目录
        # 创建目录操作函数
        os.makedirs(path)
        print(path , ' 创建成功')
        return True
    else:
        # 如果目录存在则不创建，并提示目录已存在
        print(path , ' 目录已存在')
        return False

# json.load()函数的使用，将读取json信息
file = open('annotations/tablebank_latex_test.json','r',encoding='utf-8')
data = json.load(file)
categories = {item.get('id', 'NA'):item.get('name', 'NA') for item in data['categories']}
#print(categories[1])

images = {item.get('id', 'NA'):{'id':item.get('id', 'NA'),'file_name':item.get('file_name', 'NA'),'height':item.get('height', 'NA'),'width':item.get('width', 'NA'),'license':item.get('license', 'NA')} for item in data['images']}
#images = [(item.get('id', 'NA'),item.get('file_name', 'NA'),item.get('height', 'NA'),item.get('width', 'NA'),item.get('license', 'NA')) for item in data['images']]

#annotations = {item.get('id', 'NA'):{'id':item.get('id', 'NA'),'image_id':item.get('image_id', 'NA'),'category_id':item.get('category_id', 'NA'),'iscrowd':item.get('iscrowd', 'NA'),'segmentation':item.get('segmentation', 'NA'),'area':item.get('area', 'NA'),'bbox':item.get('bbox', 'NA')} for item in data['annotations']}

#annotations = [(item.get('id', 'NA'),item.get('image_id', 'NA'),item.get('category_id', 'NA'),item.get('iscrowd', 'NA'),item.get('segmentation', 'NA'),item.get('area', 'NA'),item.get('bbox', 'NA')) for item in data['annotations']]
#print(annotation[11])
xml_path = 'Pascal_VOC/Annotations/' #注意后面有/
mkdir(xml_path)
imgs_dir = 'Pascal_VOC/JPEGImages/' #注意后面有/
mkdir(imgs_dir)
trains = {}
for item in data['annotations'] :
    image_id = item.get('image_id', 'NA')
    file_name = images[image_id]['file_name']
    category_id = item.get('category_id', 'NA')
    bbox = item.get('bbox', 'NA') 
    if trains.__contains__(image_id): 
        file_bboxs = trains[image_id] + ' ' + ','.join(str(s) for s in bbox if s not in [None,'']) 
        file_bboxs = file_bboxs + ',' +  str(category_id)
        trains[image_id] = file_bboxs 
    else: 
        file_bboxs = file_name + ' ' + ','.join(str(s) for s in bbox if s not in [None,'']) 
        file_bboxs = file_bboxs + ',' +  str(category_id)
        trains[image_id] = file_bboxs

for key in trains:
    file_bboxs = trains[key].split( ) 
    file_name = os.path.splitext(file_bboxs[0])[0]
    num = len(file_bboxs)
    train_txt = open(xml_path + file_name + ".xml",'w+')  
    print('<annotation verified="no">',file = train_txt)
    print("    <folder>Annotations</folder>",file = train_txt)
    print("    <filename>" + file_bboxs[0] + "</filename>",file = train_txt)
    print("    <path>"  + imgs_dir + file_bboxs[0] + "</path>",file=train_txt)
    print("    <source>",file=train_txt)
    print("        <database>Unknown</database>",file=train_txt)
    print("    </source>",file=train_txt)
    print("    <size>",file=train_txt)
    print("        <width>"+str(images[key]['width'])+"</width>",file=train_txt)
    print("        <height>"+str(images[key]['height'])+"</height>",file=train_txt)
    print("        <depth>3</depth>",file=train_txt)
    print("    </size>",file=train_txt)
    print("    <segmented>0</segmented>",file=train_txt)
 
    for i in range(1,num): 
        bbox = file_bboxs[i].split(',') 
        if len(bbox)>3:
            print("    <object>",file=train_txt)
            print("        <name>"+str(bbox[4])+"</name>",file=train_txt)
            print("        <pose>Unspecified</pose>",file=train_txt)
            print("        <truncated>0</truncated>",file=train_txt)
            print("        <difficult>0</difficult>",file=train_txt)
            print("        <bndbox>",file=train_txt)
            print("            <xmin>"+str(math.fabs(int(float(bbox[0]))))+"</xmin>",file=train_txt)
            print("            <ymin>"+str(math.fabs(int(float(bbox[1]))))+"</ymin>",file=train_txt)
            print("            <xmax>"+str(math.fabs(int(float(bbox[0]) + float(bbox[2]))))+"</xmax>",file=train_txt)
            print("            <ymax>"+str(math.fabs(int(float(bbox[1]) + float(bbox[3]))))+"</ymax>",file=train_txt)
            print("        </bndbox>",file=train_txt)
            print("    </object>",file=train_txt) 
    print("</annotation>",file=train_txt)
     
    train_txt.close()

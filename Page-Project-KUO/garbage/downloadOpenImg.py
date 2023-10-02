import fiftyone as fo
import fiftyone.zoo as foz

dataset = foz.load_zoo_dataset(
    "open-images-v6",
    split="train",  # 下载训练集
    label_types=["detections"],  # 下载目标检测标注文件
    classes=["Lighter"],  # 下载数据集中的某几类别
    max_samples=1500,  # 下载图片数目
    only_matching=True,  # 只下载匹配到类别的图片
    dataset_dir=".",  # 下载到当前目录 ..表上個目錄
)


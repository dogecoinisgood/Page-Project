import os

# 設定兩個資料夾的路徑
jpg_folder = 'C:/Users/Wang Yu/Desktop/marine_litter/images/train'  # jpg folder
txt_folder = 'C:/Users/Wang Yu/Desktop/marine_litter/labels/train'  # txt folder

# 取得兩個資料夾中的檔案名稱列表
jpg_files = os.listdir(jpg_folder)
txt_files = os.listdir(txt_folder)

# 取得檔案名稱的前綴部分（不包括檔案擴展名）
jpg_file_names = [os.path.splitext(file)[0] for file in jpg_files]
txt_file_names = [os.path.splitext(file)[0] for file in txt_files]

# 轉換成集合(set)以便比對檔案名稱
jpg_file_set = set(jpg_file_names)
txt_file_set = set(txt_file_names)

# 找到在兩個集合中都存在的檔案名稱
matching_files = jpg_file_set.intersection(txt_file_set)

# 列印出配對到的檔案名稱
print("配對到的檔案名稱:")
for file in matching_files:
    print(file)

# 計算配對到的筆數
matching_count = len(matching_files)
print(f"總共有 {matching_count} 筆配對到的檔案名稱。")

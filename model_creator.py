import xgboost as xgb
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
import time

class ModelCreator():

    def __init__(self, config, patient_ID = None, mode = 'train'):
        self.config = config
        self.model_checkpoint_path = config.model_checkpoint_path
        self.submited_data_path  = config.submited_data_path
        self.unsubmited_data_path  = config.unsubmited_data_path
        self.mode = mode
        if self.mode == 'train':
            self.data = pd.read_excel(self.submited_data_path  , sheet_name = 'Sheet_name_1', index_col = None)
        elif self.mode == 'test':
            self.data = pd.read_excel(self.unsubmited_data_path, sheet_name = 'Sheet_name_1', index_col = None)
            if not patient_ID:
                raise ValueError('The patient ID is None')
            else:
                self.data = self.data[self.data['ID']==patient_ID]
        else:
            raise ValueError("mode of model must in ['train', 'test'].")
        if not self.data.empty:
            self.preprocess_data()
        
        if mode == 'test':
            self.model = xgb.XGBClassifier()  # init model
            self.model.load_model(self.model_checkpoint_path)
        elif mode == 'train':
            self.model = model = xgb.XGBClassifier(random_state=2, max_depth=10, learning_rate=0.1, importance_type='gain')

    def edu_level(self,item):
        levels = ['mù chữ','thcs','thpt','trung cấp, cao đẳng','đại học trở lên']
        try:
            return levels.index(item.lower())
        except:
            return np.nan

    def preprocess_data(self):
        # Tính tuổi từ năm sinh
        self.data["Nam_Sinh"] = self.data["NAMSINH"].apply(lambda x: time.localtime().tm_year - int(x))

        self.data["KhuVuc"] = self.data["KHUVUC"].astype('category')
        self.data["Nghe_Nghiep"] = self.data["NGHENGHI"]
        self.data["Dan_Toc"] = self.data["DANTOC"]
        self.data["Ton_Giao"] = self.data["TONGIAO"].astype('category')
        self.data["Trinh_Do_Hoc_Van"] = self.data["HOCVAN"]
        self.data["Tinh_Trang_hon_nhan"] = self.data["HONNHAN"]

        self.data["So_Lan_Mang_Thai"] = self.data["SOLANMAN"]
        self.data["So_Lan_Sinh_Con"] = self.data["SOCONSINH"]

        self.data["Tien_Su_Tranh_Thai"] = self.data["TRANHTHA"] 

        self.data["Tien_Su_Gia_Dinh"] = self.data["TIENSUGD"]
        self.data["Tien_Su_MangThai"] = self.data["TIENSUMT"]

        print(self.data.columns.tolist())
    def train(self):
        train, valid = train_test_split(self.data, test_size=0.1, random_state=7, stratify=self.data['Label'])
        valid, test = train_test_split(valid, test_size=0.3, random_state=7, stratify=valid['Label'])
        self.model.fit(train[self.config.training_features], train['Label'])
        self.model.save(self.config.model_checkpoint_path)

    def predict(self):        
        features = self.config.training_features  # danh sách cột dùng để train
        return self.model.predict_proba(self.data[features])

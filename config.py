import time 
import os
class Config():
    def __init__(self):
        BASE_DIR = os.path.dirname(os.path.abspath(__file__))
        self.unsubmited_data_path = os.path.join(BASE_DIR, "storages", "database_V1", "unsubmited_data.xlsx")
        self.submited_data_path = os.path.join(BASE_DIR, "storages", "database_V1", "submited_data.xlsx")
        self.original_data_path = os.path.join(BASE_DIR, "storages", "database_V1", "original_data.xlsx")
        self.knowledgeTest_path = os.path.join(BASE_DIR, "storages", "database_V1", "knowledgeTest_data.xlsx")
        self.model_checkpoint_path = os.path.join(BASE_DIR, "storages", "model_checkpoint", "xgb_model.model_1")
        self.training_features      = [ 'Nam_Sinh', 'KhuVuc', 'Nghe_Nghiep', 'Dan_Toc', 'Ton_Giao', 
                                       'Trinh_Do_Hoc_Van', 'Tinh_Trang_hon_nhan', 'So_Lan_Mang_Thai', 
                                       'So_Lan_Sinh_Con', 'Tien_Su_Tranh_Thai', 'Tien_Su_Gia_Dinh', 'Tien_Su_MangThai']
        self.current_year           = time.localtime().tm_year
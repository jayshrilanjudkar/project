import pickle 
import json
import numpy as np
import config

class MedicalInsurance():
    def __init__(self, age,gender, bmi, children, smoker, region):
        self.age = age
        self.gender = gender
        self.bmi = bmi  
        self.children = children
        self.smoker = smoker
        self.region = 'region_' + region

    def load_model(self):
        with open(config.MODEL_FILE_PATH, 'rb') as f:
            self.model = pickle.load(f)

        with open(config.JSON_FILE_PATH, 'r') as f:
            self.json_data = json.load(f)

    def get_predicted_price(self):
        self.load_model()

        region_index = self.json_data['columns'].index(self.region)
        test_array = np.zeros((1, len(self.json_data['columns']))) # 9 columns in json file
        test_array[0][0] = self.age
        test_array[0][1] = self.json_data['gender'][self.gender]
        test_array[0][2] = self.bmi
        test_array[0][3] = self.children
        test_array[0][4] = self.json_data['smoker'][self.smoker]
        test_array[0][region_index] = 1

        print("Test array:", test_array)

        predicted_charges = self.model.predict(test_array)

        return predicted_charges[0]
    
    if __name__ == '__main__':
        age = 25
        gender = 'male'
        bmi = 30.5  
        children = 2
        smoker = 'no'
        region = 'northeast'
        med_insurance = MedicalInsurance(age, gender, bmi, children, smoker, region)
        print(med_insurance.get_predicted_price())
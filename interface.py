from flask import Flask, request, render_template
import numpy as np
import config

from project_app.utils import MedicalInsurance

app = Flask(__name__)

@app.route('/', methods=['GET'])
def home():
    return render_template('input.html', result=None, values={}, error=None)

@app.route('/predict_charges', methods=['POST'])
def get_insurance_charges():
    values = {}
    try:
        data = request.form
        age = int(data.get('age', 0))
        gender = data.get('gender', 'male').strip().lower()
        bmi = float(data.get('bmi', 0))
        children = int(data.get('children', 0))
        smoker = data.get('smoker', 'no').strip().lower()
        region = data.get('region', 'northeast').strip().lower()
        patient_name = data.get('patient_name', '').strip()

        values = {
            'age': age,
            'gender': gender,
            'bmi': bmi,
            'children': children,
            'smoker': smoker,
            'region': region,
            'patient_name': patient_name,
        }

        med_insurance = MedicalInsurance(age, gender, bmi, children, smoker, region)
        charges = med_insurance.get_predicted_price()
        result = {
            'predicted_charges': float(np.round(charges, 2)),
            'patient_name': patient_name,
        }

        return render_template('input.html', result=result, values=values, error=None)
    except Exception as exc:
        values = data.to_dict(flat=True) if 'data' in locals() else {}
        return render_template('input.html', result=None, values=values, error=str(exc))

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=config.PORT_NUMBER)

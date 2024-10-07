from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)
def create_db():
    conn = sqlite3.connect('bmi_history.db')
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS bmi_data (
            gender TEXT,
            athletic TEXT,
            weight REAL,
            height REAL,
            bmi REAL
        )
    ''')
    conn.commit()
    conn.close()

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        gender = request.form['gender']
        athletic = request.form['athletic']
        
        weight = float(request.form['weight'])
        weight_unit = request.form['weight_unit']
        
        if weight_unit == 'g':
            weight_kg = weight / 1000
        elif weight_unit == 'lb':
            weight_kg = weight * 0.453592
        else:
            weight_kg = weight
        
        height = float(request.form['height'])
        height_unit = request.form['height_unit']
        
        if height_unit == 'cm':
            height_m = height / 100
        elif height_unit == 'ft':
            height_m = height * 0.3048
        else:
            height_m = height
        
        bmi = calculate_bmi(weight_kg, height_m)
        
        save_data(gender, athletic, weight_kg, height_m, bmi)
        
        return redirect(url_for('result', bmi=bmi))
    
    return render_template('index.html')

@app.route('/result')
def result():
    bmi = request.args.get('bmi')
    category = get_bmi_category(float(bmi))
    
    return render_template('result.html', bmi=bmi, category=category)

def calculate_bmi(weight, height):
    return weight / (height ** 2)

def save_data(gender, athletic, weight, height, bmi):
    conn = sqlite3.connect('bmi_history.db')
    c = conn.cursor()
    c.execute("INSERT INTO bmi_data (gender, athletic, weight, height, bmi) VALUES (?, ?, ?, ?, ?)", 
              (gender, athletic, weight, height, bmi))
    
    conn.commit()
    conn.close()

def get_bmi_category(bmi):
    if bmi < 18.5:
        return "Underweight"
    elif 18.5 <= bmi < 24.9:
        return "Normal weight"
    elif 25 <= bmi < 29.9:
        return "Overweight"
    else:
        return "Obesity"

if __name__ == '__main__':
    create_db()
    app.run(debug=True)
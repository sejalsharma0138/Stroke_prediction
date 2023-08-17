# save this as app.py
from flask import Flask, escape, request, render_template
import pickle
from sklearn.preprocessing import StandardScaler
scaler = StandardScaler()

model = pickle.load(open("model_pickle.pkl", 'rb'))

app = Flask(__name__)
@app.route('/')
def analysis():
    return render_template("index.html")

@app.route('/blog')
def blog():
    return render_template("blog.html")

@app.route('/analysis')
def dataset():
    return render_template("analysis.html")

@app.route('/contact')
def contact():
    return render_template("contact.html")



@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method =="POST":
        gender = request.form['gender']
        age = int(request.form['age'])
        hypertension = int(request.form['hypertension'])
        disease = int(request.form['disease'])
        married = request.form['married']
        work = request.form['work']
        residence = request.form['residence']
        glucose = float(request.form['glucose'])
        bmi = float(request.form['bmi'])
        smoking = request.form['smoking']

        # gender
        if (gender == "Male"):
            gender_male=1
            gender_other=0
        elif(gender == "Other"):
            gender_male = 0
            gender_other = 1
        else:
            gender_male=0
            gender_other=0
        
        # married
        if(married=="Yes"):
            married_yes = 1
        else:
            married_yes=0

        # work  type
        if(work=='Self-employed'):
            work_type_Never_worked = 0
            work_type_Private = 0
            work_type_Self_employed = 1
            work_type_children=0
        elif(work == 'Private'):
            work_type_Never_worked = 0
            work_type_Private = 1
            work_type_Self_employed = 0
            work_type_children=0
        elif(work=="children"):
            work_type_Never_worked = 0
            work_type_Private = 0
            work_type_Self_employed = 0
            work_type_children=1
        elif(work=="Never_worked"):
            work_type_Never_worked = 1
            work_type_Private = 0
            work_type_Self_employed = 0
            work_type_children=0
        else:
            work_type_Never_worked = 0
            work_type_Private = 0
            work_type_Self_employed = 0
            work_type_children=0

        # residence type
        if (residence=="Urban"):
            Residence_type_Urban=1
        else:
            Residence_type_Urban=0

        # smoking sttaus
        if(smoking=='formerly smoked'):
            smoking_status_formerly_smoked = 1
            smoking_status_never_smoked = 0
            smoking_status_smokes = 0
        elif(smoking == 'smokes'):
            smoking_status_formerly_smoked = 0
            smoking_status_never_smoked = 0
            smoking_status_smokes = 1
        elif(smoking=="never smoked"):
            smoking_status_formerly_smoked = 0
            smoking_status_never_smoked = 1
            smoking_status_smokes = 0
        else:
            smoking_status_formerly_smoked = 0
            smoking_status_never_smoked = 0
            smoking_status_smokes = 0

        feature = scaler.fit_transform([[age, hypertension, disease, glucose, bmi, gender_male, gender_other, married_yes, work_type_Never_worked, work_type_Private, work_type_Self_employed, work_type_children, Residence_type_Urban,smoking_status_formerly_smoked, smoking_status_never_smoked, smoking_status_smokes]])

        prediction = model.predict(feature)[0]
        # print(prediction) 
        # 
        if prediction==0:
            prediction = "  No" #"KUDOS, You have negligible chances of getting a brain stroke!" 
        elif prediction==1:
            prediction = "Yes" #"You have a high chance of getting a brain stroke. Please consult to your doctor immediately." 

        return render_template("index.html", Prediction_Score="Chance of Stroke Prediction is --> {}".format(prediction))   
         

    else:
        return render_template("index.html")





if __name__ == "__main__":
    app.run(debug=True)
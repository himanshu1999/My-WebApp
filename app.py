from flask import Flask , render_template ,request
from pymongo import MongoClient
from werkzeug.utils import secure_filename
import os

app=Flask("myapp")


client = MongoClient('mongodb://127.0.0.1:27017')
mydb = client["student_db"]
mycol = client["result"]

@app.route("/index")
def home():
    return render_template("index.html")

@app.route("/")
def admin():
    return render_template("admin.html")

@app.route("/register",methods =['POST', 'GET'])
def auth():
       return render_template("register.html")


@app.route('/submit',methods =['POST'])
def up():
    if request.method == "POST":
        #Values getting from HTML Form 
        name=request.form.get("name")
        rollno=request.form.get("rollno")
        mobile=request.form.get("mobile")
        phym=request.form.get("physics")
        chm=request.form.get("chemistry")
        mthm=request.form.get("maths")
       
        values=[{
                    "name"	:name,
                    "phone" :mobile,
                    "rollno":int(rollno),
                    "marks" : {
                                "physics":int(phym),
                                "chemistry":int(chm),
                                "maths" : int(mthm)
                                },
                   

                }]
        client['student_db']['result'].insert_many(values)
        return render_template("registerc.html" , uname=name)
    


@app.route("/result")
def result():
    if request.method == "GET":
        name=request.args.get("name")
        roll=request.args.get("roll")
        result = client['student_db']['result'].find({"name" : name , "rollno" : int(roll)} )
        if result.count() == 0:
            return render_template("index.html")

        for i in result:
            namer=(i['name'])
            rollr=(i['rollno'])
            physics=(i['marks']['physics'])
            chemistry=(i['marks']['chemistry'])
            maths=(i['marks']['maths'])
           

            total=physics+chemistry+maths
            per=(total/300)*100
            per=round(per)
            formrender=render_template(
                "result.html",name=namer, roll=rollr,phy=str(physics) , chem=str(chemistry) , mth=str(maths) , tot=str(total) , percent=str(per) 
            )
            output="Marks obtained by " + name + " are : " + str(total) + "percentage = " + str(per)
            return formrender
                      
        
if __name__ == '__main__':
    app.run(debug=True)


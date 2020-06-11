from flask import Flask, render_template, url_for, request, redirect, abort, session
from forms import loginForm, createuserForm, addDeviceForm, updateUserForm, changePin
from flask_bootstrap import Bootstrap
import mysql.connector

app = Flask (__name__)
app.config['SECRET_KEY'] = "My Secret key"
Bootstrap(app)


@app.route('/')
def index():
     return render_template("index.html")


@app.route('/home')
def home():
    if 'uid' in session:
        uname = session['firstName']
        return render_template("home.html", name=uname)
    else:
        return redirect(url_for('login'))


@app.route('/login', methods = ['GET', 'POST'])
def login():
    form = loginForm(request.form)
    if request.method == 'POST' and form.validate_on_submit:
        try:
            mydb = mysql.connector.connect(
                host="iot.c8yxuwoh5r6m.us-east-1.rds.amazonaws.com",
                user="master",
                password="IOT_GroupD",
                database="securitysys_db"
            )

            mycursor = mydb.cursor()
            sql = "SELECT * FROM Users WHERE Email = %s AND Password = %s"

            input = (form.email.data, form.password.data)
            mycursor.execute(sql, input)
            myresult = mycursor.fetchone()

            session['uid'] = myresult[0]
            session['firstName'] = myresult[1]

            mycursor.close()
            mydb.close()
            return redirect(url_for('home'))
        except:
            abort(401)

    else:
        return render_template("login.html",  form=form)
    

@app.route('/createuser', methods = ['GET', 'POST'])
def createuser():
    form = createuserForm(request.form)
    if request.method == 'POST' and form.validate_on_submit:
        try:
            mydb = mysql.connector.connect(
                host="iot.c8yxuwoh5r6m.us-east-1.rds.amazonaws.com",
                user="master",
                password="IOT_GroupD",
                database="securitysys_db"
            )

            mycursor = mydb.cursor()

            sql = "INSERT INTO Users (FirstName, LastName, Password, Email) VALUES (%s, %s, %s, %s)"
            val = (form.firstName.data, form.lastName.data, form.password.data, form.email.data)
            mycursor.execute(sql, val)

            mydb.commit()
            mycursor.close()
            mydb.close()
            return redirect(url_for('home'))
        except:
            abort(401)

    else:
        return render_template("createuser.html",  form=form)


@app.route('/account',  methods = ['GET', 'POST'])
def information():
    if 'uid' in session:
        form = updateUserForm(request.form)
        try:
            mydb = mysql.connector.connect(
                host="iot.c8yxuwoh5r6m.us-east-1.rds.amazonaws.com",
                user="master",
                password="IOT_GroupD",
                database="securitysys_db"
            )

            mycursor = mydb.cursor()
            uid = session['uid']
            sql = 'SELECT * FROM Users WHERE UserId = ' + str(uid)
            mycursor.execute(sql)
            myresult = mycursor.fetchone()

            form.firstName.data = myresult[1]
            form.lastName.data = myresult[2]
            form.email.data = myresult[3]
            form.password.data = myresult[4]

            mycursor.close()
            mydb.close()

            return render_template("update.html", form=form)
        except:
            return "<p>Error</p><p><a href=" + "/home" + ">Home<a/></p>"
    else:
        return redirect(url_for('login'))


@app.route('/changepin', methods = ['GET', 'POST'])
def changepin():
    if 'uid' in session:
        form = changePin(request.form)
        if request.method == 'POST' and form.validate_on_submit:
            try:
                mydb = mysql.connector.connect(
                    host="iot.c8yxuwoh5r6m.us-east-1.rds.amazonaws.com",
                    user="master",
                    password="IOT_GroupD",
                    database="securitysys_db"
                )

                mycursor = mydb.cursor()
                sql = "UPDATE Device SET Pin = %s WHERE UserId = %s"
                uid = session['uid']
                val = (form.pin.data, uid)

                mycursor.execute(sql, val)

                mydb.commit()
                mycursor.close()
                mydb.close()
                return redirect(url_for('home'))
            except:
                abort(401)
        else:
            try:
                mydb = mysql.connector.connect(
                    host="iot.c8yxuwoh5r6m.us-east-1.rds.amazonaws.com",
                    user="master",
                    password="IOT_GroupD",
                    database="securitysys_db"
                )

                mycursor = mydb.cursor()
                uid = session['uid']
                sql = 'SELECT * FROM Device WHERE UserID = ' + str(uid)
                mycursor.execute(sql)
                myresult = mycursor.fetchone()
                cpin = myresult[3]


                mycursor.close()
                mydb.close()
                return render_template("changepin.html", currentPin=cpin, form=form)
            except:
                abort(401)
    else:
        return redirect(url_for('login'))

@app.route('/keypadLogds', methods = ['GET', 'POST'])
def keypadLogds():
    if 'uid' in session:
        try:
            mydb = mysql.connector.connect(
                host="iot.c8yxuwoh5r6m.us-east-1.rds.amazonaws.com",
                user="master",
                password="IOT_GroupD",
                database="securitysys_db"
            )

            uid = session['uid']

            mycursor = mydb.cursor()
            uid = session['uid']
            sql = "SELECT LogKeypad.AccessDateTime, LogKeypad.DeviceStatus, LogKeypad.DeviceId From LogKeypad INNER JOIN Device ON LogKeypad.DeviceId = Device.DeviceId WHERE Device.UserId = " + str(uid)
            mycursor.execute(sql)
            myresult = mycursor.fetchall()
            mycursor.close()
            mydb.close()
            return render_template("keypadLogs.html", logs=myresult)
        except:
            abort(401)
    else:
        return redirect(url_for('login'))


@app.route('/securityLogs', methods = ['GET', 'POST'])
def securityLogs():
    if 'uid' in session:
        try:
            mydb = mysql.connector.connect(
                host="iot.c8yxuwoh5r6m.us-east-1.rds.amazonaws.com",
                user="master",
                password="IOT_GroupD",
                database="securitysys_db"
            )

            mycursor = mydb.cursor()
            uid = session['uid']
            sql = "SELECT LogMotionSensor.AccessDateTime, LogMotionSensor.DeviceStatus, LogMotionSensor.DeviceId From LogMotionSensor INNER JOIN Device ON LogMotionSensor.DeviceId = Device.DeviceId WHERE Device.UserId = " + str(uid)
            mycursor.execute(sql)
            myresult = mycursor.fetchall()
            mycursor.close()
            mydb.close()
            return render_template("securityLogs.html", logs=myresult)
        except:
            abort(401)
    else:
        return redirect(url_for('login'))


@app.route('/addDevice', methods=['GET', 'POST'])
def addDevice():
    if 'uid' in session:
        form = addDeviceForm(request.form)
        if request.method == 'POST' and form.validate_on_submit:
            try:
                mydb = mysql.connector.connect(
                    host="iot.c8yxuwoh5r6m.us-east-1.rds.amazonaws.com",
                    user="master",
                    password="IOT_GroupD",
                    database="securitysys_db"
                )
                mycursor = mydb.cursor()
                uid = session['uid']
                sql = 'SELECT * FROM Device WHERE DeviceId = ' + form.deviceID.data
                mycursor.execute(sql)
                myresult = mycursor.fetchone()
                if myresult[2] == None:
                    sql = "UPDATE Device SET UserId = %s WHERE DeviceId = %s"
                    uid = session['uid']
                    val = (uid, form.deviceID.data)

                    mycursor.execute(sql, val)

                    mydb.commit()
                    mycursor.close()
                    mydb.close()
                    return redirect(url_for('home'))
                else:
                    return "<p>Unable to add new device. Device already registered</p><p><a href=" + "/addDevice" + ">Add Device<a/></p>"

            except:
                return "<p>Unable to add new device</p><p><a href=" + "/addDevice" + ">Add Device<a/></p>"

        else:
            return render_template("add_device.html",  form=form)
    else:
        return redirect(url_for('login'))


@app.route('/logout')
def logout():
    session.pop('uid', None)
    session.pop('firstName', None)
    return redirect(url_for('login'))


if __name__ == "__main__":
    
    app.run(debug=True)

    
from flask_wtf import Form
from wtforms import StringField, PasswordField, SubmitField, validators, IntegerField

class loginForm(Form):
    email = StringField("Email", [validators.DataRequired("Enter your email"), validators.Email("Please enter your email address.")])
    password = PasswordField("Password", [validators.DataRequired("Enter your Password.")])
    submit = SubmitField("Login")

class createuserForm(Form):
    firstName = StringField("First name", [validators.DataRequired("First name can't be empty")])
    lastName = StringField("Last name", [validators.DataRequired("Last name can't be empty")])
    email = StringField("Email", [validators.DataRequired("Enter your email"),
                                  validators.Email("Please enter your email address.")])
    password = PasswordField("Password", [validators.DataRequired("Enter your Password.")])
    submit = SubmitField("Submit")

class addDeviceForm(Form):
    deviceID = StringField("Device ID", [validators.DataRequired("Device ID can't be empty")])
    submit = SubmitField("Add")

class changePin(Form):
    pin = StringField("New Pin", [validators.DataRequired("New Pin can't be empty")])
    submit = SubmitField("Change")

class updateUserForm(Form):
    firstName = StringField("First name", [validators.DataRequired("First name can't be empty")])
    lastName = StringField("Last name", [validators.DataRequired("Last name can't be empty")])
    email = StringField("Email", [validators.DataRequired("Enter your email"),
                                  validators.Email("Please enter your email address.")])
    password = PasswordField("Password", [validators.DataRequired("Enter your Password.")])
    submit = SubmitField("Submit")
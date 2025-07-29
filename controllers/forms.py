from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField,IntegerField
from wtforms.validators import Email,Length,DataRequired,ValidationError
from models.model import User

class RegisterForm(FlaskForm):
    def validate_email(self,useremail):
        user=User.query.filter_by(email=useremail.data).first()
        if user:
            print("Username already exists")
            raise ValidationError("User name already exist")

    email = StringField(label="Email:",validators=[Email()])
    password = PasswordField(label="Password:",validators=[Length(min=8)])
    name = StringField(label="Name:",validators=[DataRequired()])
    address = StringField(label="Address:",validators=[DataRequired()])
    pincode = StringField(label="Pincode:",validators=[Length(min=6)])
    submit = SubmitField(label="Submit")

class LoginForm(FlaskForm):
    email=StringField(label='Email',validators=[Email()])
    password=PasswordField(label='Password',validators=[Length(min=8)])
    submit=SubmitField(label='Submit')

class AddingParkinglot(FlaskForm):
    city=StringField(label='City:',validators=[DataRequired()])
    locationName=StringField(label='Location Name:',validators=[DataRequired()])
    price=IntegerField(label='Price:',validators=[DataRequired()])
    address = StringField(label="Address:", validators=[DataRequired()])
    pincode=StringField(label='Pincode:',validators=[DataRequired(),Length(min=6)])
    No_Spots=IntegerField(label='Number of Spots:',validators=[DataRequired()])
    submit=SubmitField(label='Submit')

class Edit_Profile(FlaskForm):
    name = StringField(label='Name:',validators=[DataRequired()])
    current_password = PasswordField(label="Current Password:",validators=[Length(min=8)])
    password = PasswordField(label="New Password:",validators=[Length(min=8)])
    confirm_password = PasswordField(label="Confirm Password:",validators=[Length(min=8)])
    submit = SubmitField(label="Submit")

class Release_Spot_Form(FlaskForm):
    booking_id = IntegerField(label="Booking ID:")
    vehicle_no = StringField(label="Vehicle No:")
    Park_in_timestamp = StringField(label="Parking In Timestamp:")
    Leave_out_timestamp = StringField(label="Leaving Timestamp:")
    Total_cost = IntegerField(label="Total Cost:")
    Release_Out = SubmitField(label="Release Out")

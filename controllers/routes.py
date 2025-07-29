from flask import render_template,url_for,redirect,request,flash,session
from controllers.forms import *
from models.model import *
from datetime import datetime
from controllers.appFunctions import SetPrice

def init_routes(app):

    """========= Admin Creation ========"""
    @app.route('/', methods=['GET', 'POST'])
    def admin_creation():
        admin=Admin.query.filter_by(email='admin@parking.com').first()
        if not admin:
            admin=Admin('admin@parking.com','Nanda','password')
            db.session.add(admin)
            db.session.commit()
        return redirect('login')

    """========== Home Page ================"""
    @app.route('/home',methods=['GET','POST'])
    @app.route('/login', methods=['GET', 'POST'])
    def login():

        form=LoginForm()

        if form.validate_on_submit():
            user=User.query.filter_by(email=form.email.data).first()
            admin=Admin.query.filter_by(email=form.email.data).first()
            if user:
                if user.check_password(form.password.data):
                    session.clear()
                    session['name'] = user.name
                    session['userid'] = user.id
                    session['email'] = form.email.data
                    session['userType'] = 'user'
                    flash(f'Success! You are logged in as {user.name}',
                          'success')
                    return redirect(url_for('dashboard'))
                else:
                    flash(f"Password is wrong! Check the password again!", 'warning')
                    return redirect(url_for('login'))

            elif admin:
                if admin.check_password(form.password.data):
                    session.clear()
                    session['name'] = admin.name
                    session['email'] = form.email.data
                    session['userid'] = admin.id
                    session['userType'] = 'admin'
                    flash(f'Success! You are logged in as {admin.name}',
                          'success')
                    return redirect(url_for('dashboard'))
                else:
                    flash(f"Password is wrong! Check the password again!", 'warning')
                    return redirect(url_for('login'))
            else:
                flash(f"No user exist with the email: {form.email.data}", 'warning')
                return redirect(url_for('login'))

        return render_template('login.html',form=form)

    """========== Register Page ============"""
    @app.route('/register',methods=['GET', 'POST'])
    def register():
        form = RegisterForm()

        if form.validate_on_submit():
            existing_user=User.query.filter_by(email=form.email.data).first()

            if existing_user:
                flash(f'Email is already Registered','danger')
                return render_template('register.html',form=form)
            user_to_create= User(email=form.email.data,password=form.password.data,
                                 name=form.name.data,address=form.address.data,
                                 pincode=form.pincode.data)
            session.clear()
            db.session.add(user_to_create)
            db.session.commit()
            session['name']=form.name.data
            session['email']=form.email.data
            session['userid'] = (User.query.filter_by(email=form.email.data).first()).id
            session['userType']='user'
            flash("User Registered Successfully!!",category='success')
            return redirect(url_for('dashboard'))

        if form.errors != {}:
            for msg in form.errors.values():
                flash(msg,category='danger')
        return render_template('register.html',form=form)

    """========== Dashboard ================"""
    @app.route('/dashboard',methods=['GET','POST'])
    def dashboard():
        email=session.get('email')
        if not email:
            flash("Session Expired! Login Again!",'warning')
            return redirect(url_for('login'))
        
        if session.get('userType')=='user':
            userspot = Reserve_Parking_Spot.query.filter_by(user_id=session.get('userid')).\
                order_by(Reserve_Parking_Spot.Parking_timestamp.desc()).limit(4).all()
            if request.method=="POST":
                return redirect(url_for('Release_Spot',booking_id=int(request.form.get('release_out'))))

            return render_template('Userdashboard.html',spots=userspot)


        elif session.get('userType')=='admin':
            lots=Parking_Lot.query.all()
            spots=[]
            for lot in lots:
                spot = Parking_Spot.query.filter_by(lot_id=lot.id).all()
                spots.append(spot)
            if request.method == "POST":
                action = request.form.get('action')
                lotid = request.form.get('lot_id')
                if action=='edit':
                    return redirect(url_for('editparkinglot',lot_id=int(lotid)))
                elif action=='delete':
                    lot = Parking_Lot.query.filter_by(id=int(lotid)).first()
                    spot=Parking_Spot.query.filter_by(lot_id=lot.id,status='O').all()
                    if spot:
                        flash(f"Some spots are occupied in lot {lot.id}! Cannot be deleted!",
                              category="danger")
                        return redirect(url_for('dashboard'))
                    db.session.delete(lot)
                    db.session.commit()
                    return redirect(url_for('dashboard'))

            return render_template('AdminDashboard.html',lots=lots,spots=spots)

        else:
            flash('Error in Login','warning')
            return redirect(url_for('login'))

    """============User- To release the spot============"""
    @app.route('/dashboard/release_spot/<int:booking_id>',methods=['GET','POST'])
    def Release_Spot(booking_id):

        email = session.get('email')
        if not email:
            flash("Session Expired! Login Again!", 'warning')
            return redirect(url_for('login'))

        form = Release_Spot_Form()
        spot = Reserve_Parking_Spot.query.filter_by(id=booking_id).first()
        record = Booking_records.query.filter(and_(Booking_records.user_id==session.get('userid'),
                                                   Booking_records.vehicle_no==spot.vehicle_no,
                                                   Booking_records.id==booking_id)).first()

        curr_time = datetime.now()
        if request.method=='GET':

            price = spot.spot.lot.price
            spot.Leaving_timestamp = curr_time
            form.booking_id.data = booking_id
            form.vehicle_no.data = spot.vehicle_no
            form.Park_in_timestamp.data = f"{spot.Parking_timestamp.strftime('%d-%m-%Y')} - {spot.Parking_timestamp.strftime('%H:%M:%S')}"
            form.Leave_out_timestamp.data = f"{spot.Leaving_timestamp.strftime('%d-%m-%Y')} - {spot.Leaving_timestamp.strftime('%H:%M:%S')}"
            calculated_price = SetPrice(price, spot.Parking_timestamp, spot.Leaving_timestamp)
            form.Total_cost.data = calculated_price

        if form.validate_on_submit():
            spot.spot.lot.no_spot_occupied -= 1
            price = spot.spot.lot.price
            spot.Leaving_timestamp = curr_time
            calculated_price = SetPrice(price, spot.Parking_timestamp, curr_time)
            spot.parking_cost = calculated_price
            record.price = calculated_price
            record.leaving_timestamp = curr_time
            spot.occupancy = "Released"
            spot.spot.status = "A"
            db.session.commit()
            return redirect(url_for('dashboard'))

        return render_template("release_spot.html",form=form)

    '''========== Adding Parking Lot ================'''
    @app.route('/dashboard/AddParkingLot',methods=['GET','POST'])
    def AddingParkingLot():

        email=session.get('email')
        if not email:
            flash("Session Expired! Login Again!",'warning')
            return redirect(url_for('login'))

        form=AddingParkinglot()

        if form.validate_on_submit():
            createparkingspot=Parking_Lot(city=form.city.data,prime_location_name=form.locationName.data,
                                          price=form.price.data,address=form.address.data,
                                          pincode=form.pincode.data,max_no_spots=form.No_Spots.data)
            db.session.add(createparkingspot)
            db.session.commit()
            lotNo=Parking_Lot.query.filter_by(prime_location_name=form.locationName.data).first().id
            for i in range(form.No_Spots.data):
                spot=Parking_Spot(lot_id=lotNo,status="A")
                db.session.add(spot)
            db.session.commit()
            return redirect(url_for('dashboard'))

        return render_template('AddParkingLot.html',form=form)

    '''========== Adding Parking Spot ================'''
    @app.route('/dashboard/AddParkingSpot',methods=['GET','POST'])
    def AddingParkingSpot():

        email=session.get('email')
        if not email:
            flash("Session Expired! Login Again!",'warning')
            return redirect(url_for('login'))

        Areas=[]
        selected_city=None
        Lots=db.session.query(Parking_Lot.city).distinct().all()
        city_list = [c[0] for c in Lots]
        if request.method=='POST':
            selected_city=request.form.get('ChoosingArea')
            if selected_city:
                Areas=(db.session.query(Parking_Lot.prime_location_name)\
                       .filter_by(city=selected_city).distinct().all())
        area_list = [c[0] for c in Areas]

        return render_template('AddingParkingSpot.html',Lots=city_list,
                               Areas=area_list,selected_city=selected_city)

    '''========== Admin-Functionality-To View Users ================'''
    @app.route('/dashboard/users')
    def viewusers():
        email=session.get('email')
        if not email:
            flash("Session Expired! Login Again!",'warning')
            return redirect(url_for('login'))

        if session.get('userType')=='admin':
            users=User.query.all()
            user_id_list=[user.id for user in users]
            detail_of_user = []
            for i in user_id_list:
                details=Booking_records.query.filter_by(user_id=i)
                detail_of_user.append(details)
            list_of_spots = [k for i in detail_of_user for k in i]
            '''
            for user in users:
                user_id_list.append(user.id)
            for i in user_id_list:
                details=Reserve_Parking_Spot.query.filter_by(user_id=i).all()
                
            '''
            return render_template('ViewUsers.html',
                                   users=users,spots=list_of_spots)
        return redirect(url_for('dashboard'))

    '''========== Admin-Functionality-To Edit ParkingLot ================'''
    @app.route('/dashboard/editparkingLot/<int:lot_id>',methods=['GET','POST'])
    def editparkinglot(lot_id):
        email=session.get('email')
        if not email:
            flash("Session Expired! Login Again!",'warning')
            return redirect(url_for('login'))

        if session.get('userType')=='admin':
            form=AddingParkinglot()
            lot=Parking_Lot.query.filter_by(id=lot_id).first()
            old_spot=lot.max_no_spots

            if request.method=="GET":
                form.city.data = lot.city
                form.locationName.data = lot.prime_location_name
                form.price.data = lot.price
                form.address.data = lot.address
                form.pincode.data = lot.pincode
                form.No_Spots.data = lot.max_no_spots

            if form.validate_on_submit():
                lot.city = form.city.data
                lot.prime_location_name = form.locationName.data
                lot.price = form.price.data
                lot.address = form.address.data
                lot.pincode = form.pincode.data
                lot.max_no_spots = form.No_Spots.data

                if old_spot<form.No_Spots.data:
                    for _ in range(form.No_Spots.data-old_spot):
                        new_spot=Parking_Spot(lot_id=lot_id,status="A")
                        db.session.add(new_spot)

                elif old_spot>form.No_Spots.data:
                    spot_to_delete=Parking_Spot.query.filter_by(lot_id=lot_id,status='A')\
                        .order_by(Parking_Spot.id.desc())\
                        .limit(old_spot-form.No_Spots.data).all()
                    for spot in spot_to_delete:
                        db.session.delete(spot)
                db.session.commit()
                return redirect(url_for('dashboard'))

            return render_template('EditParkingLot.html',form=form)

        return redirect(url_for('dashboard'))

    '''========== Admin-Functionality-To Edit ParkingSpot ================'''
    @app.route('/dashboard/editparkingspot/<int:lot_id>',methods=['GET','POST'])
    def EditParkingSpot(lot_id):

        email=session.get('email')
        if not email:
            flash("Session Expired! Login Again!",'warning')
            return redirect(url_for('login'))

        if session.get('userType')=='admin':

            spots = Parking_Spot.query.filter_by(lot_id=lot_id).all()
            lot = Parking_Lot.query.filter_by(id=lot_id).first()
            detail = Reserve_Parking_Spot.query.join(Parking_Spot).filter(Parking_Spot.status=='O')\
                .filter(Reserve_Parking_Spot.occupancy=="Occupied").all()

            if request.method=="POST":
                if request.form.get('action')=='delete':
                    spotid = request.form.get('spot_id')
                    spot = Parking_Spot.query.filter_by(id=int(spotid)).first()
                    no_spots = Parking_Lot.query.filter_by(id=lot_id).first()
                    no_spots.max_no_spots -=1
                    flash(f'Successfully deleted the spot {spot.id}',
                          'success')
                    db.session.delete(spot)
                    db.session.commit()
                    return redirect(url_for("EditParkingSpot",lot_id=lot_id))

            return render_template('EditParkingSpot.html',spots=spots,
                                   lot=lot,details=detail)

        return redirect(url_for('dashboard'))

    '''========== User-Functionality-To book ParkingSpot ================'''
    @app.route('/dashboard/bookspot/<int:user_id>',methods=['GET','POST'])
    def UserBookSpot(user_id):

        email=session.get('email')
        if not email:
            flash("Session Expired! Login Again!",'warning')
            return redirect(url_for('login'))

        if session.get('userType')=='user':
            Lots=db.session.query(Parking_Lot.city).distinct().all()
            #Lots=Parking_Lot.query.distinct().all()
            city_list = [c.city for c in Lots]
            selected_city=None
            area=[]

            if request.method=="POST":
                selected_city=request.form.get("ChoosingArea")

                if selected_city:
                    area=Parking_Lot.query.filter_by(city=selected_city).distinct().all()

                selected_area=request.form.get('Area')
                vehicle_no=request.form.get("vehicleNo")

                if selected_city and selected_area and vehicle_no:
                    lotId=Parking_Lot.query.filter_by(city=selected_city,prime_location_name=selected_area).first()
                    spotId=Parking_Spot.query.filter_by(lot_id=lotId.id,status='A').first()
                    reverse_spot=Reserve_Parking_Spot(spot_id=spotId.id,user_id=user_id,
                                                      vehicle_no=vehicle_no,parking_timestamp=datetime.now())
                    record=Booking_records(user_id=user_id,lot_id=lotId.id,spot_id=spotId.id,
                                           parking_timestamp=datetime.now(),vehicle_no=vehicle_no,
                                           location_name=lotId.prime_location_name)
                    spotId.status='O'
                    lotId.no_spot_occupied+=1
                    db.session.add(reverse_spot)
                    db.session.add(record)
                    db.session.commit()
                    return redirect(url_for('dashboard'))

            return render_template("UserBookingLot.html",Lots=city_list,
                                   selected_city=selected_city,Areas=area)

        return redirect(url_for('dashboard'))

    '''============Edit Profile for Users=============='''
    @app.route('/dashboard/edit-profile',methods=['GET','POST'])
    def editprofile():
        email=session.get('email')
        if not email:
            flash("Session Expired! Login Again!",'warning')
            return redirect(url_for('login'))
        form = Edit_Profile()
        user = User.query.filter_by(id=session.get('userid')).first()
        if request.method=='GET':
            form.name.data = user.name
        if form.validate_on_submit():
            if user and user.check_password(form.current_password.data):
                if form.password.data == form.confirm_password.data:
                    user.password = user.set_password(form.password.data)
                    db.session.commit()
                    flash("Password updated successfully", "success")
                    return redirect(url_for('dashboard'))
                else:
                    flash('New Password and Confirm Password not Matching',"danger")
                    return redirect(url_for('editprofile'))
            else:
                flash("Current Password and Existing Password not matching!",'danger')
                return redirect(url_for('editprofile'))
        return render_template('editprofile.html',form = form)

    """=========Summary==========="""
    @app.route('/dashboard/summary')
    def summary():

        email=session.get('email')
        if not email:
            flash("Session Expired! Login Again!",'warning')
            return redirect(url_for('login'))

        if session.get('userType')=='admin':
            user_price=db.session.query(Booking_records.user_id,func.sum(Booking_records.price))\
                .group_by(Booking_records.user_id).all()
            user=["User Id "+str(i[0]) for i in user_price]
            price=[i[1] for i in user_price]
            total_spots=db.session.query(func.sum(Parking_Lot.max_no_spots)).scalar()
            total_occupied_spots=db.session.query(func.sum(Parking_Lot.no_spot_occupied)).scalar()
            total_unoccupied_spot=total_spots-total_occupied_spots
            return render_template('AdminSummary.html',User=user,
                                   Price=price,Occupied_spot=total_occupied_spots,
                                   UnOccupiedSpot=total_unoccupied_spot)
        elif session.get('userType')=='user':
            userid=session.get('userid')
            records=Booking_records.query.filter(Booking_records.user_id==userid,
                                                      Booking_records.leaving_timestamp!=None).all()
            total_spots=db.session.query(func.sum(Parking_Lot.max_no_spots)).scalar()
            total_occupied_spots=db.session.query(func.sum(Parking_Lot.no_spot_occupied)).scalar()
            total_unoccupied_spot=total_spots-total_occupied_spots
            return render_template('UserSummary.html',Occupied_spot=total_occupied_spots,
                                   UnOccupiedSpot=total_unoccupied_spot,records=records)
        return None

    """========Admin Search Option============"""
    @app.route('/dashboard/search',methods=['GET','POST'])
    def search():
        email=session.get('email')
        if not email:
            flash("Session Expired! Login Again!",'warning')
            return redirect(url_for('login'))
        selected_option=None
        results=[]
        lots=[]
        user=None
        flag=0
        if request.method=="POST":
            category=request.form.get("search_by")
            search_string=request.form.get('search')
            if category=="User":
                flag=1
                selected_option='User'
                try:
                    user_id = int(search_string)
                except:
                    user_id = None
                user=User.query.filter(
                    or_(User.id == user_id,
                        User.email.ilike(f"%{search_string}%"),
                        User.name.ilike(f"%{search_string}%"))).first()
                if user:
                    results=Booking_records.query.filter_by(user_id=user.id).all()
            if category=="parking_location":
                selected_option='parking_location'
                flag=2
                try:
                    lot_id=int(search_string)
                except:
                    lot_id=None
                lots=Parking_Lot.query.filter(or_(
                    Parking_Lot.id==lot_id,
                    Parking_Lot.city.ilike(f"%{search_string}%"),
                    Parking_Lot.prime_location_name.ilike(f"%{search_string}%")
                )).all()
        return render_template('AdminSearch.html',
                               selected_option=selected_option,user=user,
                               results=results,flag=flag,lots=lots)
    
    """========Logout========="""
    @app.route('/logout')
    def logout():
        session.pop('email',None)
        session.pop('name',None)
        session.pop('userType',None)
        session.clear()
        flash("You are logged out!!!",'info')
        return redirect(url_for('login'))
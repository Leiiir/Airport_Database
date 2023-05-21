from io import SEEK_CUR
from flask import Flask, request, session, redirect, url_for, render_template, jsonify
# from flask import Flask, request, session, redirect, url_for, render_template, jsonify

from datetime import datetime
import calendar
from flaskext.mysql import MySQL
import pymysql
import re
import yaml
from markupsafe import escape
import random
#import pandas as pd

# flask --app testflask --debug run

app = Flask(__name__)
mysql = MySQL()

app.config['MYSQL_DATABASE_HOST'] = 'database-1-kevin-sun.cvxdo8dkmepm.us-east-1.rds.amazonaws.com'
app.config['MYSQL_DATABASE_USER'] = 'admin'
app.config['MYSQL_DATABASE_PASSWORD'] = 'Killccp720513'
app.config['MYSQL_DATABASE_DB'] = 'feitian'

mysql.init_app(app)

# change this to your secret key
# (can be anything, it's for extra protection)
app.secret_key = "SOH"


@app.route("/", methods=["GET", "POST"])
def login():

    # connect
    conn = mysql.connect()
    cursor = conn.cursor(pymysql.cursors.DictCursor)

    # output message if something goes wrong...
    msg = "FAILED TO CONNECT"

    if request.method == 'POST':
        if request.form.get('loginbutton') == 'submit':
           # global global_username
            #global_username = request.form['username']
            #global_password = request.form['password']

            username = request.form['username']
            password = request.form['password']

            cursor.execute(
                "SELECT * FROM Account WHERE Account_Username = %s AND Account_Password = %s",
                (username, password),
            )

            account = cursor.fetchone()

            # if account exists in accounts table in our database
            if account:
                persontype = account['person_type']
                
                if persontype == 'manager':
                    return render_template('manager.html')

                if persontype == 'customer':
                    return render_template('customer.html')


            else:
                # account doesnt exist or username/password incorrect
                msg = "Incorrect username or password!"
                return f'<h1>{msg}<br></h1>'
        else:
            return     f'<h1> "password!"</h1>'    

    else:
        # return render_template('index.html')
        return render_template('index.html')
    
@app.route("/logout")
def logout():
    return redirect(url_for("login"))



@app.route("/manager", methods=["GET", "POST"])
def manager():

    # connect

    conn = mysql.connect()
    cursor = conn.cursor(pymysql.cursors.DictCursor)

    if request.method == 'POST':
        if request.form.get('Logout') == 'submit':
            return redirect(url_for("login"))


        if request.form.get('searchbutton') == 'submit':

            startdate = request.form['startdate']
            enddate = request.form['enddate']

            cursor.execute(
                """
                SELECT *
                FROM Reservation 
                WHERE DATE(Reserved_Date) BETWEEN %s AND %s
                """,
                (startdate, enddate),
            )
            result = cursor.fetchall()

            return render_template('query_result.html', result=result)
        
        if request.form.get('allflights') == 'submit':

            cursor.execute(
                """
                select *
                from Flights
                """
            )

            result = cursor.fetchall()
            return render_template('query_result.html', result=result)
        if request.form.get('Add_information_for_employee') == 'submit':

            SSN_Add_Update_information_for_employee= request.form['SSN_Add_Update_information_for_employee']
            Start_Date_Add_Update_information_for_employee = request.form['Start_Date_Add_Update_information_for_employee']
            Hourly_Rate_Add_Update_information_for_employee = request.form['Hourly_Rate_Add_Update_information_for_employee']
            add_employee_information = (
             "INSERT INTO `feitian`.`Employee` (`SSN`, `Start_Date`, `Hourly_Rate`)"
             "VALUES (%s, %s, %s)"
              )
            add_employee_information_data = (SSN_Add_Update_information_for_employee,Start_Date_Add_Update_information_for_employee,Hourly_Rate_Add_Update_information_for_employee)  
            cursor.execute(add_employee_information,add_employee_information_data)
            conn.commit()

            return  render_template('manager.html')

        if request.form.get('Update_information_for_employee') == 'submit':

            SSN_Update_information_for_employee= request.form['SSN_Update_information_for_employee']
            Hourly_Rate_Update_information_for_employee = request.form['Hourly_Rate_Update_information_for_employee']
            #cursor.execute("""UPDATE `feitian`.`Employee` SET `Hourly_Rate` = 'Hourly_Rate_Update_information_for_employee ' WHERE (`SSN` = 'SSN_Update_information_for_employee');""")
            cursor.execute ("""
              UPDATE `feitian`.`Employee`
              SET `Hourly_Rate`=%s
              WHERE `SSN`=%s
               """, (Hourly_Rate_Update_information_for_employee, SSN_Update_information_for_employee))   
            conn.commit()
            #return f'<p>{SSN_Update_information_for_employee}</p>'
            return  render_template('manager.html')   

        if request.form.get('Delete_information_for_employee') == 'submit':

            SSN_Delete_information_for_employee= request.form['SSN_Delete_information_for_employee']
            #cursor.execute("""UPDATE `feitian`.`Employee` SET `Hourly_Rate` = 'Hourly_Rate_Update_information_for_employee ' WHERE (`SSN` = 'SSN_Update_information_for_employee');""")
            delete_information_Employee = "DELETE FROM `feitian`.`Employee` WHERE  `SSN` =%s"
            cursor.execute(delete_information_Employee, (SSN_Delete_information_for_employee))
            conn.commit()
            return render_template('manager.html') 
        if request.form.get('Add_information_for_Customer') == 'submit':

            SSN_Add_information_for_Customer= request.form['SSN_Add_information_for_Customer']
            Email_Address_Add_information_for_Customer= request.form['Email_Address_Add_information_for_Customer']
            Credit_Card_Add_information_for_Customer= request.form['Credit_Card#_Add_information_for_Customer']
            Account_Add_information_for_Customer= request.form['Account#_Add_information_for_Customer']
            Preference_Add_information_for_Customer= request.form['Preference_Add_information_for_Customer']
            #cursor.execute("""UPDATE `feitian`.`Employee` SET `Hourly_Rate` = 'Hourly_Rate_Update_information_for_employee ' WHERE (`SSN` = 'SSN_Update_information_for_employee');""")
            Add_information_Customer ="""`feitian`.`Customer` (`SSN`, `Email_Address`, `Credit_Card#`, `Account#`, `Preference`)
            VALUES (%s, %s, %s, %s, %s);"""
        
            cursor.execute(Add_information_Customer, (SSN_Add_information_for_Customer,Email_Address_Add_information_for_Customer,Credit_Card_Add_information_for_Customer,Account_Add_information_for_Customer, Preference_Add_information_for_Customer))
            conn.commit()
            return render_template('manager.html') 
        if request.form.get('Update_Customer_information') == 'submit':

            Credit_Card_Update_information_for_Customer= request.form['Credit_Card#_Update_information_for_Customer']
            Preference_Update_information_for_Customer= request.form['Preference_Update_information_for_Customer']
            Update_information_Customer ="""`UPDATE `feitian`.`Customer` SET `Preference` = %s WHERE (`Credit_Card#` = %s);;"""
        
            cursor.execute(Update_information_Customer , (Credit_Card_Update_information_for_Customer,Preference_Update_information_for_Customer))
            conn.commit()
            return render_template('manager.html')      
        if request.form.get('Delete_information_for_Customer') == 'submit':

            Credit_Card_Update_information_for_Customer= request.form['Credit_Card#_Delete_information_for_Customer']
            Delete_information_Customer ="""DELETE FROM `feitian`.`Customer` WHERE (`Credit_Card#` = %s);"""
        
            cursor.execute(Delete_information_Customer , (Credit_Card_Update_information_for_Customer))
            conn.commit()
            return render_template('manager.html')                                 
            #return  render_template('manager.html')    
        if request.form.get('reservations_by_flights_number') == 'submit':

            List_of_reservations_by_flights_number= request.form['List_of_reservations_by_flights_number']

            cursor.execute("""
            SELECT *
            FROM Reservation 
            WHERE `Flight#` = %s
            """ , (List_of_reservations_by_flights_number))
            result = cursor.fetchall()
            conn.commit()
            return render_template('reservations.html',result=result)  
        if request.form.get('reservations_by_flights_number') == 'submit':

            List_of_reservations_by_flights_number= request.form['List_of_reservations_by_flights_number']

            cursor.execute("""
            SELECT *
            FROM Reservation 
            WHERE `Flight#` = %s
            """ , (List_of_reservations_by_flights_number))
            result = cursor.fetchall()
            conn.commit()
            return render_template('reservations.html',result=result)  

        if request.form.get('reservations_by_customer_name') == 'submit':

            List_of_reservations_by_Account= request.form['List_of_reservations_by_Account']

            cursor.execute("""
            SELECT *
            FROM Reservation 
            WHERE `Account_Num`  = %s
            """ , (List_of_reservations_by_Account))
            result = cursor.fetchall()
            conn.commit()
            return render_template('reservations.html',result=result) 

            
        if request.form.get('revenue_generated_by_a_particular_flight') == 'submit':

            Summary_of_revenue_generated_by_a_particular_flight= request.form['Summary_of_revenue_generated_by_a_particular_flight']

            cursor.execute("""
                        select `Flight#`, sum(TotalFare)
                        from Reservation 
                        WHERE `Flight#`=  %s 
                        group by `Flight#` 
            """ , (Summary_of_revenue_generated_by_a_particular_flight) )
            result = cursor.fetchall()
            conn.commit()
            return f'<p>{result}</p>'

        if request.form.get('revenue_generated_by_a_particular_Customer') == 'submit':

            Summary_of_revenue_generated_by_a_particular_Customer= request.form['Summary_of_revenue_generated_by_a_particular_Customer']

            cursor.execute("""
                            select Account_Num, sum(TotalFare)
                            from Reservation 
                            where Account_Num = %s
            """ , (Summary_of_revenue_generated_by_a_particular_Customer))
            result = cursor.fetchall()
            conn.commit()
            return f'<p>{result}</p>'  



            
        if request.form.get('Determine_which_customer_generated_most_total_revenue') == 'submit':
            cursor.execute("""
                            select First_Name, Last_Name, Account_Num, sum_totafare 
                            from
                            (select SSN, Account_Num, sum_totafare
                            from
                            (select *
                            from
                            (select Account_Num, sum(TotalFare) as sum_totafare
                            from Reservation 
                            group by Account_Num 
                            order by sum(TotalFare) desc
                            limit 1) as tmp , Customer c
                            where c.`Account#` = tmp.Account_Num) as tmp1) as tmp2, People p
                            where tmp2.SSN = p.SSN
            """ )
            result = cursor.fetchall()
            conn.commit()
            return f'<p>{result}</p>' 



        if request.form.get('Most_Active_Flight') == 'submit':
            cursor.execute("""
                                    select `Flight#`, Days_of_Week
                                    from Flights 
                                    group by `Flight#`
                                    order by char_length(Days_of_Week) desc
                                    limit 3
            """ )
            result = cursor.fetchall()
            conn.commit()
            return render_template('query_result.html', result=result)      

        if request.form.get('List_of_all_customers_who_have_seats_reserved_on_a_given_flight') == 'submit':
            customers_who_have_seats_reserved_on_a_given_flight= request.form['customers_who_have_seats_reserved_on_a_given_flight']

            cursor.execute("""
                                   select c.`Account#`, p.First_Name, p.Last_Name, r.`Flight#`
                                    from Reservation r, Customer c, People p
                                    where `Flight#` = 'HI_002' AND r.Account_Num = c.`Account#` AND c.SSN = p.SSN
            """ )
            result = cursor.fetchall()
            conn.commit()
            #return f'<p>{result}</p>'  
            return render_template('query_result.html', result=result)



        if request.form.get('Produce_a_List_of_all_flights_for_a_given_airport') == 'submit':
            List_of_all_flights_for_a_given_airport= request.form['List_of_all_flights_for_a_given_airport']

            cursor.execute("""
                            select f.`Flight#`, s.AirportID, f.Flight_Fare, f.`Destination-City`
                            from Stops s, Flights f
                            where s.AirportID = %s AND s.`Flight#` = f.`Flight#`
            """ ,(List_of_all_flights_for_a_given_airport))
            
            result = cursor.fetchall()
            conn.commit()
            #return f'<p>{result}</p>'  
            return render_template('query_result.html', result=result)   


        else: return f'<p>Button not function (issure of post) </p>'
                            
    else:
        return render_template('manager.html')


@app.route("/customer", methods=["GET", "POST"])
def customer():
    # connect
    conn = mysql.connect()
    cursor = conn.cursor(pymysql.cursors.DictCursor)

    if request.method == 'POST':
        if  request.form.get('Logout_customer') == 'submit': 
            return redirect(url_for("login"))

        if  request.form.get('citysearch') == 'submit':  
            city = request.form['citytogo']
            city = str(city)
            cursor.execute(
                # select AirlineID, fl.`Flight#`, Flight_Fare, Stops, Number_of_Seats, Days_of_Week
                # select fl.*
                """
                select *
                from Flights fl
                inner join Stops st on fl.`Flight#` = st.`Flight#` 
                inner join Airport ar on st.AirportID = ar.AirportID
                where ar.City = %s
                """,
                (city)
                )
            result = cursor.fetchall()

            return render_template('reserveticket.html', result=result)

        if  request.form.get('search') == 'submit':   
            whichway = request.form.getlist('whichway') 
            travel = request.form.getlist('travel')
                
            if len(travel) == 0:
                cursor.execute(
                """
                SELECT *
                FROM Flights 
                WHERE Flight_type = %s
                """,
                (whichway[0])
                )
                result = cursor.fetchall()

                return render_template('reserveticket.html', result=result)
                # return render_template('query_result.html', result=result)
                # return f'{travel}'
            
            else:
                cursor.execute(
                """
                SELECT *
                FROM Flights 
                WHERE Flight_type = %s AND Travel = %s
                """,
                (whichway[0], travel[0])
                )
                result = cursor.fetchall()

                if len(result) == 0:
                    return "<h1>Sorry we don't provide such flights yet<h1>"
                
                else: 
                    return render_template('reserveticket.html', result=result)
                    # return render_template('query_result.html', result=result)

        if  request.form.get('bestseller') == 'submit':
            cursor.execute(
            """
            select Times_Purchased, fl.* 
            from
            (select `Flight#` as ppfl, count(*) as Times_Purchased
            from Reservation r
            group by `Flight#`
            order by count(*) desc) as popular, Flights fl
            where popular.ppfl = fl.`Flight#`
            order by Times_Purchased desc
            """
            )
            result = cursor.fetchall()
            
            return render_template('reserveticket.html', result=result)
            # return render_template('query_result.html', result=result)

        if  request.form.get('cancelbutton') == 'submit':

            cancelnum = request.form['cancelnum']

            cursor.execute(
            f"""
            DELETE FROM `feitian`.`Reservation` WHERE (`Reservation_Num` = {cancelnum});
            """,
            ()
            )
            conn.commit()

            return f'SUCCEFFULLY CANCELED {cancelnum}'

    else:
        return render_template('customer.html')


@app.route("/reserveticket", methods=["GET", "POST"])
def reserveticket():

    # connect
    conn = mysql.connect()
    cursor = conn.cursor(pymysql.cursors.DictCursor)

    if request.method == 'POST':
        if  request.form.get('reservebutton') == 'submit':  
            accountnum = request.form['Account#']
            flightnum = request.form['Flight#']
            reservetime = str(datetime.now())
            preferseat = request.form['preferseat']
            prefermeal = request.form['prefermeal']
            reservationnum = random.randint(111329, 111999)
            fare = request.form['Flight_Fare']

            cursor.execute(
                f'''
                INSERT INTO `feitian`.`Reservation` (`Reservation_Num`, `Account_Num`, `Flight#`, `TotalFare`, `Reserved_Date`, `Seat_Preference`, `Preferred_Meal`) 
                VALUES ('{reservationnum}', '{accountnum}', '{flightnum}', '{fare}', '{reservetime}', '{preferseat}', '{prefermeal}');
                '''
            )
            conn.commit()
            return f'SUCCEFULLY RESERVED FOR {flightnum},\n,Your Reservation Number: {reservationnum}'
        else:
            return "AN ERROR OCCURED DIDN'T RESERVE"

    else:
        return render_template('reserveticket.html')


if __name__ == '__main__':
    # app.run(debug=True)
    app.run(host='0.0.0.0', port=80, debug=True)

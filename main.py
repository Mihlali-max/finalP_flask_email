import sqlite3
from flask import Flask, request, jsonify
from flask_mail import Mail , Message

from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# configuration of mail
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = 'momozamihlali@gmail.com'
app.config['MAIL_PASSWORD'] = 'khazimla'
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
mail = Mail(app)


# Defining the function that opens sqlite database and creates table
def create_users_table():
    connect = sqlite3.connect('food.db')
    print("Databases has opened")

    connect.execute('CREATE TABLE IF NOT EXISTS users (user id INTEGER, fullname TEXT, email_address TEXT, phone INTEGER, Adults INTEGER, Children INTEGER,  Checkin TEXT ,Checkout TEXT, DISH TEXT, ANYTHINGELSE TEXT )')
    print("Table was created successfully")
    connect.close()


def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d


create_users_table()

# Route for opening the registration form


# Fetching form info and adding users to database
@app.route('/')
@app.route('/add/', methods=['POST', 'GET'])

def add_users():
    if request.method == 'POST':
        try:

            fullname = request.form['customer_name']
            email_address = request.form['customers_email']
            phone = request.form['visitor_phone']
            Adults = request.form['total_adults']
            Children = request.form['total_children']
            Checkin = request.form['checkin']
            Checkout = request.form['checkout']
            DISH =request.form['dish']
            ANYTHINGELSE =request.form['text']

            #username = request.form['username']
            #password = request.form['password']
            #confirm_password = request.form['confirm']
            # email = request.form['email']

            if fullname == fullname:
                with sqlite3.connect('food.db') as con:
                    cursor = con.cursor()
                    cursor.execute("INSERT INTO users (fullname, email_address, phone, Adults, Children ,Checkin ,Checkout , DISH ,ANYTHINGELSE) VALUES (?, ?, ?, ?, ?,?,?,?,?)", (fullname, email_address, phone, Adults,Children,Checkin,Checkout,DISH,ANYTHINGELSE))
                    con.commit()
                    msg = fullname + " was added to the databases"
                    send_mail(fullname, email_address, Adults,Children, Checkin ,Checkout, DISH)
                    return jsonify(msg)
        except Exception as e:
            # con.rollback()
            msg = "Error occured in insert " + str(e)
        # finally:
        #
        #     # con.close()
        # return jsonify(msg=msg)

        finally:

            con.close()
        return jsonify(msg=msg)


@app.route('/show-bookers/', methods=['GET'])
def show_bookers():
    users = []
    try:
        with sqlite3.connect('food.db') as connect:
            connect.row_factory = dict_factory
            cursor = connect.cursor()
            cursor.execute("SELECT * FROM users")
            users = cursor.fetchall()
    except Exception as e:
        connect.rollback()
        print("There was an error fetching results from the database: " + str(e))
    finally:
        connect.close()
        return jsonify(users)


# message object mapped to a particular URL ‘/’
@app.route('/mail/')
def index():
    msg = Message(
        "Hello Jason",
        sender='momozamihlali@gmail.com',
        recipients=['momozamihlali@gmail.com']
    )
    msg.body = 'Hello Flask message sent from Flask-Mail'
    mail.send(msg)
    return 'Sent'


def send_mail(fullname, email_address, Adults , Children, Checkin, Checkout,DISH):
    msg = Message(
        "Confirmation of booking",
        sender=email_address,
        recipients=[email_address]
    )
    msg.body = """
        Hello there {fullname},
        
        We are glad to hear that you are booking a table at Flavoursome for {no_adults} adults and {children} children on {checkin} :{checkout}
        
        Your mouth watering {food} is ready for you.
        
        For further information we'll contact you shortly at your email address : {email}
        
        we can't wait to see you !!
    """.format(fullname = fullname, email = email_address, no_adults = Adults ,children=Children ,checkin=Checkin,checkout=Checkout, food=DISH)
    mail.send(msg)


if __name__ =='__main__':
    app.run(debug=True)

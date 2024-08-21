from flask import *

import pymysql 

app = Flask(__name__)

# set secret key to secure you session/ nust be unique
app.secret_key ="AW_r%@jN*HU4AW_r%@jN*HU4AW_r%@jN*HU4"

@app.route('/')
def home():
    # connect database
        connection = pymysql.connect(host='localhost',user='root',password='',database='oryxdb')

    # smartphones category
        # create cursor which executes the sql query
        cursor =connection.cursor()


        # sql query
        smartphone_sql = "select * from products where product_category = 'Smartphones'"        
        # execute the query
        cursor.execute(smartphone_sql)
        # fetch the rows
        smartphones = cursor.fetchall()

        # sql query
        electronic_sql = "select * from products where product_category = 'Electronics'"        
        # execute the query
        cursor.execute(electronic_sql)
        # fetch the rows
        electronics = cursor.fetchall()


        # render to front-end
        return render_template('home.html', smartphones=smartphones,electronics=electronics)

@app.route('/upload',methods=['POST','GET'])
def upload():
    if request.method =='POST':
        product_name = request.form['product_name']
        product_desc = request.form['product_desc']
        product_cost = request.form['product_cost']
        product_category = request.form['product_category']
        product_image_name = request.files['product_image_name']
        product_image_name.save('static/images/'+product_image_name.filename)

        # connect database
        connection = pymysql.connect(host='localhost',user='root',password='',database='oryxdb')

        # create cursor which executes the sql query
        cursor =connection.cursor()

        # prepare data
        data =(product_name,product_desc,product_cost,product_category,product_image_name.filename)

        # sql query
        sql ='insert into products(product_name,product_desc,product_cost,product_category,product_image_name) VALUES (%s,%s,%s,%s,%s)'

        cursor.execute(sql,data)

        connection.commit()

        return render_template('upload.html',message='product added successffuly')
    else:
        return render_template('upload.html')
    
    
@app.route('/single_item/<product_id>')
def single(product_id):
    # connect database
    connection = pymysql.connect(host='localhost',user='root',password='',database='oryxdb')

    # create cursor which executes the sql query
    cursor =connection.cursor()

    # Create SQL  - %s is a placeholder, which will take the actual ID during Query Execution.
    product_sql = "SELECT * FROM products WHERE product_id = %s"

    # Execute SQL providing product_id - NB: Sql had a placeholder in the Where clause thats why we provide the product_id
    cursor.execute(product_sql, (product_id))

    # Get the product retrieved 
    product = cursor.fetchone()

    # similar product
    product_category =product[5]

    new_cursor = connection.cursor()

    similar_products = "select * from products where product_category = %s"

    new_cursor.execute(similar_products,product_category)

    similar =cursor.fetchall()
    
    # Return the product to single.html
    return render_template('single.html', product=product)


# sign up
@app.route('/signup', methods=['POST','GET'])
def signup():
     if request.method=='POST':
          username = request.form['username']
          email = request.form['email']
          phone = request.form['phone']
          password1 = request.form['password1']
          password2 = request.form['password2']

        #   check password
          if len(password1)< 8 :
               return render_template('signup.html', error='password must be more than 8 xters')
          elif password1 != password2 :
               return render_template('signup.html', error='password do not match')
          else:
               
            #connect to database
            connection = pymysql.connect(host='localhost',user='root',password='',database='oryxdb')

            # create cursor which executes the sql query
            cursor =connection.cursor()
            # prepare data
            userdata = (username,password2,email,phone)
            # sql query 
            user_sql = 'insert into users (username,password,email,phone) VALUES (%s,%s,%s,%s)'
            # execute the query
            cursor.execute(user_sql,(userdata))
            # commit to save in the database
            connection.commit()

            # send sms
            import sms
            sms.send_sms(phone, "Thank you for Registering")
            # return to the usr
            return render_template('signup.html' , success='Registration Successful')
     else:
          return render_template('signup.html')     

# sign in
    
@app.route('/signin', methods=['POST','GET'])
def signin():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
          #connect to database
        connection = pymysql.connect(host='localhost',user='root',password='',database='oryxdb')
        # create cursor which executes the sql query
        cursor =connection.cursor()
        # prepare data
        signindata =(username,password)
        # sql query
        signin_sql = 'select * from users where username = %s and password = %s'
        # execute
        cursor.execute(signin_sql,(signindata))
        # check the credentials
        if cursor.rowcount == 0:
             return render_template('signin.html', error='Invalid Credentials')
        else:
            #  successful login
            #  limk the session key with username
             session['key'] = username 
             return redirect('/')
    else:
          return render_template('signin.html')      

# Sign Out
@app.route('/logout')
def logout():
     session.clear()
     return redirect('/signin')

# payment
@app.route('/mpesa', methods=['POST'])
def mpesa():
     phone = request.form['phone']
     amount = request.form['amount']
    #  import mpesa.py module 
     import mpesa
     mpesa.stk_push(phone,amount)
    #  return message to user
     return '<h3>Complete payment on the phone</h3>'\
            '<a href="/">Back to Products</a>'


if __name__ == '__main__':
    app.run(debug=True)
from flask import *

import pymysql 

app = Flask(__name__)

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
    
    # Return the product to single.html
    return render_template('single.html', product=product)


if __name__ == '__main__':
    app.run(debug=True)
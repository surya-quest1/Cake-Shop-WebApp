from flask import Flask,request,jsonify
from flask_jwt_extended import JWTManager,create_access_token, jwt_required, get_jwt_identity
from dotenv import load_dotenv
import psycopg2
import os
import uuid


load_dotenv()
SECRET_DB = os.getenv('DB_CONNECTION_STRING')
JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY')

app = Flask(__name__)
app.config['JWT_SECRET_KEY'] = JWT_SECRET_KEY

jwt = JWTManager(app)

conn = psycopg2.connect(SECRET_DB)
cur = conn.cursor()

@app.route('/')
def main():
    return "Hello World"
    
@app.route('/users',methods=['POST'])
@jwt_required()
def create_user():
    
    user_params = request.args
    user_id = len(retrieve_data_from_db('users'))+1
    
    query = "INSERT INTO Users (UserID, Username, Email, Password) values (%s,%s,%s,%s);"
    data  = (user_id,user_params['username'],user_params['email'],user_params['password'])
    cur.execute(query,data)

    conn.commit()
    
    return jsonify(retrieve_data_from_db('users'))

@app.route('/users/u/<user_id>',methods=['PUT'])
def update_user(user_id):
    
    update_params = request.args
    update_attributes = ' '.join([str(key)+"='"+str(val)+"'" for key,val in update_params.items()])
            
    update_query = "UPDATE Users SET "+update_attributes.rstrip()+f" WHERE UserID = {user_id}"
    cur.execute(update_query)
        
    conn.commit()
    
    return jsonify(retrieve_data_from_db('users'))

@app.route('/users/u/<user_id>',methods=['DELETE'])
def delete_user(user_id):
    
    orderdet_delete_query = "DELETE FROM OrderDetails WHERE OrderID IN (SELECT OrderID FROM Orders WHERE UserID = %s);"
    cur.execute(orderdet_delete_query,user_id)
    
    order_delete_query = "DELETE from Orders where UserID = %s"
    cur.execute(order_delete_query,user_id)
    
    user_delete_query = "DELETE from Users where UserID = %s"
    cur.execute(user_delete_query,user_id)
    
    conn.commit()
    
    return jsonify(retrieve_data_from_db('users'))


@app.route('/products',methods=['POST'])
def create_product():
    
    product_params = request.args
    product_id = len(retrieve_data_from_db('products'))+1+100
    
    query = "INSERT INTO Products (ProductID, ProductName, Description, Price, Stock) VALUES (%s, %s, %s, %s, %s);"
    data  = (product_id,product_params['productname'],product_params['desc'],product_params['price'],product_params['stock'])
    
    cur.execute(query,data)
    
    conn.commit()
       
    return jsonify(retrieve_data_from_db('products'))

@app.route('/products/<product_id>',methods=['PUT'])
def update_product(product_id):
    
    update_params = request.args
    update_attributes = ' '.join([str(key)+"='"+str(val)+"'" for key,val in update_params.items()])
    
    update_query = "UPDATE Products SET "+update_attributes.rstrip()+f" WHERE ProductID = {product_id}"    
    cur.execute(update_query)
    
    conn.commit()
    
    return jsonify(retrieve_data_from_db('products'))

@app.route('/orders',methods=['POST'])
def create_orders():
    
    product_params = request.args
    product_id = len(retrieve_data_from_db('products'))+1+100
    
    query = "INSERT INTO Products (ProductID, ProductName, Description, Price, Stock) VALUES (%s, %s, %s, %s, %s);"
    data  = (product_id,product_params['productname'],product_params['desc'],product_params['price'],product_params['stock'])
    
    cur.execute(query,data)
    
    conn.commit()
       
    return jsonify(retrieve_data_from_db('products'))

@app.route('/products/<product_id>',methods=['PUT'])
def update_product(product_id):
    
    update_params = request.args
    update_attributes = ' '.join([str(key)+"='"+str(val)+"'" for key,val in update_params.items()])
    
    update_query = "UPDATE Products SET "+update_attributes.rstrip()+f" WHERE ProductID = {product_id}"    
    cur.execute(update_query)
    
    conn.commit()
    
    return jsonify(retrieve_data_from_db('products'))

@app.route('/products/<product_id>',methods=['DELETE'])
def delete_product(product_id):
    
    orderdet_delete_query = f"DELETE FROM OrderDetails WHERE OrderID IN (SELECT OrderID FROM Orders WHERE ProductID = {product_id});"
    cur.execute(orderdet_delete_query)
        
    product_delete_query = f"DELETE from Products where ProductID = {product_id}"
    cur.execute(product_delete_query)
    
    conn.commit()
    
    return jsonify(retrieve_data_from_db('products'))

@app.route('/data/<table_name>')
def retrieve_data_from_db(table_name):
    query = f"SELECT * FROM {table_name};"
    cur.execute(query)
    records = cur.fetchall()

    return records


if __name__ == '__main__':
    app.run(debug=True)
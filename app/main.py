from flask import Flask, request, jsonify
import os
import mysql.connector
from mysql.connector import Error

app = Flask(__name__)

def get_db_connection():
    try:
        connection = mysql.connector.connect(
            host=os.getenv('DB_HOST', 'db_master'),
            user=os.getenv('DB_USER', 'root'),
            password=os.getenv('DB_PASSWORD', 'root'),
            database=os.getenv('DB_NAME', 'testdb')
        )
        return connection
    except Error as e:
        print(f"Error connecting to MySQL: {e}")
        return None

@app.route('/')
def index():
    return jsonify({
        "message": "Flask MySQL Application",
        "status": "running"
    })

@app.route('/users', methods=['GET', 'POST'])
def users():
    connection = get_db_connection()
    if not connection:
        return jsonify({"error": "Database connection failed"}), 500
    
    cursor = connection.cursor(dictionary=True)
    
    if request.method == 'POST':
        data = request.get_json()
        name = data.get('name')
        email = data.get('email')
        
        if not name or not email:
            return jsonify({"error": "Name and email are required"}), 400
        
        try:
            cursor.execute(
                "INSERT INTO users (name, email) VALUES (%s, %s)",
                (name, email)
            )
            connection.commit()
            return jsonify({
                "message": "User created successfully",
                "user": {"name": name, "email": email}
            }), 201
        except Error as e:
            return jsonify({"error": str(e)}), 400
        finally:
            cursor.close()
            connection.close()
            
    elif request.method == 'GET':
        try:
            cursor.execute(""" 
                CREATE TABLE IF NOT EXISTS users (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    name VARCHAR(255) NOT NULL,
                    email VARCHAR(255) NOT NULL UNIQUE,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            
            # Verifica si hay usuarios en la tabla
            cursor.execute("SELECT COUNT(*) as count FROM users")
            count = cursor.fetchone()['count']
            
            # Inserta usuarios por defecto si la tabla está vacía
            if count == 0:
                default_users = [
                    ("Juan Pérez", "juan@example.com"),
                    ("Ana López", "ana@example.com"),
                    ("Carlos Gómez", "carlos@example.com")
                ]
                cursor.executemany(
                    "INSERT INTO users (name, email) VALUES (%s, %s)",
                    default_users
                )
                connection.commit()
            
            # Recupera y devuelve todos los usuarios
            cursor.execute("SELECT * FROM users")
            users = cursor.fetchall()
            return jsonify(users)
        except Error as e:
            return jsonify({"error": str(e)}), 400
        finally:
            cursor.close()
            connection.close()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

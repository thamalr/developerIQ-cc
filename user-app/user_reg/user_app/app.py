from flask import Flask, request, jsonify
import mysql.connector

app = Flask(__name__)

# Replace these values with your AWS RDS credentials
db_config = {
    'user': 'admin',
    'password': 'SxOg6M4EkmXXH01QU5AF',
    'host': 'database-cc.cgsfbie6tmcp.ap-southeast-1.rds.amazonaws.com',
    'database': 'database_users',
    'port': 3306,  # Change the port if your RDS instance uses a different one
    #'ssl_disabled': True,  # If you don't have SSL configured for your RDS instance
}

@app.route('/save_user', methods=['POST'])
def save_user():
    data = request.get_json()

    name = data.get('name')
    username = data.get('username')
    email = data.get('email')
    role = data.get('username')


    if not username or not email:
        return jsonify({'error': 'Missing required fields'}), 400

    try:
        # Create a connection to the RDS instance
        connection = mysql.connector.connect(**db_config)

        # Create a cursor to interact with the database
        cursor = connection.cursor()

        # Example query to insert user details into the database
        query = "INSERT INTO user (name, username, email, role) VALUES (%s, %s, %s, %s)"
        values = (name, username, email, role)

        cursor.execute(query, values)

        # Commit the changes
        connection.commit()

        return jsonify({'message': 'User details saved successfully'}), 201

    except Exception as e:
        return jsonify({'error': f'Failed to save user details: {str(e)}'}), 500

    finally:
        # Close the cursor and connection
        cursor.close()
        connection.close()

if __name__ == '__main__':
    app.run(debug=True)
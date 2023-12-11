from flask import Flask, render_template, jsonify
import mysql.connector

app = Flask(__name__)

# Replace the following with your AWS RDS database credentials
db_config = {
    'user': 'admin',
    'password': 'SxOg6M4EkmXXH01QU5AF',
    'host': 'database-cc.cgsfbie6tmcp.ap-southeast-1.rds.amazonaws.com',
    'database': 'database_users',
    'port': 3306,  # Change the port if your RDS instance uses a different one
}



@app.route('/users', methods=['GET'])
def view_all_users():
    try:
        connection = mysql.connector.connect(**db_config)
        cursor = connection.cursor()

        query = "SELECT user_id FROM productivity_metrics"
        cursor.execute(query)

        results = cursor.fetchall()

        users = [result[0] for result in results]

        return f"Registered Users with metrics: {', '.join(users)}"
    except Exception as e:
        return f"Error: {e}"

    finally:
        cursor.close()
        connection.close()

@app.route('/user/<user_id>', methods=['GET'])
def view_user_details(user_id):
    try:
        connection = mysql.connector.connect(**db_config)
        cursor = connection.cursor()

        # Fetch data from both tables using a JOIN
        query = f"""
            SELECT p.user_id, u.name, u.email, u.role, p.total_commits, p.total_pull_requests, p.total_issues
            FROM productivity_metrics p
            JOIN user u ON p.user_id = u.username
            WHERE p.user_id = '{user_id}'
        """
        cursor.execute(query)
        result = cursor.fetchone()

        if result:
            user_data = {
                'userid': result[0],
                'name': result[1],
                'email': result[2],
                'role': result[3],
                'total_commits': result[4],
                'total_pull_requests': result[5],
                'total_issues': result[6]
            }

            return jsonify(user_data)
        else:
            return jsonify({'error': 'User not found'})

    except Exception as e:
        return jsonify({'error': str(e)})

    finally:
        cursor.close()
        connection.close()

if __name__ == '__main__':
    app.run(debug=True)

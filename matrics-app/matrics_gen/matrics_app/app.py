from flask import Flask, jsonify, request
import mysql.connector
import requests

app = Flask(__name__)

# Replace the follpiowing with your AWS RDS database credentials
db_config = {
    'user': 'admin',
    'password': 'SxOg6M4EkmXXH01QU5AF',
    'host': 'database-cc.cgsfbie6tmcp.ap-southeast-1.rds.amazonaws.com',
    'database': 'database_users',
    'port': 3306,  # Change the port if your RDS instance uses a different one
    #'ssl_disabled': True,  # If you don't have SSL configured for your RDS instance
}

@app.route('/fetch_and_save_productivity/<username>', methods=['GET'])
def fetch_and_save_productivity(username):
    # Check if the user is registered
    user_id = get_user_id(username)

    if user_id is None:
        return jsonify({'error': 'User not found'}), 404

    # Retrieve the GitHub API token from your environment variables
    #github_api_token = 'your_github_api_token'
    #headers = {'Authorization': f'token {github_api_token}'}

    # Make a request to the GitHub API to get user activity metrics
    github_api_url = f'https://api.github.com/users/{username}/events'
    #response = requests.get(github_api_url, headers=headers)
    response = requests.get(github_api_url)
    if response.status_code == 200:
        events = response.json()

        # Calculate GitHub metrics
        total_commits = sum(1 for event in events if event['type'] == 'PushEvent')
        total_pull_requests = sum(1 for event in events if event['type'] == 'PullRequestEvent')
        total_issues = sum(1 for event in events if event['type'] == 'IssuesEvent')

        # Save metrics to the database
        save_metrics(user_id, total_commits, total_pull_requests, total_issues)

        return jsonify({'message': 'GitHub metrics saved successfully'}), 200
    else:
        return jsonify({'error': 'Failed to fetch data from GitHub API'}), response.status_code

def get_user_id(username):
    try:
        connection = mysql.connector.connect(**db_config)
        cursor = connection.cursor()

        query = "SELECT username FROM user WHERE username = %s"
        cursor.execute(query, (username,))
        result = cursor.fetchone()

        if result:
            return result[0]

    except Exception as e:
        print(f"Error: {e}")

    finally:
        cursor.close()
        connection.close()

    return None

def save_metrics(user_id, total_commits, total_pull_requests, total_issues):
    try:
        connection = mysql.connector.connect(**db_config)
        cursor = connection.cursor()

        query = "INSERT INTO productivity_metrics (user_id, total_commits, total_pull_requests, total_issues) VALUES (%s, %s, %s, %s)"
        values = (user_id, total_commits, total_pull_requests, total_issues)

        cursor.execute(query, values)
        connection.commit()

    except Exception as e:
        print(f"Error: {e}")

    finally:
        cursor.close()
        connection.close()

if __name__ == '__main__':
    app.run(debug=True)

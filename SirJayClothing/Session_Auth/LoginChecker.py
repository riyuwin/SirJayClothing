import requests

# Create a session object
session = requests.Session()

# Login
login_url = 'http://localhost:8000/api/auth/login/'
login_data = {
    'username': 'janjan',
    'password': 'janjan'
}

# Use the session object to send the login request
login_response = session.post(login_url, json=login_data)

if login_response.status_code == 200:
    print('Login successful!')
    # Access the token if the login was successful
    token = login_response.json().get('token')

    print(token)
    
    # Add the token to the session headers
    session.headers.update({'Authorization': f'Bearer {token}'})

        
    # Assuming session is your requests.Session() object
    authorization_header_value = session.headers.get('Authorization')
    print(f"Hey: {authorization_header_value}")
    
    # Check if the session token matches the user
    user_check_url = 'http://localhost:8000/api/auth/check_user/'
    user_check_response = session.get(user_check_url)
    
    if user_check_response.status_code == 200:
        print('Token matches the logged-in user.')
    else:
        print('Token does not match the logged-in user.')
else:
    print('Login failed:', login_response.text)

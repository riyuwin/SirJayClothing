import requests

# Assuming you have a practice token and username for demonstration purposes
token = 'f1270dac1e5b41fc7ab7c58eb433e1fa65bb5d90'
username = 'erwin'

# Logout
logout_url = 'http://localhost:8000/api/auth/logout/'

headers = {'Authorization': token}  # Assuming your API uses JWT tokens

print(headers['Authorization'])

logout_response = requests.post(logout_url, headers=headers)  # Corrected headers argument

if logout_response.status_code == 200:
    print('Logout successful!')
else:
    print('Logout failed:', logout_response.text)
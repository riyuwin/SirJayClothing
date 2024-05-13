import requests

# Create a session object
session = requests.Session()

# Assuming session is your requests.Session() object
authorization_header_value = session.headers.get('Authorization')
print(f"Hey: {authorization_header_value}")
 

# Check session cookies and headers
print("Cookies:")
print(session.cookies.get_dict())  # Get cookies as a dictionary

print("Headers:")
print(session.headers)  # Get session headers

# Access and print the token if it exists in cookies or headers
if 'token' in session.cookies:
    token = session.cookies['token']
    print("Token from cookies:", token)
elif 'token' in session.headers:
    token = session.headers['token']
    print("Token from headers:", token)
else:
    print("Token not found in cookies or headers")
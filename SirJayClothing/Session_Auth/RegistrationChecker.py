import requests

url = 'http://localhost:8000/api/auth/register/'
data = {
    'username': 'bogart',
    'password': 'bogart',
    'email': 'bogart@gmail.com'
}

response = requests.post(url, json=data)

if response.status_code == 201:
    print('Registration successful!')
else:
    print('Registration failed:', response.text)
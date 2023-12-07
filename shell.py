from django.contrib.auth.hashers import check_password
from ecommerce_app.models import Customer  # Cambia 'myapp' por el nombre de tu aplicación

# Reemplaza 'user@example.com' por el correo electrónico del usuario que estás probando
customer = Customer.get_customer_by_email('prueba2@gmail.com')
# Reemplaza 'su_contraseña' por la contraseña real que estás intentando verificar
is_correct = check_password('12345', customer.password)
print(is_correct)  # Esto debería ser True si la contraseña es correcta

####/////////////////verificacion  para realizar el  hash password


from django.contrib.auth.hashers import make_password
hashed_password = make_password('pruebados')
print(hashed_password)


##//////////////// comprobar password
from django.contrib.auth.hashers import check_password

# Reemplaza esto con el hash que generaste
password_hash = 'pbkdf2_sha256$260000$6XZ5yN0S9R6iOODYTjO0oX$+1/32aPNo3OSEH2zgmVz0M0QvhPmXMxB5WpmDiIIhc0=' 

# La contraseña que quieres verificar
password_to_check = 'pruebatres'

# Verifica si la contraseña coincide con el hash
is_valid = check_password(password_to_check, password_hash)
print(is_valid)
from flask import Flask, jsonify, request
from flask_jwt_extended import JWTManager, create_access_token, jwt_required
from prisma import Prisma
import uuid

app = Flask(__name__)
app.config['JWT_SECRET_KEY'] = 'super-secret'  
jwt = JWTManager(app)

def is_valid_uuid(uuid_str):
    try:
        uuid_obj = uuid.UUID(uuid_str)
        return True
    except ValueError:
        return False

@app.route('/api/createuser', methods=['POST'])
async def create_user():
    data = request.json
    email = data.get('email')
    password = data.get('password')
    uuid = data.get('uuid')

    print(data)

    if email is None or password is None or uuid is None:
        return jsonify({"test": "test"})
    
    if email == "" or password == "" or uuid == "":
        return jsonify({"message": "email, password or uuid is missing"})
    
    if uuid is None or not is_valid_uuid(uuid):
        return jsonify({"error": "Invalid UUID."}), 400
  
    jwtToken = create_access_token(identity={'email': email})  
    user_dict = {  
        'email': email,
        'password': password,
        'uuid': uuid,
        'jwt_token': jwtToken  
    }

    prisma = Prisma()
    await prisma.connect()
    user = await prisma.user.create(  
        data=user_dict
    )

    user_dict['id'] = user.id
    user_dict['status'] = 201

    return jsonify(user_dict)



@app.route('/api/authorize_uuid', methods=['POST'])
async def authorize_uuid():
    data = request.json
    email = data.get('email')
    password = data.get('password')
    uuid = data.get('uuid')

    if email is None or uuid is None or password is None:
        return jsonify({"error": "Email, user_id, and secret are required in the request."}), 400
    
    user = await Prisma.user.find_unique(
        where={
            uuid: uuid
        }
    )

    if user.isadmin:
        access_token = create_access_token(identity=user)
        return jsonify({"message": "access granted", "access_token": access_token})
    else:
        return jsonify({"message": "access denied"})

@app.route('/api/login', methods=['POST'])
async def login():
    data = request.json
    email = data.get('email')
    password = data.get('password')
    prisma = Prisma()
    await prisma.connect()

    
    print(email)
    if email is None or password is None:
        return jsonify({"error": "Email, user_id, and secret are required in the request."}), 400
    
    user = await prisma.user.find_first(where={"email": email})

    if user.password == password:
        return jsonify({"jwt_token": user.jwt_token})
    

@app.route('/api/checkforjwt', methods=["POST"])
async def checkforjwt():
    data = request.json
    jwt = data.get('jwtToken')

    print(jwt)

    if jwt is None:
        return jsonify({"message": "missing token"}), 400

    prisma = Prisma()
    await prisma.connect()

    user = await prisma.user.find_unique(where={"jwt_token": jwt})

    print(user)

    if user is None:
        return jsonify({"message": "jwt token not found"}), 400
    
    return jsonify({"success": "jwt token exists"}), 200



if __name__ == '__main__':
    app.run(debug=True)

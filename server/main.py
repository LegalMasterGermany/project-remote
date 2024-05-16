from flask import Flask, jsonify, request
from flask_jwt_extended import JWTManager, create_access_token, jwt_required
from prisma import Prisma
import uuid
from PIL import Image
from io import BytesIO
import os

app = Flask(__name__)
app.config['JWT_SECRET_KEY'] = 'super-secret'  
jwt = JWTManager(app)

def is_valid_uuid(uuid_str):
    try:
        uuid_obj = uuid.UUID(uuid_str)
        return True
    except ValueError:
        return False
    

ALLOWED_EXTENSIONS = {'png'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/api/createuser', methods=['POST'])
async def create_user():
    data = request.json
    email = data.get('email')
    password = data.get('password')
    uuid = data.get('uuid')

    if email is None or password is None or uuid is None:
        return jsonify({"message": "email, password or uuid is missing"}), 400
    
    if email == "" or password == "" or uuid == "":
        return jsonify({"message": "email, password or uuid cannot be empty"}), 400
    
    if not is_valid_uuid(uuid):
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
    user = await prisma.user.create(data=user_dict)

    SCREENSHOT_FOLDER = 'data'
    uuid_folder = os.path.join(SCREENSHOT_FOLDER, uuid)
    os.makedirs(uuid_folder, exist_ok=True)

    user_dict['id'] = user.id
    user_dict['status'] = 201

    return jsonify(user_dict), 201



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



@app.route('/api/screenshot', methods=['POST'])
def receive_screenshot():
    try:
        uuid = request.form.get('uuid')
        screenshot = request.files['screenshot']

        if not screenshot or not uuid:
            return jsonify({'error': 'Invalid request parameters'}), 400

        if not allowed_file(screenshot.filename):
            return jsonify({'error': 'Invalid file format. Only PNG files are allowed.'}), 415

        SCREENSHOT_FOLDER = 'data'
        os.makedirs(SCREENSHOT_FOLDER, exist_ok=True)
        uuid_folder = os.path.join(SCREENSHOT_FOLDER, uuid)
        os.makedirs(uuid_folder, exist_ok=True)
        
        screenshots_folder = os.path.join(uuid_folder, 'Screenshots')
        os.makedirs(screenshots_folder, exist_ok=True)
        
        image_path = os.path.join(screenshots_folder, 'screenshot.png')

        screenshot.save(image_path)

        return jsonify({'success': True}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

    




if __name__ == '__main__':
    app.run(debug=True)

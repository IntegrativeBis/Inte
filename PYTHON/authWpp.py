from flask import Flask, request, jsonify
from twilio.rest import Client
import random


# Configuración de Twilio
TWILIO_ACCOUNT_SID = 'TU_ACCOUNT_SID'
TWILIO_AUTH_TOKEN = 'TU_AUTH_TOKEN'
TWILIO_WHATSAPP_NUMBER = 'whatsapp:+14155238886'  # Número de Twilio para WhatsApp
client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)

# Almacenamiento temporal de códigos OTP
otp_storage = {}

# Ruta para enviar un código OTP por WhatsApp
@app.route('/send-otp', methods=['POST'])
def send_otp():
    data = request.json
    phone_number = data.get('phone_number')  # Debe incluir el código de país, por ejemplo: +521234567890
    
    if not phone_number:
        return jsonify({'error': 'Número de teléfono requerido'}), 400

    # Generar un OTP de 6 dígitos
    otp = random.randint(100000, 999999)
    otp_storage[phone_number] = otp  # Guardar el OTP en memoria (temporal)

    # Enviar el OTP por WhatsApp
    try:
        message = client.messages.create(
            body=f'Tu código de verificación es: {otp}',
            from_=TWILIO_WHATSAPP_NUMBER,
            to=f'whatsapp:{phone_number}'
        )
        return jsonify({'message': 'Código OTP enviado', 'sid': message.sid}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Ruta para verificar el OTP
@app.route('/verify-otp', methods=['POST'])
def verify_otp():
    data = request.json
    phone_number = data.get('phone_number')
    otp = data.get('otp')

    if not phone_number or not otp:
        return jsonify({'error': 'Número de teléfono y OTP requeridos'}), 400

    # Validar el OTP
    stored_otp = otp_storage.get(phone_number)
    if stored_otp and int(otp) == stored_otp:
        del otp_storage[phone_number]  # Eliminar OTP después de la validación
        return jsonify({'message': 'Verificación exitosa'}), 200
    else:
        return jsonify({'error': 'OTP inválido o expirado'}), 400


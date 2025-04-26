from flask import Flask,render_template,send_file,request
from io import BytesIO
import qrcode,base64
from urllib.parse import unquote

app = Flask(__name__)

def generate_qr_code(data):
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(data)
    qr.make(fit=True)
    return qr.make_image(fill_color="black", back_color="white")

def image_to_base64(img):
    img_io = BytesIO()
    img.save(img_io, format="PNG")
    return base64.b64encode(img_io.getvalue()).decode()

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/wifi',methods=['GET', 'POST'])
def wifi():
    if request.method == 'POST':
        ssid = request.form['ssid']
        password = request.form['password']
        security= request.form['security']
        hidden= request.form['hidden']
        data = f"WIFI:T:{security};S:{ssid};P:{password};H:{hidden};;"
        
       # Generate QR code
        qr = generate_qr_code(data)
        # Convert image to base64 for displaying
        img_str=image_to_base64(qr)
        return render_template('view.html',qr_image=img_str,data=data)
    return render_template('wifi.html')


@app.route('/web',methods=['GET','POST'])
def web():
    if request.method == 'POST':
        url = request.form['url']
        data = f'\nURL:{url}'
        #genaratebnQr code
        qr = generate_qr_code(data)
        img_str = image_to_base64(qr)
        return render_template('view.html',qr_image=img_str,data=data)   
    return render_template('web.html')

@app.route('/email',methods=['GET','POST'])
def email():
    if request.method =='POST':
        email = request.form.get('email', '') 
        data = f"\nEMAIL:{email}"
        #genaratebnQr code
        qr = generate_qr_code(data)
        img_str = image_to_base64(qr)
        return render_template('view.html',qr_image=img_str,data=data)
    return render_template('email.html')

@app.route('/phone',methods=['GET','POST'])
def phone():
    if request.method == 'POST':
        phone = request.form.get('phone_number','')
        data = f"\nPHONE:{phone}"
        qr = generate_qr_code(data)
        img_str = image_to_base64(qr)
        return render_template('view.html',qr_image=img_str,data=data)
    return render_template('phone.html')


@app.route('/card',methods=['GET','POST'])
def card():
    if request.method =='POST':
        name = request.form.get('name','')
        phone = request.form.get('phone','')
        email = request.form.get('email','')
        org = request.form.get('org','')
        address= request.form.get('address','')
        data = f"BEGIN:VCARD\nVERSION:3.0\nN:{name}\nTEL:{phone}\nEMAIL:{email}\nORG:{org}\nADR:{address}\nEND:VCARD"
        qr = generate_qr_code(data)
        img_str = image_to_base64(qr)
        return render_template('view.html',qr_image=img_str,data=data)
    return render_template('card.html')



@app.route('/download')
def download():
    raw_data = request.args.get('data', '')
    if not raw_data:
        return "No data provided", 400

    data = unquote(raw_data)
    qr = generate_qr_code(data)
    img_io = BytesIO()
    qr.save(img_io, format='PNG')
    img_io.seek(0)
    return send_file(img_io, mimetype='image/png', as_attachment=True, download_name="qr_code.png")


if __name__ == '__main__':
    app.run(debug=True)



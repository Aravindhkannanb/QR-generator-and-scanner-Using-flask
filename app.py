from flask import Flask,render_template,redirect,url_for,request
import qrcode
from PIL import Image
import cv2
app=Flask(__name__)
@app.route("/",methods=["POST","GET"])
def open():
    return render_template("home.html")
@app.route("/home",methods=["GET","POST"])
def home():
    if request.method=="POST":
        first=request.form.get("firstname")
        last=request.form.get("lastname")
        course=request.form.get("option")
        gender=request.form.get("gender")
        address=request.form.get("address")
        data="FirstName:{}\n LastName:{}\n Gender:{}\n Course:{} \n Address:{}".format(first,last,gender,course,address)
        qr=qrcode.QRCode(
            version=15,
            border=4,
            box_size=10
        )
        qr.add_data(data)
        qr.add_data("apple.png")
        qr.make(fit=True)
        img=qr.make_image(fill_color="black",back_color="white")
        img.save("{}.png".format(first))
        return redirect(url_for("home"))
    return render_template("index.html")
@app.route("/home/photo",methods=["POST","GET"])
def photo():
    if request.method=="POST":
        global cam
        cam=cv2.VideoCapture(0)
        while(True):
            ret,image=cam.read()
            cv2.imshow("image",image)
            if cv2.waitKey(1) & 0xFF ==ord('q'):
                break
            cv2.imwrite("apple.png",image)
        return redirect(url_for("home"))
    return redirect(url_for("home"))
@app.route("/scan",methods=["POST","GET"])
def scan():
    if request.method=="POST":
        cam=cv2.VideoCapture(0)
        code=[]
        while True:
            ret,image=cam.read()
            cv2.imshow("image",image)
            if cv2.waitKey(1) & 0xFF==ord('q'):
                break
            cv2.imwrite("QR.png",image)
        det=cv2.QRCodeDetector()
        val,pts,st_code=det.detectAndDecode(image)
        code.append(val)
        print(val)
        return render_template("scan.html",data=code)
if __name__=="__main__":
    app.run(debug=True,port=3000)
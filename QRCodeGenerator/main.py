import pyqrcode

# Data to be inserted in the QR code
data = " name: Roushan Agarwal \n Branch: ISE \n Institute: BMSIT \n Location: Bangalore"

# Creating the QR code
qr = pyqrcode.QRCode(data)

# Saving the QR code into a PNG file
qr.png('qrcode.png', scale=8)

# Saving the QR code into an SVG file 
qr.svg('qrcode.svg', scale=8)
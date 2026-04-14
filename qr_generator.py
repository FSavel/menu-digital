import qrcode

# 🔗 TROCA AQUI PELO TEU LINK DO RENDER
url = "https://TEU-SITE.onrender.com/"

qr = qrcode.make(url)

qr.save("qr_menu.png")

print("QR Code criado com sucesso!")
import os
from pysnmp.hlapi import *
import smtplib
from email.mime.text import MIMEText
from datetime import datetime

# Función para obtener el nivel de tinta usando SNMP
def get_ink_level(ip, oid):
    iterator = getCmd(
        SnmpEngine(),
        CommunityData('public', mpModel=0),
        UdpTransportTarget((ip, 161)),
        ContextData(),
        ObjectType(ObjectIdentity(oid))
    )

    errorIndication, errorStatus, errorIndex, varBinds = next(iterator)

    if errorIndication:
        print(errorIndication)
        return None
    elif errorStatus:
        print('%s at %s' % (errorStatus.prettyPrint(),
                            errorIndex and varBinds[int(errorIndex) - 1][0] or '?'))
        return None
    else:
        for varBind in varBinds:
            # Imprime el resultado SNMP
            return int(varBind[1])  # Convertimos el valor a número entero

# OIDs para los niveles de tinta (ajústalas según el modelo de impresora)
oids = {
    'black': '1.3.6.1.2.1.43.11.1.1.9.1.1',
    'cyan': '1.3.6.1.2.1.43.11.1.1.9.1.2',
    'magenta': '1.3.6.1.2.1.43.11.1.1.9.1.3',
    'yellow': '1.3.6.1.2.1.43.11.1.1.9.1.4'
}

# IP de la impresora
printer_ip = input("Introduce la IP de la impresora: ")

# Obtener niveles de tinta
ink_levels = {color: get_ink_level(printer_ip, oid) for color, oid in oids.items()}

# Mostrar niveles de tinta en consola
print("Niveles de tinta:")
for color, level in ink_levels.items():
    print(f"{color.capitalize()}: {level}%")

# Guardar resultados en un archivo
with open('niveles_tinta.txt', 'a') as f:
    f.write(f"\n{datetime.now()} - IP: {printer_ip}\n")
    for color, level in ink_levels.items():
        f.write(f"{color.capitalize()}: {level}%\n")

# Enviar correo con los resultados (opcional)
def send_email_report(ink_levels, printer_ip):
    sender = 'tu_correo@example.com'
    recipient = 'destinatario@example.com'
    subject = 'Reporte de Niveles de Tinta'
    body = f"Niveles de tinta de la impresora ({printer_ip}):\n" + \
           '\n'.join([f"{color.capitalize()}: {level}%" for color, level in ink_levels.items()])

    msg = MIMEText(body)
    msg['From'] = sender
    msg['To'] = recipient
    msg['Subject'] = subject

    try:
        with smtplib.SMTP('smtp.example.com', 587) as server:
            server.starttls()
            server.login(sender, 'tu_contraseña')
            server.sendmail(sender, recipient, msg.as_string())
            print("Correo enviado exitosamente.")
    except Exception as e:
        print(f"Error al enviar el correo: {e}")

# Enviar reporte por correo (descomenta para habilitar)
# send_email_report(ink_levels, printer_ip)

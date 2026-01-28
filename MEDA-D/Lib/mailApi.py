import os
import smtplib
from email.message import EmailMessage

def SendExercise(
    smtp_server: str,
    smtp_port: int,
    smtp_user: str,
    smtp_password: str,
    senderUser : str,
    patient_email: str,
    patient_name: str,
    a: str,  # Squat
    b: str,  # Kollar Yana
    c: str,  # Kollar Öne
    d: str   # Topuk Kaldırma
):

    program_name = "MEDA"
    plain = f"""Merhaba {patient_name},

{program_name} tarafından gönderilen egzersiz programınız:
 - Squat: {a}
 - Kollar Yana: {b}
 - Kollar Öne: {c}
 - Topuk Kaldırma: {d}

İyi çalışmalar,
{program_name} ekibi
"""

    html = f"""\
<!DOCTYPE html>
<html>
  <head>
    <meta charset="utf-8" />
  </head>
  <body style="font-family: Arial, Helvetica, sans-serif; color:#222; margin:0; padding:20px;">
    <div style="max-width:600px; margin:0 auto; border:1px solid #eee; border-radius:8px; padding:18px;">
      <h1 style="margin:0 0 8px 0; color:#0b63a5;">{program_name} - Medikal Egzersiz Dijital Arayüzü</h1>
      <p style="margin:0 0 16px 0;">Merhaba <strong>{patient_name}</strong>,</p>

      <p style="margin:0 0 12px 0;">Aşağıda bugün için önerilen egzersizleriniz bulunmaktadır. Lütfen hareketleri doğru formda yapmaya dikkat edin. Sorularınız olursa programdan iletiniz.</p>

      <table style="width:100%; border-collapse:collapse; margin-top:12px;">
        <thead>
          <tr>
            <th style="text-align:left; padding:8px; border-bottom:2px solid #e6eef6;">Egzersiz</th>
            <th style="text-align:left; padding:8px; border-bottom:2px solid #e6eef6;">Miktar</th>
          </tr>
        </thead>
        <tbody>
          <tr>
            <td style="padding:10px 8px; border-bottom:1px solid #f0f0f0;">Squat</td>
            <td style="padding:10px 8px; border-bottom:1px solid #f0f0f0;"><strong>{a}</strong></td>
          </tr>
          <tr>
            <td style="padding:10px 8px; border-bottom:1px solid #f0f0f0;">Kollar Yana</td>
            <td style="padding:10px 8px; border-bottom:1px solid #f0f0f0;"><strong>{b}</strong></td>
          </tr>
          <tr>
            <td style="padding:10px 8px; border-bottom:1px solid #f0f0f0;">Kollar Öne</td>
            <td style="padding:10px 8px; border-bottom:1px solid #f0f0f0;"><strong>{c}</strong></td>
          </tr>
          <tr>
            <td style="padding:10px 8px;">Topuk Kaldırma</td>
            <td style="padding:10px 8px;"><strong>{d}</strong></td>
          </tr>
        </tbody>
      </table>

      <p style="margin-top:18px; font-size:14px; color:#555;">
        Tavsiye: Her egzersiz seti arasında 30-60 saniye dinlenin. Ağrı hissettiğinizde durun ve bize bildirin.
      </p>
      <br>
      <p> Gönderen : {senderUser}</p>

      <div style="margin-top:18px;">
        <a style="display:inline-block; text-decoration:none; padding:10px 16px; border-radius:6px; border:1px solid #0b63a5;">
          Sorularınız için bize uygulamadan ulaşabilirsiniz, Direkt mail üzerinden gönderilen iletilerin cevaplanması çok uzun sürer.
        </a>
      </div>

      <p style="margin-top:18px; font-size:12px; color:#999;">Bu e-posta {program_name} tarafından gönderilmiştir.</p>
    </div>
  </body>
</html>
"""

    msg = EmailMessage()
    msg['From'] = smtp_user
    msg['To'] = patient_email
    msg['Subject'] = f"{program_name} - Dijital Egzersiz"
    msg.set_content(plain)
    msg.add_alternative(html, subtype='html')

    try:
        with smtplib.SMTP(smtp_server, smtp_port) as smtp:
            smtp.ehlo()
            if smtp_port == 587:
                smtp.starttls()
                smtp.ehlo()
            smtp.login(smtp_user, smtp_password)
            smtp.send_message(msg)
        print("E-posta gönderildi:", patient_email)
    except Exception as e:
        print("E-posta gönderme hatası:", e)
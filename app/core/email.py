import smtplib  # SMTP server se connect karne ke liye "ek module hai smtp protocol ke through email send karta hai"
from email.message import (  # email object banane ke liye email modeule ke andar sub module message uske andar ek class EmailMessage
    EmailMessage,
)


def send_blog_email(user_email: str, title: str, content: str):

    #  Ye sender ka Gmail hai (jisse mail jayega)
    EMAIL_ADDRESS = "abhay20043@gmail.com"

    EMAIL_PASSWORD = "roqqpkroewvoxzgt"

    msg = EmailMessage()  # ye class ka object banaya

    msg["Subject"] = "New Blog Created"

    msg["From"] = EMAIL_ADDRESS

    msg["To"] = "akashup3434@gmail.com"

    msg.set_content(
        f"""
        New Blog Added!

        User Email: {user_email}
        Blog Title: {title}
        Blog Content: {content}
        """
    )

    with smtplib.SMTP(
        "smtp.gmail.com", 587
    ) as server:  # server se connect tcp protocol se bhejte hai

        server.starttls()  # connection secure karta hai

        server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)  # gmail login karta hai

        server.send_message(msg)  # email bhej deta hai

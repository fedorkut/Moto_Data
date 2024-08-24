import os
import time
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
from fastapi import FastAPI, HTTPException, Query
from app.controller import Controller


app = FastAPI()

def send_email_with_csv(sender_email, sender_password, recipient_email, subject, body, csv_file_path):
    message = MIMEMultipart()
    message["From"] = sender_email
    message["To"] = recipient_email
    message["Subject"] = subject

    message.attach(MIMEText(body, "plain"))

    with open(csv_file_path, "rb") as attachment:
        part = MIMEBase('application', 'octet-stream')
        part.set_payload(attachment.read())
        encoders.encode_base64(part)
        part.add_header('Content-Disposition', f'attachment; filename={os.path.basename(csv_file_path)}')
        message.attach(part)

    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(sender_email, sender_password)
        server.sendmail(sender_email, recipient_email, message.as_string())
        server.quit()
        print("Email sent successfully!")
    except Exception as e:
        print(f"Failed to send email: {e}")

@app.post("/run-all-scripts")
async def run_all_scripts(
    recipient_email: str = Query(..., description="Recipient email address for the CSV"),
    make: str = Query(..., description="Make of the car for the dealership search"),
    postcode: str = Query(..., description="Postcode for the dealership search"),
    radius: int = Query(..., description="Radius for the dealership search")
):
    controller = Controller()
    try:
        controller.execute_all(make, postcode, radius)

        # After all scripts have run, send the email
        sender_email = "enquiries.ldncreative@gmail.com"
        sender_password = "swxh xnfh svpy hhox"  # Use an App Password if 2-Step Verification is enabled
        subject = "CSV File Attached"
        body = "Please find the attached CSV file."
        csv_file_path = "output/1000_checked.csv"  # Replace with the path to your CSV file

        send_email_with_csv(sender_email, sender_password, recipient_email, subject, body, csv_file_path)

    except Exception as e:
        print(f"Error during script execution or email sending: {e}")
        raise HTTPException(status_code=500, detail="Error during script execution or email sending")

    return {"status": "All scripts completed and email sent"}

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

# This block runs the app when executing 'python main.py'
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, log_level="info")

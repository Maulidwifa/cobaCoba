import subprocess
import json
import sendgrid
from sendgrid.helpers.mail import Mail, Email, To, Content

# Fungsi untuk menjalankan Newman dan menghasilkan laporan JSON
def run_newman():
    try:
        # Jalankan perintah Newman untuk melakukan test dan menghasilkan newman-report.json
        result = subprocess.run(
            [r'C:\Users\admin\AppData\Roaming\npm\newman.cmd', 'run', 'User_Management.postman_collection.json', '--environment', 'Dev.postman_environment.json', '--reporters', 'cli,json', '--reporter-json-export', 'newman-report.json'],
            check=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
        print("Newman test executed successfully")
        return 'newman-report.json'
    
    except subprocess.CalledProcessError as e:
        print(f"Error running Newman: {e}")
        return None

# Fungsi untuk membaca laporan JSON dan menentukan status serta nama tes
def determine_status_and_name(report_file):
    try:
        with open(report_file, 'r') as f:
            result = json.load(f)

        # Mengambil nama tes dan statusnya
        name = result['collection']['item'][0].get('name')
        passed = result['run']['stats']['assertions'].get('passed', 0)
        failed = result['run']['stats']['assertions'].get('failed', 0)

        # Menentukan status berdasarkan jumlah assertion yang gagal
        if failed > 0:
            status = 'Test Failed'
            result_detail = 'There are failed tests.'
        else:
            status = 'Success'
            result_detail = 'All tests passed successfully. (Manual)'

        return status, result_detail, name

    except Exception as e:
        print(f"Error reading report file: {e}")
        return None, None, None

# Fungsi untuk mengirim email menggunakan SendGrid
def send_email(status, result_detail, name):
    # API Key SendGrid
    SENDGRID_API_KEY = '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'
    SENDER_EMAIL = 'maulidwifairuz@gmail.com'
    RECIPIENT_EMAIL = 'maulidwifairuz@gmail.com'
    # Membuat objek sendgrid client
    sg = sendgrid.SendGridAPIClient(api_key=SENDGRID_API_KEY)

    # Membuat objek Mail
    from_email = Email(SENDER_EMAIL)
    to_email = To(RECIPIENT_EMAIL)
    subject = f"Postman Test Results for {name}"
    content = Content("text/plain", f"The Postman tests for : {name} have completed. \nStatus: {status}. \nDetails: {result_detail}")

    # Mengirimkan email
    mail = Mail(from_email, to_email, subject, content)

    # Mengirimkan email dan memeriksa statusnya
    response = sg.send(mail)
    print(f"Email sent! Status code: {response.status_code}")
    print(f"Response body: {response.body}")
    print(f"Response headers: {response.headers}")

# Main program
def main():
    # Jalankan Newman dan dapatkan path file laporan JSON
    report_file = run_newman()
    
    if not report_file:
        print("Error: Newman test execution failed. Email not sent.")
        return

    # Menentukan status, detail error, dan nama tes dari laporan
    status, result_detail, name = determine_status_and_name(report_file)

    if status and result_detail and name:
        print(f"Test status: {status}")
        print(f"Result details: {result_detail}")
        print(f"Test name: {name}")

        # Kirim email dengan hasil tes
        send_email(status, result_detail, name)
    else:
        print("Error: Could not determine the test status or test name.")

# Jalankan program utama
if __name__ == '__main__':
    main()


# import subprocess
# import json
# import sendgrid
# from sendgrid.helpers.mail import Mail, Email, To, Content

# # Fungsi untuk membaca hasil dari newman-report.json dan menentukan status
# def determine_status(report_file):
#     try:
#         # Membaca file JSON
#         with open(report_file, 'r') as f:
#             result = json.load(f)
        
#         # Mengecek apakah struktur yang kita cari ada
#         if 'run' in result and 'stats' in result['run'] and 'assertions' in result['run']['stats']:
#             passed = result['run']['stats']['assertions'].get('passed', 0)
#             failed = result['run']['stats']['assertions'].get('failed', 0)

#             # Menentukan status berdasarkan jumlah assertion yang gagal
#             if failed > 0:
#                 status = 'Test Failed'
#                 result_detail = 'There are failed tests.'
#             else:
#                 status = 'Success'
#                 result_detail = 'All tests passed successfully.'
            
#             return status, result_detail
#         else:
#             print("Error: Struktur JSON tidak sesuai. Pastikan file report mengandung bagian 'run.stats.assertions'.")
#             return None, None

#     except Exception as e:
#         print(f"Error reading report file: {e}")
#         return None, None

# # Fungsi untuk mengirim email menggunakan SendGrid
# def send_email(status, result_detail):
#     # API Key SendGrid
#     SENDGRID_API_KEY = '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'
#     SENDER_EMAIL = 'maulidwifairuz@gmail.com'
#     RECIPIENT_EMAIL = 'maulidwifairuz@gmail.com'

#     # Membuat objek sendgrid client
#     sg = sendgrid.SendGridAPIClient(api_key=SENDGRID_API_KEY)

#     # Membuat objek Mail
#     from_email = Email(SENDER_EMAIL)
#     to_email = To(RECIPIENT_EMAIL)
#     subject = "Postman Test Results"
#     content = Content(
#         "text/plain", f"The Postman tests have completed. Status: {status}. Details: {result_detail} (MANUAL)"
#         )

#     # Mengirimkan email
#     mail = Mail(from_email, to_email, subject, content)

#     # Mengirimkan email dan memeriksa statusnya
#     response = sg.send(mail)
#     print(f"Email sent! Status code: {response.status_code}")
#     print(f"Response body: {response.body}")
#     print(f"Response headers: {response.headers}")

# # Fungsi untuk menjalankan Newman dengan menggunakan subprocess
# def run_newman():
#     try:
#         # Menentukan path lengkap ke executable node dan newman
#         node_path = r'C:\Program Files\nodejs\node.exe'  # Pastikan path ini benar sesuai dengan instalasi Node.js
#         newman_path = r'C:\Users\admin\AppData\Roaming\npm\node_modules\newman\bin\newman.js'  # Path Newman yang benar

#         # Jalankan Newman (Collection Postman Silahkan Diganti)
#         result = subprocess.run(
#             [node_path, newman_path, 'run', 'Test.postman_collection.json', '--environment', 'Development.postman_environment.json', '--reporters', 'cli,json', '--reporter-json-export', 'newman-report.json'],
#             check=True,
#             stdout=subprocess.PIPE,
#             stderr=subprocess.PIPE
#         )

#         # Cetak output untuk debugging
#         print(result.stdout.decode())  # Output dari Newman
#         return 'newman-report.json'
    
#     except subprocess.CalledProcessError as e:
#         print(f"Error running Newman: {e.stderr.decode()}")
#         return None

# # Main program
# def main():
#     # Tentukan path ke file laporan Newman
#     report_file = run_newman()

#     if report_file:
#         print(f"Test report saved to: {report_file}")
        
#         # Menentukan status dan detail error
#         status, result_detail = determine_status(report_file)

#         if status and result_detail:
#             print(f"Test status: {status}")
#             print(f"Result Detail: {result_detail}")

#             # Kirim email dengan hasil tes
#             send_email(status, result_detail)
#         else:
#             print("Error: Could not determine the test status.")
#     else:
#         print("Newman test execution failed.")

# # Jalankan program utama
# if __name__ == '__main__':
#     main()

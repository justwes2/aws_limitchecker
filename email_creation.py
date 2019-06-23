# This is done using the smtplib library, but if availible, SES may be a better solution.
# SES is not availible in govCloud Environments
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

class EmailGenerator:
    limits = None
    table = ''
    utilization = ''

    def __init__(self, limits):
        self.limits = limits

    def create_html(self):
        # Put data from all accounts into a single list
        all_accounts = []
        for account in self.limits.itervalues():
            all_accounts += account.comparison
        # Sort list by utilization %
        all_accounts.sort(reverse=True, key=self.returnLast)
        table = '<table><tr><th>Account</th><th>Instance Type</th><th>Number in Use</th><th>Current Limit</th><th>Percent Capacity</th></tr>'
        for row in all_accounts:
            table += '<tr>'
            for cell in row:
                line = '' # To make sure no residual data is left from the previous line
                line += '<td>{}</td>'.format(cell)
                table += line
            table += '</tr>'
        table += '</table>'
        self.table = table
        self.utilization = all_accounts

    def send_email(self):
        s = smtplib.SMTP()
        s.connect(<EMAIL SERVER ADDRESS>, 25)

        # This is the origin address of the email, it cannont be replied to, but the domain can be anything
        noreply = 'no-reply@domain.com'
        # This is the recipient. If there is more than one, add them all to the same string separated by commas 
        recipient = 'admin@domain.com' 
        # You can add a cc
        cc = ''

        msg = MIMEMultipart('alternative')
        msg['Subject'] = 'EC2 Usage Report'
        msg['From'] = noreply
        msg['To'] = recipient
        msg['Cc'] = cc

        html = """\
            <html>
                <head></head>
                <h2>EC2 Usage Report</h2>
                <p>{}</p>
            </html>
            """.format(self.table)
        
        emailadd = MIMEText(html, 'html')
        msg.attach(emailadd)

        s.sendmail(noreply, [recipient, cc], msg.as_string())
        s.quit()
        print('Email Sent')

    def returnLast(self, elem):
        return int(elem[-1][:-1])
        
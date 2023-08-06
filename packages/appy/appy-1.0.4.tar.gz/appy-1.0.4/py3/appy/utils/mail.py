'''Functions for sending emails'''

#- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
# Copyright (C) 2007-2020 Gaetan Delannay

# This file is part of Appy.

# Appy is free software: you can redistribute it and/or modify it under the
# terms of the GNU General Public License as published by the Free Software
# Foundation, either version 3 of the License, or (at your option) any later
# version.

# Appy is distributed in the hope that it will be useful, but WITHOUT ANY
# WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR
# A PARTICULAR PURPOSE. See the GNU General Public License for more details.

# You should have received a copy of the GNU General Public License along with
# Appy. If not, see <http://www.gnu.org/licenses/>.

#- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
import smtplib, socket, time
from email import encoders
from email.header import Header
from email.utils import formatdate
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

from appy.utils import sequenceTypes

#- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
NO_CONFIG = 'must send mail but no SMTP server configured.'
NO_SERVER = 'no mailhost defined'
DISABLED = 'mail disabled%s: should send mail from %s to %d recipient(s): %s.'
MSG_REPLY_TO = 'reply to: %s'
MSG_SUBJECT = 'subject: %s'
MSG_BODY = 'body: %s'
MSG_ATTACHMENTS = '%d attachment(s).'
MSG_SENDING = 'sending mail from %s to %s (subject: %s).'
MAIL_RECIPIENTS_KO = 'could not send mail to some recipients. %s'
MAIL_SENT = 'mail sent in %.2f secs.'
MAIL_NOT_SENT = '%s: mail sending failed (%s)'

#- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
class Config:
    '''Parameters for connecting to a SMTP server'''

    # Currently we don't check the connection to the SMTP server at startup
    testable = False

    def __init__(self, fromName=None, fromEmail='info@appyframework.org',
                 replyTo=None, server='localhost', port=25, secure=False,
                 login=None, password=None, enabled=True):
        # The name that will appear in the "from" part of the messages
        self.fromName = fromName
        # The mail address that will appear in the "from" part of the messages
        self.fromEmail = fromEmail
        # The optional "reply-to" mail address
        self.replyTo = replyTo
        # The SMTP server address and port
        if ':' in server:
            self.server, port = server.split(':')
            self.port = int(port)
        else:
            self.server = server
            self.port = int(port) # That way, people can specify an int or str
        # Secure connection to the SMTP server ?
        self.secure = secure
        # Optional credentials to the SMTP server
        self.login = login
        self.password = password
        # Is this server connection enabled ?
        self.enabled = enabled

    def init(self, tool): pass

    def getFrom(self):
        '''Gets the "from" part of the messages to send.'''
        if self.fromName: return '%s <%s>' % (self.fromName, self.fromEmail)
        return self.fromEmail

    def __repr__(self):
        '''Short string representation of this mail config, for logging and
           debugging purposes.'''
        r = 'mail: %s:%d' % (self.server, self.port)
        if self.login: r += ' (login as %s)' % self.login
        return r

#- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
def sendMail(config, to, subject, body, attachments=None, log=None,
             replyTo=None):
    '''Sends a mail, via the SMTP server defined in the p_config'''
    # p_config is an instance of class appy.utils.mail.Config above.
    # This function sends a mail to p_to (a single email recipient or a list of
    # recipients). Every (string) recipient can be an email address or a string
    # of the form "[name] <[email]>".

    # p_attachments must be a list or tuple whose elements can have 2 forms:
    # 1. a tuple (fileName, fileContent): "fileName" is the name of the file
    #    as a string; "fileContent" is the file content, also as a string;
    # 2. an instance of class appy.model.fields.file.FileInfo.

    # p_log can be a function accepting 2 args:
    # - the message to log (as a string);
    # - the second must be named "type" and will receive string
    #   "info", "warning" or "error".

    # A p_replyTo mail address or recipient can be specified.
    start = time.time()
    to = [to] if isinstance(to, str) else to
    if not config:
        if log: log(NO_CONFIG)
        return
    # Just log things if mail is disabled
    fromAddress = config.getFrom()
    replyTo = replyTo or config.replyTo
    if not config.enabled or not config.server:
        msg = '' if config.server else ' (%s)' % NO_SERVER
        if log:
            toLog = DISABLED % (msg, fromAddress, len(to), ', '.join(to))
            if replyTo: toLog += ' (%s).' % (REPLY_TO % replyTo)
            log(toLog)
            log(MSG_SUBJECT % subject)
            log(MSG_BODY % body)
        if attachments and log: log(MSG_ATTACHMENTS % len(attachments))
        return
    if log: log(MSG_SENDING % (fromAddress, str(to), subject))
    # Create the base MIME message
    body = MIMEText(body, 'plain')
    if attachments:
        msg = MIMEMultipart()
        msg.attach(body)
    else:
        msg = body
    # Add the header values
    msg['Subject'] = Header(subject)
    msg['From'] = fromAddress
    msg['Date'] = formatdate(localtime=True)
    if replyTo: msg.add_header('reply-to', replyTo)
    if len(to) == 1:
        msg['To'] = to[0]
    else:
        msg['To'] = fromAddress
        msg['Bcc'] = ', '.join(to)
    # Add attachments
    if attachments:
        for attachment in attachments:
            # 2 possible forms for an attachment
            if isinstance(attachment, tuple) or isinstance(attachment, list):
                fileName, fileContent = attachment
            else:
                # a FileInfo instance
                fileName = attachment.uploadName
                f = file(attachment.fsPath, 'rb')
                fileContent = f.read()
                f.close()
            part = MIMEBase('application', 'octet-stream')
            part.set_payload(fileContent)
            encoders.encode_base64(part)
            part.add_header('Content-Disposition',
                            'attachment; filename="%s"' % fileName)
            msg.attach(part)
    # Send the email
    try:
        smtpServer = smtplib.SMTP(config.server, port=config.port)
        if config.secure:
            smtpServer.ehlo()
            smtpServer.starttls()
        if config.login:
            smtpServer.login(config.login, config.password)
        r = smtpServer.sendmail(fromAddress, to, msg.as_string())
        smtpServer.quit()
        if log:
            if r:
                log(MAIL_RECIPIENTS_KO % str(r), type='warning')
            else:
                log(MAIL_SENT % (time.time() - start))
    except smtplib.SMTPException as e:
        if log:
            log(MAIL_NOT_SENT % (config, str(e)), type='error')
    except socket.error as se:
        if log:
            log(MAIL_NOT_SENT % (config, str(se)), type='error')
#- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

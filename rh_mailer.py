from openerp import addons
from openerp.osv import fields, osv
from openerp.tools.translate import _
from openerp import tools as tools
from openerp.tools import html2text

from email.MIMEText import MIMEText
from email.MIMEBase import MIMEBase
from email.MIMEMultipart import MIMEMultipart
from email.Charset import Charset
from email.Header import Header
from email.Utils import formatdate, make_msgid, COMMASPACE
from email import Encoders
import logging
import re
import smtplib

COMMASPACE = ';'

class rh_mailer_smtpserver(osv.osv):
	_name = 'rh.mailer.smtpserver'
	
	_columns = {
		'name': fields.char('Description'),
		'employee_id':fields.many2one('rh.employee','Employee'),
		'host': fields.char('SMTP Server'),
		'port': fields.integer('Port'),
		'encryption':fields.selection([
			('none', 'None'),
            ('tls', 'TLS(STARTTLS)'),
            ('ssl', 'SSL/TLS')],
            'Connection encryption'),
		'username': fields.char('Username'),
		'password': fields.char('Password'),
		}
	def test_smtp_connection(self, cr, uid, ids, context=None):
		for smtp_server in self.browse(cr, uid, ids, context=context):
			smtp = False
			try:
				smtp = self.connect(smtp_server.host, smtp_server.port, user=smtp_server.username,
									password=smtp_server.password, encryption=smtp_server.encryption)
			except Exception, e:
				raise osv.except_osv(_("Connection Test Failed!"), _("Error:\n %s") % tools.ustr(e))
			finally:
				try:
					if smtp: smtp.quit()
				except Exception:
					# ignored, just a consequence of the previous exception
					pass
		raise osv.except_osv(_("Connection Test Succeeded!"), _("Everything seems properly set up!"))
	
	def test_smtp_email(self,cr,uid,ids,context=None):
		for req in self.browse(cr,uid,ids,context):
			server_from=req.username
			server_to='ab.salhi@gmail.com'
			server_subject=u'Test of Connection with OpenERP'
			server_body='<html><body><h1>Test of connection with OpenERP succeeded!</h1><p>The connection with your OpenERP server is Succeeded, this e-mail server will be used as sender for all emails sended with this sesssion.</p><p>Tanks for using ouer service!</p></body><html>'
						
		msg=self.build_email(server_from, server_to, server_subject,server_body)
		self.send_email(cr, uid, msg, [1])
		raise osv.except_osv(_("Connection Test Succeeded!"), _("Everything seems properly set up!"))
		return False
	
	def connect(self, host, port, user=None, password=None, encryption=False):
		if encryption == 'ssl':
			if not 'SMTP_SSL' in smtplib.__all__:
				raise osv.except_osv(
							 _("SMTP-over-SSL mode unavailable"),
							 _("Your OpenERP Server does not support SMTP-over-SSL. You could use STARTTLS instead."
							   "If SSL is needed, an upgrade to Python 2.6 on the server-side should do the trick."))
			connection = smtplib.SMTP_SSL(host, port)
		else:
			connection = smtplib.SMTP(host, port)
			
		if encryption == 'tls':
			connection.starttls()
			a=connection.ehlo()
		if user:
			user = tools.ustr(user).encode('utf-8')
			password = tools.ustr(password).encode('utf-8') 
			connection.login(user, password)
		return connection
	
	
	def build_email(self, email_from, email_to, subject, body):
		assert email_from, "You must either provide a sender address explicitly "
		assert email_to, "You must either provide a precipitant address  "
		msg = MIMEMultipart()
		msg['Subject'] = subject
		msg['From'] =email_from
		msg['To'] = email_to
		msg['Date'] = formatdate(localtime=True)
		msg.attach( MIMEText(body, 'html'))
		return msg
		
	def send_email(self, cr, uid, message, mail_server_id):
		for mail_server in self.browse(cr, uid, mail_server_id):
			smtp_server = mail_server.host
			smtp_user = mail_server.username
			smtp_password = mail_server.password
			smtp_port = mail_server.port
			smtp_encryption = mail_server.encryption
			smtp_from = mail_server.username
		smtp_to_list=message['To']
		assert(mail_server),"SMTP Server not defined!"
		       
		if not smtp_server:
			raise osv.except_osv(
						 _("Missing SMTP Server"),
						 _("Please define at least one SMTP server, or provide the SMTP parameters explicitly."))

		try:
			smtp = self.connect(smtp_server, smtp_port, smtp_user, smtp_password, smtp_encryption or False)
			smtp.sendmail(smtp_from, smtp_to_list, message.as_string())
		except Exception, e:
			msg = _("Mail delivery failed via SMTP server '%s'.\n%s: %s") % (tools.ustr(smtp_server),
																			 e.__class__.__name__,
																			 tools.ustr(e))
			raise osv.except_osv(_('Mail delivery failed:'), msg)																	 
		finally:
			try:
				# Close Connection of SMTP Server
				smtp.quit()
			except Exception:
					# ignored, just a consequence of the previous exception
				pass
		return False

        
rh_mailer_smtpserver()

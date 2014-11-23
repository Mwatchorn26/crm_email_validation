# -*- coding: utf-8 -*-
##############################################################################
#
#    Transformix Engineering Inc.
#    Copyright (C) 2004-today Transformix Engineering (<http://www.transformix.com>)
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################

from openerp import fields, models, api, _
from openerp.exceptions import Warning
import urllib
import urllib2
   

class email_validation(models.Model):
    """Validates lead's email address
    
    This module adds to the CRM module to validate a lead's email address."""
    _inherit = "crm.lead"
    #Add the new columns to the database table. (These are specifically for 
    #lead, but  Opportunities and Leads share the same table.)
    email_status = fields.Selection([
            ('unknown', 'Unknown'),
            ('valid', 'Valid'),
            ('accepted', 'Server Accepted'),
            ('bad_mailbox', 'Bad Mailbox')
            ], default='unknown', track_visibility='onchange')   
     
    email_status_msg=fields.Text(string="Email Validation Message", track_visibility='onchange')

    #Referenced the Python Docs How-To page 
    #https://docs.python.org/2/howto/urllib2.html
    def validate_email_address(self):
        # The API key provided for your account goes here
        PersonalAPIKey = "<!-- your key goes here -->"
        
        # Read in the email address
        emailAddress = self.email_from #input("Enter Email:\n")
        
        #The URL of the JSON web service we'll be using to do the validation. 
        #You'll need to purchase a subscription in order to use this service.
        #You can try it out by getting a free evaluation API for 100 validations.
        url = 'http://api.email-validator.net/api/verify'
        values = {'EmailAddress' : emailAddress,
                  'APIKey' : PersonalAPIKey}
        
        data = urllib.urlencode(values)
        req = urllib2.Request(url, data)
        response = urllib2.urlopen(req)
        return_code = response.read()
        print(the_page)
        self.status_code(return_code)
    
        
        
    def status_code(self):
        general_status="unknown"
        
        #PROBLEM
        if code=='114':
            #Validation Delayed    yes     
            email_status_msg = "SMTP address validation is still in progress (API only)."
        if code=='118':
            #Rate Limit Exceeded    yes     
            email_status_msg = "The API rate limit for your account has been exceeded (API only)."
        if code=='119':
            #API Key Invalid or Depleted    no     
            email_status_msg = "The API key is invalid, or the account balance is depleted (API only)."
        if code=='121':
            #Task Accepted    no     
            email_status_msg = "The validation task was accepted."
        if code=='302':
            #Local Address    no     
            email_status_msg="The mail address lacks the domain qualifier. It may work locally within some organization, but otherwise it is unusable."
        if code=='303':    
            #IP Address Literal    no          
            email_status_msg="The mail address is syntactically correct, but the domain part defines an IP address. This kind of address may work, but is usually only used by spammers, or for testing purposes."
        if code=='305':    
            #Disposable Address    no          
            email_status_msg="The mail address is provided by a disposable email address service. Disposable addresses only work for a limited amount of time, or for a limited amount of messages."
        if code=='308':    
            #Role Address    no          
            email_status_msg="The mail address is a role address and typically not associated with a particular person."
        if code=='313':    
            #Server Unavailable    yes          
            email_status_msg="The mail server for this domain could not be contacted, or did not respond."
        if code=='314':    
            #Address Unavailable    yes          
            email_status_msg="The mail server for this domain responded with an error condition for this address."
        if code=='316':    
            #Duplicate Address    no          
            email_status_msg="The address is a duplicate of an address that has already been processed (batch processing only)."
        if code=='401':    
            #Bad Address    no               
            email_status_msg="The mail address failed to pass basic syntax checks."
        if code=='404':    
            #Domain Not Fully Qualified    no               
            email_status_msg="The mail address is syntactically correct, but the domain part of the mail address is not fully qualified, and the address is not usable."
        if code=='406':    
            #MX Lookup Error    no               
            email_status_msg="There is no valid DNS MX record associated with this domain, or one or more MX entries lack an A record. Messages to this domain cannot be delivered."
        if code=='409':    
            #No-Reply Address    no               
            email_status_msg="The mail address appears to be a no-reply address, and is not usable as a recipient of email messages."
        if code=='413':    
            #Server Unavailable    no               
            email_status_msg="The mail server for this domain could not be contacted, or did not accept mail over an extended period of time."
        if code=='414':    
            #Address Unavailable    no               
            email_status_msg="The mail server for this domain responded with an error condition for this address over an extended period of time."
        if code=='420':    
            #Domain Name Misspelled    no               
            email_status_msg="The domain name is probably misspelled."
    #BAD ADDRESS
        if code=='410':    
            #Address Rejected    no     
            email_status_msg="The mail server for the recipient domain does not accept messages to this address."
            general_status="bad_mailbox"
        if code=='317':
            #Server Reject    no          
            email_status_msg="The server refuses to answer to SMTP commands, probably because some very strict anti-spam measures are in effect."
            general_status="bad_mailbox"
    #VALID                
        if code=='200':
            #OK - Valid Address    no          
            email_status_msg="The mail address is valid."
            general_status="valid"        
    #ACCEPTED
        if code=='207':
            #OK - Catch-All Active    no          
            email_status_msg="The mail server for this domain accepts the address, but it also implements a catch-all policy. For this reason, it is not possible to determine if a mail account with this name actually exists, without sending a message and waiting for a reply."
            general_status="accepted"
        if code=='215':
            #OK - Catch-All Test Delayed    yes     
            email_status_msg="The mail server for this domain accepts the address, the Catch-All test returned a temporary error (API only)."
            general_status="accepted"
            
        if general_status=="unknown":
            raise Warning(_(email_status_msg))

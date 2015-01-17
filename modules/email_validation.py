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
import ast
   

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
            ], required=False, string="Email Status" , default='unknown', track_visibility='onchange')   
     
    email_status_msg=fields.Text(string="Email Validation Message", track_visibility='onchange')

    #Referenced the Python Docs How-To page 
    #https://docs.python.org/2/howto/urllib2.html
    @api.one
    def validate_email_address(self):
        # The API key provided for your account goes here
        PersonalAPIKey = "ENTER YOUR API KEY HERE"
        
        # Read in the email address
        emailAddress = self.email_from #input("Enter Email:\n")
        
        #The URL of the JSON web service we'll be using to do the validation. 
        #You'll need to purchase a subscription in order to use this service.
        #You can try it out by getting a free evaluation API for 100 validations.
        #url = 'http://api.email-validator.net/api/verify'
        print "."
        print ".."
        print "..."
        sale_config = self.env['sale.config.settings']
        #print self.env['sale.config.settings'].email_validation_url
        url = self.env['sale.config.settings'].email_validation_url
        values = {'EmailAddress' : emailAddress,
                  'APIKey' : PersonalAPIKey}
        print values
        data = urllib.urlencode(values)             # Convert the data to the format we use in a URL GET call.
        req = urllib2.Request(url, data)            # Setup the request for the server with the URL address and the data we want an answer for.
        response = urllib2.urlopen(req)             # Make the request to the actual Email Validation server
        return_str = response.read()                # Extract the part of the response that we want.
        print return_str
        return_dict = ast.literal_eval(return_str)  # Convert the returned string to a dictionary
        
        #print(return_code)
        #print "1"
        #print "2"
        #print "3"
        #type(return_code).__name__
        #type(return_code_dict).__name__
        #print(return_code['status'])
        self.status_code(return_dict['status'])
        #self.status_code(response.code)
                
        
    def status_code(self, code):
        general_status="unknown"
        
        #PROBLEM
        if code==114:
            #Validation Delayed    yes     
            self.email_status_msg = "SMTP address validation is still in progress (API only)."
        if code==118:
            #Rate Limit Exceeded    yes     
            self.email_status_msg = "The API rate limit for your account has been exceeded (API only)."
        if code==119:
            #API Key Invalid or Depleted    no     
            self.email_status_msg = "The API key is invalid, or the account balance is depleted (API only)."
        if code==121:
            #Task Accepted    no     
            self.email_status_msg = "The validation task was accepted."
        if code==302:
            #Local Address    no     
            self.email_status_msg="The mail address lacks the domain qualifier. It may work locally within some organization, but otherwise it is unusable."
        if code==303:    
            #IP Address Literal    no          
            self.email_status_msg="The mail address is syntactically correct, but the domain part defines an IP address. This kind of address may work, but is usually only used by spammers, or for testing purposes."
        if code==305:    
            #Disposable Address    no          
            email_status_msg="The mail address is provided by a disposable email address service. Disposable addresses only work for a limited amount of time, or for a limited amount of messages."
        if code==308:    
            #Role Address    no          
            self.email_status_msg="The mail address is a role address and typically not associated with a particular person."
        if code==313:    
            #Server Unavailable    yes          
            self.email_status_msg="The mail server for this domain could not be contacted, or did not respond."
        if code==314:    
            #Address Unavailable    yes          
            self.email_status_msg="The mail server for this domain responded with an error condition for this address."
        if code==316:    
            #Duplicate Address    no          
            self.email_status_msg="The address is a duplicate of an address that has already been processed (batch processing only)."
        if code==401:    
            #Bad Address    no               
            self.email_status_msg="The mail address failed to pass basic syntax checks."
        if code==404:    
            #Domain Not Fully Qualified    no               
            self.email_status_msg="The mail address is syntactically correct, but the domain part of the mail address is not fully qualified, and the address is not usable."
        if code==406:    
            #MX Lookup Error    no               
            self.email_status_msg="There is no valid DNS MX record associated with this domain, or one or more MX entries lack an A record. Messages to this domain cannot be delivered."
        if code==409:    
            #No-Reply Address    no               
            self.email_status_msg="The mail address appears to be a no-reply address, and is not usable as a recipient of email messages."
        if code==413:    
            #Server Unavailable    no               
            self.email_status_msg="The mail server for this domain could not be contacted, or did not accept mail over an extended period of time."
        if code==414:    
            #Address Unavailable    no               
            self.email_status_msg="The mail server for this domain responded with an error condition for this address over an extended period of time."
        if code==420:    
            #Domain Name Misspelled    no               
            self.email_status_msg="The domain name is probably misspelled."
    #BAD ADDRESS
        if code==410:    
            #Address Rejected    no     
            self.email_status_msg="The mail server for the recipient domain does not accept messages to this address."
            general_status="bad_mailbox"
        if code==317:
            #Server Reject    no          
            self.email_status_msg="The server refuses to answer to SMTP commands, probably because some very strict anti-spam measures are in effect."
            general_status="bad_mailbox"
    #VALID                
        if code==200:
            #OK - Valid Address    no          
            self.email_status_msg="The mail address is valid."
            general_status="valid"        
    #ACCEPTED
        if code==207:
            #OK - Catch-All Active    no          
            self.email_status_msg="The mail server for this domain accepts the address, but it also implements a catch-all policy. For this reason, it is not possible to determine if a mail account with this name actually exists, without sending a message and waiting for a reply."
            general_status="accepted"
        if code==215:
            #OK - Catch-All Test Delayed    yes     
            self.email_status_msg="The mail server for this domain accepts the address, the Catch-All test returned a temporary error (API only)."
            general_status="accepted"
        
        #Permanently store the result
        self.email_status = general_status
        
        #Raise a warning alert if after the test it is still unknown.
        if general_status=="unknown":
            raise Warning(_(self.email_status_msg))
        

class validation_config_settings(models.TransientModel):
    
    _inherit = 'sale.config.settings'
    
    email_validation_url = fields.Char(string='email_validation', default="http://api.email-validator.net/api/verify", help="This is the URL of the site providing the email validation")
    api_key= fields.Char(string='api_key', help="This API Key is provided by the supplier of the service once you have purchased some credits. Visit www.email-validator.net to purchase credits.")

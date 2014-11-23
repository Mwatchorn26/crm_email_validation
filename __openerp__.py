# -*- coding: utf-8 -*-
{
    "name" : "CRM - Email Validation",
    "summary":"""
        Validate email addresses using the API from email-validator.net
    """,
    "description" : """
    This module allows the salesman the ability to validate the email and returns one of 3 possible results:
    
    
    * Red Dot indicates there was a problem validating the email address
    
    * Yellow Dot indicates the server accepts all email sent to that domain, whether or not the mailbox exists.
    
    * Green Dot indicates the mailbox exists, and the email address has been validated.
    """,
    "author" : "Transformix Engineering Inc.", 
    "website" : "http://www.Transformix.com",
    "depends" : ['base','crm'],
    "category" : "Customer Relationship Management",
    "version" : "0.1",
    "sequence": 16,
    #"init" : [],
    "demo" : [],
    "data" : ["crm_email_validation_view.xml",], 
    #"data" : [],    
    'test': [],
    #'installable': True,   
    #'complexity': "easy",
    #'active': False,
}
# -*- coding: utf-8 -*-
# this file is released under public domain and you can use without limitations

#########################################################################
## This is a sample controller
## - index is the default action of any application
## - user is required for authentication and authorization
## - download is for downloading files uploaded in the db (does streaming)
## - call exposes all registered services (none by default)
#########################################################################

def show(): 
   """
   test SQL query and display
   """
   query1 = ((db.QUOTE._id==db.QUOTE_WORK.QuoteID) & 
   	(db.QUOTE_WORK.WorkID==db.WORK._id) & 
   	(db.WORK._id==db.WORK_TR.WorkID) & 
   	(db.QUOTE.QuoteLanguageID==db.WORK_TR.LanguageID) & 
   	(db.QUOTE.QuoteLanguageID==db.LANGUAGE._id))
   query2 = db((db.WORK_TR.LanguageID==1) & 
   	(db.AUTHOR_TR.LanguageID==1) & 
   	(db.QUOTE._id==db.QUOTE_WORK.QuoteID) & 
   	(db.QUOTE_WORK.WorkID==db.WORK._id) & 
   	(db.WORK._id==db.WORK_TR.WorkID) & 
   	(db.WORK._id==db.WORK_AUTHOR.WorkID) & 
   	(db.WORK_AUTHOR.AuthorID==db.AUTHOR_TR.AuthorID) & 
   	(db.QUOTE.Text.like('%every%'))).select(db.QUOTE.Text, db.AUTHOR_TR.DisplayName, db.WORK_TR.WorkName, db.WORK_TR.id, groupby=db.QUOTE.Text)
   
   return dict(results1=SQLFORM.grid(query1, 
    	fields=[db.QUOTE.Text, db.LANGUAGE.EnglishName, db.WORK_TR.WorkName], 
    	headers={'QUOTE.Text': 'Text', 
    			'LANGUAGE.EnglishName': 'Language', 
    			'WORK_TR.WorkName': 'Source'},
    	maxtextlength=80),
    	header1='Example query (all quotes)',
    	results2=query2,
    	header2='Example query (text search, \"every\")')




def index():
    """
    ***for testing purposes only***
    
    function to list data on the main page
   
    """
    return dict(quotes=SQLFORM.grid(db.QUOTE), authors=SQLFORM.grid(db.AUTHOR),
    	authors_tr=SQLFORM.grid(db.AUTHOR_TR), works=SQLFORM.grid(db.WORK),
    	works_tr=SQLFORM.grid(db.WORK_TR), users=SQLFORM.grid(db.USER), 
    	languages=SQLFORM.grid(db.LANGUAGE), translations=SQLFORM.grid(db.TRANSLATION))



def user():
    """
    exposes:
    http://..../[app]/default/user/login
    http://..../[app]/default/user/logout
    http://..../[app]/default/user/register
    http://..../[app]/default/user/profile
    http://..../[app]/default/user/retrieve_password
    http://..../[app]/default/user/change_password
    http://..../[app]/default/user/manage_users (requires membership in
    use @auth.requires_login()
        @auth.requires_membership('group name')
        @auth.requires_permission('read','table name',record_id)
    to decorate functions that need access control
    """
    return dict(form=auth())

@cache.action()
def download():
    """
    allows downloading of uploaded files
    http://..../[app]/default/download/[filename]
    """
    return response.download(request, db)


def call():
    """
    exposes services. for example:
    http://..../[app]/default/call/jsonrpc
    decorate with @services.jsonrpc the functions to expose
    supports xml, json, xmlrpc, jsonrpc, amfrpc, rss, csv
    """
    return service()


#@auth.requires_signature()
def data():
    """
    http://..../[app]/default/data/tables
    http://..../[app]/default/data/create/[table]
    http://..../[app]/default/data/read/[table]/[id]
    http://..../[app]/default/data/update/[table]/[id]
    http://..../[app]/default/data/delete/[table]/[id]
    http://..../[app]/default/data/select/[table]
    http://..../[app]/default/data/search/[table]
    but URLs must be signed, i.e. linked with
      A('table',_href=URL('data/tables',user_signature=True))
    or with the signed load operator
      LOAD('default','data.load',args='tables',ajax=True,user_signature=True)
    """
    return dict(form=crud())

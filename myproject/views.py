from pyramid.view import view_config


@view_config(route_name='home', renderer='templates/mytemplate.pt')
def home_view(request):
	#get size, and section from route
	#request reddit JSON
	#parse JSON for pictures with .jpg that are large enough
	#send list of JSON objects which match the requirements to template for display
	
    print request

    return {'project': 'MyProject'}


@view_config(route_name='query', renderer='templates/mytemplate.pt')
def query_view(request):
    
    print request.matchdict['subreddit']
    print request.matchdict['minsize']

    return {'project': 'MyProject'}
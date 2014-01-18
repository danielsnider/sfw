from pyramid.view import view_config


@view_config(route_name='home', renderer='templates/mytemplate.pt')
def my_view(request):
	#get size, and section from route
	#request reddit JSON
	#parse JSON for pictures with .jpg that are large enough
	#send list of JSON objects which match the requirements to template for display
    return {'project': 'MyProject'}

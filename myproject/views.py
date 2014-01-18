import urllib2
from pyramid.view import view_config


@view_config(route_name='home', renderer='templates/mytemplate.pt')
def home_view(request):
    # nothing to see here...
    return query_view(request) # reuse query_view route

@view_config(route_name='query', renderer='templates/mytemplate.pt')
def query_view(request):
    if 'subreddits' not in request.matchdict or 'minsize' not in request.matchdict:
        subreddits = "earthporn+waterporn+skyporn+spaceporn+fireporn+destructionporn+geologyporn+winterporn+autumnporn+cityporn+villageporn+abandonedporn+infrastructureporn+machineporn+militaryporn+cemeteryporn+architectureporn+carporn+gunporn+boatporn+aerialporn+F1porn+ruralporn+animalporn+botanicalporn+humanporn+adrenalineporn+climbingporn+culinaryporn+foodporn+dessertporn+agricultureporn+designporn+albumartporn+movieposterporn+adporn+geekporn+instrumentporn+macroporn+artporn+fractalporn+exposureporn+microporn+metalporn+streetartporn+historyporn+mapporn+bookporn+newsporn+quotesporn+futureporn"
        minsize = 1000
    else:
        subreddits = request.matchdict['subreddits']
        minsize = request.matchdict['minsize']
    
    print subreddits
    print minsize

    reddit_url = "http://www.reddit.com/r/" + subreddits + "/hot.json"

    json = get_url(reddit_url)

    if json == None: 
        print "No JSON found so send a default image!"

    print json

    return {'project': 'MyProject', 'subreddits': subreddits, 'minsize': minsize}


def get_url(url):
    try:
        response = urllib2.urlopen(url)
        html = response.read()
        print html
    except URLError as e:
        print e.reason
        return None
    return html

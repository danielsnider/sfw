import urllib2
import json
import re
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
        minsize = int(request.matchdict['minsize'])
    
    print subreddits
    print minsize

    reddit_url = "http://www.reddit.com/r/" + subreddits + "/hot.json"
    images = find_images(reddit_url, minsize)

    print images
    print "YAY"

    return {'project': 'MyProject', 'subreddits': subreddits, 'minsize': minsize}


def find_images(reddit_url, minsize):
    images = []

    json_str = get_url(reddit_url)
    if json_str == None: 
        print "Error: get_url failed \n Falling back to default image"
        images = [{'domain': 'ppcdn.500px.org', 'banned_by': None, 'media_embed': {}, 'subreddit': 'VillagePorn', 'selftext_html': None, 'selftext': '', 'likes': None, 'secure_media': None, 'link_flair_text': None, 'id': '1vg203', 'secure_media_embed': {}, 'clicked': False, 'stickied': False, 'author': 'soupyhands', 'media': None, 'width': 1920, 'score': 358, 'approved_by': None, 'over_18': False, 'hidden': False, 'thumbnail': 'http://a.thumbs.redditmedia.com/7rkYTCpFYUZKiMXr.jpg', 'subreddit_id': 't5_2sm1u', 'edited': False, 'link_flair_css_class': None, 'author_flair_css_class': 'Cottage', 'downs': 20, 'saved': False, 'is_self': False, 'height': 1280, 'permalink': '/r/VillagePorn/comments/1vg203/sunset_in_the_windows_of_the_old_bergen_museum/', 'name': 't3_1vg203', 'created': 1389995666.0, 'url': 'http://ppcdn.500px.org/57985348/fedb8cc44992e05f23dbf885a013dfbca4998e11/2048.jpg', 'author_flair_text': None, 'title': 'Sunset in the windows of the old Bergen Museum, Norway [1920x1280] photo by Tore H.', 'created_utc': 1389966866.0, 'ups': 378, 'num_comments': 8, 'visited': False, 'num_reports': None, 'distinguished': None}]
        return images

    json_str = json_str.replace("\u00d7", "x") # fix unicode problem: covert multiplication symbol to x
    objects = json.loads(json_str) 
    objects = convert(objects) # fix unicode problem: remove 'u' before every key and value

    for obj in objects['data']['children']: 
        if 'data' in obj: 
            obj = obj['data']
            if 'url' in obj:
                if contains_image_file_extension(obj['url']):
                    size = extract_image_size(obj['title'])
                    if size:
                        if size[0] > minsize and size[1] > minsize:
                            image = obj
                            image['width'] = size[0]
                            image['height'] = size[1]
                            images.append(image) 

    return images

def get_url(url):
    try:
        response = urllib2.urlopen(url)
        html = response.read()
        print html
    except Exception as e:
        print e
        return None
    return html

def convert(input):
    # This recursive function will convert any decoded JSON object from unicode strings to UTF-8-encoded byte strings
    # source: http://stackoverflow.com/questions/956867/how-to-get-string-objects-instead-of-unicode-ones-from-json-in-python#answer-13105359
    if isinstance(input, dict):
        return {convert(key): convert(value) for key, value in input.iteritems()}
    elif isinstance(input, list):
        return [convert(element) for element in input]
    elif isinstance(input, unicode):
        return input.encode('utf-8')
    else:
        return input

def contains_image_file_extension(string):
    img_formats = [".jpg", ".jpeg", ".gif", ".png", ".svg", ".tiff", ".bmp", ".JPG", ".JPEG", ".GIF", ".PNG", ".SVG", ".TIFF", ".BMP" ]
    if any(img_format in string for img_format in img_formats):
        return True
    else:
        return False

def extract_image_size(string):
    size = re.search(r'\d+\s*[x]\s*\d+', string)
    if size: 
        size = size.group().replace(" ", "")
        size = size.replace(" ", "")
        size = size.split("x")
        size[0] = int(size[0])
        size[1] = int(size[1])
        return size
    else:
        return False
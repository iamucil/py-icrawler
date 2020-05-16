from uuid import uuid4
from urllib.parse import urlparse
from django.core.validators import URLValidator
from django.core.exceptions import ValidationError
from django.views.decorators.http import require_POST, require_http_methods
from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from scrapyd_api import ScrapydAPI
# from main.utils import URLUtil
from main.models import ScrapyItem

# connect to scrapyd service
# change to proper domain
# in this project we use docker-compose
# view in file docker-compose.yaml and check service block scrapyd
scrapyd = ScrapydAPI('http://scrapyd:6800')

def is_valid_url(url):
    validate = URLValidator()
    try:
        # check if url format is valid
        validate(url)
    except ValidationError:
        return False

    return True

@csrf_exempt
# only get and post
@require_http_methods(['POST', 'GET'])
def Crawl(request):
    # POST request are for new crawling task
    if request.method == 'POST':
        url = request.POST.get('url', None)  # take url comes from client.

        if not url:
            return JsonResponse({'error': 'Mising args'})

        if not is_valid_url(url):
            return JsonRepsonse({'error': "URL is invalid"})

        domain = urlparse(url)
        unique_id = str(uuid4())  # create a unique ID

        # This is the custom settings for scrapy spider
        # We can send anything we want to use it inside spiders and pipelines
        # I mean, anything
        settings = {
            'unique_id': unique_id,  # unique ID for each record for DB
            'USER_AGENT': 'Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)'
        }
        # Here we schedule a new crawling task from scrapyd
        # Notice that settings is a special argument name.
        # But we can pass other arguments, though
        # this returns a ID which belongs and will be belong to this task
        # We are going to use that to check task's status.
        task = scrapyd.schedule('default', 'pyicrawler', settings=settings, url=url, domain=domain)

        return JsonResponse({'task_id': task, 'unique_id': unique_id, 'status': 'started'})

    # Get requests are for getting result of a specific crawling task
    elif request.method == 'GET':
        # We we passed the from past request above. Remember?
        # They were trying to survive in client side.
        # now they are here again, thankfully.
        # We passed them back to here to check the status of crawling
        # and if crawling is completed, we respond back with a crawled data.
        task_id = request.GET.get('task_id', None)
        unique_id = request.GET.get('unique_id', None)

        if not task_id or not unique_id:
            return JsonResponse({'error': 'Mising args'})

        # Here we check status of crawling that just started a few seconds ago.
        # If it is finished, we can query from database and get results
        # if it is not finished we can return active status
        # possible results are -> pending, running or finished
        status = scrapyd.job_status('default', task_id)
        if status == 'finished':
            try:
                # This is the unique_id that we created even before crawling started.
                item = ScrappyItem.objects.get(unique_id=unique_id)
                return JsonResponse({'data': item.to_dict['data']})
            except Exception as e:
                return JsonResponse({'error': str(e)})
        else:
            return JsonResponse({'status':status})

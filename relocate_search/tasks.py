import requests
from bs4 import BeautifulSoup
import json

from relocate_search.models import Job, JobTag, JobLocation

def grab_hh():
    url_template = 'https://api.hh.ru/vacancies?area=1001&specialization=1.221&page=%d'
    page = 0 
    locations_dict = {}
    while True:
        url = url_template % page
        doc = requests.get(url).text
        parsed = json.load(doc)
        jobs_list = parsed['items']
        if len(jobs_list) == 0:
            break
        page += 1
        for job in jobs_list:
            job_str = job["area"]["name"]
            job_link = job["alternate_url"]
            job_tags = []


            if Job.objects.filter(link=job_link).count() > 0:
                print(job_str, job_link, 'exists')
                continue


            if JobLocation.objects.filter(name=location_str).count() > 0:
                location = JobLocation.objects.get(name=location_str)
            else:
                google_location = requests.request("GET", "https://maps.googleapis.com/maps/api/geocode/json", params={
                    'address': location_str,
                    'key': 'AIzaSyDwqiAaG2FzfgnCvvKX9wTfV7AgJ_t38I0'
                })
                google_location = json.loads(google_location.text)['results'][0]['geometry']['location']
                locations_list = JobLocation.objects.filter(latitude=google_location['lat'], longitude=google_location['lng'])
                if len(locations_list) > 0:
                    location = locations_list[0]
                else:
                    location = JobLocation.objects.create(name=location_str, latitude=google_location['lat'], longitude=google_location['lng'])


            not_existing_tags = [t for t in job_tags if t not in set(JobTag.objects.filter(name__in=job_tags).values_list('name', flat=True))]
            for t in not_existing_tags:
                JobTag.objects.create(name=t)

            job_object = Job.objects.create(name = job_str,
                                            location = location,
                                            link=job_link,
                                            )
            job_object.tags = JobTag.objects.filter(name__in=job_tags).values_list('id', flat=True)
            job_object.save()
            print(job_object.name, job_object.location.name)

def grab_stack_overflow():
    url_template = 'https://stackoverflow.com/jobs?sort=i&v=true&pg=%d'
    page = 1

    locations_dict = {}
    while True:
        url = url_template % page
        html_doc = requests.get(url).text
        soup = BeautifulSoup(html_doc, 'html.parser')
        jobs_list = soup.findAll('div', {'class':'-job'})
        if len(jobs_list) == 0:
            break
        print('Page %d' % page)
        page += 1
        for job in jobs_list:
            location_str = job.find('div', {'class': '-location'}).text.replace('\n', '').replace('\r', '').replace('- ', '').strip()
            job_str = job.find('a', {'class':'job-link'}).text.strip()
            job_link = job.find('a', {'class':'job-link'})['href']
            job_tags = [tag.text.lower().strip() for tag in job.findAll('a', {'class':'post-tag'})]


            if Job.objects.filter(link=job_link).count() > 0:
                print(job_str, job_link, 'exists')
                continue


            if JobLocation.objects.filter(name=location_str).count() > 0:
                location = JobLocation.objects.get(name=location_str)
            else:
                google_location = requests.request("GET", "https://maps.googleapis.com/maps/api/geocode/json", params={
                    'address': location_str,
                    'key': 'AIzaSyDwqiAaG2FzfgnCvvKX9wTfV7AgJ_t38I0'
                })
                google_location = json.loads(google_location.text)['results'][0]['geometry']['location']
                locations_list = JobLocation.objects.filter(latitude=google_location['lat'], longitude=google_location['lng'])
                if len(locations_list) > 0:
                    location = locations_list[0]
                else:
                    location = JobLocation.objects.create(name=location_str, latitude=google_location['lat'], longitude=google_location['lng'])


            not_existing_tags = [t for t in job_tags if t not in set(JobTag.objects.filter(name__in=job_tags).values_list('name', flat=True))]
            for t in not_existing_tags:
                JobTag.objects.create(name=t)

            job_object = Job.objects.create(name = job_str,
                                            location = location,
                                            link=job_link,
                                            )
            job_object.tags = JobTag.objects.filter(name__in=job_tags).values_list('id', flat=True)
            job_object.save()
            print(job_object.name, job_object.location.name)


def grab_moikrug():
    url_template = 'https://moikrug.ru/vacancies?page=%d'
    page = 1

    while True:
        url = url_template % page
        html_doc = requests.get(url).text
        soup = BeautifulSoup(html_doc, 'html.parser')
        jobs_list = soup.findAll('div', {'class':'job'})
        if len(jobs_list) == 0:
            break
        print('Page %d' % page)
        page += 1
        for job in jobs_list:
            if not job.find('span', {'class': 'location'}):
                continue
            location_str = job.find('span', {'class': 'location'}).text.replace('\n', '').replace('\r', '').replace('- ', '').strip()

            job_link = 'https://moikrug.ru' + job.find('div', {'class':'title'}).find('a')['href']
            job_str = job.find('div', {'class':'title'}).find('a').text.strip()
            job_tags = [tag.text.lower().strip() for tag in job.findAll('a', {'class':'skill'})]


            if Job.objects.filter(link=job_link).count() > 0:
                print(job_str, job_link, 'exists')
                continue


            if JobLocation.objects.filter(name=location_str).count() > 0:
                location = JobLocation.objects.get(name=location_str)
            else:
                google_location = requests.request("GET", "https://maps.googleapis.com/maps/api/geocode/json", params={
                    'address': location_str,
                    'key': 'AIzaSyDwqiAaG2FzfgnCvvKX9wTfV7AgJ_t38I0'
                })
                google_location = json.loads(google_location.text)['results'][0]['geometry']['location']
                locations_list = JobLocation.objects.filter(latitude=google_location['lat'], longitude=google_location['lng'])
                if len(locations_list) > 0:
                    location = locations_list[0]
                else:
                    location = JobLocation.objects.create(name=location_str, latitude=google_location['lat'], longitude=google_location['lng'])


            not_existing_tags = [t for t in job_tags if t not in set(JobTag.objects.filter(name__in=job_tags).values_list('name', flat=True))]
            for t in not_existing_tags:
                JobTag.objects.create(name=t)

            job_object = Job.objects.create(name = job_str,
                                            location = location,
                                            link=job_link,
                                            )
            job_object.tags = JobTag.objects.filter(name__in=job_tags).values_list('id', flat=True)
            job_object.save()
            print(job_object.name, job_object.location.name)



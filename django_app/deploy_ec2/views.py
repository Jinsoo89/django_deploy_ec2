import json

import requests
from django.shortcuts import render

from utils.settings import get_setting


def search_from_youtube(keyword, page_token=None):
    youtube_api_key = get_setting()['youtube']['API_KEY']

    # 3. requests 라이브러리를 이용(pip install requests), GET요청으로 데이터를 받아온 후
    # 이렇게 Parameter와 URL을 분리합니다
    params = {
        'part': 'snippet',
        'q': keyword,
        'maxResults': 6,
        'key': youtube_api_key,
        'type': 'video',
        'order': 'viewCount'
    }
    r = requests.get('https://www.googleapis.com/youtube/v3/search',
                     params=params)
    # print(type(r))
    result = r.text

    # 4. 해당 내용을 다시 json.loads()를 이용해 파이썬 객체로 변환
    result_dict = json.loads(result)

    return result_dict


def index(request):
    videos = []
    context = {
        'videos': videos,
    }
    # 포스트일 경우에만 검색결과에 내용이 추가됨
    keyword = '트와이스'
    page_token = request.GET.get('page_token')

    if keyword != '':
        search_result = search_from_youtube(keyword, page_token)

        next_page_token = search_result.get('nextPageToken')
        prev_page_token = search_result.get('prevPageToken')
        total_results = search_result['pageInfo'].get('totalResults')
        context['next_page_token'] = next_page_token
        context['prev_page_token'] = prev_page_token
        context['total_results'] = total_results

        items = search_result['items']
        for item in items:
            # published_date_str = item['snippet']['publishedAt']

            # 다음페이지 있냐 없냐

            youtube_id = item['id']['videoId']
            title = item['snippet']['title']
            description = item['snippet']['description']
            url_thumbnail = item['snippet']['thumbnails']['high']['url']

            cur_item_dict = {
                "title": title,
                "description": description,
                'youtube_id': youtube_id,
                'url_thumbnail': url_thumbnail,
            }

            videos.append(cur_item_dict)

    return render(request, 'main/index.html', context)

#
# def index(request):
#     context = {
#
#     }
#     return render(request, 'main/index.html', context)

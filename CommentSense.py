#importing the required modules
import csv
import os
import google.oauth2.credentials
from textblob import TextBlob
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from google_auth_oauthlib.flow import InstalledAppFlow

# unique credentials required to communicate with the youtube api
def get_authorised():
    #youtube data api v3:
    DEVELOPER_KEY = "AIzaSyBD515PArdQGQiSNzeYmJ9luxqWYZ5_5BM"
    API_SERVICE_NAME = "youtube"
    API_VERSION = "v3"
    
    return build(API_SERVICE_NAME, API_VERSION, developerKey=DEVELOPER_KEY)

# ===========================REQUIRED FUNCTIONS=============================
def get_video_comments(service, **kwargs):
    comments = []
    results = service.commentThreads().list(**kwargs).execute()

    while results:
        for item in results['items']:
            comment = item['snippet']['topLevelComment']['snippet']['textDisplay']
            comments.append(comment)

        # Check if another page exists
        if 'nextPageToken' in results:
            kwargs['pageToken'] = results['nextPageToken']
            results = service.commentThreads().list(**kwargs).execute()
        else:
            break

    return comments


def write_to_csv(comments):
    with open('comments.csv', 'w') as comments_file:
        comments_writer = csv.writer(comments_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        comments_writer.writerow(['Video ID', 'Title', 'Comment'])
        for row in comments:
            # convert the tuple to a list and write to the output file
            comments_writer.writerow(list(row))


def get_videos(service, **kwargs):
    final_results = []
    results = service.search().list(**kwargs).execute()

    i = 0
    max_pages = 1
    while results and i < max_pages:
        final_results.extend(results['items'])

        # Check if another page exists
        if 'nextPageToken' in results:
            kwargs['pageToken'] = results['nextPageToken']
            results = service.search().list(**kwargs).execute()
            i += 1
        else:
            break

    return final_results


def search_videos_by_keyword(service, **kwargs):
    results = get_videos(service, **kwargs)
    final_result = []
    for item in results:
        title = item['snippet']['title']
        video_id = item['id']['videoId']
        comments = get_video_comments(service, part='snippet', videoId=video_id, textFormat='plainText')
        # make a tuple consisting of the video id, title, comment and add the result to 
        # the final list
        final_result.extend([(video_id, title, comment) for comment in comments]) 
    
    write_to_csv(final_result)

def sentiment_analytics():
    with open('comments.csv','r+') as csv_file:
        csv_read=csv.DictReader(csv_file, delimiter=',')
        line_count=0
        text=""
        for row in csv_read:
            text=text.strip()+row["Comment".strip()]
            line_count=line_count+1


    print("==========================")
    print(line_count,"comments processed",end="")
    print("\n==========================")
    blob = TextBlob(text)
    print("Polarity of the comments:")
    print(blob.sentiment.polarity,end="")
    print("\n==========================")

#==================================start from here====================================
if __name__ == '__main__':
    
    os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'
    service = get_authorised()
    keyword = input('Enter a keyword: ')
    maxres=int(input("Number of results: "))
    print("\nscrapping the web...")
    search_videos_by_keyword(service, q=keyword, part='id,snippet', type='video', maxResults=maxres, order='relevance')
    sentiment_analytics()   
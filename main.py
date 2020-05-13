import requests
import re
from pprint import pprint

class DailyMotion:

	base = "https://www.dailymotion.com" #/video/x7t1hps
	video_ep = '/video/'
	video_metadata_ep = '/player/metadata/video/'

	@classmethod
	def get(cls, url):
		if not url.startswith(cls.base + cls.video_ep):
			return Exception('DailyMotion: Invalid URL')
		eyed = url.partition(cls.base + cls.video_ep)[-1]
		response = requests.get(url=cls.base + cls.video_metadata_ep + eyed)
		if response.status_code == 200:
			try:
				manifest_url = response.json()['qualities']['auto'][0]['url']
				data = requests.get(manifest_url).content.decode('utf-8')
				uris = re.findall('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', data)
				
				# download first uri; add functionality to choose resolution
				print (f"Downloading....")
				video_data = requests.get(uris[0])
				with open(f'./{eyed}.mp4', 'wb') as f:
					f.write(video_data.content)
				print ('Saved.')

			except Exception as err:
				return Exception(f'DailyMotion unexpected manifest url/data response. Error: {err}')
		else:
			return Exception(f'DailyMotion metadata request response: {response.status_code}; HTML: {response.json()}')



if __name__ == '__main__':
	url = 'https://www.dailymotion.com/video/x7t1hps'
	DailyMotion.get(url)
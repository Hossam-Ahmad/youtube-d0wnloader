from flask import Flask, request, render_template
from pytube_src import Playlist, YouTube

app = Flask(__name__)


@app.route('/api', methods=['POST', 'GET'])
def api():
    playlist_link = str(request.form['search'])
    playlist = Playlist(playlist_link)
    playlist.populate_video_urls()

    links_360 = []
    links_720 = []
    links_1080 = []

    for i in range(len(playlist.video_urls)):
        # if i < 5:
            try:
                video = playlist.video_urls[i]
                yt = YouTube(video)
                link_360 = yt.streams.filter(subtype='mp4').filter(res='360p').all()
                if len(link_360) > 0:
                    links_360.append(link_360[0].url.replace("videoplayback", "videoplayback/"+link_360[0].title.replace(' ', '_').replace('&#x202c;&rlm;','').replace('&#x202a;','').replace('/', '_').replace('&amp;','')+".mp4"))
                link_720 = yt.streams.filter(subtype='mp4').filter(res='720p').all()
                if len(link_720) > 0:
                    links_720.append(link_720[0].url.replace("videoplayback", "videoplayback/"+link_720[0].title.replace(' ', '_').replace('&#x202c;&rlm;','').replace('&#x202a;','').replace('/', '_').replace('&amp;','')+".mp4"))
                link_1080 = yt.streams.filter(subtype='mp4').filter(res='1080p').all()
                if len(link_1080) > 0:
                    links_1080.append(links_1080[0].url.replace("videoplayback", "videoplayback/"+links_1080[0].title.replace(' ', '_').replace('&#x202c;&rlm;','').replace('&#x202a;','').replace('/', '_').replace('&amp;','')+".mp4"))
            except:
                pass

    return ",".join(links_360)

    return render_template('index.html', result='\n'.join(links_360))

    # class Response:
    #     def __init__(self, items360, items720, items1080):
    #         self.items360 = items360
    #         self.items720 = items720
    #         self.items1080 = items1080
    #
    #     def toJSON(self):
    #         return json.dumps(self, default=lambda o: o.__dict__, sort_keys=True, indent=4)
    #
    # response = Response(links_360, links_720, links_1080)
    # return(response.toJSON())

@app.route('/')
def main():
    return render_template('index.html')


if __name__ == '__main__':
    app.run()
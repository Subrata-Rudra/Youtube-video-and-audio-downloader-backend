from flask import *
import json
from flask_cors import CORS
from pytube import YouTube

app = Flask(__name__)
CORS(app)

# **************************************************HomePage Start**********************************************
@app.route('/', methods=['GET'])
def home_page():
    data_set = {'Page': 'HomePage of YouTube Downloader',
                'Message': 'Successfully loaded the HomePage🎉'}
    json_dump = json.dumps(data_set)
    return json_dump
# **************************************************HomePage End*************************************************


# ***********************************************Video Download Start********************************************
@app.route('/video/', methods=['GET'])
def download_video():
    link = str(request.args.get('link'))
    utube = YouTube(link)
    Title = utube.title
    Thumbnail = utube.thumbnail_url

    videos = utube.streams

    # To get only the (audio + video) streams
    vdos = videos.filter(progressive=True)

    resolution_list = []
    itag_list = []
    ind = 0

    for vdo in vdos:
        resolution_list.insert(ind, vdo.resolution)
        itag_list.insert(ind, vdo.itag)
        ind = ind + 1

    resolution_list_json = json.dumps(resolution_list)

    dwnld_link_list = []
    indx = 0
    for i in itag_list:
        dwnld_link_list.insert(indx, vdos.get_by_itag(i).url)
        indx = indx + 1

    dwnld_link_list_json = json.dumps(dwnld_link_list)

    data_set = {'video_title': Title, 'video_thumbnail': Thumbnail,
                'video_resolution_list': resolution_list_json, 'video_download_link_list': dwnld_link_list_json}

    json_dump = json.dumps(data_set)

    return json_dump
# **************************************************Video Download End*******************************************


# *************************************************Audio Download Start******************************************
@app.route('/audio/', methods=['GET'])
def download_audio():
    link = str(request.args.get('link'))
    utube = YouTube(link)
    Title = utube.title
    Thumbnail = utube.thumbnail_url

    # To get only the audio streams
    ados = utube.streams.filter(only_audio=True)
    resolution_list = []
    itag_list = []
    ind = 0

    for ado in ados:
        resolution_list.insert(ind, ado.abr)
        itag_list.insert(ind, ado.itag)
        ind = ind + 1

    resolution_list_json = json.dumps(resolution_list)

    dwnld_link_list = []
    indx = 0
    for i in itag_list:
        dwnld_link_list.insert(indx, ados.get_by_itag(i).url)
        indx = indx + 1

    dwnld_link_list_json = json.dumps(dwnld_link_list)

    data_set = {'audio_title': Title, 'audio_thumbnail': Thumbnail,
                'audio_resolution_list': resolution_list_json, 'audio_download_link_list': dwnld_link_list_json}

    json_dump = json.dumps(data_set)

    return json_dump

# ***************************************************Audio Download End********************************************


if __name__ == '__main__':
    app.run()

import requests
import json
from datetime import datetime
import subprocess as sp
import sys
import shlex

'''
    Returns a DTO containing information about a given course's lectures.
'''
def get_media_recordings_dto(course_id, auth_token):
    hed = {'Authorization': 'Bearer ' + auth_token}
    url = 'https://lrswapi.campus.mcgill.ca/api/MediaRecordings/dto/{0}'.format(course_id)
    response = requests.get(url, headers=hed)
    if (response.status_code != 200):
        raise RuntimeError('Request failed. Status code: {}'.format(response.status_code))
    dto = response.json()
    return dto

def get_m3u8_stream(lecture):
    sources = lecture['sources']
    return "{0}.m3u8".format(sources[0]['src'])

def print_progress(percent: float, duration_down: int, total_duration: int, elapsed: float) -> None:
    bar_ = list('|' + (20 * ' ') + '|')
    to_fill = int(round((duration_down / total_duration) * 20)) or 1
    for x in range(1, to_fill):
        bar_[x] = '░'
    bar_[to_fill] = '░'
    s_bar = ''.join(bar_)
    sys.stdout.write('\r{}  {:5.1f}%   {:f} / {:f} seconds downloaded;   '
                     'elapsed time: {:.2f} seconds'.format(
                         s_bar, percent, duration_down, total_duration, elapsed))
    sys.stdout.flush()

def download(in_file, out_file, duration):
    commands = shlex.split(
        'ffmpeg -nostats -loglevel 0 -progress - -protocol_whitelist file,http,https,tcp,tls,crypto -i {} -c copy {}'.format(in_file, out_file)
        )
    start = datetime.now()
    out_time_prefix = "out_time_us="
    p = sp.Popen(commands, shell=False, stdout=sp.PIPE)
    # Poll process.stdout to show stdout live
    while True:
        output = p.stdout.readline()
        if p.poll() is not None:
            break
        if output:
            out = output.strip().decode('utf-8')
            if out_time_prefix in out:
                duration_down = int(out[len(out_time_prefix):]) / 1000000 
                print_progress(float(duration_down)/float(duration)*100, duration_down, duration, (datetime.now()-start).total_seconds())
    
    print('\n')

def run(course_id, output_dir, auth_token):
    course_dto = get_media_recordings_dto(course_id, auth_token)
    date_format = 'YYYY-MM-DD'

    for lecture in course_dto:
        date = lecture['dateTime'][:len(date_format)]
        duration = int(lecture['durationSeconds'])
        id = lecture['recordingInt']
        file_name = "{}_{}.mp4".format(id, date)
        print('Downloading lecture from {} to {} ...'.format(date, file_name))

        m3u8 = get_m3u8_stream(lecture)
        out = output_dir + file_name
        download(m3u8, out, duration)

        print('Lecture {} downloaded to {}'.format(file_name, output_dir))


def probe(in_file):
    commands = shlex.split('ffprobe -v quiet -print_format json -show_format -show_streams {}'.format(in_file))
    json_object = json.loads(sp.check_output(commands, encoding='utf-8'))
    return json_object



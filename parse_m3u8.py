import m3u8

_path = input('Enter m3u8 path:')

playlist = m3u8.load(_path)

# playlist = m3u8.load('https://dplusindia-google.prod-vod.h264.io/d6e4176a-8384-4b8f-98f1-9688721421c4/x-goog-token=Expires=1590180862&KeyName=prod-sign-url-key&Signature=E_6EtuTzw6abggGHrOfxUkKaWcs/Master.m3u8')
# playlist = m3u8.load('https://test-streams.mux.dev/x36xhzz/x36xhzz.m3u8')
# playlist = m3u8.load('https://bitdash-a.akamaihd.net/content/sintel/hls/playlist.m3u8')
# playlist = m3u8.load('https://test-streams.mux.dev/x36xhzz/url_2/193039199_mp4_h264_aac_ld_7.m3u8')

# this is an absolute filename
# playlist = m3u8.load('../sample-stream-playlists/sintel/playlist.m3u8')


# print(playlist.segments)
# print(playlist.target_duration)
# print(playlist.media)
# print(playlist.playlists)
# print(playlist.playlists[0].stream_info.resolution)
# print(playlist.playlists[0].media[0].type)
# print(playlist.files)

# if you want to write a file from its content
# playlist.dump('playlist.m3u8')

if playlist.playlists:
    print('%s playlists found...' % len(playlist.playlists))
    count = 0
    for pl in playlist.playlists:
        count += 1
        print('%d - Resolution: %s Bandwidth: %s' %
              (count, pl.stream_info.resolution, pl.stream_info.bandwidth))

    selected_pl = input('Select playlist to fetch:')

    try:
        selected_pl = int(selected_pl)
    except ValueError:
        exit('Invalid input! Not a number')

    if selected_pl > count or selected_pl <= 0:
        exit('Invalid selection!')

    # fetch input in loop until user selects correct playlist
    # selected_pl = input('Select playlist to fetch:')
    # while selected_pl > count or selected_pl <= 0:
    #     print('Invalid selection!')
    #     selected_pl = input('Select playlist to fetch:')

    stream = playlist.playlists[selected_pl-1]
    print('Selected playlist URI: %s' % stream.uri)
    vstream = {'uri': stream.absolute_uri,
               'resolution': stream.stream_info.resolution}

    if stream.media:
        print('%d total sub-media streams found...' % len(stream.media))
        aucount = 0  # audio count
        stcount = 0  # subtitle count
        austreams = {}
        ststreams = {}
        for mstream in stream.media:
            if mstream.type == 'AUDIO':
                austreams[aucount] = {'uri': mstream.absolute_uri,
                                      'language': mstream.language, 'name': mstream.name, 'group_id': mstream.group_id}
                aucount += 1
            elif mstream.type == "SUBTITLES":
                ststreams[stcount] = {'uri': mstream.absolute_uri,
                                      'language': mstream.language, 'name': mstream.name, 'group_id': mstream.group_id}
                stcount += 1

    print('%d Audio Streams found' % aucount)
    print('%d Subtitles Streams found' % stcount)

cmd1 = ["ffmpeg",
        "-loglevel", "warning",
        "-allowed_extensions", "ALL",
        "-i", vstream.get('uri'),
        "-acodec", "copy",
        "-vcodec", "copy",
        "-bsf:a", "aac_adtstoasc",
        "output.mkv"]
# print('Use this command %s', cmd1)

cmd_start = 'ffmpeg -i "' + vstream.get('uri') + '" '
map_attr = '-map 0:v '
metadata_attr = ''

map_attr_indx = 1
metadata_attr_indx = 0
for aui, auitem in austreams.items():
    cmd_start += '-i "' + auitem.get('uri') + '" '
    metadata_attr += '-metadata:s:a:' + str(metadata_attr_indx) + ' language=' + \
        auitem.get('language') + ' -metadata:s:a:' + str(metadata_attr_indx) + \
        ' title="' + auitem.get('name') + '" '
    metadata_attr_indx += 1
    map_attr += '-map ' + str(map_attr_indx) + ':a '
    map_attr_indx += 1

metadata_attr_indx = 0
for sui, stitem in ststreams.items():
    cmd_start += '-i "' + stitem.get('uri') + '" '
    metadata_attr += '-metadata:s:s:' + str(metadata_attr_indx) + ' language=' + \
        stitem.get('language') + ' -metadata:s:s:' + str(metadata_attr_indx) + \
        ' title="' + stitem.get('name') + '" '
    metadata_attr_indx += 1
    map_attr += '-map ' + str(map_attr_indx) + ':s '
    map_attr_indx += 1

cmd_end = '-c:v copy -c:a copy output.mkv'
cmd_end = '-c copy -bsf:a aac_adtstoasc -vcodec copy -crf 50 output.mp4'
cmd_end = '-c copy -c:s mov_text output.mp4'
cmd2 = cmd_start + map_attr + metadata_attr + cmd_end

print('\nUse following command on terminal to download video:\n\n' +cmd2)
print('hi')

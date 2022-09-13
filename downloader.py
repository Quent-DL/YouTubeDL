from pytube import YouTube, Playlist
import pytube as pt
import sys
import scripts as scr
import urllib

_FORBIDDEN_CHARS_IN_FILENAME = '\\/:*?"<>|'

class DownloadRequest:
    def __init__(
            self, 
            link="", 
            path=None, 
            name="ytdl_result", 
            audio_only=False,
            is_playlist=False,
            uiw=None):
        
        self.__videos_downloaded = 0
        self.__bytes_downloaded = 0
        self.__total_size = None

        self.__is_playlist = is_playlist
        if path == "": raise ValueError(scr.ERR_NO_PATH)
        self.__path = path
        self.__custom_name = name
        self.__ext = (scr.EXT_TYPES[0] if audio_only else scr.EXT_TYPES[1])

        # these two functions redirect to actual callback functions that
        # also accept a UI_Work object as argument
        on_progress = lambda s, c, b: self.__on_progress(s, b, uiw)
        on_complete = lambda s, p: self.__on_complete(s, uiw)
        try:
            if self.__is_playlist:
                yts = [YouTube(url=vid_url, on_progress_callback=on_progress,
                               on_complete_callback=on_complete)
                    for vid_url in Playlist(link).video_urls]
                if (yts == []): raise ValueError(scr.ERR_PLAYLIST)
            else: 
                yts = YouTube(url=link, on_progress_callback=on_progress, 
                              on_complete_callback=on_complete)
        except (pt.exceptions.RegexMatchError, KeyError):
            raise ValueError(scr.ERR_URL)
        except pt.exceptions.VideoUnavailable:
            ### TODO Change ValueError to customException (e.g. ConnectionError)
            raise ValueError(scr.ERR_UNAVAILABLE_VIDEO)
        except urllib.error.URLError:
            ### TODO Change ValueError to customException (e.g. ConnectionError)
            raise ValueError(scr.ERR_CONNECTION)

        # Fetches the appropriate method to call for the wanted Stream object 
        get_proper_stream = (pt.query.StreamQuery.get_audio_only if audio_only 
                             else pt.query.StreamQuery.get_highest_resolution)
        if self.__is_playlist:
            # No 'Private Video' issue to treat here : they are automatically
            # removed from the Playlist object
            self.__streams = [get_proper_stream(yt.streams) for yt in yts]
        else:
            try:
                self.__streams = [get_proper_stream(yts.streams)]
            except pt.exceptions.VideoPrivate:
                raise ValueError(scr.ERR_VIDEO_PRIVATE)

        """####### DELETED LINES ############################################
        if (audio_only): 
            self.__streams = [yt.streams.get_audio_only() for yt in yts]
        else: 
            self.__streams = [yt.streams.get_highest_resolution() for yt in yts]"""


    def total_byte_size(self):
        """Returns the total number of bytes contained in a video/playlist.
        Only the bytes that are necessary for a video to be played are counted
        (title, description, author, etc. are ignored).
        
        Args:
        - streams (pytube.Stream or pytube.Stream[]): the video/playlist to get
        the total size of. 

        Returns:
        - (int) : the total size in bytes."""
        if self.__total_size != None: return self.__total_size
        count = 0
        for stream in self.__streams: count += stream.filesize
        self.__total_size = count
        return count

    
    def __on_progress(self, stream, stream_remaining_bytes, uiw):
        uiw.update_progress_bar(
            self.__bytes_downloaded + stream.filesize - stream_remaining_bytes,
            f"{self.__videos_downloaded}/{len(self.__streams)}")


    def __on_complete(self, stream, uiw):
        self.__bytes_downloaded += stream.filesize
        self.__videos_downloaded += 1
        uiw.update_progress_bar(
            self.__bytes_downloaded,
            f"{self.__videos_downloaded}/{len(self.__streams)}")


    def download(self):
        ### TODO : si erreur liée à vidéo privée, continuer avec le reste de la playlist
        self.__bytes_downloaded = 0
        use_title = (self.__is_playlist) or (self.__custom_name == "")
        for s in self.__streams:
            fn = (s.title if use_title else self.__custom_name) + self.__ext
            for c in _FORBIDDEN_CHARS_IN_FILENAME:
                fn = fn.replace(c, "_")
            s.download(
                output_path=self.__path,
                filename=fn)


### For command-line activation
if __name__ == '__main__': 
    try:
        YouTube(sys.argv[1]).streams.get_highest_resolution().download(
            output_path="./vids"
        )
        print("Task Completed!") 
    except Exception:
        pass

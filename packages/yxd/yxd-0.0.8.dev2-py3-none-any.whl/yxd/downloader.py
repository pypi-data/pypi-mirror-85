import os
import signal
import time
from . import util
from .arguments import Arguments
from .exceptions import InvalidVideoIdException, NoContents, PatternUnmatchError, UnknownConnectionError
from .extractor import Extractor
from .html_archiver import HTMLArchiver
from .util.extract_video_id import extract_video_id
from .progressbar import ProgressBar
from .videoinfo import VideoInfo
from .youtube import channel
from json.decoder import JSONDecodeError
from pathlib import Path
from typing import List, Dict


class Downloader:

    def __init__(self, dir_videos: set):
        self._dir_videos = dir_videos

    def video(self, video) -> None:
        try:
            video_id = extract_video_id(video.get('id'))
        except Exception as e:
            video_id = video.get("id")
            print(type(e), str(e))
        try:

            if not os.path.exists(Arguments().output):
                raise FileNotFoundError
            separated_path = str(Path(Arguments().output)) + os.path.sep
            path = util.checkpath(separated_path + video_id + '.html')
            # check if the video_id is already exists the output folder
            if video_id in self._dir_videos:
                print(
                    f"Video [{video_id}] is already exists in {os.path.dirname(path)}. Skip process.")
                return False
            time.sleep(1)
            print(f"\n"
                  f"[title]    {video.get('title')}\n"
                  f"[id]       {video_id}    [published] {video.get('time_published')}\n"
                  f"[channel]  {video.get('author')}"
                  )
            print(f"[path]     {path}")
            if video.get("error"):
                # error getting video info in parse()
                print(f"The video [{video_id}] may be private or deleted.")
                return False
            try:
                duration = video["duration"]
            except KeyError:
                return False
            pbar = ProgressBar(total=(duration * 1000), status="Extracting")

            ex = Extractor(video_id,
                           callback=pbar._disp)
            signal.signal(signal.SIGINT, (lambda a, b: self.cancel(ex, pbar)))
            transcripts = ex.extract()
            if transcripts[0].get("error"):
                if transcripts[0]["error"] == 4:  # cancel
                    exit(0)
                return False
            pbar.reset("#", "=", total=len(transcripts), status="Rendering  ")
            processor = HTMLArchiver(
                Arguments().output + video_id + '.html', callback=pbar._disp)
            processor.process(transcripts)
            processor.finalize()
            pbar.close()
            print("\nCompleted")

            print()
            if pbar.is_cancelled():
                print("\nThe extraction process has been discontinued.\n")
                return False
            return True

        except InvalidVideoIdException:
            print("Invalid Video ID or URL:", video_id)
        except NoContents as e:
            print('---' + str(e) + '---')
        except FileNotFoundError:
            print("The specified directory does not exist.:{}".format(
                Arguments().output))
            exit(0)
        except JSONDecodeError as e:
            print(e.msg)
            print("Cannot parse video information.:{}".format(video_id))
            if Arguments().save_error_data:
                util.save(e.doc, "ERR_JSON_DECODE", ".dat")
        except PatternUnmatchError as e:
            print("Cannot parse video information.:{}".format(video_id))
            if Arguments().save_error_data:
                util.save(str(e), "ERR_PATTERN_UNMATCH", ".dat")
        except Exception as e:
            print("[OUTER EXCEPTION]" + str(type(e)), str(e))

    def videos(self, video_ids: List[int]) -> None:
        for i, video_id in enumerate(video_ids):
            print(f"\n{'-'*10} video:{i+1} of {len(video_ids)} {'-'*10}")
            if '[' in video_id or ']' in video_id:
                video_id = video_id.replace('[', '').replace(']', '')
            try:
                video = self.get_info(video_id)
                if video.get("error"):
                    print("The video id is invalid :", video_id)
                    continue
                self.video(video)
            except InvalidVideoIdException:
                print(f"Invalid video id: {video_id}")
            except UnknownConnectionError:
                print(f"Network Error has occured during processing:[{video_id}]")  # -!-
            except Exception as e:
                print("[OUTER EXCEPTION]" + str(type(e)), str(e))

    def channels(self, channels: List[str]) -> None:
        for i, ch in enumerate(channels):
            counter = 0
            for video in channel.get_videos(channel.get_channel_id(ch)):
                if counter > Arguments().first - 1:
                    break
                print(
                    f"\n{'-'*10} channel: {i+1} of {len(channels)} / video: {counter+1} of {Arguments().first} {'-'*10}")
                ret = self.video(video)
                if ret:
                    counter += 1

    def cancel(self, ex, pbar) -> None:
        print("cancel")
        pbar.cancel()
        exit(0)

    def get_info(self, video_id: str) -> Dict:
        video = dict()
        for i in range(3):
            try:
                info = VideoInfo(video_id)
                break
            except PatternUnmatchError:
                time.sleep(2)
                continue
            except Exception as e:
                print("[OUTER EXCEPTION]" + str(type(e)), str(e))
                return {"error": True}    
        else:
            print(f"PatternUnmatchError:{video_id}")
            video['id'] = ""
            video['author'] = ""
            video['time_published'] = ""
            video['title'] = ""
            video['duration'] = ""
            video['error'] = True
            return video

        video['id'] = video_id
        video['author'] = str(info.get_channel_name())
        video['time_published'] = "Unknown"
        video['title'] = str(info.get_title())
        video['duration'] = str(info.get_duration())
        return video

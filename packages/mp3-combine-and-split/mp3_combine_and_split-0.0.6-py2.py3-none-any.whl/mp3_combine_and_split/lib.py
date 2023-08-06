"""Main MP3CombineAndSplit module."""
import os

import eyed3
from eyed3.mimetype import guessMimetype
from eyed3.mp3 import MIME_TYPES as MP3_MIME_TYPES
import natsort
from os import listdir
from os.path import isfile, join
from pydub import AudioSegment


class MP3CombineAndSplit(object):
    def __init__(
        self,
        input_directory,
        out_directory=None,
        duration="2690",  # Default 44 mins 50 seconds
    ):

        self.input_directory = input_directory
        self.out_directory = out_directory
        self.duration_seconds = duration
        self.duration_miliseconds = self.duration_seconds * 1000
        self.artist = None
        self.album = None

    def combine_mp3s(self):
        mp3files = self.find_mp3_files_in_input_directory()
        combined_mp3_path = None
        if mp3files:
            combined_mp3_path = join(self.out_directory, "combined.mp3")
            if not isfile(combined_mp3_path):
                combined_mp3 = AudioSegment.from_mp3(mp3files[0])

                for mp3file in mp3files[1:]:
                    mp3_obj = AudioSegment.from_mp3(mp3file)
                    print(f"combining {mp3file}")
                    combined_mp3 = combined_mp3 + mp3_obj

                combined_mp3_path = join(self.out_directory, "combined.mp3")
                combined_mp3.export(
                    combined_mp3_path,
                    format="mp3",
                    tags={"artist": self.artist, "album": self.album},
                )

        return combined_mp3_path

    def split_mp3(self, combined_mp3):
        split_mp3s = []
        combined_mp3 = AudioSegment.from_mp3(combined_mp3)

        for i, chunk in enumerate(combined_mp3[:: self.duration_miliseconds]):
            split_mp3_track_num = i + 1
            split_mp3_path = join(
                self.out_directory,
                f"{self.artist}-{self.album}-{split_mp3_track_num}.mp3",
            )
            with open(split_mp3_path, "wb") as split_mp3:
                chunk.export(
                    split_mp3,
                    format="mp3",
                    tags={
                        "artist": self.artist,
                        "album": self.album,
                        "tracknum": split_mp3_track_num,
                    },
                )
                split_mp3s.append(split_mp3_path)
        return split_mp3s

    def find_mp3_files_in_input_directory(self):
        mp3files = []
        mp3_file_by_track_num = dict()
        sort_order_index = 0
        for input_file in natsort.natsorted(listdir(self.input_directory)):
            file_path = join(self.input_directory, input_file)
            if isfile(file_path):
                mime_type = guessMimetype(file_path)
                if mime_type in MP3_MIME_TYPES:
                    sort_order_index = sort_order_index + 1
                    mp3_file_object = eyed3.load(file_path)
                    # using sort order index as track number can't be relied
                    # upon especially if multiple albums in the same directory"
                    mp3_file_object_track_num = sort_order_index

                    try:
                        self.album = mp3_file_object.tag.album
                    except AttributeError:
                        fallback_album = os.path.basename(self.input_directory)
                        print(
                            f"{file_path} does not have a valid album - using {fallback_album} instead"
                        )
                        self.album = fallback_album

                    try:
                        self.artist = mp3_file_object.tag.artist
                    except AttributeError:
                        fallback_artist = os.path.basename(self.input_directory)
                        print(
                            f"{file_path} does not have a valid artist - using {fallback_artist} instead"
                        )
                        self.artist = fallback_artist

                    mp3_file_by_track_num[mp3_file_object_track_num] = file_path

        sorted_track_nums = sorted(mp3_file_by_track_num.keys())
        for sorted_track_num in sorted_track_nums:
            mp3files.append(mp3_file_by_track_num[sorted_track_num])
        return mp3files

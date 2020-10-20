#!/usr/bin/python3
"""
Application:  mkv_extractor
Author:  BSFEMA
Started:  2008-10-18
Prerequisites:  You need to have MKVToolNix installed:  https://mkvtoolnix.download/downloads.html
                Try running "mkvmerge --version" in terminal
                If that works, then you are good to go, otherwise install MKVToolNix
Command Line Parameters:  There is just 1:
                          It is the folder path that will be used to start looking at the *.mkv files from.
                          If this value isn't provided, then the starting path will be where this application file is located.
                          The intention is that you can call this application from a context menu from a file browser (e.g. Nemo) and it would automatically load up that folder.
Purpose:  I couldn't find a good mkvextract frontend for Linux, so I decided to make my own and used this as an oppertunity to learn python subprocess and json.
          This currently exports all tracks (audio, video, subtitles) as well as chapters and attachments.
          I have never used mkv [tags, CUE sheets, timestamps, cues], so I'm not going to bother with them here.
Resources:  https://mkvtoolnix.download/doc/mkvextract.html
"""


import sys
import os
import subprocess
import json


default_folder_path = ""  # The path for this application to run against.
files = []  # A list of files in the 'default_folder_path' to run against.
json_data = ""  # This stores the json data for the mkv object's information.


def export_all_audios(file):
    filename = file[0:len(file) - 4]
    if not (json_data.get("tracks") is None):
        command = ""
        for track in json_data["tracks"]:
            if track["type"] == "audio":
                track_type = track["properties"]["codec_id"]
                track_id = track["id"]
                track_lang = track["properties"]["language_ietf"]
                if not (track["properties"].get("track_name") is None):
                    track_filename = filename + ".track_" + str(track_id) + "." + track["properties"]["track_name"] + "." + track_lang
                else:
                    track_filename = filename + ".track_" + str(track_id) + "." + track_lang
                # Give the subtitles file a proper extension
                """
                A_AAC/MPEG2/*, A_AAC/MPEG4/*, A_AAC 	All AAC files will be written into an AAC file with ADTS headers before each packet. The ADTS headers will not contain the deprecated emphasis field.
                A_AC3, A_EAC3 	These will be extracted to raw AC-3 files.
                A_ALAC 	ALAC tracks are written to CAF files.
                A_DTS 	These will be extracted to raw DTS files.
                A_FLAC 	FLAC tracks are written to raw FLAC files.
                A_MPEG/L2 	MPEG-1 Audio Layer II streams will be extracted to raw MP2 files.
                A_MPEG/L3 	These will be extracted to raw MP3 files.
                A_OPUS 	Opus(tm) tracks are written to OggOpus(tm) files.
                A_PCM/INT/LIT, A_PCM/INT/BIG 	Raw PCM data will be written to a WAV file. Big-endian integer data will be converted to little-endian data in the process.
                A_REAL/* 	RealAudio(tm) tracks are written to RealMedia(tm) files.
                A_TRUEHD, A_MLP 	These will be extracted to raw TrueHD/MLP files.
                A_TTA1 	TrueAudio(tm) tracks are written to TTA files. Please note that due to Matroska(tm)'s limited timestamp precision the extracted file's header will be different regarding two fields: data_length (the total number of samples in the file) and the CRC.
                A_VORBIS 	Vorbis audio will be written into an OggVorbis(tm) file.
                A_WAVPACK4 	WavPack(tm) tracks are written to WV files.
                """
                if "AAC" in track_type:
                    track_filename = track_filename + ".aac"
                elif "AC3" in track_type:
                    track_filename = track_filename + ".ac3"
                elif "ALAC" in track_type:
                    track_filename = track_filename + ".caf"
                elif "DTS" in track_type:
                    track_filename = track_filename + ".dts"
                elif "FLAC" in track_type:
                    track_filename = track_filename + ".flac"
                elif "MPEG/L2" in track_type:
                    track_filename = track_filename + ".mp2"
                elif "MPEG/L3" in track_type:
                    track_filename = track_filename + ".mp3"
                elif "OPUS" in track_type:
                    track_filename = track_filename + ".ogg"
                elif "PCM" in track_type:
                    track_filename = track_filename + ".wav"
                elif "REAL" in track_type:
                    track_filename = track_filename + ".ra"
                elif "TRUEHD" in track_type:
                    track_filename = track_filename + ".thd"
                elif "MLP" in track_type:
                    track_filename = track_filename + ".mlp"
                elif "TTA1" in track_type:
                    track_filename = track_filename + ".tta"
                elif "VORBIS" in track_type:
                    track_filename = track_filename + ".ogg"
                elif "WAVPACK4" in track_type:
                    track_filename = track_filename + ".wv"
                # Build command line for current track
                if default_folder_path == "":
                    command = command + "\"" + str(track_id) + ":" + str(track_filename) + "\" "
                else:
                    command = command + "\"" + str(track_id) + ":" + str(default_folder_path) + "/" + str(track_filename) + "\" "
    else:
        command = ""
    return command


def export_all_videos(file):
    filename = file[0:len(file) - 4]
    if not (json_data.get("tracks") is None):
        command = ""
        for track in json_data["tracks"]:
            if track["type"] == "video":
                track_type = track["properties"]["codec_id"]
                track_id = track["id"]
                track_lang = track["properties"]["language_ietf"]
                if not (track["properties"].get("track_name") is None):
                    track_filename = filename + ".track_" + str(track_id) + "." + track["properties"]["track_name"] + "." + track_lang
                else:
                    track_filename = filename + ".track_" + str(track_id) + "." +  track_lang
                # Give the video file a proper extension
                """
                V_MPEG1, V_MPEG2 	MPEG-1 and MPEG-2 video tracks will be written as MPEG elementary streams.
                V_MPEG4/ISO/AVC 	H.264 / AVC video tracks are written to H.264 elementary streams which can be processed further with e.g. MP4Box(tm) from the GPAC(tm) package.
                V_MPEG4/ISO/HEVC 	H.265 / HEVC video tracks are written to H.265 elementary streams which can be processed further with e.g. MP4Box(tm) from the GPAC(tm) package.
                V_MS/VFW/FOURCC 	Fixed FPS video tracks with this CodecID are written to AVI files.
                V_REAL/* 	RealVideo(tm) tracks are written to RealMedia(tm) files.
                V_THEORA 	Theora(tm) streams will be written within an Ogg(tm) container
                V_VP8, V_VP9 	VP8 / VP9 tracks are written to IVF files. 
                """
                if "V_MPEG1" in track_type or "V_MPEG2" in track_type:
                    track_filename = track_filename + ".mpg"
                elif track_type == "V_MPEG4/ISO/AVC":
                    track_filename = track_filename + ".h264"
                elif "HEVC" in track_type:
                    track_filename = track_filename + ".h265"
                elif track_type == "V_MS/VFW/FOURCC":
                    track_filename = track_filename + ".avi"
                elif "V_REAL" in track_type:
                    track_filename = track_filename + ".rm"
                elif track_type == "V_THEORA":
                    track_filename = track_filename + ".ogg"
                elif "V_VP8" in track_type or "V_VP9" in track_type:
                    track_filename = track_filename + ".ivf"
                # Build command line for current track
                if default_folder_path == "":
                    command = command + "\"" + str(track_id) + ":" + str(track_filename) + "\" "
                else:
                    command = command + "\"" + str(track_id) + ":" + str(default_folder_path) + "/" + str(track_filename) + "\" "
    else:
        command = ""
    return command


def export_all_subtitles(file):
    filename = file[0:len(file) - 4]
    if not (json_data.get("tracks") is None):
        command = ""
        for track in json_data["tracks"]:
            if track["type"] == "subtitles":
                track_type = track["properties"]["codec_id"]
                track_id = track["id"]
                track_lang = track["properties"]["language_ietf"]
                if not (track["properties"].get("track_name") is None):
                    track_filename = filename + ".track_" + str(track_id) + "." + track["properties"]["track_name"] + "." + track_lang
                else:
                    track_filename = filename + ".track_" + str(track_id) + "." + track_lang
                # Give the subtitles file a proper extension
                """
                S_HDMV/PGS 	PGS subtitles will be written as SUP files.
                S_TEXT/SSA, S_TEXT/ASS, S_SSA, S_ASS 	SSA and ASS text subtitles will be written as SSA/ASS files respectively.
                S_TEXT/UTF8, S_TEXT/ASCII 	Simple text subtitles will be written as SRT files.
                S_VOBSUB 	VobSub(tm) subtitles will be written as SUB files along with the respective index files, as IDX files.
                S_TEXT/USF 	USF text subtitles will be written as USF files.
                S_TEXT/WEBVTT 	WebVTT text subtitles will be written as WebVTT files.
                """
                if "PGS" in track_type:
                    track_filename = track_filename + ".sup"
                elif "ASS" in track_type:
                    track_filename = track_filename + ".ass"
                elif "SSA" in track_type:
                    track_filename = track_filename + ".ssa"
                elif "UTF8" in track_type or "ASCII" in track_type:
                    track_filename = track_filename + ".srt"
                elif "VOBSUB" in track_type:
                    track_filename = track_filename + ".sub"
                elif "USF" in track_type:
                    track_filename = track_filename + ".usf"
                elif "WEBVTT" in track_type:
                    track_filename = track_filename + ".vtt"
                # Build command line for current track
                if default_folder_path == "":
                    command = command + "\"" + str(track_id) + ":" + str(track_filename) + "\" "
                else:
                    command = command + "\"" + str(track_id) + ":" + str(default_folder_path) + "/" + str(track_filename) + "\" "
    else:
        command = ""
    return command


def export_all_attachments(file):
    if not (json_data.get("attachments") is None):
        command = " attachments "
        for attachment in json_data["attachments"]:
            id = attachment["id"]
            filename = attachment["file_name"]
            # Build command line for current attachment
            if default_folder_path == "":
                command = command + str(id) + ':\"' + str(filename) + "\" "
            else:
                command = command + str(id) + ':\"' + str(default_folder_path) + "/" + str(filename) + "\" "
    else:
        command = ""
    return command


def export_chapters(file):
    filename = file[0:len(file) - 4]
    if not (json_data.get("chapters") is None):
        if default_folder_path == "":
            command = " chapters \"" + filename + ".chapters.xml\""
        else:
            command = " chapters \"" + default_folder_path + "/" + filename + ".chapters.xml\""
    else:
        command = ""
    return command


def process_files():
    global json_data
    # User imput for what action to take
    print("Choose what to extract:")
    print("1)  Everything")
    print("2)  Tracks (Audio + Video + Subtitles)")
    print("3)  Attachments")
    print("4)  Subtitles")
    print("5)  Videos")
    print("6)  Audios")
    print("7)  Chapters")
    action = ""
    while action == "":
        action = input("Enter manga URL: ").strip()
    action = str(action)
    for file in files:
        # Get information from mkv file in json format:
        if default_folder_path == "":
            cmd = ["mkvmerge --identify --identification-format json " + file]
        else:
            cmd = ["mkvmerge --identify --identification-format json \"" + default_folder_path + "/" + file + "\""]
        proc = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
        json_data, err = proc.communicate()
        json_data = json_data.decode("utf-8")
        json_data = json.loads(json_data)  # json information of all objects in the mkv file
        # Build options based on actions selection:
        options = ""
        if action == "1":  # Everything
            options = " tracks "
            options = options + export_all_subtitles(file)
            options = options + export_all_videos(file)
            options = options + export_all_audios(file)
            options = options + export_all_attachments(file)
            options = options + export_chapters(file)
        elif action == "2":  # Tracks (audio + video + subtitles)
            options = " tracks "
            options = options + export_all_subtitles(file)
            options = options + export_all_videos(file)
            options = options + export_all_audios(file)
        elif action == "3":  # Attachments
            options = options + export_all_attachments(file)
        elif action == "4":  # Subtitles
            options = " tracks "
            options = options + export_all_subtitles(file)
        elif action == "5":  # Video
            options = " tracks "
            options = options + export_all_videos(file)
        elif action == "6":  # Audio
            options = " tracks "
            options = options + export_all_audios(file)
        elif action == "7":  # Chapters
            options = options + export_chapters(file)
        if default_folder_path == "":
            command = "mkvextract \"" + file + "\" " + options
        else:
            command = "mkvextract \"" + default_folder_path + "/" + file + "\" " + options
        # Execute extraction command
        # print(command)  # Debug - prints the mkvextract command line for each mkv file
        proc = subprocess.call(command, shell=True, stdout=subprocess.PIPE)


def main():
    global default_folder_path
    global files
    # Check for command line arguments, and set the default_folder_path appropriately
    if len(sys.argv) > 1:  # If there is a command line argument, check if it is a folder
        if os.path.isdir(sys.argv[1]):  # Valid folder, so set the default_folder_path to it
            default_folder_path = sys.argv[1]
        elif os.path.isdir(os.path.dirname(os.path.abspath(sys.argv[1]))):  # If file path was sent, use folder path from it.
            default_folder_path = os.path.dirname(os.path.abspath(sys.argv[1]))
        else:  # Invalid folder, so set the default_folder_path to where the python file is
            default_folder_path = sys.path[0]
    else:  # No command line argument, so set the default_folder_path to where the python file is
        default_folder_path = sys.path[0]
    # Get all *.mkv files from the 'default_folder_path' location
    for filename in os.listdir(default_folder_path):
        if str(filename[-3:]).lower() == "mkv":
            files.append(filename)
    files = sorted(files)  # Because a sorted list is better
    process_files()


if __name__ == "__main__":
    main()

#!/usr/bin/env python3

'''
desc:
  create cue file for music files in a directory
  the track/performer/title are got from filename

usage:
  python3 cue.py [-a album] [-p performer] [-d directory]

params:
  use current director if no directory provided
  parse directory for album if no album provided
  parse directory or use "various artists" for performer if no performer provided
  parse filename for track or use sequencial

music file formats supported:
  wav/flac/ape/m4a/dsf

following formats supported:(blank between is optional)
  track. performer - title
  track. title -- performer
  track. title
  performer - title
  title -- performer
  title

cue file:
  the name of cue file created is always "cdimage.cue"
  manually rename it if you like
'''

# _*_ coding: utf-8 _*_
# @Date: 2020/12/01

import os
import argparse

CUEFILENAME = 'cdimage.cue'
FILEFORMATS = ['.wav', '.flac', '.ape', '.m4a', '.dsf']


class Cue:
    '''
    main class
    '''

    def __init__(self, album, performer, directory):
        if directory is None or not os.path.isdir(directory):
            directory = os.getcwd()
        self.directory = directory

        _, dirname = os.path.split(self.directory)
        pa = dirname.split('-')

        if album is None:
            if len(pa) > 1:
                self.album = pa[1].strip()
            else:
                self.album = dirname
        else:
            self.album = album

        if performer is None:
            if len(pa) > 1:
                self.performer = pa[0].strip()
            else:
                self.performer = 'various artists'
        else:
            self.performer = performer

        self.track = 0

    def make_cue(self):
        '''
        main method
        '''

        cuefile = os.path.join(self.directory, CUEFILENAME)
        file_handle = open(cuefile, 'w')

        file_handle.write('TITLE "' + self.album + '"\n')
        file_handle.write('PERFORMER "' + self.performer + '"\n')

        files = os.listdir(self.directory)
        files.sort()
        for file_name in files:
            for file_format in FILEFORMATS:
                if file_name.endswith(file_format):
                    self.add_track(file_handle, file_name, self.next_track())
                    break

        file_handle.close()

    @staticmethod
    def add_track(file_handle, file_name, track):
        '''
        use track string from file_name if exist, else from param
        '''
        title = None
        performer = None

        file_handle.write('FILE "' + file_name + '" WAVE\n')

        file_name, _ = os.path.splitext(file_name)
        finfo = file_name.split('.', 1)
        if len(finfo) > 1:
            track1 = finfo[0].strip()
            if track1.isnumeric():
                track = track1
                file_name = finfo[1].strip()

        finfo = file_name.split('--', 1)
        if len(finfo) > 1:
            title = finfo[0].strip()
            performer = finfo[1].strip()
        else:
            finfo = file_name.split('-', 1)
            if len(finfo) > 1:
                performer = finfo[0].strip()
                title = finfo[1].strip()
            else:
                title = file_name

        file_handle.write('  TRACK ' + track + ' AUDIO\n')
        file_handle.write('    TITLE "' + title + '"\n')
        if performer is not None:
            file_handle.write('    PERFORMER "' + performer + '"\n')
        file_handle.write('    INDEX 01 00:00:00\n')

    def next_track(self):
        '''
        get track string in two words
        '''
        self.track += 1
        if self.track < 10:
            return '0' + str(self.track)
        return str(self.track)


PARSER = argparse.ArgumentParser()
PARSER.add_argument('--album', '-a')
PARSER.add_argument('--performer', '-p')
PARSER.add_argument('--directory', '-d')
ARGS = PARSER.parse_args()

if __name__ == '__main__':
    CUE = Cue(ARGS.album, ARGS.performer, ARGS.directory)
    CUE.make_cue()

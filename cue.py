#!/usr/bin/env python3

'''
desc:
  create cue file for music files in a directory
  the index/performer/title are get from filename

usage:
  python3 cue.py [-t title] [-p performer] [directory]

params:
  use directory name as title if no title param
  use "various artists" as performer if no performer param
  use current director if no directory param

music file formats supported:
  wav/flac/ape/m4a/dsf

following formats supported:(blank between is optional)
  index. performer - title
  index. title -- performer
  index. title
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

    def __init__(self, title, performer, directory):
        self.title = title
        self.performer = performer
        self.directory = os.path.abspath(os.path.join(os.getcwd(), directory))
        self.track = 0

    def make_cue(self):
        '''
        main method
        '''
        _, dirname = os.path.split(self.directory)
        if self.title is None:
            self.title = dirname

        cuefile = os.path.join(self.directory, CUEFILENAME)
        file_handle = open(cuefile, 'w')

        file_handle.write('TITLE "' + self.title + '"\n')
        if self.performer:
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
            track = finfo[0].strip()
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
        if performer:
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
PARSER.add_argument('--title', '-t', help='album title')
PARSER.add_argument('--performer', '-p',
                    help='song performer', default='varial artists')
PARSER.add_argument('directory', help='target directory')
ARGS = PARSER.parse_args()

if __name__ == '__main__':
    CUE = Cue(ARGS.title, ARGS.performer, ARGS.directory)
    CUE.make_cue()

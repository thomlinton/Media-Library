#!/usr/bin/env python

from mutagen.id3 import ID3, APIC, ID3NoHeaderError, error
from mutagen.flac import FLAC, Picture
from mutagen.mp3 import MP3, EasyMP3

from deluge.maketorrent import TorrentMetadata

import subprocess
import argparse
import datetime
import shelve
import base64
import shutil
import shlex
import sys
import os

try:
    import readline
except ImportError:
    pass


DEFAULTS = {
    'base_dir': '.',
    'source_dir': 'source',
    'shelve_release_location': 'release_info.shelve',
    'shelve_track_location': 'track_info.shelve',
    'cartridge': "Denon DL-110",
    'tracker': "http://tracker.what.cd:34000/gvs76ndnvk2o6lzf0yt1jr6e5ibr7cbd/announce",

    'data_dir': '/pub/torrents/completed/what.cd/',
    'torrent_dir': '/pub/torrents/upload/',
}



import logging, logging.config
logging.config.dictConfig({
    'version': 1,
    'disable_existing_loggers': True,
    'formatters': {
        'verbose': {
            'format': '%(levelname)s %(asctime)s %(module)s %(process)d %(thread)d %(message)s'
        },
        'simple': {
            'format': '%(levelname)s %(asctime)s %(message)s'
        },
    },
    'handlers': {
        'console':{
            'level':'DEBUG',
            'class':'logging.StreamHandler',
            'formatter': 'simple'
        },
    },
    'loggers': {
        'library': {
            'handlers': ['console'],
            'level': 'INFO',
        },
    }
})
logger = logging.getLogger('library.music.utilities.vinyl')


class SoXExport(object):
    """
    A simple base class to express parameterized audio transforms; specifically,
    format, rate and bit-depth transforms.
    """
    cached_data = None
    id3_apic_types = {
        'front': 3,
        'back': 4,
        'leaflet': 5,
        'media': 6,
    }
    release_information = """
%(additional_information)s

== Signal Path ==

Vinyl rip was performed with the following signal path:

    %(cartridge)s -> Audio Technica ATLP-120 -> Cambridge Audio 640p -> Xonar Essence STX

== Release Information ==

Format, bit-depth and frequency sampling transforms completed using the following SoX command::

     %(sox_command)s

Prepared on %(prepare_date)s.

== Methodology ==

This release was prepared directly from 32bit/96kHz or 32bit/192kHz uncompressed PCM using Audacity and SoX.

Generated formats will depend on the spectrals from rip (e.g., format/nature of the mastering), but will
follow the listing below:

[*] FLAC 24bit (96kHz or 48kHz)
[*] FLAC 16bit (44.1kHz)
[*] MP3 320kpbs

Unless noted otherwise, rips come only from mint records. In general, no post-processing (e.g., de-clicking) 
other than normalization is performed. If an attempt to rip a record finds that it is rife with distracting noise, 
attempts to rip again will be prefered (after tooling about, taking measurements, &c. to ensure the TT is setup 
correctly and, if necessary, clean the disc) over post-processing the signal.

== Conversion Summary ==

%(soxi_headers)s
"""
    spectrogram_dir = 'spectrograms'
    release_filename = 'release.txt'

    ### Options ###
    downsample_quality = 'h'
    bitrate = None
    bitdepth = 16
    dither = 's'
    freq = 44100

    cmd_template = "sox -S %(source_file)s %(bitdepth)s %(output_file)s %(freq)s %(dither)s"
    cmd_bitdepth = "-b %(val)d"
    cmd_freq = "rate -%(quality)s %(val)d"
    cmd_dither = "dither -%(type)s"

    spectrogram = True
    output_dir_template = "%(artist)s - %(album)s - %(file_extension)s %(bitdepth)d|%(freq)s"
    file_extension = ''

    def __init__(self, base_dir, source_dir):
        source_path = os.path.join( base_dir, source_dir )

        self.load_cached_release_info( source_path )
        self.output_dir = self.generate_output_dir()

        # XXX: Make following section more clear?
        logger.info( "Current output directory: %s" % (self.output_dir) )
        if not self.output_dir:
            self.output_dir = raw_input("Output directory is not set. Output directory: " % (output_dir))
        logger.info( "Using output directory: %s" % (self.output_dir) )

        output_path = os.path.join( base_dir, self.output_dir )
        if not os.access( output_path, os.F_OK ):
            logger.info( "Creating %s" % (output_path) )
            os.mkdir( output_path )

        self.job_params = {
            'source_dir':source_path, 
            'output_dir':output_path, 
            'files':[f for f in os.listdir(source_path) if f.endswith('wav')]
        }

    def __del__(self):
        if hasattr(self, 'cached_release_info') and self.cached_release_info:
            self.cached_release_info.close()
        if hasattr(self, 'cached_track_info') and self.cached_track_info:
            self.cached_track_info.close()

    def load_cached_release_info(self, source_dir, shelve_location=DEFAULTS['shelve_release_location']):
        self.cached_release_info = shelve.open(os.path.join(source_dir, shelve_location))
        logger.info( "Loaded release information: %s" % (self.cached_release_info) )

    def load_cached_track_info(self, source_dir, shelve_location=DEFAULTS['shelve_track_location']):
        self.cached_track_info = shelve.open(os.path.join(source_dir, shelve_location))
        logger.info( "Loaded track information: %s" % (self.cached_track_info) )

    def get_command_params(self, **kwargs):
        bitdepth = ''
        if self.bitdepth:
            bitdepth = self.cmd_bitdepth % {'val': self.bitdepth}
        freq = ''
        if self.freq:
            downsample_quality = self.downsample_quality if self.downsample_quality else ''
            freq = self.cmd_freq % {'quality': self.downsample_quality, 'val': self.freq}
        dither = ''
        if self.dither:
            dither = self.cmd_dither % {'type': self.dither}
        return {'bitdepth':bitdepth, 'freq':freq, 'dither':dither}

    def generate_output_dir(self):
        if 'artist' in self.cached_release_info and 'album' in self.cached_release_info:
            return self.output_dir_template % {
                'artist': self.cached_release_info['artist'], 'album': self.cached_release_info['album'],
                'file_extension': self.file_extension.upper(), 'bitdepth': self.bitdepth,
                'freq': self.freq/1000, 'bitrate': self.bitrate,
            }
        return ''

    def write_soxi_info(self, target):
        try:
            return subprocess.check_output(["soxi", target])
        except subprocess.CalledProcessError, e:
            raise e

    def write_spectrogram(self, output_dir, output_file):
        f_base, f_ext = output_file.rsplit('.', 1)
        source_path = os.path.join( output_dir, output_file )
        spec_base = os.path.join( output_dir, self.spectrogram_dir )
        spec_file = "%s.%s" %  (f_base, 'png')
        spec_path = os.path.join( spec_base, spec_file )

        if not os.access( spec_base, os.F_OK ):
            logger.info( "Creating %s" % (spec_base) )
            os.mkdir( spec_base )
            
        if not os.access( spec_path, os.F_OK ):
            logger.info( "Generating spectrogram ..." )
            subprocess.call(["sox", source_path, "-n", "spectrogram", "-o", spec_path])

    def write_release_information(self, source_dir, output_dir, processed):
        soxi_headers = [self.write_soxi_info(os.path.join(output_dir,filename)) for filename in processed]
        if type(soxi_headers) == list:
            soxi_headers = ''.join(soxi_headers)

        cmd_params = self.get_command_params()
        cmd_params.update({'source_file':"[SOURCE FILE]", 'output_file':"[OUTPUT_FILE]"})
        print "CMD_PARAMS: %s" % (cmd_params)
        params = {
            'sox_command': self.cmd_template % cmd_params,
            'soxi_headers': soxi_headers,
        }
        if 'release_information' not in self.cached_release_info:
            cartridge = DEFAULTS['cartridge']
            response = raw_input("Specify cartridge (default: %s): " % (cartridge))
            if response:
                cartridge = response
            additional_information = raw_input("Additional release information: ")
            cached_params = {
                'additional_information': additional_information,
                'cartridge': cartridge,
                'prepare_date': datetime.date.today(), 
            }
            self.cached_release_info['params'] = cached_params
        params.update(self.cached_release_info['params'])
        release_information = self.release_information % params

        release_filename = os.path.join( output_dir, self.release_filename )
        if os.access( release_filename, os.F_OK ):
            logger.info( "Release information exists. Not generating" )
        else:
            with open(release_filename, 'w') as f:
                f.write( self.release_information % params )

    def write_metadata(self, source_dir, output_dir, processed_files):
        files = os.listdir( source_dir )
        images = {}
        for f in files:
            key, ext = f.rsplit('.', 1)
            if ext == 'png':
                images[key.lower()] = f
                shutil.copyfile( os.path.join(source_dir,f), os.path.join(output_dir,f) )
        logger.info( "Found %d images: %s" % (len(images), images) )

        if 'artist' not in self.cached_release_info:
            self.cached_release_info['artist'] = raw_input("Artist: ")
        if 'album' not in self.cached_release_info:
            self.cached_release_info['album'] = raw_input("Album: ")
        if 'year' not in self.cached_release_info:
            self.cached_release_info['year'] = raw_input("Year: ")

        self.load_cached_track_info(source_dir)
        for f in processed_files:
            logger.info( "Tagging %s" % (f) )
            output_path = os.path.join(output_dir, f)
            track, title, ext = f.split('.', 2)

            track_info = {}
            if track in self.cached_track_info:
                track_info = self.cached_track_info[track]

            if 'track' not in track_info:
                answer = raw_input("Track number (default=%s): " % (track))
                track_info['track'] = answer if answer else track
            if 'title' not in track_info:
                answer = raw_input("Track title (default=%s): " % (title))
                track_info['title'] = answer if answer else title

            if track not in self.cached_track_info:
                self.cached_track_info[track] = track_info

            metadata = self.get_metadata_object( output_path )

            metadata['title'] = track_info['title'].strip().decode('utf-8')
            metadata['tracknumber'] = track_info['track']
            metadata['artist'] = self.cached_release_info['artist'].strip().decode('utf-8')
            metadata['album'] = self.cached_release_info['album'].strip().decode('utf-8')
            metadata['date'] = self.cached_release_info['year'].strip()

            self.commit_metadata_object( metadata, output_path )

            for key, image in images.iteritems():
                key_parts  = key.split('-')
                apic_key = key_parts[0]
                desc = key_parts[0]
                if len(key_parts) > 1:
                    desc = key_parts[1]
                    
                with open( os.path.join(output_dir, image), 'rb' ) as image_f:
                    picture = self.get_metadata_image_object()
                    picture.encoding = 3 # utf-8
                    picture.mime = 'image/png'

                    picture.type = 0 # other
                    if apic_key in self.id3_apic_types:
                        picture.type = self.id3_apic_types[apic_key]

                    picture.desc = desc.title()
                    picture.data = image_f.read()
                    self.attach_metadata_image(metadata, picture)

    def get_metadata_object(self, f):
        raise NotImplementedError

    def commit_metadata_object(self, metadata_obj, f):
        metadata_obj.pprint()
        metadata_obj.save()

    def get_metadata_image_object(self):
        raise NotImplementedError

    def attach_metadata_image(self, metadata_obj, image_obj):
        raise NotImplementedError

    def encode_data(self):
        source_dir = self.job_params['source_dir']
        output_dir = self.job_params['output_dir']
        files = self.job_params['files']
        processed = []

        for f in files:
            f_base, f_ext = f.rsplit('.',1)

            source_path = os.path.join(source_dir, f)
            output_file = "%s.%s" % (f_base, self.file_extension)
            output_path = os.path.join(output_dir, output_file)

            logger.info( "Input path %s" % (source_path) )
            logger.info( "Output path %s" % (output_path) )

            if os.access( output_path, os.F_OK ):
                logger.info( "Audio file exists. Not regenerating." )
            else:
                params = self.get_command_params()
                params.update({
                    'source_file': '"%s"' % (source_path),
                    'output_file': '"%s"' % (output_path)
                    })
                logger.info( "CMD: %s" % (self.cmd_template%params) )
                retcode = subprocess.call(
                    shlex.split(self.cmd_template%params)
                )
            if self.spectrogram:
                self.write_spectrogram(output_dir, output_file)
            processed.append( output_file )

        self.write_release_information(source_dir, output_dir, processed)
        self.write_metadata(source_dir, output_dir, processed)

        return output_dir

    def prepare_torrent_file(self, data_path):
        torrent_dir = DEFAULTS['torrent_dir']
        torrent_path = os.path.join(torrent_dir, "%s.torrent" % self.output_dir)

        if os.access( torrent_path, os.F_OK ):
            logger.info( "Torrent file has already been generated" )
        else:
            try:
                t = TorrentMetadata()
                t.private = True
                t.data_path = data_path
                t.trackers = [[ DEFAULTS['tracker'] ]]
                t.save(torrent_path)
            except IOError, e:
                logger.error( str(e) )

        return torrent_path

    def prepare_data_directory(self):
        data_dir = DEFAULTS['data_dir']
        data_path = os.path.join(data_dir, self.output_dir)
        output_dir = self.job_params['output_dir']

        if os.access( data_path, os.F_OK ):
            logger.info( "Data directory has already been moved" )
        else:
            try:
                logger.info( "Moving %s to %s" % (output_dir, data_dir) )
                shutil.move( output_dir, data_dir )
            except IOError, e:
                logger.error( str(e) )

        return data_path

    def export_torrent(self):
        data_path = self.prepare_data_directory()
        torrent_path = self.prepare_torrent_file(data_path)
        logger.info( "Exported torrent: %s" % (torrent_path) )

class SoXFLACExport(SoXExport):
    file_extension = 'flac'
    spectrogram = True

    def get_metadata_object(self, f):
        return FLAC(f)

    def get_metadata_image_object(self):
        return Picture()

    def attach_metadata_image(self, metadata_obj, image_obj):
        metadata_obj.add_picture( image_obj )
        metadata_obj.save()

class SoXMP3Export(SoXExport):
    file_extension = 'mp3'
    spectrogram = True

    cmd_template = "sox -S %(source_file)s %(bitrate)s %(output_file)s %(freq)s %(dither)s"
    cmd_bitrate = "-C %(bitrate)d.01"

    output_dir_template = "%(artist)s - %(album)s - %(file_extension)s %(bitrate)dkbps"

    def get_metadata_object(self, f):
        temp = EasyMP3(f) # utilizes EasyID3
        try:
            temp.add_tags()
        except error:
            logger.info( "Found existing ID3 tag. We should probably just let ID3 tags fuck everyone. That'd be nice." )
        return temp

    def get_metadata_image_object(self):
        return APIC()

    def attach_metadata_image(self, metadata_obj, image_obj):
        temp = MP3(metadata_obj.filename)
        temp.tags.add( image_obj )
        temp.save()

class FLAC_24Bit_Export(SoXFLACExport):
    downsample_quality = 'v'
    bitdepth = 24
    freq = 96000
    dither = None

class FLAC_24Bit_48kHz_Export(FLAC_24Bit_Export):
    freq = 48000

class FLAC_24Bit_44kHz_Export(FLAC_24Bit_Export):
    freq = 44100

class FLAC_16Bit_Export(FLAC_24Bit_Export):
    downsample_quality = 'h'
    bitdepth = 16
    freq = 44100
    dither = 's'

class MP3_320kbps_Export(SoXMP3Export):
    downsample_quality = 'h'
    bitrate = 320
    freq = 44100
    dither = 's'

    def get_command_params(self):
        params = super(MP3_320kbps_Export, self).get_command_params()
        params['bitrate'] = self.cmd_bitrate % {'bitrate':self.bitrate}
        return params

export_types = {
    'flac_24bit': FLAC_24Bit_Export,
    'flac_24bit_48khz': FLAC_24Bit_48kHz_Export,
    'flac_24bit_44khz': FLAC_24Bit_44kHz_Export,
    'flac_16bit': FLAC_16Bit_Export,
    'mp3_320kbps': MP3_320kbps_Export,
}

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description='Process uncompressed audio and transform to 24bit/96kHz and 16bit/44.1kHz.')
    parser.add_argument(
        'base_dir', type=str, default=DEFAULTS['base_dir'], help='The base path (default: "%s")' % (DEFAULTS['base_dir']) )

    parser.add_argument(
        '--source_dir', type=str, dest="source_dir", default=DEFAULTS['source_dir'], help='The source directory (default: "%s").' % (DEFAULTS['source_dir']) )

    parser.add_argument(
        '--encode-data', action="store_true", help='Generate requested formats from source data.')
    # parser.add_argument(
    #     '--write-info', action="store_true", help='Write release information.')
    parser.add_argument(
        '--export-torrent', action="store_true", help='Generate a torrent for the given exports.')

    parser.add_argument(
        '--flac-24bit', action="store_true", help='Turn on 24bit (96kHz) FLAC export.')
    parser.add_argument(
        '--flac-24bit-48khz', action="store_true", help='Turn on 24bit (48kHz) FLAC export.')
    parser.add_argument(
        '--flac-24bit-44khz', action="store_true", help='Turn on 24bit (44.1kHz) FLAC export.')
    parser.add_argument(
        '--flac-16bit', action="store_true", help='Turn on 16bit (44.1kHz) FLAC export.')
    parser.add_argument(
        '--mp3-320kbps', action="store_true", help='Turn on 320kbps MP3 export.')

    args = vars(parser.parse_args())
    base_dir, source_dir = (args['base_dir'], args['source_dir'])
    for export_type, export_cls in export_types.iteritems():
        if export_type not in args or not args[export_type]:
            continue

        logger.info( "Processing mode=%s" % (export_type) )
        obj = export_cls( base_dir, source_dir )
        if args['encode_data']:
            obj.encode_data()
        if args['export_torrent']:
            obj.export_torrent()

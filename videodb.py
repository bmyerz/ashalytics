import os

_basedir = '/root/data/videos'

_videos = ['opendap_hyrax_large_format_RS03ASHS-PN03B-06-CAMHDA301_2016_01_01_CAMHDA301-20160101T000000Z.mp4',
          'opendap_hyrax_large_format_RS03ASHS-PN03B-06-CAMHDA301_2016_01_01_CAMHDA301-20160101T060000Z.mp4',
          'opendap_hyrax_large_format_RS03ASHS-PN03B-06-CAMHDA301_2016_01_01_CAMHDA301-20160101T180000Z.mp4',
          'opendap_hyrax_large_format_RS03ASHS-PN03B-06-CAMHDA301_2016_02_10_CAMHDA301-20160210T180000Z.mp4']
_videos = [os.path.join(_basedir, p) for p in _videos]


def getvideopaths():
    return _videos



from .collector import *

__all__ = [
    'collector', 'LineData', 'OtherAssets',
    'Electrification', 'ELRMileages', 'LineNames', 'LocationIdentifiers', 'LOR', 'TrackDiagrams',
    'Depots', 'Features', 'SignalBoxes', 'Stations', 'Tunnels', 'Viaducts']

__package_name__ = 'pyrcs'
__package_name_alt__ = 'PyRCS'
__version__ = '0.2.12'
__author__ = u'Qian Fu'
__email__ = 'qian.fu@outlook.com'
__description__ = "A web-scraping tool for collecting railway codes used in different UK rail industry systems."

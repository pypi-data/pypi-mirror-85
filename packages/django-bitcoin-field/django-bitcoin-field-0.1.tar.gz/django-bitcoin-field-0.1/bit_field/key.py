"""
Get the right Key from bit.
Will use PrivateKey or PrivateKeyTestnet depending on settings.
If BIT_NETWORK is present:
True will use PrivateKey (Regular Bitcoin Network)
False will use PrivateKeyTestnet (Test Network)
Else if Debug is true will use TestNetwork, else Regular Network
"""
from django.conf import settings

from bit import PrivateKey, PrivateKeyTestnet, wif_to_key


_bit_net = None if not hasattr(settings, 'BIT_NETWORK') else getattr(settings, 'BIT_NETWORK')
if _bit_net is None:
    _bit_net = True if settings.DEBUG else False

Key = PrivateKey if _bit_net else PrivateKeyTestnet


def get_wallet(wif=None):
    if wif is None:
        return Key()
    else:
        return wif_to_key(wif)



# -*- coding: utf-8 -*-
"""
 GBElevation - QGIS Plugin
 *************************
 Copyright (c) 2017 Luke Butler (luke@matrado.ca) - Matrado Limited
 Licence - github.com/lbutler/GBElevation/blob/master/LICENSE
"""


# noinspection PyPep8Naming
def classFactory(iface):  # pylint: disable=invalid-name
    """Load GBElevation class from file GBElevation.

    :param iface: A QGIS interface instance.
    :type iface: QgsInterface
    """
    #
    from .gb_elevation import GBElevation
    return GBElevation(iface)

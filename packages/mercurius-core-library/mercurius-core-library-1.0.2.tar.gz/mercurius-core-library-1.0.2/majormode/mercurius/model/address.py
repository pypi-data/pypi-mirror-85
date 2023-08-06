# Copyright (C) 2019 Majormode.  All rights reserved.
#
# Permission is hereby granted, free of charge, to any person obtaining
# a copy of this software and associated documentation files (the
# "Software"), to deal in the Software without restriction, including
# without limitation the rights to use, copy, modify, merge, publish,
# distribute, sublicense, and/or sell copies of the Software, and to
# permit persons to whom the Software is furnished to do so, subject to
# the following conditions:
#
# The above copyright notice and this permission notice shall be
# included in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
# MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
# IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY
# CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT,
# TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE
# SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

from majormode.perseus.model.enum import Enum
from majormode.perseus.model.locale import DEFAULT_LOCALE
from majormode.perseus.model.locale import Locale
from majormode.perseus.utils import cast

from majormode.mercurius.constant.place import AddressComponentName


class Address:
    """
    Represent the address information of a place.
    """
    def __init__(self, components, locale=None):
        """
        Build a new instance `Address`.


        :param components: A dictionary of address components where the key
            corresponds to the type `AddressComponentName` of an address
            component.

        :param locale: An object `Locale` representing the language which the
            address information is written in.  By default, English.
        """
        if not isinstance(components, dict):
            raise TypeError("argument 'components' MUST be a dictionary")

        if not isinstance(locale, Locale):
            raise TypeError("argument 'locale' MUST be an object 'Locale'")

        self.__components = dict([
            (name if isinstance(name, Enum)
                else cast.string_to_enum(name, AddressComponentName),
             value)
            for name, value in components.items()])

        self.__locale = locale or DEFAULT_LOCALE

    @property
    def components(self):
        return self.__components.copy()

    @property
    def locale(self):
        return self.__locale

# -*- coding: utf-8 -*-
##############################################################################
#
# Copyright (C) Stephane Wirtel
# Copyright (C) 2011 Nicolas Vanhoren
# Copyright (C) 2011 OpenERP s.a. (<http://openerp.com>)
# Copyright (C) 2018 Odoo s.a. (<http://odoo.com>).
# Copyright (C) 2025 Jimmy McCann
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#
# 1. Redistributions of source code must retain the above copyright notice, this
# list of conditions and the following disclaimer.
# 2. Redistributions in binary form must reproduce the above copyright notice,
# this list of conditions and the following disclaimer in the documentation
# and/or other materials provided with the distribution.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND
# ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
# DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT OWNER OR CONTRIBUTORS BE LIABLE FOR
# ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
# (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
# LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND
# ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
# (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
# SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
#
##############################################################################

from typing import Optional
from xmlrpc.client import SafeTransport

from .xml_rpc import XmlRpcConnector


class XmlRpcsConnector(XmlRpcConnector):
    """
    A type of connector that uses the secured XMLRPC protocol.
    """

    PROTOCOL = "xmlrpcs"

    def __init__(
        self,
        hostname: str,
        port=8069,
        version: Optional[str] = "2",
        transport: Optional[SafeTransport] = None,
    ):
        super(XmlRpcsConnector, self).__init__(hostname, port, version, transport)
        self.url = (
            "https://%s:%d/xmlrpc" % (hostname, port)
            if version is None
            else "https://%s:%d/xmlrpc/%s" % (hostname, port, version)
        )

# -*- coding: utf-8 -*-

from openerp import models, fields, api
import logging
logger = logging.getLogger(__name__)
import urllib
from werkzeug.wrappers import Response


from openerp import http, SUPERUSER_ID
from openerp.http import request



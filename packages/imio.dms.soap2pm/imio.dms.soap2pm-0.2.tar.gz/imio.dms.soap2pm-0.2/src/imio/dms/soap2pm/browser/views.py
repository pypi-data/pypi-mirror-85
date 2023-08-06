# -*- coding: utf-8 -*-

import base64

from Products.CMFPlone.utils import safe_unicode
from Products.Five import BrowserView
from Products.CMFCore.utils import getToolByName


def object_link(obj, view='', title=''):
    href = view and "%s/%s" % (obj.absolute_url(), view) or obj.absolute_url()
    tit = title and safe_unicode(title) or safe_unicode(obj.Title())
    return u'<a href="%s">%s</a>' % (href, tit)


class IncomingMailSoapClientView(BrowserView):
    """ Adapts an incomingmail to prepare data to exchange within imio.pm.wsclient """

    def get_main_files(self):
        pc = getToolByName(self.context, 'portal_catalog')
        res = []
        for brain in pc(portal_type='dmsmainfile', path='/'.join(self.context.getPhysicalPath())):
            obj = brain.getObject()
            res.append({'title': obj.title.encode('utf8'),
                        'filename': obj.file.filename.encode('utf8'),
                        'file': base64.b64encode(obj.file.data)})
        return res

    def detailed_description(self):
        """ Return a link to current object """
        return u"<p>Fiche courrier liée: %s</p>" % object_link(self.context)

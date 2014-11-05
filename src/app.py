#encoding=utf-8
from __future__ import absolute_import
from __future__ import division
from __future__ import unicode_literals

from flask import Flask
from flask import render_template
from flask import request
from time import time

import datetime
import pytz
import locale

#from wsgiref.handlers import CGIHandler

from cgi import escape
#import urlparse
#from mako.template import Template
#from mako.lookup import TemplateLookup

import os
import oursql

app = Flask(__name__)

for loc in ['no_NO', 'nb_NO.utf8']:
    try:
        locale.setlocale(locale.LC_ALL, loc.encode('utf-8'))
    except locale.Error:
        pass

events = {
    0: {
        'name': u'Åremålsvalg 4. pulje 2012',
        'url': '//no.wikipedia.org/wiki/Wikipedia:Administratorer/kandidater/2012-11-15',
        'reqs': [
            ['edits_total', 200],
            ['edits_between', 20120914220000, 20121114230000, 30],
            ['registration_before', 20120914230000],
            ['has_not_role', 'bot']
        ],
        'extra_reqs': [
            u'brukeren ikke har vært blokkert i mer enn to dager i perioden fra og med 14. september til 15. november 2012 (<a href="//no.wikipedia.org/w/index.php?title=Spesial%3ALogg&type=block&user=&page=Bruker%3A{USER}">sjekk blokklogg</a>)'
        ]
    },
    1: {
        'name': u'Åremålsvalg 1. pulje 2013',
        'url': '//no.wikipedia.org/wiki/Wikipedia:Administratorer/kandidater/2013-05-15',
        'reqs': [
            ['edits_total', 200],
            ['edits_between', 20130314230000, 20130514220000, 30],
            ['registration_before', 20130314230000],
            ['has_not_role', 'bot']
        ],
        'extra_reqs': [
            u'brukeren ikke har vært blokkert i mer enn to dager i perioden fra og med 15. mars til 15. mai 2013 (<a href="//no.wikipedia.org/w/index.php?title=Spesial%3ALogg&type=block&user=&page=Bruker%3A{USER}">sjekk blokklogg</a>)'
        ]
    },
    2: {
        'name': u'Åremålsvalg 2. pulje 2013',
        'url': '//no.wikipedia.org/wiki/Wikipedia:Administratorer/kandidater/2013-11-15',
        'reqs': [
            ['edits_total', 200],
            ['edits_between', 20130914220000, 20131114230000, 30],
            ['registration_before', 20130914220000],
            ['has_not_role', 'bot']
        ],
        'extra_reqs': [
            u'brukeren ikke har vært blokkert i mer enn to dager i perioden fra og med 15. september til 15. november 2013 (<a href="//no.wikipedia.org/w/index.php?title=Spesial%3ALogg&type=block&user=&page=Bruker%3A{USER}">sjekk blokklogg</a>)'
        ]
    },
    3: {
        'name': u'Åremålsvalg 3. pulje 2014',
        'url': '//no.wikipedia.org/wiki/Wikipedia:Administratorer/kandidater/2014-05-15',
        'reqs': [
            ['edits_total', 200],
            ['edits_between', 20140314230000, 20140514220000, 30],
            ['registration_before', 20140314230000],
            ['has_not_role', 'bot']
        ],
        'extra_reqs': [
            u'brukeren ikke har vært blokkert i mer enn to dager i perioden fra og med 15. mars til 15. mai 2014 (<a href="//no.wikipedia.org/w/index.php?title=Spesial%3ALogg&type=block&user=&page=Bruker%3A{USER}">sjekk blokklogg</a>)'
        ]
    },
    4: {
        'name': u'Åremålsvalg 4. pulje 2014',
        'url': '//no.wikipedia.org/wiki/Wikipedia:Administratorer/kandidater/2014-11-15',
        'reqs': [
            ['edits_total', 200],
            ['edits_between', 20140914220000, 20141114230000, 30],
            ['registration_before', 20140914220000],
            ['has_not_role', 'bot']
        ],
        'extra_reqs': [
            u'brukeren ikke har vært blokkert i mer enn to dager i perioden fra og med 15. september til 15. november 2014 (<a href="//no.wikipedia.org/w/index.php?title=Spesial%3ALogg&type=block&user=&page=Bruker%3A{USER}">sjekk blokklogg</a>)'
        ]
    },
    5: {
        'name': u'Åremålsvalg 1. pulje 2015',
        'url': '//no.wikipedia.org/wiki/Wikipedia:Administratorer/kandidater/2015-05-15',
        'reqs': [
            ['edits_total', 200],
            ['edits_between', 20150314230000, 20150514220000, 30],
            ['registration_before', 20150314230000],
            ['has_not_role', 'bot']
        ],
        'extra_reqs': [
            u'brukeren ikke har vært blokkert i mer enn to dager i perioden fra og med 15. mars til 15. mai 2015 (<a href="//no.wikipedia.org/w/index.php?title=Spesial%3ALogg&type=block&user=&page=Bruker%3A{USER}">sjekk blokklogg</a>)'
        ]
    }
}


@app.route('/')
def show_index():

    #d = urlparse.parse_qs(environ['QUERY_STRING'])
    #if d.get('show', [''])[0] == 'source':
    #    start_response('200 OK', [('Content-Type', 'text/plain')])
    #    f = open('index.fcgi', 'r')
    #    c = f.read()
    #    f.close()
    #    yield c
    #    return

    #start_response('200 OK', [('Content-Type', 'text/html')])
    uname = request.args.get('user', '')
    if len(uname) > 1:
        uname = uname[0].upper() + uname[1:]
    event = int(request.args.get('event', 4))
    event = events[event]

    osl = pytz.timezone('Europe/Oslo')

    if uname == '':
        html = ''
    else:

        db = oursql.connect(db='nowiki_p',
                            host='nowiki.labsdb',
                            read_default_file=os.path.expanduser('~/replica.my.cnf'),
                            charset=None,
                            use_unicode=False
                            )
        cur = db.cursor()
        html = '<h2>Analyse</h2>\n'
        html += '<ul class="analysis">\n'
        eligible = True
        cur.execute('SELECT user_id, user_registration, user_editcount FROM user WHERE user_name=? LIMIT 1', [uname.encode('utf-8')])
        user_row = cur.fetchall()
        if len(user_row) != 1:
            html += u'<li class="fail">er ikke registrert (sjekk at brukernavnet er skrevet riktig)</li>\n'
            eligible = False
        else:
            user_row = user_row[0]
            user_id = int(user_row[0])
            for req in event['reqs']:

                if req[0] == 'edits_between':
                    cur.execute('SELECT COUNT(rev_id) FROM revision WHERE rev_user_text=? AND rev_timestamp BETWEEN ? AND ?', [uname.encode('utf-8'), req[1], req[2]])
                    usum = int(cur.fetchone()[0])
                    d0 = pytz.utc.localize(datetime.datetime.strptime(str(req[1]), '%Y%m%d%H%M%S')).astimezone(osl).strftime('%d. %B %Y')
                    d1 = pytz.utc.localize(datetime.datetime.strptime(str(req[2]), '%Y%m%d%H%M%S')).astimezone(osl).strftime('%d. %B %Y')
                    if usum >= req[3]:
                        html += u'<li class="ok">har gjort minst %s redigeringer i perioden fra og med %s til %s (har gjort %s redigeringer)</li>\n' % (req[3], d0, d1, usum)
                    else:
                        html += u'<li class="fail">har gjort færre enn %s redigeringer i perioden fra og med %s til %s (har gjort %s redigeringer)</li>\n' % (req[3], d0, d1, usum)
                        eligible = False

                elif req[0] == 'edits_total':
                    if user_row[2] >= req[1]:
                        html += u'<li class="ok">har gjort minst %d redigeringer totalt (har gjort %d redigeringer)</li>\n' % (req[1], user_row[2])
                    else:
                        html += u'<li class="fail">har gjort mindre enn %d redigeringer totalt (har gjort %d redigeringer)</li>\n' % (req[1], user_row[2])
                        eligible = False

                elif req[0] == 'registration_before':
                    d0 = pytz.utc.localize(datetime.datetime.strptime(str(req[1]), '%Y%m%d%H%M%S')).astimezone(osl).strftime('%d. %B %Y')
                    if user_row[1] == None:
                        # før 2005/2006 en gang
                        html += u'<li class="ok">registrerte seg før %s</li>\n' % (d0) 
                    else:
                        regdate = int(user_row[1])
                        d1 = pytz.utc.localize(datetime.datetime.strptime(str(user_row[1]), '%Y%m%d%H%M%S')).astimezone(osl).strftime('%e. %B %Y')
                        if regdate < req[1]:
                            html += u'<li class="ok">registrerte seg før %s (registrerte seg %s)</li>\n' % (d0, d1)
                        else:
                            html += u'<li class="fail">registrerte seg etter %s (registrerte seg %s)</li>\n' % (d0, d1)
                            eligible = False

                elif req[0] == 'has_not_role':
                    cur.execute('SELECT COUNT(ug_user) FROM user_groups WHERE ug_user=? AND ug_group=?', (user_id, req[1]))
                    usum = int(cur.fetchall()[0][0])
                    if usum == 0:
                        html += u'<li class="ok">er ikke en %s</li>\n' % req[1]
                    else:
                        html += u'<li class="fail">er en %s</li>\n' % req[1]
                        eligible = False
                
        html += '</ul>'
        html += '<h2>Resultat</h2>'

        if eligible:
            extra = '.'
            if 'extra_reqs' in event and len(event['extra_reqs']) > 0:
                extra = ', forutsatt at <ul>\n'
                for ext in event['extra_reqs']:
                    extra += u'<li>%s</li>\n' % ext.replace('{USER}', uname)
                extra += '</ul>'
            html += '<div id="result" class="success">%s er stemmeberettiget ved <a title="%s" href="%s">%s</a>%s</div>' % (uname, event['name'], event['url'], event['name'], extra)
        else:
            html += '<div id="result" class="fail">%s er ikke stemmeberettiget ved <a title="%s" href="%s">%s</a>. </div>' % (uname, event['name'], event['url'], event['name'])

    return render_template('main.html', results=html, uname=uname, event_name=event['name'])

if __name__ == "__main__":
    app.run()

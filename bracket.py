from random import randint, sample
import csv
import logics as lo
from flask import Blueprint, url_for, g, redirect, render_template

bp = Blueprint('bracket', __name__, url_prefix='/')

def get_state():
    if 'state' not in g:
        g.state = lo.load_competitors()
    return g.state

@bp.route('/')
def hello():
    return "Welcome to the thunderdome"

@bp.route('/standings')
def standings():
    comps = get_state()

#    htext = "<html>\n<head> <title>Current Standings</title> </head>\n<body>"
#    ftext = "</body>\n</html>"
#
#    st = "Scores<br>--------<br>"
#    for i in comps:
#        s = ",".join([str(x) for x in i.scores])
#        url = url_for('bracket.view_comp', competitor=i.name)
#        st = st + f"<a href={url}>{i.name:>10}</a>: {i.total:>5} ({s})<br>"
#    reurl = url_for('bracket.rematch')
#    st += f"<br><form action='{reurl}'><button type='submit'>Go Again?</button></form>"
#
#    return htext+st+ftext
    return render_template('bracket/standings.html')

@bp.route('/rematch')
def rematch():
    comps = get_state()
    brackets = lo.new_bracket(comps)
    for i in brackets:
        lo.randBracketWin(i)
    for i in comps:
        i.totalScore()
    lo.sortComps(comps)
    lo.saveComps(comps)
    return redirect(url_for('bracket.standings')) 

@bp.route('/<competitor>')
def view_comp(competitor):
    comps = get_state()
    for i in comps:
        if i.name == competitor:
            s = ",".join([str(x) for x in i.scores])
            return f"{i.name:>10}: {i.total:>5} ({s})"

def get_blueprint():
    return bp

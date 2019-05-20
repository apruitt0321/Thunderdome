import logics as lo
from flask import Blueprint, url_for, g, request, redirect, render_template

bp = Blueprint('bracket', __name__, url_prefix='/')

def get_blueprint():
    return bp

def get_state():
    if 'state' not in g:
        g.state = lo.load_competitors()
    return g.state

@bp.route('/')
def home():
    return render_template('bracket/home.html')

@bp.route('/new', methods=("GET", "POST"))
def new_comp():
    if request.method == "POST":
        comp1 = request.form['competitor1']
        return redirect(url_for('bracket.standings'))
    return render_template('bracket/new.html')

@bp.route('/standings')
def standings():
    comps = get_state()
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


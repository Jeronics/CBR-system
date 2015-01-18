from flask import Flask, render_template, request, session

from cbr.core import main as core_main
from cbr.core.wrapper import Match

app = Flask(__name__)
app.secret_key = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RTasdf7808012342'


def get_teams():
    if 'teams' not in session:
        session['teams'] = core_main.get_matches().get_all_teams()
    return session['teams']

@app.route('/', methods=['GET', 'POST'])
def index():
    teams = get_teams()
    team_form = [("Home Team", "home_team"), ("Away Team", "away_team")]
    providers = [(Match.provider_names[idx],
                  (("1", Match.home_odds_params[idx]),
                  ("X", Match.draw_odds_params[idx]),
                  ("2", Match.away_odds_params[idx])))
                 for idx, _ in enumerate(Match.home_odds_params)]

    #in case a form has been submitted
    if request.method == 'POST':
        output = core_main.run([None, "Real Madrid", "Barcelona"])
    else:
        output = None

    return render_template('index.html', teams=teams, team_form=team_form, providers=providers, prediction=output)


if __name__ == '__main__':
    app.run(debug=True)
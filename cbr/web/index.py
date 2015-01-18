from flask import Flask
from flask import render_template

from cbr.core import main as core_main
from cbr.core.wrapper import Match


app = Flask(__name__)

@app.route('/')
def index():
    output = core_main.run([None, "Real Madrid", "Barcelona"])
    teams = core_main.get_matches().get_all_teams()
    team_form = [("Home Team", "home_team"), ("Away Team", "away_team")]
    providers = [(Match.provider_names[idx],
                  (("1", Match.home_odds_params[idx]),
                  ("X", Match.draw_odds_params[idx]),
                  ("2", Match.away_odds_params[idx])))
                 for idx, _ in enumerate(Match.home_odds_params)]
    if prediction
    return render_template('index.html', teams=teams, team_form=team_form, providers=providers, prediction=output)


if __name__ == '__main__':
    app.run(debug=True)
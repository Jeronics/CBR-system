from flask import Flask, render_template, request, session

from cbr.core import main as core_main
from cbr.core.wrapper import MatchesCaseBase, Match

app = Flask(__name__)
app.secret_key = 'A0Zr98sdfgsdj/3yX R~XHH!jmN]LWX/,?RTasdf7808012342'


def get_teams():
    if 'teams' not in session:
        session['teams'] = core_main.get_matches().get_all_teams()
    return session['teams']

home_team_form = "home_team"
away_team_form = "away_team"
odd_name_triples = [(Match.home_odds_params[idx], Match.draw_odds_params[idx], Match.away_odds_params[idx])
                    for idx, _ in enumerate(Match.home_odds_params)]

@app.route('/', methods=['GET', 'POST'])
def index():
    teams = get_teams()
    team_form = [("Home Team", home_team_form), ("Away Team", away_team_form)]
    providers = [(Match.provider_names[idx],
                  (("1", odd_triple[0]),
                  ("X", odd_triple[1]),
                  ("2", odd_triple[2]))) for idx, odd_triple in enumerate(odd_name_triples)]

    input_match = None
    prediction = None
    #in case a form has been submitted
    if request.method == 'POST':
        team1 = request.form[home_team_form]
        team2 = request.form[away_team_form]
        odds = {}
        for odd_triple in odd_name_triples:
            for odd_key in odd_triple:
                if odd_key in request.form:
                    value = request.form[odd_key]
                    if value:
                        odds[odd_key] = value
        input_match = core_main.gen_input_match(team1, team2, odds)
        prediction = core_main.run(input_match)
        prediction = Match.map_to_human_prediction(prediction)

    return render_template('index.html', teams=teams, team_form=team_form, providers=providers, input_match=input_match, prediction=prediction)


if __name__ == '__main__':
    app.run(debug=True)
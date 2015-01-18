import operator
import pandas as pd
import glob
import random
import numpy as np
import jsonpickle
from joblib import Parallel, delayed

from cbr.core import utils as ut
from cbr.core.internal_repr.model import CBRclass, Case, CaseBase


class Match(Case):
    # these need to be static for the web access
    provider_names = ["Bet365", "Blue Square", "Bet&Win", "Gamebookers", "Interwetten",
                      "Ladbrokes", "Pinnacle", "Sporting", "Sportingbet", "Stan James",
                      "Stanleybet", "VC Bet", "William Hill" ]
    home_odds_params = ['B365H', 'BSH', 'BWH', 'GBH', 'IWH', 'LBH', 'PSH', 'SOH', 'SBH', 'SJH', 'SYH', 'VCH', 'WHH']
    draw_odds_params = ['B365D', 'BSD', 'BWD', 'GBD', 'IWD', 'LBD', 'PSD', 'SOD', 'SBD', 'SJD', 'SYD', 'VCD', 'WHD']
    away_odds_params = ['B365A', 'BSA', 'BWA', 'GBA', 'IWA', 'LBA', 'PSA', 'SOA', 'SBA', 'SJA', 'SYA', 'VCA', 'WHA']

    # odd_params = [ 'B365H', 'B365D', 'B365A', 'BSH', 'BSD', 'BSA', 'BWH', 'BWD', 'BWA', 'GBH', 'GBD', 'GBA', 'IWH', 'IWD',
    # 'IWA', 'LBH', 'LBD', 'LBA', 'PSH', 'PSD', 'PSA', 'SOH', 'SOD', 'SOA', 'SBH', 'SBD', 'SBA',
    #                 'SJH', 'SJD', 'SJA', 'SYH', 'SYD', 'SYA', 'VCH', 'VCD', 'VCA', 'WHH', 'WHD', 'WHA']

    # params_names = ['Div', 'FTHG', 'FTAG', 'HTHG', 'HTAG', 'HTR', 'Attendance', 'Referee', 'HS', 'AS', 'HST', 'AST',
    #                 'HHW', 'AHW', 'HC', 'AC', 'HF', 'AF', 'HO', 'AO', 'HY', 'AY', 'HR', 'AR', 'HBP', 'ABP', 'B365H',
    #                 'B365D', 'B365A', 'BSH', 'BSD', 'BSA', 'BWH', 'BWD', 'BWA', 'GBH', 'GBD', 'GBA', 'IWH', 'IWD',
    #                 'IWA', 'LBH', 'LBD', 'LBA', 'PSH', 'PSD', 'PSA', 'SOH', 'SOD', 'SOA', 'SBH', 'SBD', 'SBA',
    #                 'SJH', 'SJD', 'SJA', 'SYH', 'SYD', 'SYA', 'VCH', 'VCD', 'VCA', 'WHH', 'WHD', 'WHA', 'Bb1X2',
    #                 'BbMxH', 'BbAvH', 'BbMxD', 'BbAvD', 'BbMxA', 'BbAvA', 'BbOU', 'BbMx>2.5', 'BbAv>2.5',
    #                 'BbMx<2.5', 'BbAv<2.5', 'GB>2.5', 'GB<2.5', 'B365>2.5', 'B365<2.5', 'BbAH', 'BbAHh', 'BbMxAHH',
    #                 'BbAvAHH', 'BbMxAHA', 'BbAvAHA', 'GBAHH', 'GBAHA', 'GBAH', 'LBAHH', 'LBAHA', 'LBAH', 'B365AHH',
    #                 'B365AHA', 'B365AH']

    def __init__(self, params):
        """
        :type  params: dict
        :param params: parameters of the match:
                        - Date = Date of the match
                        - Div = Division of the match
                        - HomeTeam = Home Team
                        - AwayTeam = Away Team
                        - FTHG = Full Time Home Goals
                        - FTAG = Full Time Away Goals
                        - FTR = Full Time Result
                        - HTHG = Half Time Home Goals
                        - HTAG = Half Time Away Goals
                        - HTR = Half Time Result
                        - Attendance = Crowd Attendance
                        - Referee = Match Referee
                        - HS = Home Team Shots
                        - AS = Away Team Shots
                        - HST = Home Team Shots on Target
                        - AST = Away Team Shots on Target
                        - HHW = Home Team Hit Woodwork
                        - AHW = Away Team Hit Woodwork
                        - HC = Home Team Corners
                        - AC = Away Team Corners
                        - HF = Home Team Fouls Committed
                        - AF = Away Team Fouls Committed
                        - HO = Home Team Offsides
                        - AO = Away Team Offsides
                        - HY = Home Team Yellow Cards
                        - AY = Away Team Yellow Cards
                        - HR = Home Team Red Cards
                        - AR = Away Team Red Cards
                        - HBP = Home Team Bookings Points (10 = yellow, 25 = red)
                        - ABP = Away Team Bookings Points (10 = yellow, 25 = red)

                        - B365H = Bet365 home win odds
                        - B365D = Bet365 draw odds
                        - B365A = Bet365 away win odds
                        - BSH = Blue Square home win odds
                        - BSD = Blue Square draw odds
                        - BSA = Blue Square away win odds
                        - BWH = Bet&Win home win odds
                        - BWD = Bet&Win draw odds
                        - BWA = Bet&Win away win odds
                        - GBH = Gamebookers home win odds
                        - GBD = Gamebookers draw odds
                        - GBA = Gamebookers away win odds
                        - IWH = Interwetten home win odds
                        - IWD = Interwetten draw odds
                        - IWA = Interwetten away win odds
                        - LBH = Ladbrokes home win odds
                        - LBD = Ladbrokes draw odds
                        - LBA = Ladbrokes away win odds
                        - PSH = Pinnacle Sports home win odds
                        - PSD = Pinnacle Sports draw odds
                        - PSA = Pinnacle Sports away win odds
                        - SOH = Sporting Odds home win odds
                        - SOD = Sporting Odds draw odds
                        - SOA = Sporting Odds away win odds
                        - SBH = Sportingbet home win odds
                        - SBD = Sportingbet draw odds
                        - SBA = Sportingbet away win odds
                        - SJH = Stan James home win odds
                        - SJD = Stan James draw odds
                        - SJA = Stan James away win odds
                        - SYH = Stanleybet home win odds
                        - SYD = Stanleybet draw odds
                        - SYA = Stanleybet away win odds
                        - VCH = VC Bet home win odds
                        - VCD = VC Bet draw odds
                        - VCA = VC Bet away win odds
                        - WHH = William Hill home win odds
                        - WHD = William Hill draw odds
                        - WHA = William Hill away win odds

                        - Bb1X2 = Number of BetBrain bookmakers used to calculate match odds averages and maximums
                        - BbMxH = Betbrain maximum home win odds
                        - BbAvH = Betbrain average home win odds
                        - BbMxD = Betbrain maximum draw odds
                        - BbAvD = Betbrain average draw win odds
                        - BbMxA = Betbrain maximum away win odds
                        - BbAvA = Betbrain average away win odds

                        - BbOU = Number of BetBrain bookmakers used to calculate over/under 2.5 goals (total goals) averages and maximums
                        - BbMx>2.5 = Betbrain maximum over 2.5 goals
                        - BbAv>2.5 = Betbrain average over 2.5 goals
                        - BbMx<2.5 = Betbrain maximum under 2.5 goals
                        - BbAv<2.5 = Betbrain average under 2.5 goals

                        - GB>2.5 = Gamebookers over 2.5 goals
                        - GB<2.5 = Gamebookers under 2.5 goals
                        - B365>2.5 = Bet365 over 2.5 goals
                        - B365<2.5 = Bet365 under 2.5 goals

                        - BbAH = Number of BetBrain bookmakers used to Asian handicap averages and maximums
                        - BbAHh = Betbrain size of handicap (home team)
                        - BbMxAHH = Betbrain maximum Asian handicap home team odds
                        - BbAvAHH = Betbrain average Asian handicap home team odds
                        - BbMxAHA = Betbrain maximum Asian handicap away team odds
                        - BbAvAHA = Betbrain average Asian handicap away team odds

                        - GBAHH = Gamebookers Asian handicap home team odds
                        - GBAHA = Gamebookers Asian handicap away team odds
                        - GBAH = Gamebookers size of handicap (home team)
                        - LBAHH = Ladbrokes Asian handicap home team odds
                        - LBAHA = Ladbrokes Asian handicap away team odds
                        - LBAH = Ladbrokes size of handicap (home team)
                        - B365AHH = Bet365 Asian handicap home team odds
                        - B365AHA = Bet365 Asian handicap away team odds
                        - B365AH = Bet365 size of handicap (home team)
        """
        date = params['Date']
        home = params['HomeTeam']
        away = params['AwayTeam']
        name = date + home + away
        problem = CBRclass(name=name)
        Case.__init__(self, name, problem)

        home_odd = 0
        draw_odd = 0
        away_odd = 0
        counter = 0
        for p in Match.home_odds_params:
            if p in params:
                if params[p] is str or params[p] != params[p]:
                    continue
                else:
                    home_odd = home_odd + float(params[p])
                    counter = counter + 1
        if counter != 0:
            home_odd = home_odd / counter

        counter = 0

        for p in Match.draw_odds_params:
            if p in params:
                if params[p] is str or params[p] != params[p]:
                    continue
                else:
                    draw_odd = draw_odd + float(params[p])
                    counter = counter + 1
        if counter != 0:
            draw_odd = draw_odd / counter

        counter = 0

        for p in Match.away_odds_params:

            if p in params:
                if params[p] is str or params[p] != params[p]:
                    continue
                else:
                    away_odd = away_odd + float(params[p])
                    counter = counter + 1
        if counter != 0:
            away_odd = away_odd / counter

        self.problem.add_feature(name='date', values=ut.date_to_python_date(date))
        self.problem.add_class('home', home)
        self.problem.add_class('away', away)
        self.set_solution(params['FTR'])
        self.problem.add_feature(name='home_odd', values=home_odd)
        self.problem.add_feature(name='draw_odd', values=draw_odd)
        self.problem.add_feature(name='away_odd', values=away_odd)


    def __str__(self):
        return str(self.get_date()) + ': ' + self.get_home() + ' vs ' + self.get_away() + ' --> ' + self.get_solution()

    def get_date(self):
        """
        Returns the date the match was played.
        """
        return self.problem.get_feature('date')

    def get_home(self):
        """
        Returns the name of the home team in the match.
        """
        return str(self.problem.get_class('home').name)

    def get_away(self):
        """
        Returns the name of the away team in the match.
        """
        return str(self.problem.get_class('away').name)


    def get_home_odd(self):
        """
        Returns the odd of the home team in the match.
        """
        return str(self.problem.get_feature('home_odd'))

    def get_draw_odd(self):
        """
        Returns the odd of the draw in the match.
        """
        return str(self.problem.get_feature('draw_odd'))

    def get_away_odd(self):
        """
        Returns the odd of the away team in the match.
        """
        return str(self.problem.get_feature('away_odd'))


    def get_params(self):
        """
        Returns a dictionary with the parameters of the match.
        """
        return self.problem.get_feature('params')

    def get_home_or_away(self, team):
        """
        Returns 'home' or 'away' depending on the position the team is playing in the match.

        :type  team: str
        :param team: Team in the match

        :return: 'home' or 'away'
        """
        return 'home' if self.problem.get_class('home') == team else 'away'

    def get_team(self, where):
        """
        Returns the team playing in the position 'where'.

        :type  where: str
        :param where: 'home' or 'away'

        :return: Team's name playing 'where'
        """
        return self.get_home() if where == 'home' else self.get_away()


class MatchesCaseBase(CaseBase):
    def add_match(self, match):
        """
        Add an already created match to the MatchCaseBase.
        """
        self.add_case(match)

    def create_match(self, params):
        """
        Creates a match calling the 'create_match' method of the class Match.
        And adds the match to the MatchesCaseBase.
        """
        m = Match(params)
        self.add_case(m)
        return m

    def get_all_teams(self):
        case_values = self.cases.values()
        teams = [cv.get_home() for cv in case_values] + [cv.get_away() for cv in case_values]
        teams = sorted(list(set(teams)))
        return teams

    def get_case_team(self, team, where, **kwargs):
        """
        Get the matches a team has played.

        :type  team: str
        :param team: Name of the team

        :type  where: str
        :param where: 'home' or 'away'

        :param kwargs: num: Number of matches to retrieve,
                       date: Time from where to retrieve matches
        :return:
        """
        all_matches = {i.name: i for i in self.cases.values() if i.get_team(where) == team}
        if 'num' in kwargs and 'date' in kwargs:
            sorted_matches = sorted(all_matches.values(), key=operator.methodcaller('get_date'))
            count = 0
            matches = {}
            for m in sorted_matches:
                if m.get_date() < kwargs['date']:
                    count += 1
                    matches[m.name] = m
                    if count >= kwargs['num']:
                        break
            return matches
        else:
            return all_matches

    def get_hist(self, m, n):
        """
        Get the nth recent history of matches of both teams playing in the match.

        :type  m: Match
        :param m: The reference match from where to extract the history.

        :type  n: int
        :param n: Number of matches to be returned.

        :return: Both list of past matches of home and away teams.
                ({home_hist}, {ayaw_hist})
        """
        home = m.get_home()
        away = m.get_away()
        date = m.get_date()
        return (self.get_case_team(home, 'home', **{'date': date, 'num': n}),
                self.get_case_team(away, 'away', **{'date': date, 'num': n}))

    def get_common_matches(self, m, n):
        """
        Get the 'common' matches between two teams, meaning the matches that share
        the same opponent between the home and away teams, i.e. home_team vs team1
        and team1 vs away_team.

        :type  m: Match
        :param m: Match

        :type  n: int
        :param n: maximum number of matches retrieved

        :return: Tuple containing the home common matches and the away common matches.
        """
        home = m.get_home()
        away = m.get_away()
        date = m.get_date()

        home_matches = self.get_case_team(home, 'home', **{'date': date, 'num': n})
        home_opponent = [a.name for a in home_matches.values()]
        away_matches = self.get_case_team(away, 'away', **{'date': date, 'num': n})
        away_opponent = [h.name for h in away_matches.values()]

        return ({m.name: m for m in home_matches.values() if m.get_away().name in away_opponent},
                {m.name: m for m in away_matches.values() if m.get_home().name in home_opponent})


def similarity_function(match1, match2, weighting_method=3):
    """
    Calculate the similarity between the two matches.

    :type match1: Match
    :type match2: Match
    :type weighting_method: int
    :param weighting_method: It allows you to choose between 3 different weighting
                             methods (1: W. method 1, 2: W. method 2, 3: Use Euclidean
                             distance with the betting odds to choose the similar matches)
    :return: Similarity between match1 and match2 (0 - 1)
    """
    if weighting_method == 1:
        # Weighting method 1:
        #
        #   1-. Location
        #         + equality 1
        #         + different 0.5
        #   2-. Data
        #         + For each year * 0.1

        league_years_since_game = ut.diff_in_league_years(match2.get_date(), match1.get_date())
        wYears = float(league_years_since_game) * 0.1

        if match1.get_home() == match2.get_home() and match1.get_away() == match2.get_away():
            similarity = max(0.1, float(1 - wYears))
            return similarity
        if match1.get_home() == match2.get_away() and match1.get_away() == match2.get_home():
            similarity = max(0.1, float(0.5 - wYears))
            return similarity
    if weighting_method == 2:
        # Weighting method 2:
        #
        # 1-. Location
        #       + equality 1
        #       + difference 0.8
        # 2-. Data
        #     + 1 / (1 + passed years)

        league_years_since_game = ut.diff_in_league_years(match2.get_date(), match1.get_date())
        w_years = 1 / float(1 + league_years_since_game)
        if match1.get_home() == match2.get_home() and match1.get_away() == match2.get_away():
            same_local = 1
            sim = w_years * same_local
            return sim
        if match1.get_home() == match2.get_away() and match1.get_away() == match2.get_home():
            same_local = 0.8
            sim = w_years * same_local
            return sim
    if weighting_method == 3:
        # Weighting method 3:
        #   With euclidean distance between the bet houses.
        #
        league_years_since_game = ut.diff_in_league_years(match2.get_date(), match1.get_date())
        w_years = 1 / float(1 + league_years_since_game)

        train = np.array((match1.get_home_odd(), match1.get_draw_odd(), match1.get_away_odd()), np.float)
        test = np.array((match2.get_home_odd(), match2.get_draw_odd(), match2.get_away_odd()), np.float)

        train_norm = np.linalg.norm(train)
        test_norm = np.linalg.norm(test)

        train_normalized = train / train_norm
        test_normalized = test / test_norm

        euclidean_distance = np.linalg.norm(train_normalized - test_normalized)

        sim = 1 / (euclidean_distance * w_years)


    return sim

HOME_TEAM_WINS = "H"
AWAY_TEAM_WINS = "A"
DRAW = "D"


def reuse_matches(actual_case, similar_cases, similarities):

    try:
        win_prob = 0
        draw_prob = 0
        lose_prob = 0
        for idx, similar_case in enumerate(similar_cases):
            # H = Home team wins.
            if str(similar_case.get_solution()) == HOME_TEAM_WINS:
                if str(actual_case.get_home()) == str(similar_case.get_home()):
                    win_prob += 1 * similarities[idx]
                else:
                    lose_prob += 1 * similarities[idx]
            # A = Away team wins.
            elif str(similar_case.get_solution()) == AWAY_TEAM_WINS:
                if str(actual_case.get_away()) == str(similar_case.get_away()):
                    lose_prob += 1 * similarities[idx]
                else:
                    win_prob += 1 * similarities[idx]
            # D = Draw
            elif str(similar_case.get_solution()) == DRAW:
                draw_prob += 1 * similarities[idx]

        total = win_prob + lose_prob + draw_prob

        probabilities = {HOME_TEAM_WINS: win_prob / total, AWAY_TEAM_WINS: lose_prob / total, DRAW: draw_prob / total}
        result = max(probabilities, key=probabilities.get)
    except Exception as e:
        # print e.message
        # print 'no similar cases in the history'
        result = random.choice([HOME_TEAM_WINS, AWAY_TEAM_WINS, DRAW])
    return result


def expert_function(match, predicted_result):
    """
    Check whether the proposed solution is correct, returns 1
    if so and 0 otherwise.

    :type  match: Match
    :param match: Current Case

    :type predicted_result: str
    :param predicted_result: Proposed Result of the match.

    :return: Confidence of the proposed solution being certain.
    """
    if match.get_solution() == predicted_result:
        return [1]
    else:
        return [0]


def read_match_dataset(dataset, mcb):
    """
    Read a csv document and save all the matches (lines) in a MatchesCaseBase class
    and return it.

    :type  mcb: MatchesCaseBase
    :param mcb: Match Case Base where to store the data from the dataset.

    :type  dataset:str
    :param dataset: Name of the file.

    :return: MatchCaseBase
    """
    # using pandas instead of numpy because the csv files are not well-formed and cannot be parsed by numpy
    data = pd.read_csv(dataset, sep=',', header=0)
    for i in data.index:
        # data.irow()[] is deprecated, use data.loc instead
        params = {c: data.loc[i, c] for c in data.columns}
        mcb.create_match(params)


def save_case_base(case_base, filename):
    """
    Save the MatchesCaseBase class into a pickle file.

    :type  case_base: CaseBase
    :param case_base: Object class to save.

    :type  filename: str
    :param filename: name of the file.
    """
    f = open(filename, 'wb')
    json = jsonpickle.encode(case_base)
    f.write(json)
    f.close()


def read_case_base(filename):
    """
    Read a pickle file.

    :type  filename: str
    :param filename: Name of the file to unpickle.

    :return: Return the unpickled object.
    """
    f = open(filename, 'rb')
    matches_base = jsonpickle.decode(f.read())
    f.close()
    return matches_base


def read_from_csv(data):
    """
    :param data:
    :return:
    """
    matches_data = MatchesCaseBase()
    read_match_dataset(data, matches_data)
    return matches_data

if __name__ == '__main__':
    # Create Train Data set
    dataset = [files for files in glob.glob("../data/Train/*.csv")]

    matches_data = MatchesCaseBase()
    skip_dataset_index = 8

    Parallel(n_jobs=8)(delayed(read_match_dataset)(dataset[i], matches_data) for i in range(len(dataset)))

    # save_case_base(matches_data, '../data/Train/train.jpkl')

    # # Create Test Data set
    # test_matches = MatchesCaseBase()
    # test_matches = read_match_dataset('../data/Test/LaLiga2013-14.csv', test_matches)
    # save_case_base(test_matches, '../data/Test/test.jpkl')
    #
    # matches = read_case_base('../data/Test/test.jpkl')
    #
    # print matches.get_case_values()[0].get_home()

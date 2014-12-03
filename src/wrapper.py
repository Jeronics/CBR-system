import glob
import operator
import utils
import pandas as pd
import cPickle as cpi
from internal_repr.model import CBRclass, Case, CaseBase


class Match(Case):
    def __init__(self, params):
        """
        :param name: Name of the match (id)
        :param date: Date of the match
        :param ht: Home Team
        :param at: Away Team
        :param fthg: Full Time Home Goals
        :param ftag: Full Time Away Goals
        :param ftr: Full Time Result
        :param hthg: Half Time Home Goals
        :param htag: Half Time Away Goals
        :param htr: Half Time Result
        :param kwargs: Optional match parameters:
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
        :return:
        """
        date = params['Date']
        home = params['HomeTeam']
        away = params['AwayTeam']
        name = date + home + away
        problem = CBRclass(name=name)
        Case.__init__(self, name, problem)

        params_names = ['Div', 'FTHG', 'FTAG', 'HTHG', 'HTAG', 'HTR', 'Attendance', 'Referee', 'HS', 'AS', 'HST', 'AST',
                        'HHW', 'AHW', 'HC', 'AC', 'HF', 'AF', 'HO', 'AO', 'HY', 'AY', 'HR', 'AR', 'HBP', 'ABP', 'B365H',
                        'B365D', 'B365A', 'BSH', 'BSD', 'BSA', 'BWH', 'BWD', 'BWA', 'GBH', 'GBD', 'GBA', 'IWH', 'IWD',
                        'IWA', 'LBH', 'LBD', 'LBA', 'PSH', 'PSD', 'PSA', 'SOH', 'SOD', 'SOA', 'SBH', 'SBD', 'SBA',
                        'SJH', 'SJD', 'SJA', 'SYH', 'SYD', 'SYA', 'VCH', 'VCD', 'VCA', 'WHH', 'WHD', 'WHA', 'Bb1X2',
                        'BbMxH', 'BbAvH', 'BbMxD', 'BbAvD', 'BbMxA', 'BbAvA', 'BbOU', 'BbMx>2.5', 'BbAv>2.5',
                        'BbMx<2.5', 'BbAv<2.5', 'GB>2.5', 'GB<2.5', 'B365>2.5', 'B365<2.5', 'BbAH', 'BbAHh', 'BbMxAHH',
                        'BbAvAHH', 'BbMxAHA', 'BbAvAHA', 'GBAHH', 'GBAHA', 'GBAH', 'LBAHH', 'LBAHA', 'LBAH', 'B365AHH',
                        'B365AHA', 'B365AH']
        self.problem.add_feature(name='date', values=utils.date_to_python_date(date))
        self.problem.add_class('home', home)
        self.problem.add_class('away', away)
        self.set_solution(params['FTR'])
        self.problem.add_feature(name='params', values={p: params[p] for p in params_names if p in params})

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
        return self.problem.get_class('home').name

    def get_away(self):
        """
        Returns the name of the away team in the match.
        """
        return self.problem.get_class('away').name

    def get_params(self):
        """
        Returns a dictionary with the parameters of the match.
        """
        return self.problem.get_feature('params')

    def get_home_or_away(self, team):
        """
        Returns 'home' or 'away' depending on the position the team is playing in the match.
        :param team: Team in the match
        :return: 'home' or 'away'
        """
        return 'home' if self.problem.get_class('home') == team else 'away'

    def get_team(self, where):
        """
        Returns the team playing in the position 'where'.
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

    def get_case_team(self, team, where, **kwargs):
        """
        Get the matches a team has played.
        :param team: Name of the team
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
        :type m: Match
        :param m: The reference match from where to extract the history.
        :type n: int
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
        :param m: Match
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


def read_match_dataset(dataset):
    data = pd.read_csv(dataset, sep=',', header=0)
    mcb = MatchesCaseBase()
    for i in data.index:
        params = {c: data.irow(i)[c] for c in data.columns}
        mcb.create_match(params)
    return mcb


def read_datasets(dataset):
    save_file = open(dataset, 'rb')
    matches_data = MatchesCaseBase()
    matches_data = cpi.load(save_file)
    save_file.close()
    return matches_data

if __name__ == '__main__':
    dataset = []
    for files in glob.glob("../data/train/*.csv"):
        dataset.append(files)


    for data in dataset:
        matches_data = read_match_dataset(data)

    save_file = open('../data/train/train.pkl', 'wb')
    cpi.dump(matches_data, save_file, -1)
    save_file.close()


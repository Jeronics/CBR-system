from internal_repr.model import CBRclass, Case
import utils


class Match(Case):
    def __init__(self, name):
        problem = CBRclass(name=name)
        Case.__init__(self, name, problem)

    def create_match(self, date, home_team, away_team, result, **kwargs):
        """
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
        params_names = ['FTHG', 'FTAG', 'HTHG', 'HTAG', 'HTR', 'Attendance', 'Referee', 'HS', 'AS', 'HST', 'AST', 'HHW',
                        'AHW', 'HC', 'AC', 'HF', 'AF', 'HO', 'AO', 'HY', 'AY', 'HR', 'AR', 'HBP', 'ABP', 'B365H',
                        'B365D', 'B365A', 'BSH', 'BSD', 'BSA', 'BWH', 'BWD', 'BWA', 'GBH', 'GBD', 'GBA', 'IWH', 'IWD',
                        'IWA', 'LBH', 'LBD', 'LBA', 'PSH', 'PSD', 'PSA', 'SOH', 'SOD', 'SOA', 'SBH', 'SBD', 'SBA',
                        'SJH', 'SJD', 'SJA', 'SYH', 'SYD', 'SYA', 'VCH', 'VCD', 'VCA', 'WHH', 'WHD', 'WHA', 'Bb1X2',
                        'BbMxH', 'BbAvH', 'BbMxD', 'BbAvD', 'BbMxA', 'BbAvA', 'BbOU', 'BbMx>2.5', 'BbAv>2.5',
                        'BbMx<2.5', 'BbAv<2.5', 'GB>2.5', 'GB<2.5', 'B365>2.5', 'B365<2.5', 'BbAH', 'BbAHh', 'BbMxAHH',
                        'BbAvAHH', 'BbMxAHA', 'BbAvAHA', 'GBAHH', 'GBAHA', 'GBAH', 'LBAHH', 'LBAHA', 'LBAH', 'B365AHH',
                        'B365AHA', 'B365AH']
        self.problem.add_feature(name='date', values=utils.date_to_python_date(date))
        self.problem.add_class(name='home', values=home_team)
        self.problem.add_class(name='away', values=away_team)
        self.set_solution(result)
        self.problem.add_feature(name='params', values={p: kwargs[p] for p in params_names if p in kwargs})


if __name__ == '__main__':
    match = Match(name='match1')
    match.create_match(date='04/05/14', home_team='FCB', away_team='RMD', result='1')
    print match
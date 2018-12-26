# This Python file uses the following encoding: utf-8
import requests
import re
import numpy as np
import pandas as pd
from bs4 import BeautifulSoup
import datetime

def find_in_list(name_list, name):
        full_name = [l for l in name_list for m in [re.search(name, l, flags=re.IGNORECASE)] if m]
        if len(full_name) > 1:
            return(name+': Enter Manually: '+'/'.join(full_name))
        if len(full_name) == 0:
            return(name+': Enter Manually')
        return full_name[0]

# Read in match data
all_matches = pd.read_excel('convert.xlsx')

for index, match in all_matches.iterrows():
    q = 1
    #### Scorecard details
    link = match['scorecard']
    page = requests.get(link)
    soup = BeautifulSoup(page.content, 'lxml')
    
    all_table = soup.find_all('table', class_="batting-table innings")
    
    extras = pd.DataFrame()
    bat_name = [[],[]]
    dismissal = [[],[]]
    bat_scores = [[],[]]
    team_total = [None,None]
    wickets = [None,None]
    batting = [None,None]
    
    i = 0
    
    # Find bat first
    if all_table:
        bat_1 = all_table[0].find('th', class_='th-innings-heading')
        bat_1 = re.search('(.+) innings',bat_1.text,flags=re.IGNORECASE).group(1)
        
    for team_score in all_table:
        b = lb = w = nb = pen = '0'
        scores = pd.DataFrame()
        
        # Team Total
        total_txt = team_score.find('td', class_='total-details')
        team_total[i] = int(total_txt.find_next('td').text)
        wickets[i] = 10 if re.search('all out', total_txt.text) else int(re.search('([0-9]+) wicket', total_txt.text).group(1))

        ## Finding all extras
        extra_txt = team_score.find('td', class_="extra-details")
        extra_txt = extra_txt.text
        
        if re.search("(?<![l,n])b [0-9]+", extra_txt):
            temp1 = re.search("(?<![l,n])b ([0-9]+)", extra_txt)
            b = temp1.group(1)
        
        if re.search("lb [0-9]+", extra_txt):
            temp1 = re.search("lb ([0-9]+)", extra_txt)
            lb = temp1.group(1)
        
        if re.search("w [0-9]+", extra_txt):
            temp1 = re.search("w ([0-9]+)", extra_txt)
            w = temp1.group(1)
        
        if re.search("nb [0-9]+", extra_txt):
            temp1 = re.search("nb ([0-9]+)", extra_txt)
            nb = temp1.group(1)
        
        if re.search("pen [0-9]+", extra_txt):
            temp1 = re.search("pen ([0-9]+)", extra_txt)
            pen = temp1.group(1)
        
        extras = extras.append({
                'Inn': 1 if i==0 else 2, 'byes': b, 'legbyes': lb, 
                'wides': w,'noballs': nb, 'penalty': pen
                }, ignore_index=True)
        
        # All Players and dismissals
        minutes = 1 if team_score.find_all('th',class_='th-m') else None
        
        for row in team_score.find_all('tr')[1:]:
            col1 = row.find('td', class_='batsman-name')
            if col1:
                column_1 = col1.text
                column_1 = re.sub(r'[†*]|\s+$','', column_1)
                bat_name[i].append(column_1)
            
                col2 = row.find('td', class_='dismissal-info')
                column_2 = col2.text
                column_2 = re.sub('[†*]','', column_2)
                dismissal[i].append(column_2)
                runs = None
                balls = None
                fours = None
                sixes = None
                col3 = col2.next_sibling.next_sibling
                runs = col3.text
                col4 = col3.next_sibling.next_sibling.next_sibling.next_sibling if minutes else col3.next_sibling.next_sibling
                balls = col4.text
                col5 = col4.next_sibling.next_sibling
                fours = col5.text
                col6 = col5.next_sibling.next_sibling
                sixes = col6.text
                scores = scores.append({'player':column_1, 'R':runs, 'B':balls,
                                        'fours':fours, 'sixes':sixes}, ignore_index=True)
        
        bat_scores[i] = scores.set_index('player')
        
        # Get remaining players in Did not bat section
        temp1 = team_score.next_sibling.next_sibling
        temp1 = temp1.find('div', class_='to-bat')
        if temp1:
            temp1 = temp1.find_all('a', class_='playerName')
        
        if temp1:    
            for row in temp1:
                player = row.text
                player = re.sub('[†*]','', player)
                bat_name[i].append(player)
        
        i += 1
     
    # Get dismissal fielders and wicket type    
    
    wkt_field = [[],[]]
    wkt_type = [[],[]]
    i = 0
    
    for dism_team in dismissal:
        k = 0
        for dism_text in dism_team:
            fielder = None
            wicket_kind = None
            dism_text = re.sub('^\s+','', dism_text)
            if re.search('c ((?:[a-zA-z\']+ )+)+b (?:[a-zA-z\']+ )+', dism_text):
                temp2 = re.search('c ((?:[a-zA-z\']+ )+)+b ((?:[a-zA-z\']+ )+)', dism_text)
                fielder = temp2.group(1)
                fielder = re.sub(r'\s+$','',fielder)
                fielder = find_in_list(bat_name[1 if i == 0 else 0], fielder)
                wicket_kind = 'caught'
                wkt_field[i].append(fielder)
                wkt_type[i].append(wicket_kind)

            elif re.match(r'b \w+', dism_text):
                wicket_kind = 'bowled'
                wkt_field[i].append(fielder)
                wkt_type[i].append(wicket_kind)

            elif re.search('lbw', dism_text):
                wicket_kind = 'lbw'
                wkt_field[i].append(fielder)
                wkt_type[i].append(wicket_kind)
                
            elif re.search('run out', dism_text, flags=re.IGNORECASE):
                wicket_kind = 'run out'
                if re.search('run out \((.+)\)', dism_text):    
                    temp2 = re.search('run out \((.+)\)', dism_text).group(1)
                    if re.search('/', temp2):
                        temp2 = re.split("/", temp2)
                        for j in range(len(temp2)):
                            temp2[j] = find_in_list(bat_name[1 if i == 0 else 0], temp2[j])
                        temp2 = '/'.join(temp2)
                        fielder = temp2
                    else:
                        fielder = find_in_list(bat_name[1 if i == 0 else 0], temp2)
                else:
                    fielder = 'add manually:'
                wkt_field[i].append(fielder)
                wkt_type[i].append(wicket_kind)
                
            elif re.search('c & b', dism_text):
                wicket_kind = 'caught and bowled'
                wkt_field[i].append(fielder)
                wkt_type[i].append(wicket_kind)
                
            elif re.search('st \w+', dism_text):
                wicket_kind = 'stumped'
                fielder = re.search('st ((?:[a-zA-z\']+ )+)+b (?:[a-zA-z\']+ )+', dism_text).group(1)
                fielder = re.sub(r'\s+$','',fielder)
                wkt_field[i].append(fielder)
                wkt_type[i].append(wicket_kind)
                
            elif re.search('retired hurt', dism_text):
                wicket_kind = 'retired hurt'
                wkt_field[i].append(fielder)
                wkt_type[i].append(wicket_kind)
                
            elif re.search('hit wicket', dism_text):
                wicket_kind = 'hit wicket'
                wkt_field[i].append(fielder)
                wkt_type[i].append(wicket_kind)
                
            elif re.search('obstructing the field', dism_text):
                wicket_kind = 'obstructing the field'
                wkt_field[i].append(fielder)
                wkt_type[i].append(wicket_kind)
                
            elif re.search('hit the ball twice', dism_text):
                wicket_kind = 'hit the ball twice'
                wkt_field[i].append(fielder)
                wkt_type[i].append(wicket_kind)
                
            elif re.search('handled the ball', dism_text):
                wicket_kind = 'handled the ball'
                wkt_field[i].append(fielder)
                wkt_type[i].append(wicket_kind)
                
            elif re.search('timed out', dism_text):
                wicket_kind = 'timed out'
                wkt_field[i].append(fielder)
                wkt_type[i].append(wicket_kind)
                
            else:
                wkt_field[i].append(fielder)
                wkt_type[i].append(wicket_kind)
            k += 1
        i += 1
        
    # Make wicket type and fielders same length as all players
    for i in range(2):    
        while(len(wkt_type[i]) < 11):
            wkt_type[i].append(None)
    for i in range(2):    
        while(len(wkt_field[i]) < 11):
            wkt_field[i].append(None)
            
    team_dism = [None, None]
    team_dism[0] = pd.DataFrame({
            'wicket_player_out': bat_name[0],
            'wicket_kind': wkt_type[0],
            'wicket_fielders': wkt_field[0]
            })
    team_dism[1] = pd.DataFrame({
            'wicket_player_out': bat_name[1],
            'wicket_kind': wkt_type[1],
            'wicket_fielders': wkt_field[1]
            })
#    temp4 = pd.merge(bat_scores[0], team_dism[0].rename(columns={'wicket_player_out':'player'}), 'right')
#    temp5 = pd.merge(bat_scores[1], team_dism[1].rename(columns={'wicket_player_out':'player'}), 'right')
    
    # Bowling Table
    all_table = soup.find_all('table', class_="bowling-table")
    bowl_fig = [None,None]
    for i in range(len(all_table)):
        figures = pd.DataFrame()
        for row in all_table[i].find_all('td',class_ = 'bowler-name'):
            col1 = row.find_next('td')
            col2 = col1.find_next('td').find_next('td')
            col3 = col2.find_next('td',class_='td-extra')
            if col3:    
                if re.search('[0-9]+w',col3.text):
                    wd = re.search('([0-9]+)w',col3.text).group(1)
                else:
                    wd = '0'
                if re.search('[0-9]+nb',col3.text):
                    nb = re.search('([0-9]+)nb',col3.text).group(1)
                else:
                    nb = '0'
            figures = figures.append({'player':row.text, 'B':col1.text, 'R':col2.text,'wd':wd, 'nb':nb}, ignore_index=True)
        figures['B'] = figures['B'].apply(lambda x: int(x.split('.')[0]) * 6 if len(x.split('.')) == 1 else (int(x.split('.')[0]) * 6) + int(x.split('.')[1]))
        bowl_fig[i] = figures.set_index('player')
                
    ###### Match info data
    
    df_info = pd.DataFrame()
    
    # Scraping only male ODI matches
    df_info = df_info.append({'value':'male', 'L2':'gender', 'L4':None, 'L3':None}, ignore_index=True)
    df_info = df_info.append({'value':'ODI', 'L2':'match_type', 'L4':None, 'L3':None}, ignore_index=True)
    df_info = df_info.append({'value':'50', 'L2':'overs', 'L4':None, 'L3':None}, ignore_index=True)
    
    temp1 = soup.find('div', class_='row brief-summary')
    
    # Teams playing
    teams = temp1.find_all('a', class_='teamLink')
    team1 = teams[0].text
    team2 = teams[1].text
    
    df_info = df_info.append({'value':team1, 'L2':'teams', 'L4':None, 'L3':None}, ignore_index=True)
    df_info = df_info.append({'value':team2, 'L2':'teams', 'L4':None, 'L3':None}, ignore_index=True)
    
    result = temp1.find('div', class_='innings-requirement').text
    
    won = margin = result_type = None
    
    # Match outcomes
    if re.search('won', result, flags=re.IGNORECASE) and not re.search('eliminator|bowl-out', result, flags=re.IGNORECASE):
        temp2 = re.search('([\w+ ]+) won by ([0-9]+) (\w+)', result)
        won = temp2.group(1)
        margin = temp2.group(2)
        result_type = temp2.group(3)
        df_info = df_info.append({'value':margin, 'L2':'outcome', 'L4':result_type, 'L3':'by'}, ignore_index=True)
        df_info = df_info.append({'value':won, 'L2':'outcome', 'L4':None, 'L3':'winner'}, ignore_index=True)
    
    if re.search('tied', result, flags=re.IGNORECASE):
        if re.search('eliminator', result, flags=re.IGNORECASE):
            temp2 = re.search('([\w+ ]+) won', result)
            won = temp2.group(1)
            df_info = df_info.append({'value':won, 'L2':'outcome', 'L4':None, 'L3':'eliminator'}, ignore_index=True)
            df_info = df_info.append({'value':'tie', 'L2':'outcome', 'L4':None, 'L3':'result'}, ignore_index=True)
        elif re.search('bowl-out', result,flags=re.IGNORECASE):
            temp2 = re.search('([\w+ ]+) won', result)
            won = temp2.group(1)
            df_info = df_info.append({'value':won, 'L2':'outcome', 'L4':None, 'L3':'bowl_out'}, ignore_index=True)
            df_info = df_info.append({'value':'tie', 'L2':'outcome', 'L4':None, 'L3':'result'}, ignore_index=True)
        else:    
            result_type = 'tie'
            df_info = df_info.append({'value':result_type, 'L2':'outcome', 'L4':None, 'L3':'result'}, ignore_index=True)
        
    if re.search('no result|abandoned', result, flags=re.IGNORECASE):
        result_type = 'no result'
        df_info = df_info.append({'value':result_type, 'L2':'outcome', 'L4':None, 'L3':'result'}, ignore_index=True)
        
    temp2 = temp1.find_all('a',class_='headLink')
    # check for neutral venue
    if re.search('neutral', temp2[-1].next_sibling, flags=re.IGNORECASE):
        df_info = df_info.append({'value':'1', 'L2':'neutral_venue', 'L4':None, 'L3':None}, ignore_index=True)
        
    for row in temp2:
        if re.search('ground profile', str(row.encode('utf-8')), flags=re.IGNORECASE):
            temp3 = re.search('(.+), (.+)', row.text)
            if temp3:
                venue = temp3.group(1)
                city = temp3.group(2)
            else:
                venue = row.text
                city = None
            date = row.parent.next_sibling.next_sibling.text
            date = re.search('([0-9]+) \w+ [0-9]+', date).group(0)
            if len(re.search('([0-9]+) \w+ [0-9]+', date).group(1)) == 1:
                date = '0'+date
            date = datetime.datetime.strptime(date, '%d %B %Y')
            date = date.strftime('%Y-%m-%d')
    
    df_info = df_info.append({'value':city, 'L2':'city', 'L4':None, 'L3':None}, ignore_index=True)
    df_info = df_info.append({'value':date, 'L2':'dates', 'L4':None, 'L3':None}, ignore_index=True)
    df_info = df_info.append({'value':venue, 'L2':'venue', 'L4':None, 'L3':None}, ignore_index=True)
    
    temp1 = soup.find_all('div', class_='match-information')
    
    # take div with only match-information as the class
    for row in temp1:
        if len(row['class']) == 1:
            temp1 = row
            
    temp1 = temp1.find_all('div')
    toss = temp1[0].next_element.next_element.text
    
    temp2 = re.search('(.+), .+', toss)
    
    if temp2:
        toss = temp2.group(1)
    else:
        if re.search('no toss', toss, flags=re.IGNORECASE):
            toss = None
    
    temp2 = soup.find_all('th', class_='th-innings-heading')
    
    if toss:
        toss_decision = 'bat' if toss == bat_1 else 'field'
    else:
        toss_decision = None
    
    df_info = df_info.append({'value':toss_decision, 'L2':'toss', 'L4':None, 'L3':'decision'}, ignore_index=True)
    df_info = df_info.append({'value':toss, 'L2':'toss', 'L4':None, 'L3':'winner'}, ignore_index=True)
    
    MOM = None
    
    # Cycle all rows to get MOM and umpires
    for row in temp1:
        if re.search('player of the match ', row.text, flags=re.IGNORECASE):
            temp2 = re.search('player of the match \\n - (.+?) \(.+\)', row.text, flags=re.IGNORECASE)
            MOM = temp2.group(1)
            df_info = df_info.append({'value':MOM, 'L2':'player_of_match', 'L4':None, 'L3':None}, ignore_index=True)
            
        if re.search('players of the match', row.text, flags=re.IGNORECASE):
            temp2 = re.search('player of the match \\n - (.+?) \(.+\)', row.text, flags=re.IGNORECASE)
            MOM = temp2.group(1)
            df_info = df_info.append({'value':MOM, 'L2':'player_of_match', 'L4':None, 'L3':None}, ignore_index=True)
            MOM = temp2.group(2)
            df_info = df_info.append({'value':MOM, 'L2':'player_of_match', 'L4':None, 'L3':None}, ignore_index=True)
            
        if re.search('umpires \\n', row.text, flags=re.IGNORECASE):
            temp2 = re.search('umpires \\n - (.+?)\\n', row.text, flags=re.IGNORECASE).group(1)
            temp2 = re.sub('(?:\s)?\(.+?\)', '', temp2)
            temp2 = re.search('(.+)(?:\s+and\s+)(.+)', temp2, flags=re.IGNORECASE)
            ump1 = temp2.group(1)
            ump2 = temp2.group(2)
            df_info = df_info.append({'value':ump1, 'L2':'umpires', 'L4':None, 'L3':None}, ignore_index=True)
            df_info = df_info.append({'value':ump2, 'L2':'umpires', 'L4':None, 'L3':None}, ignore_index=True)
            
    df_info.to_csv('info-'+date+'-'+team1+'-'+team2+'.csv', date_format='%Y-%m-%d', index=False)
    
    
    
    
    #### Ball By ball details
    
    df_list = [None,None]
    over_sum = pd.DataFrame()
    
    for i in range(2):

        link = match['comm_inn_1'] if i == 0 else match['comm_inn_1'].replace('innings=1','innings=2')
        page = requests.get(link)
        soup = BeautifulSoup(page.content, 'html.parser')
        
        all_commentary = soup.find_all('div', class_=["commentary-event","end-of-over-info"])
        playing = set([bat_name[i][0], bat_name[i][1]])
        this_wkts = 0
        df = pd.DataFrame()
        l2 = '1' if i ==0 else '2'
        l3 = '1st innings' if i ==0 else '2nd innings'
        
        for j in range(len(all_commentary)):
            if all_commentary[j]['class'] ==['commentary-event']:
                byes = legbyes = noballs = wides = no_bdry = penalty = wicket_kind = out = wicket_fielders = None
                runs_bat = '0'
                
                if re.search(".*[0-9]x4.*[0-9]x6.*SR:", all_commentary[j].text):
                    text = re.sub(r'^\s+','', all_commentary[j].text)
                    out = re.match(r'(.*?)(?= lbw | hit wicket | c | b | st | run out | retired hurt | obstructing the field | hit the ball twice | handled the ball | timed out )', text)
                    out = re.sub(r'\s+$','', out.group(0))
                    
                    df.iloc[-1,df.columns.get_loc('wicket_player_out')] = out
                    this_wkts += 1
                    playing.discard(out)
                    if this_wkts < 10:
                        playing.add(bat_name[i][this_wkts+1])
                    out = None
                
                else:
                    # Handles none results
                    if all_commentary[j].find('div', class_="commentary-overs"):
                        # Handles duplicate commentary text
                        if all_commentary[j].text == all_commentary[j-1]:
                            continue
                        else:
                            over_ball = all_commentary[j].find('div', class_="commentary-overs").text
                    else:
                        continue
                    over = re.split('\.',over_ball)[0]
                    ball = re.split('\.',over_ball)[1]
                    
                    text = all_commentary[j].find('div', class_="commentary-text")
                    text = re.sub(r'\s',' ', text.p.text)
                    text = re.sub(r'^\s', '', text)
                    players = re.match("(?:(.*?) )?to (.*?)?,", text, flags=re.IGNORECASE)
                    bowler = players.group(1)
                    if bowler:
                        bowler = find_in_list(bat_name[1 if i == 0 else 0], bowler)
                    
                    batsman = players.group(2)
                    if batsman:
                        batsman = find_in_list(bat_name[1 if i == 1 else 0], batsman)
                        playing.add(batsman)
                    
                    num_text = re.search(', (.*?),|, (.*)', text).group(1)
                    if num_text is None:
                        num_text = re.search(', (.*)', text).group(1)
                        
                    if re.search("no ball", text):
                        if re.search("[0-9] no ball", text):
                            runs_bat = '0'
                            temp1 = re.search("([0-9]) no ball", text)
                            noballs = temp1.group(1)
                        else:
                            noballs = '1'
                    
                    if re.search("[0-9] bye", num_text):
                        runs_bat = '0'
                        temp1 = re.search("([0-9]) bye", num_text)
                        byes = temp1.group(1)
                    
                    if re.search("[0-9] leg bye", num_text):
                        runs_bat = '0'
                        temp1 = re.search("([0-9]) leg bye", num_text)
                        legbyes = temp1.group(1)
                    
                    if re.search("[0-9] wide", num_text):
                        runs_bat = '0'
                        temp1 = re.search("([0-9]) wide", num_text)
                        wides = temp1.group(1)
                    
                    if re.search("([0-9]|no) run", num_text):
                        temp1 = re.search("([0-9]|no) run", num_text)
                        runs_bat = temp1.group(1)
                        if temp1.group(1) == "no":
                            runs_bat = '0'
                    
                    if re.search("FOUR", num_text):
                        runs_bat = '4'
                        
                    if re.search("SIX", num_text):
                        runs_bat = '6'
                        
                    if re.search("6 runs", num_text):
                        runs_bat = '6'
                        no_bdry = '1'
                    
                    if re.search("4 runs", num_text):
                        runs_bat = '4'
                        no_bdry = '1'
                    
#                    if re.search("penalty", text, flags=re.IGNORECASE) or re.search("helmet", text, flags=re.IGNORECASE):
#                        penalty = '5'
                
                    df = df.append({'L2': l2, 'L3': l3, 'over': over, 'ball': ball, 'batsman_NA': batsman, 'bowler_NA': bowler,
                                    'extras_byes': byes, 'extras_legbyes': legbyes, 'extras_wides': wides, 'extras_noballs': noballs, 
                                    'runs_batsman': runs_bat, 'runs_non_boundary': no_bdry, 'extras_penalty': penalty, 
                                    'wicket_player_out': out, 'playing': list(playing)}, ignore_index=True)
            
            elif(all_commentary[j]["class"] == ['end-of-over-info']):             
                temp1 = all_commentary[j].find('p')
                temp1 = temp1.find_all('span')
                for row in temp1:
                    if re.search(r'end of over \d+', row.string, flags=re.IGNORECASE):
                        temp2 = re.search(r'end of over (\d+)', row.string, flags=re.IGNORECASE).group(1)
                        temp3 = row.next_element.next_element
                        # Resolves issue of maidens where legbyes or byes are runs
                        if re.search('maiden', temp3) and not re.search('run', temp3):
                            temp3 = '0'
                        else:
                            temp3 = re.search(r'\((\d+)', temp3).group(1)
                        over_sum = over_sum.append({'L2': l2, 'over': temp2, 'runs': temp3}, ignore_index=True)    
                    
        #outs = ['b','b bowler c fielder','c & b','lbw b ','st','run out','retired hurt','hit wicket b ','obstructing the field','hit the ball twice','handled the ball','timed out']
        df['runs_total'] = df[['runs_batsman','extras_byes','extras_legbyes','extras_wides','extras_noballs','extras_penalty']].apply(pd.to_numeric).sum(axis=1)
        #Add last wicket as non striker if last player doesn't get strike before all out
        if len(df.iloc[-1,df.columns.get_loc('playing')]) == 1:
            all_strike = set(df['wicket_player_out'].dropna().unique())
            if len(all_strike) == 10:
                temp2 = (set(bat_name[i]) - all_strike).pop()
                df.iloc[-1,df.columns.get_loc('playing')].append(temp2)

        df['non_striker_NA'] = df.apply(lambda x: (x['playing'][0] if x['batsman_NA'] == x['playing'][1] else x['playing'][1]) if x['playing'] is not None else None, axis=1)

        df.drop('playing', inplace=True, axis=1)
        df = pd.merge(df, team_dism[i], 'left', on = 'wicket_player_out')
        df_list[i] = df
        
    final_df = pd.concat([df_list[0], df_list[1]])
    final_df.to_csv(date+'-'+team1+'-'+team2+'.csv',index=False)
    
    
    
    ###### Error Checking
    
    # Add wrong over by over info or total info
    over_sum2 = pd.DataFrame(final_df.groupby(['L2','over'])['runs_total'].sum())
    over_sum2['over'] = over_sum2.index
    over_sum2['L2'] = over_sum2['over'].apply(lambda x: x[0])
    over_sum2['over'] = over_sum2['over'].apply(lambda x: str(int(x[1]) + 1))
    over_sum3 = pd.merge(over_sum, over_sum2, on=['over','L2'])
    over_sum3['diff'] = over_sum3.apply(lambda x: int(x['runs']) - int(x['runs_total']), axis=1)
    if over_sum3['diff'].abs().sum() != 0:
        over_sum3.to_csv(date+'-(mistakes)-'+team1+'-'+team2+'.csv' ,index=False)
    # Add wrong total or wickets info
    temp1 = over_sum2.groupby('L2')['runs_total'].sum()
    temp2 = final_df[pd.notnull(final_df['wicket_player_out'])].groupby('L2')['batsman_NA'].count()
    temp2 = final_df.wicket_player_out.notnull().groupby(final_df.L2).sum()
    temp = pd.concat([(wickets-temp2).rename('wickets'), (team_total-temp1).rename('team_runs')],axis=1)
    if np.absolute(temp.values).sum() != 0:
        temp.to_csv(date+'-(mistakes)-'+team1+'-'+team2+'.csv', mode='a')
    # Add wrong extras info
    temp1 = final_df[['L2','extras_byes','extras_legbyes','extras_noballs','extras_penalty','extras_wides']].apply(pd.to_numeric).groupby(['L2'],as_index=False).sum()
    temp1 = temp1.fillna(0)
    temp1.columns = extras.columns
    temp2 = temp1.set_index('Inn') - extras.set_index('Inn').apply(pd.to_numeric)
    if temp2.values.sum() != 0:
        temp2.to_csv(date+'-(mistakes)-'+team1+'-'+team2+'.csv', mode='a')
    # Add wrong batsman stats info
    for i in range(2):
        temp1 = df_list[i][['batsman_NA','runs_batsman']].apply(pd.to_numeric, errors='ignore').groupby('batsman_NA')['runs_batsman'].sum().rename('R')
        temp2 = df_list[i].loc[pd.isnull(df_list[i]['extras_wides']), :].groupby('batsman_NA')['L2'].count().rename('B')
        temp3 = df_list[i][(df_list[i]['runs_batsman'] == '4') & (pd.isnull(df_list[i]['runs_non_boundary']))].groupby('batsman_NA')['L2'].count().rename('fours')
        temp4 = df_list[i][(df_list[i]['runs_batsman'] == '6') & (pd.isnull(df_list[i]['runs_non_boundary']))].groupby('batsman_NA')['L2'].count().rename('sixes')
        temp5 = pd.concat([temp1,temp2,temp3,temp4], axis=1)
        temp5.fillna(0,inplace=True)
        temp = bat_scores[i].apply(pd.to_numeric) - temp5
        if np.absolute(temp.values).sum() != 0:
            temp.to_csv(date+'-(mistakes)-'+team1+'-'+team2+'.csv', mode='a')
    # Add wrong bowling stats info
    for i in range(2):
        temp1 = temp1 = df_list[i].loc[(pd.isnull(df_list[i]['extras_wides'])) & (pd.isnull(df_list[i]['extras_noballs'])), 'bowler_NA'].value_counts().rename('B')
        temp2 = df_list[i].copy().apply(pd.to_numeric,errors='ignore').fillna(0)
        temp2['runs_bowler'] = temp2.apply(lambda x: x['runs_total'] - x['extras_byes'] - x['extras_legbyes'], axis =1)
        temp2 = temp2.groupby('bowler_NA')['runs_bowler'].sum().rename('R')
        temp3 = df_list[i][pd.notnull(df_list[i]['extras_wides'])]['bowler_NA'].value_counts().rename('wd')
        temp4 = df_list[i][pd.notnull(df_list[i]['extras_noballs'])]['bowler_NA'].value_counts().rename('nb')
        temp5 = pd.concat([temp1,temp2,temp3,temp4], axis=1)
        temp5.fillna(0,inplace=True)
        temp = bowl_fig[i].apply(pd.to_numeric) - temp5
        if np.absolute(temp.values).sum() != 0:
            temp.to_csv(date+'-(mistakes)-'+team1+'-'+team2+'.csv', mode='a')
    

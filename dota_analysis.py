import pandas as pd
import json, os, math
import scipy.stats as st
from IPython.core.display import HTML

#Allow pandas to display full dataframes without truncating rows.
#Not always needed because sometimes the dataframes will have too many rows
# to read through everything, but it is useful when checking results.
pd.set_option("display.max_rows", None, "display.max_columns", None)

large_df = []
ban_df = []
iconlist = []

for i in os.listdir("tables/imagefolder"):
    iconname = "imagefolder/" + i
    iconlist.append(iconname)

for i in os.listdir('datafolder'):
    file = open('datafolder' + os.sep + i)
    tempdata = json.load(file)
    file.close()

    if "error" in tempdata.keys():
        continue

    if tempdata["lobby_type"] != 7 | tempdata["lobby_type"] != 0:
        continue

    if tempdata["human_players"] != 10:
        continue

    if not tempdata["picks_bans"]:
        continue

    winning_team = 0
    if tempdata["radiant_win"] == False:
        winning_team = 1

    picks = pd.DataFrame(tempdata["picks_bans"])
    bans = picks[picks.is_pick == False]
    picks = picks[picks.is_pick]
    picks = picks.sort_values('order')

    if len(picks.is_pick) <10:
        continue
    

    large_df.append([tempdata["match_id"],
               picks.iloc[0].hero_id,
               picks.iloc[0].order,
               picks.iloc[0].team == winning_team])

    large_df.append([tempdata["match_id"],
               picks.iloc[1].hero_id,
               picks.iloc[1].order,
               picks.iloc[1].team == winning_team])

    large_df.append([tempdata["match_id"],
               picks.iloc[2].hero_id,
               picks.iloc[2].order,
               picks.iloc[2].team == winning_team])

    large_df.append([tempdata["match_id"],
               picks.iloc[3].hero_id,
               picks.iloc[3].order,
               picks.iloc[3].team == winning_team])

    large_df.append([tempdata["match_id"],
               picks.iloc[4].hero_id,
               picks.iloc[4].order,
               picks.iloc[4].team == winning_team])

    large_df.append([tempdata["match_id"],
               picks.iloc[5].hero_id,
               picks.iloc[5].order,
               picks.iloc[5].team == winning_team])

    large_df.append([tempdata["match_id"],
               picks.iloc[6].hero_id,
               picks.iloc[6].order,
               picks.iloc[6].team == winning_team])

    large_df.append([tempdata["match_id"],
               picks.iloc[7].hero_id,
               picks.iloc[7].order,
               picks.iloc[7].team == winning_team])

    large_df.append([tempdata["match_id"],
               picks.iloc[8].hero_id,
               picks.iloc[8].order,
               picks.iloc[8].team == winning_team])

    large_df.append([tempdata["match_id"],
               picks.iloc[-1].hero_id,
               picks.iloc[-1].order,
               picks.iloc[-1].team == winning_team])

    try:
        ban_df.append([tempdata["match_id"],
                  bans.iloc[0].hero_id,
                  bans.iloc[0].order,
                  bans.iloc[0].team == winning_team])

    except:
        continue

    try:
        ban_df.append([tempdata["match_id"],
                  bans.iloc[1].hero_id,
                  bans.iloc[1].order,
                  bans.iloc[1].team == winning_team])

    except:
        continue

    try:
        ban_df.append([tempdata["match_id"],
                  bans.iloc[2].hero_id,
                  bans.iloc[2].order,
                  bans.iloc[2].team == winning_team])

    except:
        continue

    try:
        ban_df.append([tempdata["match_id"],
                  bans.iloc[3].hero_id,
                  bans.iloc[3].order,
                  bans.iloc[3].team == winning_team])

    except:
        continue

    try:
        ban_df.append([tempdata["match_id"],
                  bans.iloc[4].hero_id,
                  bans.iloc[4].order,
                  bans.iloc[4].team == winning_team])

    except:
        continue

    try:
        ban_df.append([tempdata["match_id"],
                  bans.iloc[5].hero_id,
                  bans.iloc[5].order,
                  bans.iloc[5].team == winning_team])

    except:
        continue
    
    #else:
        #ban_df.append([tempdata["match_id"],
                  #bans.iloc[1].hero_id,
                  #bans.iloc[1].order,
                  #bans.iloc[1].team == winning_team])  

heroes = pd.read_csv('hero_stats.csv')[['localized_name', 'hero_id']]
icondf = pd.DataFrame(iconlist)

ban_df = pd.DataFrame(ban_df, columns = ["match_id", "hero_id", "order", "win"])
large_df = pd.DataFrame(large_df, columns = ["match_id", "hero_id", "order", "win"])
large_df = pd.merge(large_df, heroes)
ban_df = pd.merge(ban_df, heroes) # Adds hero names
#DATA ANALYSIS/RESULTS

totalpicks = large_df.hero_id.count()



#Summary dataframe with list of heroes and number of picks, wins/losses, Wilson score rating and icon added.
pickcounts = large_df.groupby(["hero_id", "localized_name"]).hero_id.count().reset_index(name = 'picks')
wincounts = large_df.groupby("hero_id")["win"].sum().reset_index(name = "wins")
pickcounts = pd.merge(pickcounts, wincounts)
pickcounts["losses"] = pickcounts["picks"] - pickcounts["wins"]

#inserts correct hero icons to large_df
icondf = icondf.rename(columns={0 : "icons"})
icondf["hero_id"] = pickcounts.hero_id
large_df = pd.merge(large_df,icondf)
large_df.sort_values(["match_id", "order"], inplace = True, ascending = [True, True])

#icons into bans
ban_df = pd.merge(ban_df, icondf)
totalbans = ban_df.groupby(["hero_id", "localized_name", "icons"]).hero_id.count().reset_index(name = "bans")
totalbans = totalbans.sort_values("bans", ascending = False)


#Wilson confidence interval to generate a total score for hero popularity/performance
#that takes both number of picks and winrate into account.
def wilson_lower_bound(wins, losses, confidence=0.95):
    n = wins + losses
    if n == 0:
	    return 0
    z = st.norm.ppf(1 -(1 - confidence)/ 2)
    phat = 1.0 * wins / n

    return(phat + z * z /(2 * n)- z * math.sqrt((phat *(1 - phat)+ z * z /(4*n)/ n))/ (1 + z * z / n))

pickcounts["rating"]= pickcounts.apply(lambda x: \
                                       wilson_lower_bound(x["wins"],x["losses"]),axis=1)

#pickcounts.sort_values("picks")
#pickcounts["icons"] = iconlist #Adds hero icons to pickcounts df

def iconsfirst(df):
    df.insert(0, "icons", df.pop("icons")) #Makes icons the first column
    return df

#Heroes and their win rates (success rates)
def winrate_df(df):
    herowinrate = df.groupby(["hero_id", "localized_name", "icons"])["win"].mean().reset_index(name = 'winrate')
    herowinrate.winrate = herowinrate.winrate * 100
    herowinrate.winrate = herowinrate.winrate.round(2)
    
    return herowinrate

large_df_winrate = winrate_df(large_df)

#Combined win rate and pick counts
def pickcountandwin(df1,df2):
    pickcountandwin = pd.merge(df1, df2)
    pickcountandwin.sort_values(['picks', 'winrate'], inplace = True, ascending = [False, False])
    return pickcountandwin

large_df_combined = pickcountandwin(pickcounts,large_df_winrate)

iconsfirst(large_df_combined)
iconsfirst(totalbans)

totalbans["matches"] = large_df_combined.picks + totalbans.bans
#Summary Statistics

#Top meta heroes (More picks than average and successful)
def topheroes(df):
    topheroesdf = df[(df.picks > df.picks.mean()) & (df.winrate > 52)]
    topheroesdf.sort_values(['rating'], ascending = [True])
    return topheroesdf

large_df_top = topheroes(large_df_combined)
large_df_top = large_df_top.sort_values("rating", ascending = False)

#Niche/underrated hero picks (high winrate but below average pickrate)
def nicheheroes(df):
    niche = df[(df.picks < df.picks.mean()) & (df.winrate > 52)]
    niche.sort_values(['winrate'], ascending = [False])
    return niche

large_df_niche = nicheheroes(large_df_combined)

#Potentially overrated heroes (popular but not very successful on average)
def overrated(df):
    overrated = df[(df.picks > df.picks.mean()) & (df.winrate < 48)]
    overrated.sort_values(['picks'], ascending = [False])
    return overrated

large_df_overrated = overrated(large_df_combined)

#First picked heroes' winrates
firstpicks = large_df[(large_df.order.isin([0,1,2,3]))]
firstcount = firstpicks.hero_id.value_counts()
firstkeep = firstcount[firstcount > 50].index
firstpicks = firstpicks[firstpicks.hero_id.isin(firstkeep)]
firstpickwinrate = firstpicks.groupby(["hero_id", "localized_name", "icons"])["win"].mean().reset_index(name = "firstpick_winrate")
firstpickwinrate.firstpick_winrate = firstpickwinrate["firstpick_winrate"] * 100
firstpickwinrate.firstpick_winrate = firstpickwinrate["firstpick_winrate"].round(2)

firstpickdifference = pd.merge(large_df_winrate, firstpickwinrate)
firstpickdifference["difference"] = firstpickdifference.firstpick_winrate - firstpickdifference.winrate
firstpickdifference.sort_values("difference", inplace = True, ascending = False)
iconsfirst(firstpickdifference)

#Last picked heroes' winrates
lastpicks = large_df[(large_df.order.isin([8,9,10,11]))]
lastcount = lastpicks.hero_id.value_counts()
lastkeep = lastcount[lastcount > 50].index
lastpicks = lastpicks[lastpicks.hero_id.isin(lastkeep)]
lastpickwinrate = lastpicks.groupby(["hero_id", "localized_name", "icons"])["win"].mean().reset_index(name = "lastpick_winrate")
lastpickwinrate.lastpick_winrate = lastpickwinrate["lastpick_winrate"] * 100
lastpickwinrate.lastpick_winrate = lastpickwinrate["lastpick_winrate"].round(2)

lastpickdifference = pd.merge(large_df_winrate, lastpickwinrate, )
lastpickdifference["difference"] = lastpickdifference.lastpick_winrate - lastpickdifference.winrate
lastpickdifference.sort_values("difference", inplace = True, ascending = False)
iconsfirst(lastpickdifference)

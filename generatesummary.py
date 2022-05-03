import dota_analysis
import matplotlib.pyplot as plt
import seaborn as sns
#This file generates all the result tables and graphs for the current dataset.
#The website will automatically update to show any new/changed data.

#Creates image tags to display images in HTML format
def path_to_image_html(path):
    return '<img src="'+ path + '"width = 60, height=35>'

table1html = dota_analysis.large_df_combined.to_html(index=False, escape=False, formatters=dict(icons=path_to_image_html))
table2html = dota_analysis.large_df_top.to_html(index=False, escape=False, formatters=dict(icons=path_to_image_html))
table3html = dota_analysis.large_df_niche.to_html(index=False, escape=False, formatters=dict(icons=path_to_image_html))
table4html = dota_analysis.large_df_overrated.to_html(index=False, escape=False, formatters=dict(icons=path_to_image_html))
table5html = dota_analysis.firstpickdifference.to_html(index=False, escape=False, formatters=dict(icons=path_to_image_html))
table6html = dota_analysis.lastpickdifference.to_html(index=False, escape=False, formatters=dict(icons=path_to_image_html))

sns.set(rc={'axes.facecolor':'gray', 'figure.facecolor':'gray'})
summaryhead = dota_analysis.large_df_combined.head(10)
summaryhead = summaryhead.sort_values("picks", ascending = False)
summaryheadplot = sns.barplot(data = summaryhead, x = summaryhead.winrate, y = summaryhead.localized_name, palette="mako")
plt.xlim(30, 70)
plt.savefig("html files/tables/summaryplot.png", bbox_inches="tight")
plt.close()

tophead = dota_analysis.large_df_top.head(10)
tophead = tophead.sort_values("winrate", ascending = False)
topheadplot = sns.barplot(data = tophead, x = tophead.winrate, y = tophead.localized_name, palette="mako")
plt.xlim(30, 70)
plt.savefig("html files/tables/topheadplot.png", bbox_inches="tight")
plt.close()

nichehead = dota_analysis.large_df_niche.head(10)
nichehead = nichehead.sort_values("picks", ascending = False)
nicheheadplot = sns.barplot(data = nichehead, x = nichehead.winrate, y = nichehead.localized_name, palette="mako")
plt.xlim(30, 70)
plt.savefig("html files/tables/nicheheadplot.png", bbox_inches="tight")
plt.close()

overratedhead = dota_analysis.large_df_overrated.head(10)
overratedheadplot = sns.barplot(data = overratedhead, x = overratedhead["winrate"], y = overratedhead.localized_name, palette="mako")
plt.xlim(30, 70)
plt.savefig("html files/tables/overratedheadplot.png", bbox_inches="tight")
plt.close()

firstpickhead = dota_analysis.firstpickdifference.head(10)
firstpickhead = firstpickhead.sort_values("firstpick_winrate", ascending = False)
firstpickheadplot = sns.barplot(data = firstpickhead, x = firstpickhead.firstpick_winrate, y = firstpickhead.localized_name, palette="mako")
plt.xlim(30, 100)
plt.savefig("html files/tables/firstpickheadplot.png", bbox_inches="tight")
plt.close()

lastpickhead = dota_analysis.lastpickdifference.head(10)
lastpickhead = lastpickhead.sort_values("lastpick_winrate", ascending = False)
lastpickheadplot = sns.barplot(data = lastpickhead, x = lastpickhead.lastpick_winrate, y = lastpickhead.localized_name, palette="mako")
plt.xlim(30, 100)
plt.savefig("html files/tables/lastpickheadplot.png", bbox_inches="tight")
plt.close()

leastcontested = dota_analysis.large_df_combined.sort_values("picks", ascending = True)
leastcontested = leastcontested.head(5)
leastcontestedhtml = leastcontested.to_html(index=False, escape=False, formatters=dict(icons=path_to_image_html))

mostpicked = dota_analysis.large_df_combined.sort_values("picks", ascending = False)
mostpicked = mostpicked.head(5)
mostpickedhtml = mostpicked.to_html(index=False, escape=False, formatters=dict(icons=path_to_image_html))

mostbanned = dota_analysis.totalbans.sort_values("bans", ascending = False)
mostbanned = mostbanned.head(5)
mostbannedhtml = mostbanned.to_html(index=False, escape=False, formatters=dict(icons=path_to_image_html))

firstpicks = dota_analysis.firstpicks.groupby(["hero_id", "localized_name", "icons"]).hero_id.count().reset_index(name = 'picks')
dota_analysis.iconsfirst(firstpicks)
firstpicks = firstpicks.sort_values("picks", ascending = False)
firstpicks = firstpicks.head(5)
firstpickshtml = firstpicks.to_html(index=False, escape=False, formatters=dict(icons=path_to_image_html))

lastpicks = dota_analysis.lastpicks.groupby(["hero_id", "localized_name", "icons"]).hero_id.count().reset_index(name = 'picks')
dota_analysis.iconsfirst(lastpicks)
lastpicks = lastpicks.sort_values("picks", ascending = False)
lastpicks = lastpicks.head(5)
lastpickshtml = lastpicks.to_html(index=False, escape=False, formatters=dict(icons=path_to_image_html))

with open ("html files/tables/firstpicks.html", "w") as outputfile:
    outputfile.write('<link href="stylesheet.css" rel="stylesheet">')
    outputfile.write(firstpickshtml)

with open ("html files/tables/lastpicks.html", "w") as outputfile:
    outputfile.write('<link href="stylesheet.css" rel="stylesheet">')
    outputfile.write(lastpickshtml)

with open ("html files/tables/leastcontested.html", "w") as outputfile:
    outputfile.write('<link href="stylesheet.css" rel="stylesheet">')
    outputfile.write(leastcontestedhtml)

with open ("html files/tables/mostpicked.html", "w") as outputfile:
    outputfile.write('<link href="stylesheet.css" rel="stylesheet">')
    outputfile.write(mostpickedhtml)

with open ("html files/tables/mostbanned.html", "w") as outputfile:
    outputfile.write('<link href="stylesheet.css" rel="stylesheet">')
    outputfile.write(mostbannedhtml)

with open ("html files/tables/table1output.html", "w") as outputfile:
    outputfile.write('<link href="stylesheet.css" rel="stylesheet">')
    outputfile.write(table1html)

with open ("html files/tables/table2output.html", "w") as outputfile:
    outputfile.write('<link href="stylesheet.css" rel="stylesheet">')
    outputfile.write(table2html)

with open ("html files/tables/table3output.html", "w") as outputfile:
    outputfile.write('<link href="stylesheet.css" rel="stylesheet">')
    outputfile.write(table3html)

with open ("html files/tables/table4output.html", "w") as outputfile:
    outputfile.write('<link href="stylesheet.css" rel="stylesheet">')
    outputfile.write(table4html)

with open ("html files/tables/table5output.html", "w") as outputfile:
    outputfile.write('<link href="stylesheet.css" rel="stylesheet">')
    outputfile.write(table5html)

with open ("html files/tables/table6output.html", "w") as outputfile:
    outputfile.write('<link href="stylesheet.css" rel="stylesheet">')
    outputfile.write(table6html)

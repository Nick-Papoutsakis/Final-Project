Information for file structure, contents and details of the Dota 2 Metagame Analysis project.

File structure/contents:
pycache - cache folder
datafolder - Folder containing the current dataset. In its current form, it contains several thousand matches worth of data.
	    Running get_match_data.py populates the datafolder.
html files - HTML files, stylesheets, and images that go into the creation and display of the website/frontend where results are displayed.
dota_analysis.py - The bulk of the code that performs all the data pre-processing and analysis, generating results.
generate_summary.py - Script that generates all the summary tables, visualizations, statistics etc. from the results of the analysis.
		      Running this file is all that needs to be done to update the website's contents if any changes have been made.
get_hero_stats.py - Script that was used to acquire required information on Dota 2 heroes, used in analysis.
		 Generates the hero_stats.csv file. Not required to be run again.
get_match_data.py - Script that acquires match data from the Opendota API and populates datafolder with it.
		  The script will acquire a given number of match replay data files, beginning from a given match ID.
		  E.g. running the program with given match ID 5000 and a value of 10000 matches to acquire would mean the
		  program requests and acquires match data json files for Dota 2 matches from ID 5000 to 15000, and 
		  populate datafolder with them.
		  Currently, this program has a delay added in between each match ID request. This has been added in the case of
		  the user not being authenticated for unlimited requests on the Opendota API service, as using the file without the
		  delay and no authentication key would result in the requests limit being breached and the user being locked/banned
		  from using the service.
hero_stats.csv - CSV file containing all required information on Dota 2 hero characters, to enable the display of their correct names
	        in the analysis and results.

Generating results:
To generate results of the analysis of all the current matches contained in datafolder, simply run generatesummary.py. This will
generate all the resulting summary statistics, tables, graphs etc. that are automatically placed into the website files and therefore
update the website/frontend contents to also display them.
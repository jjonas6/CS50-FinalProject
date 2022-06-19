# A 2022 FIFA World Cup Simulator
#### Demo URL: https://youtu.be/qXydHEgbWMg
#### Description:
This web app allows you to run a full simulation of the 2022 Men's FIFA World Cup, which will be hosted in Qatar.
Starting on the homepage, there are two options you can choose from, running a Finals Only simulation with only teams that are currently projected to enter the tournament or running a Qualifiers simulation, which will allow you to simulate all the World Cup qualifiers as well, except for the Oceania Conference due to it mostly being an irrelevant conference in my opinion.
The Qualifiers start at the beginning of the current round that is being played in real life in each conference.
The simulation of each game uses the same formula we used for cs50's Week 6 lab which tasked us with simulating just the knockouts rounds of the tournament. The formula is only adjusted for group matches to allow for draws.

In terms of code, this project uses HTML, CSS, Javascript, and Python, using Flask as the framework.
Python handles the initial simulations of all the groups and the initial stages of each qualifiers, then passing the data to HTML and Javascript to display and run the simulations on the preceeding qualification rounds and knockout stages.
The color scheme and design of the website is inspired by multiple sources. The colors were chosen based off the official colors for the 2022 tournament. The design of the knockout round bracket was inspired by "Flex Tournament Bracket" by Shaun Dowling.
https://blog.codepen.io/2018/02/16/need-make-tournament-bracket/

Overall, this project took about a month of working 2-3 days a week (mostly due to the shere amount of databases and lines of code).

While there are thousands of lines of code, a lot of it is sets of similar lines of code just designed for a different conference using their databases.

Here is a brief rundown of what each section of the simulation does.

Index:
This is the starting page that contains a brief intro and the two buttons that'll guide you towards what type of simulation you would like to run, a Finals Only simulation or one with the qualifiers.

CONMEBOL:
Assuming you choose the Qualifiers simulation, you will be plopped first into the CONMEBOL Simulation. This is one group of all South America teams. Press the simulate button to run the simulation via Python. The top 4 teams you will see in the Finals, the 5th team will show up in the Playoff.

UEFA:
The next section contains all the UEFA Groups for their qualifiers. The top team from each group and the next 3 best second place teams advance to the finals. This is slightly different than how the real life qualifiers work due to the last 3 teams being based off of UEFA Nations League results.

CONCACAF:
The next section simulates the first round of North American qualifiers. These groups contains only the teams that aren't seeded into the final qualification stage. Once the groups are calculated, it does a quick sim in the background of Round 2, then simulates Round 3, which contains the best 4 teams from Round 1 the best teams from CONCACAF. THe top 3 advance with the 4th best team going to the Playoffs.

CAF:
The next section simulates the African qualifiers. The top team from each group advances to one of 5 play-in games. Winner goes to the World Cup.

AFC:
The last main conference we will simulate is Asia. They start with a group stage that also counts as their Asia Cup qualifiers so Qatar, the Hosts of the World Cup, are present in this round, but if they get first or second in their group, they will not advance. The top team and best 5 second place teams advance to two final groups.
The top two from each group advance to the World Cup. The 3rd place teams play one game in the background, the winner advancing to the Playoffs.

Playoffs: The 5th best team from South America, 4th best team from North America, best 3rd place team in Asia, and New Zealand play one game. Winner advances to the World Cup.

Finals:
Whether going through the qualifiers or choosing Finals Only, this section first simulates the World Cup Group Stages (Python), then the Knockouts (Javascript).
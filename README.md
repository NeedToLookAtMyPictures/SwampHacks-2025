# Welcome to PoliCheck!
## Created by: Ben Adelman, Kushagra Katiyar, Bayan Mahmoodi

https://policheck.us/

The website is stored in the front-end branch and our visualization source code is in the back-end(benji) branch. The front end utilizes a combination of HTML, CSS98 style, and JavaScript. While not having an official backend, the data was gathered and created in Python using primarly the libraries Pandas and Altair.  Polling is a crucial part of our democracy. The ability to gain insight into elections before they actually occur is invaluable in planning for the future, gauging the current cultural climate of our country, and allowing politicians to clearly see what their constituents want. However, in reasons years, polling (specifically for US Presidential elections) has fallen off a cliff in terms of accuracy. It is clear that the methodology used in these polls is flawed in some way or another.  We hope to show the need for change with our visualizations. Despite recent inaccuracies, we still believe that polling can be an extremely useful pillar of the democratic process if used properly. This was created for the SwampHacks X hackathon. We hope you enjoy our project!

### Poll Graph
The poll graph showcases the total average polling error (in this case, for simplicity, Trump's projected popular vote % compared to his actual one)by each seperate polling provider. The blue dots signify polls from the 2020 presidential election (Joe Biden vs Donald Trump) while orange is for 2024 (Donald Trump vs Kamala Harris). The polling only includes data from October 1st to the day of election for each cycle in order to increase accuracy and condense averages. The bigger a dot is on the plot, the more polls that that provider had factor into their average.

### Rankings
We included a ranking table in order to show users what specific polling companies predicted the elections (2020,2024) the best. One could look at simply the aggregated error over the two elections as the measure of this however we felt a more meticiulous approach was needed. We created our own PoliCheck score for each polling provider to measure the true accuracy of each poll. The equation for the PoliScore is $(P =(\frac{1}{ER})0.75  + (\frac{S}{max(S_n)})0.25\)$. We chose this methodolgy in order to consider both the aggregated error as well as the number of polls that were taken by each company. The error is measured inversely meaning that a lower aggregated error (ideal) leads to a higher overall score. We weighted this category at 75% due to the philosophy that accuracy should be the #1 priority when it comes to polling. We also took into consideration the relative amount of polls conducted compared to the rest of the dataset at 25%. While not as important as total error, a larger amount of polls leads to more reliable and consistent polling average. Overall, the formula used to develop our score is dynamic and changes may be made in response to future data/events.

### Why Polls?
This section was included in order to education users on the utility of polling as well as the reasons for why it is done in the first place. We have also linked articles we found informational regarding the subject of the importance of polling. 




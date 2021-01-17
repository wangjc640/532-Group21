# GapExpresser

## Introduction
Development aid agencies are varied in size, missions, expertise, and experience. Some agencies operate with a very narrow scope, in location and/or directive, while others operate globally and in many development areas.  Large agencies often have the resources to hire dedicated research staff or employ experts in their chosen area of focus, but many agencies do not have these resources.   We propose building a data visualization app to assist these organizations visually explore some key statistics for different countries/regions.  This will help them identify countries/regions that would benefit from the type of service the agency provides, or gain additional insight into a region where they already operate.  These data visualizations may also challenge some misconceptions about a particular region, which in turn can help these agencies better serve the communities they operate in.   Our app will provide these organizations a snapshot of several key development statistics. Users can explore these statistics by filtering by region and other demographic factors.

## Description of app
The app has a single main page with three visualizations that depend on the filters selected. Most importantly, the top left contains a filter which selects the statistic of interest and this is the main filter on which all of the visuals are built and includes life expectancy, child mortality, education ratio, population density and CO2 emissions. At the top of the page is a global map which displays a color gradient corresponding to the level of the chosen statistic of interest for each country. A filter can be applied for region, sub region and income group and only the countries contained in those filters will be colored on the map. Furthermore, there is a also a slider which can control the minimum and maximum population size for these countries. These filters also apply to the two bottom plots. The bottom left chart is a horizontal bar chart showing the statistic of interest for the top 5 or bottom 5 countries (controlled via a button switch) in the filtered group to allow for a closer look at the data. The bottom right chart displays the statistic of interest over time in a line plot (top 5 or bottom 5) and also has an additional filter for the date range for users to see how the data in those specific countries trended over time.

## App sketch
![dashBoard](AppSketch.png "App Sketch")


## **License**
[![MIT license](https://img.shields.io/badge/License-MIT-blue.svg)](https://github.com/UBC-MDS/532-Group21/blob/main/LICENSE)
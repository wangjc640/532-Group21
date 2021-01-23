# Proposal

## Motivation and purpose

Our role: Data scientist consultancy firm

Target audience: Development aid agencies (Not-for-profits, charities, etc.) 

Development aid agencies are varied in size, missions, expertise, and experience. Some agencies operate with a very narrow scope, in location and/or directive, while others operate globally and in many development areas.  Large agencies often have the resources to hire dedicated research staff or employ experts in their chosen area of focus, but many agencies do not have these resources.   We propose building a data visualization app to assist these organizations visually explore some key statistics for different countries/regions.  This will help them identify countries/regions that would benefit from the type of service the agency provides, or gain additional insight into a region where they already operate.  These data visualizations may also challenge some misconceptions about a particular region, which in turn can help these agencies better serve the communities they operate in.   Our app will provide these organizations a snapshot of several key development statistics. Users can explore these statistics by filtering by region and other demographic factors.

## Description of the data

We will be visualizing country data from the summarized [Gapminder dataset](https://raw.githubusercontent.com/UofTCoders/workshops-dc-py/master/data/processed/world-data-gapminder.csv) which has 14 columns containing various demographic data for each country from the year 1800 to 2018, although data from the earlier years is often missing. The majority of our dashboard will focus on  the more current data but the timeseries data will be used to show the trends over time where appropriate. Each country has has an associated region and sub_region which will be used mostly as filters along with income group (low, medium or high) and population size. The health related indicators such as life_expectancy (years) and child_mortality (deaths of children under 5 per 1,000 live births) of countries will be showcased along with carbon dioxide emissions (tonnes per capita) and population density (people per square km). Furthermore, to show the divide in education levels between men and women, we will create a ratio using the years_in_school for women and divide this statistic with year_in_school for men, allowing us to track this new variable over time and between countries more easily.  

## Research questions you are exploring

Alice is a financial manager of “One World One Dream”, a not-for-profit charity whose mission is to reduce the education imbalance between men and women in developing countries. Alice receives a $1,000,000 CAD donation from the University of British Columbia to provide financial aid to families and local organizations in Northern Africa to allow girls to stay in school as long as possible. Alice wants to [**explore**] a dataset in order to [**compare**] different West African countries’ education imbalance, so that she can [**decide**] how to distribute the fund received from UBC to maximize the impact in the region.

Alice finds the GapExpresser dashboard, she is excited to use this dashboard to find valuable insights from the data and make important decisions. This application shows an overview of the education discrepancy between men and women over time.  Alice can [**filter**] the data based on the region she is interested in (Northern Africa), and the time period she is interested in (the last 20 years).

By exploring the data provided in the app and combining that information with her domain expertise, observed from academic journals, international news and her local contacts, Alice may notice that the education level discrepancy between men and women experienced a greater decline in countries that had previously received funds from World Education Services. However, there are several countries that had previously received funds but did not show any significant improvement. Alice may choose to fund only these "fund-sensitive" countries (those that did see improvement after investment).  Alternatively Alice may further investigate why other countries did not see similar improvement (perhaps due to a lack of community engagement, environmental issues, or conflict in the region) in order to make better funding choices in the future to maximize the impact on the education level discrepancy.   Based on her analysis using the GapExpresser dashboard, Alice can make a more informed decision on which countries to fund, and how to fund them to have the most impact. 

## App sketch

> see the description of the application [here](https://github.com/UBC-MDS/532-Group21#description-of-app).

![](imgs/AppSketch.png)
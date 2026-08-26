Title: SaaS Product Analysis Based on Customer Feedback and Competitor Performance

In this project, Zoom will be analysed based on customer feedback and competitor performance data gathered using FetchLayer API. The competitors for Zoom are: Google Meet, Microsoft Teams, and Cisco Webex. The end goal is to provide decision support to the respective stakeholder i.e., Head of Product on where to invest the engineering and customer-exp resources for the coming quarter.

Project Workflow:
1. src: Fetch the raw data via api and store it in the /data folder
2. data: Store all the raw data provided via /src
3. analysis: Perform transformation using python and load cleaned data inside /data folder. Also, perform eda on cleaned data using python in the same folder
4. data_qa: Check the quality of cleaned data using Excel and create a dashboard which gets stored in /dashboard folder
5. analysis: Use SQL to find patterns, insights, and metrics to finally create the required data as views
6. dashboard: Use PowerBI to load the views and create the required dashboards
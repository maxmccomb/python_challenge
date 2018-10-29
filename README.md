# python_challenge
Python Project to perform GeoIP and RDAP lookups and use gui to filter results
I understood this project to be in four(or five) steps:
  1.	parse through the text file, and store the IP's in a list to be processed later.
  2.	perform GeoIP lookups on each IP and store those results so that I could use it as part of my filter later.
  3.	perform RDAP/Whois lookups on each IP and store those results so that I could use it as part of my filter later.
  4.	construct a way to filter through a list of IP's and distinguish them based on ceritian fields such as the country, region, city, IP type, etc. 
  5(Bonus). Create a gui of somesort to display data and filter results in a user friendly way.

General Notes and How to Run:
I coded my project using Anaconda's Spyder.  Unfortunately, I was not able to get it up and running in the cloud but as long as you some
type of Python compiler, the program should run.  I also created a simple gui using guizero to display the data in a more userfiendly way.
As of right now, running the code would display the gui but I have also provided a few test code segments that will test filtering and 
displaying GeoIP and RDAP lookup data by printing to the console. To run those segments, the code that runs the gui would need to be
commented out and the test code would need to be uncommented.  All of those segments have been labeled.

I used a packages called whois and guizero.  So if you experience problems with those modules, you may have to install them by 
typing these lines into a terminal window:
  python -m pip install -U pip
  
  pip install guizero

  pip install whois
  
Limitations:
  1. The libraries/APIs that I used were very inefficient and would take over to 20 minutes to perform GeoIP and RDAP lookups on 
  each IP.For that reason, I have the program set up only running the first 15 IPs.  I realize this is less than ideal but it shows
  some level of functionality even with a small sample size.  In a second sprint, my primary goal would be to improve the efficiency
  of my program by using different libraries or API's that gather information more efficiently, or even find a way to make the 
  existing methods more practical.  
  2. Because of the limitations with efficiency, the user can only access indicies between 0-14 while requesting GeoIP and RDAP
  lookup data.  Another goal of mine for a second or third sprint would be to allow the user to at least see the GeoIP and RDAP
  lookup data for IPs not in the initial list.







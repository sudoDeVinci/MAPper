# MAPper

Network analysis of user groups within social media platforms may be crucial in determining organic user interest, or uncovering anomalies within spheres of interest within a network.
Potential accounts of interest use twitter, usually only briefly before possibly being being mass-reported depending on their behaviours. During their short lifespans however, these accounts tend to have similar follower lists as they inform their peers of their accounts in off-site chat groups. Some of these accounts however, are more long-lived and well-established. These are generally harder to find for "normal" users and usually employ means to escape immediate detection.
Through the use of network analysis however, we can uncover the web of intertwined user relationships.

## First Run

### Small Sample
This is the output of the data scraped by the first version of MAPper.
This graph was constructed by randomly selecting 3,000 scraped accounts.

The total number of accounts scraped however, is over 20,000.

!['Network Graph'](graphs/network_3000.png)

As we can see, clear circles of interest with a section of overlap are visible. Key accounts can now be selected for directly.

### Large Sample

This is the output of the data sampled from 10,000 accounts. Our same circles of influence are present but here, new overlapping ones are present.

!['Network Graph'](graphs/network_10000.png)

## How it works

MAPper makes use of a scoring system , specific to a target group's language and identifiable symbology. In testing, it was that of the "minor attracted persons" movement known as 'MAPS' along with zoophiles. Each of these groups have their own symbology to alert one another to their activities and beliefs.
MAPper works by first being pointed at a known account of interest. This account is given a score of 1. Each subsequent follower is given a cummulative score dependant on the presence of specific symbols and keywords within their profile. This cummulative score is multiplied by the score of the person which they follow. All scores are between 0 and 1. This continues for all followers of our person of interest. The highest scoring of the followers (who has not been analyzed already) is chosen as the next account of interest.

## Scraping Method

I've chosen the Tweepy Python library for scraping as it provides very useful data structures for easy development. The downside however is that these structures are not very flexible, and the rate limits imposed by the Twitter API are more difficult to circumvent.

### Circumventing Rate Limits

With the rate limits of the Twitter API being account token specific, simply using multiple API keys within multiple processes allows us a faster scraping time, along with a wider net cast for sampling.

## Efficiency

While a single token switching scraping process is capable of indexing multiple thousands of accounts in minutes, certain speheres of interest in a network can span hundreds of thousands of accounts with thousands of connections between each account. This is why I decided to implement the idea of 'Workers'. These are worker processes which are identical, capable of scraping and switching authentication tokens as needed between them. These Workers could then be monitored/deployed/etc from a central controller process.
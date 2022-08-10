# MAPper

## Idea
Network analysis of user groups within social media platforms may be crucial in determining organic user interest, or uncovering anomalies within spheres of interest within a network.
Potential accounts of interest use twitter, usually only briefly before possibly being being mass-reported depending on their behaviours. During their short lifespans however, these accounts tend to have similar follower lists as they inform their peers of their accounts in off-site chat groups. Some of these accounts however, are more long-lived and well-established. These are generally harder to find for "normal" users and usually employ means to escape immediate detection.
Through the use of network analysis however, we can uncover the web of intertwined user relationships.

## How it works

MAPper makes use of a scoring system in the vein of sentiment analysis, specific to a target group's language and identifiable symbology. In testing, it was that of the "minor attracted persons" movement known as 'MAPS' along with zoophiles. Each of these groups have their own symbology to alert one another to their activities and beliefs.
MAPper works by first being pointed at a knwon account of interest. This account is given a score of 1. Each subsequent follower is given a cummulative score dependant on the presence of specific symbols and keywords within their profile. This cummulative score is multiplied by the score of the person which they follow. All scores are between 0 and 1. This continues for all followers of our person of interest. The highest scoring of the followers is chosen as the next account of interest.

## Scraping Method

I've chosen the Tweepy Python library for scraping as it provides very useful data structures for easy development. The downside however is that these structures are not very flexible, and the rate limits imposed by the Twitter API are more difficult to circumvent.

### Circumventing Rate Limits

With the rate limits of the Twitter API being account token specific, simply changing authorization tokens during scraping results in a mostly limit free experience. So far, I have only managed to get 3 accounts approved, but in the future this will be many more, allowing for hours of unlimited scraping potential.

## Improving efficiency

While a single token switching scraping process is capable of indexing multiple thousands of accounts in minutes, certain speheres of interest in a network can span hundreds of thousands of accounts with thousands of connections between each account. This is why I decided to implement the idea of "Nodes". These are worker processes which are identical, capable of scraping and switching authentication tokens as needed between them. These Nodes could then be monitored from a central controller process.

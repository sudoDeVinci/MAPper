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

## Architecture Changes (27/08/2022)
-> Nodes have been renamed to "Workers"

-> Each Worker will be given a general use API key for searching for new persons of interest. 
    
    └> Each API key will be stored as an API_custom object in an Array. These will be used by Workers for getting a user's followers.
    
    └> Each worker will use an API_custom instance by calling pages of followers at a time. Each page can be called separately with different API instances, and each will have a specified number of users. We can look up about 900 users in full per 15 minutes per API instance.

    └> After using an API_custom instance, it's timestamped so we know when last it's been used, and the next available API object with a timestamp over 16 minutes old is used.
    [For simplicity, and because we only have a small number of API keys, we don't reorder the array.] Taking a break to search for a new API instance will only better our chances of not hitting rate limits.
        └> Speed withing the context of MAPper is gained mostly in the ability to bypass rate limits. Any other speed-ups are trivial until a critical mass of api keys is obtained.

## Twitter Policy on collecting API keys (31/08/2022)

So far in my testing, all my Worker accounts have been banned by twitter as their actual use do not match the one specified when I appljied for them as developer accounts. Twitter of course does not like the idea of muktiple accounts being created for the sole intent of circumventing their rate limits.

### Solution

I see a two-tiered approach to solving this as the best option, this being:

1. Create multiple developer accounts and give them actual "work"to do. Instead of the conventional approach of making an account seem more "human", it is far easier to make it seem like a legitimate developer project using the twitter API. These "projects" would aim to be simple and use as few API calls as possible.

2. The second part of this is the fact that each of the accounts being made are from the same computer or at least similar public ip addresses. This is somewhat circumvented when a developer account is used to run a decoy program, but each is still liable to being found out. I would think the solution would be to use proxies and browser header spoofing for accessing the accounts during and after creation for any reason. Using proxies would be easy enough to do through a custom command-line application using the tweepy package. The browser spoofing would be more difficult but is still doable for account creation.

The main cost of this method is my time and my own sanity.



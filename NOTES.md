# MAPper

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



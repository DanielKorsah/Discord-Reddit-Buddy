# Discord-Reddit-Buddy

Discord bot for fetching Reddit posts from a subreddit by category.

Command string:"/r/"

Commands:
* Standard
  - /r/random <subreddit_name> 
    - Gets a random post from [subreddit_name]
  - /r/top <subreddit_name> [number_of_results] 
    - Gets [number_of_results] posts  from Top in <subreddit_name>.  
  - /r/hot <subreddit_name> [number_of_results] 
    - Gets [number_of_results] posts from  Hot in <subreddit_name>.
  - /r/new <subreddit_name> [number_of_results] 
    - Gets [number_of_results] latest posts from the New in <subreddit_name>.
  - /r/controversial <subreddit_name> [number_of_posts] 
    - Gets [number_of_posts] posts from  Controversial in <subreddit_name>.
  - **\*Note [number_of_posts] is optional, if no arguement is given the server default value will be used. This value is 5 until specified by an admin.**

* Admin Settings
  - /r/change_all_settings <default_results_length> <max_results_length> <nsfw> 
    - Sets server's settings, takes 3 ints, nsfw representing a bool using truthiness.
  - /r/get_settings 
    - Return tuple of server settings. 
  - /r/set_default_results <default_results_number> 
    - Set the default number of results returned from reddit requests in current server.
  - /r/set_max_results <maximum_results> 
    - Set the max number of results from a reddit request that may be requested by users.
  - /r/toggle_nsfw 
    - Toggles the boolean setting for whether or not requests may be made to an nsfw subreddit from this server.
  - **\*Note - Server settings default to (default_results_number: 5, maximum_results: 20, nsfw_restricted: 1) where 1 = True.**
 

### Install Link: https://discord.com/api/oauth2/authorize?client_id=722978593147191308&permissions=18432&scope=bot

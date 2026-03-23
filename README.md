##  Debate Topics

### 1. What were the main issues with your current implementation and how would you tackle them?
There are a few limitations with the current approach that I would address in a real-world scenario:

* **JavaScript blindness:** The requests library downloads the site skeleton (static HTML). If the animations or technologies appear after a second, the script will not see them. As a solution, I could use a tool that lets the site load completely and then retrieves the HTML code.
* **Lack of asynchronism at the thread level:** When a request is made, if that request takes a long time, we cannot move on to the next request. A solution would be to change the system with an asynchronous library so we could have a "waiter" who has multiple "tables".

### 2. How would you scale this solution for millions of domains crawled in a timely manner (1-2 months)?
To process millions of domains efficiently, the system needs to move to a better approach:

* **Distributed system:** Instead of multiple threads on a single computer, I would start as many "workers" as possible that continuously pull URLs from a queue, process them, and send them onward.
* **Storage:** If I were to write that much data to a single JSON file, the system would run out of RAM memory. Instead, the workers would write the results directly to a database, where the process would be much more efficient.

### 3. How would you discover new technologies in the future?
I would change the system to go in these ways:

* **Automated Rule Creation:** I could create a system that collects all the meta tags and headers that appear frequently. After many detections,t his technology would automatically enter our ruleset after approval by an admin.
* **Synchronizing with other databases:** I would connect our system to other open-source databases. I could import their files to easily integrate many other rulesets into our system.

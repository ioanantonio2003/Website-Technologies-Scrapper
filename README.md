## Debate topics

### 1. What were the main issues with your current implementation and how would you tackle them?

* **High CPU and RAM usage:** High CPU and RAM usage: Opening many headless browser tabs at once is a drag on the computer. I had to reduce semaphore(10) to semaphore(3) to minimize Timeout errors.

* **Site protections :** Some sites detect and block automated browsers. In the current implementation, 9 HTTP 403 errors occurred.

* **Solution :** I would try to block loading of unnecessary resources (like images) to avoid unnecessary memory usage, and I would use a proxy network to avoid being blocked by sites.

### 2. How would you scale this solution for millions of domains crawled in a timely manner (1-2 months)?

* **Distributed System Architecture:** To process millions of domains, a single local computer is not enough. I would try to change the system to a distributed one. I would run the script on as many servers as possible in the cloud, so that the work is divided and very fast.

* **Abandoning the JSON format:** For storing millions of domains, JSON would consume too much RAM. I would save the extracted data in a database or in files such as parquet format.

### 3. How would you discover new technologies in the future?
* I would continue to rely on the script created for this project (build_signature.py) but trying to extend it to learn the "rules" of more communities. That way every time a new framework appears and the community introduces it, our script starts and our "rules" are updated

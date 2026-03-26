### Methodology and evolution of the project

The project is divided into 5 parts:

1. Data preprocessing:
   * The dataset was provided in parquet format. I used the pandas library to read the file and extract the domains.
   * The raw domains (e.g., example.com) went through a normalization process, so the "https://" protocol was added to each one to ensure the format necessary for HTTP requests.

2. The ingestion engine (requester.py):
   * The initial approach was to make classic HTTP requests (using the requests library), implementing a User-Agent (simulating a real browser) to avoid Anti-Bot filters. I added error handling blocks to manage errors. I managed to extract the static HTML code and headers.
   * Since I considered that the HTML code and headers were not enough, I started to extract cookies as well as global JavaScript variables.
   * The biggest change was the switch to Playwright. Modern websites often send HTML code that is later populated with JavaScript. Using Playwright, we could wait for the full rendering of the page, making it easier to find new technologies.

3. Ruleset (build_signature.py):
   * Initially, signature.json only held a few basic rules. I realized that this solution was not very good, so I built a data pipeline.
   * The script managed to process the massive database from webappanalyzer.
   * I extracted and structured the rules into several categories: headers, cookies, html, scripts, dom, and js.

4. Analysis and Evidence Extraction (analyzer.py):
   * The data from the website and the ruleset had to be intersected, so I created a class for analysis.
   * I used the BeautifulSoup library to be able to easily navigate the raw HTML code.
   * I built functions for each component to look for specific patterns: headers_analyzer, cookies_analyzer, js_analyzer, html_analyzer (which also extracts information from metas), and CSS selectors for certain technologies.
   * I used the re library to find proofs.

5. Execution, Concurrency, and Asynchrony (main.py, requester.py):
   * I started by processing a single domain to validate the script.
   * In order to have an efficient approach, I introduced ThreadPoolExecutor, allowing multiple threads to run in parallel. Although it is fast, the resource consumption is high (especially for a project where you have a lot of data).
   * The final architecture used asyncio. Now the system launches a single Playwright browser and only opens new tabs for each site. I used semaphores to avoid overloading the processor. Semaphore(3) had much fewer Timeout errors. Even if we could put 10 workers at once for ThreadPoolExecutor, I think this is the more efficient method (if the processing power was higher, the execution time would decrease, and if there was more data, the difference in resource consumption would be significant).


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

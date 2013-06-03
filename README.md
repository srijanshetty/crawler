#Intro
Final Submission for the crawler project for CS252

#Contents

conf_crawl.py: the original dfs traversal version. (In hindsight, dfs is
                a very bad idea for crawling.)
bfs_crawl.py: the latest version, does a bfs traversal after querying
                from google.
blacklist.txt: Stores a list of urls which have to be ignored while
                crawling

#Usage

python bfs_crawl.py "Search Query" "Depth of crawl"

#Acknowledgement

I have use the git repo https://github.com/MarioVilas/google.git,
for implementing google search

#To do:
Use Markdown for the README

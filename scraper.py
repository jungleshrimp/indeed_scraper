import requests
from bs4 import BeautifulSoup


# Soup main page
def find_jobs(job, page):
	phrase = job.replace(" ", "+")
	page = page * 50
	site = "https://www.indeed.co.uk/jobs?q={}&limit=50&start={}".format(phrase, page)
	r = requests.get(site)
	soup = BeautifulSoup(r.text, "html.parser")
	return soup


# Getting all jobs IDs
def jobs_id(fun_soup):
	jobs = fun_soup.find_all("script")
	jobs = [str(x) for x in jobs]
	jobs = [x for x in jobs if "jobKeysWithInfo" in x]
	jobs = [x.split("\n") for x in jobs]
	jobs = jobs[0]
	jobs = [x for x in jobs if "jobKeysWithInfo['" in x]
	jobs = [x.replace("jobKeysWithInfo['", "").replace("'] = true;", "") for x in jobs]
	return jobs


# Checking for last page
def last_page(soup):
	next = soup.find_all("div", {"pagination"})
	next = str(next).split("</li>")
	next = [x for x in next if "Next" in x]
	if next:
		return False
	else:
		return True


if __name__ == "__main__":

	pg = 0
	while True:

		print(pg)
		job = "python developer"
		test = find_jobs(job, pg)
		my_list = jobs_id(test)

		with open('jobs.txt', 'a+') as f:
			for item in my_list:
				f.write("%s\n" % item)

		if last_page(test):
			break

		else:
			pg = pg + 1

The three modifications in the .py file have been marked in the file (both in initialization):

1. The replacement must be modified:
    Replace self.browser.get(" ") with the comment page link for the desired crawled item

2. Must be modified and replaced
    self.ASIN = '' replaced with the ASIN of the item being crawled
    self.CsvFileName = 'test.csv' replaced with custom file name

3. Can be modified and replaced
    self.CsvN = for counting -- the current number of crawled pages



Note: The domestic network is very easy to interrupt, sometimes it will be unstable with VPN; if it is interrupted, replace the link in self.browser.get(" ") with the currently broken page number link. After continuing to crawl, the content will continue to be written in the csv file, but the code that sets the first line of the csv file will be executed again. You can comment out this code, or leave it alone, and then remove it.
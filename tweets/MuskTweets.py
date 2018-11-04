import csv
import datetime
import os

with open("/home/matthew/Documents/Data Mining Project/elonmusktweets.csv", 'r') as muskTweets:
    tweetReader = csv.reader(muskTweets, delimiter=',')
    line_count = 0
    for row in tweetReader:
        if line_count == 0:
            print(f'Column names are {", ".join(row)}')
            line_count += 1
        else:
            splitWords = row[1].split(' ')
            dateOfTweet = splitWords[0].split('-')
            week = datetime.date(int(dateOfTweet[0]), int(dateOfTweet[1]), int(dateOfTweet[2])).isocalendar()[1]
            print(week)
            print(f'{row[2]}\n\n')
            if not os.path.exists('/home/matthew/Documents/Data Mining Project/%s/%s' % (dateOfTweet[0], week)):
                os.makedirs('/home/matthew/Documents/Data Mining Project/%s/%s' % (dateOfTweet[0], week))     
            fileWriting = open('/home/matthew/Documents/Data Mining Project/%s/%s/tweets.txt' % (dateOfTweet[0], week), 'a')
            fileWriting.write(f'{row[2]}\n')
            line_count += 1
    print(f'Processed {line_count} lines.')

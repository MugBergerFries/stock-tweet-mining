today=`date +%Y-%m-%d.%H:%M:%S`
twurl "/1.1/search/tweets.json?q=elon%20musk&count=100" > "elonmuskMentionsTwitter$today.json"
twurl "/1.1/search/tweets.json?q=tesla&count=100" > "tesla$today.json"
twurl "/1.1/search/tweets.json?q=@elonmusk&count=100" > "elonmuskUserAccount$today.json"
twurl "/1.1/search/tweets.json?q=@tim_cook&count=100" > "timcook$today.json"

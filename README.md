# Tap-news
A Real Time News Scraping And Recommendation System

![image](https://github.com/alexjianghuiting/Tap-news/blob/master/Pasted%20Graphic%2088.png)

## Run
cd into client ```npm install``` ```npm run build```

cd into server ```npm start```

```./news_pipeline_launcher.sh```

## Used
Front-end: React

Back-end: python RPCServer, redis, express, mongodb, RabbitMQ
  
>use redis to check if it's already scrapped
  
>use watchdog to observe the update in the model

>use RabbitMQ to fetch and send news message

Model: NLP, DNN, Tensorflow
  
>use to predict the topic 

>update user's preference from their click events by using Time decay model p = (1-α)p + α & p = (1-α)p

>use pairwise_sim = tfidf * tfidf.T to de-duplicate similar news

# REALISER

## Project Status

REALISER was originally submitted as an ideation for [Splash Awards 2022](https://www.scs.org.sg/awards/splash/2022/) by Team NoFakeNews, a duo. After 3 months of planning, programming, and pitching, REALISER eventually rose to become one of the 12 finalist projects in the competition.

Given the commencement of the competition, REALISER is no longer in development and preserved in an archived repository. Most of the code that was written (AI model, REST API, web scraper, browser extension) can be found within this repository.

Beware broken, outdated, and messy code. Dwelve at your own risk.

## Contents
- [REALISER](#realiser)
  - [Project Status](#project-status)
  - [Contents](#contents)
  - [Introduction](#introduction)
  - [Motivation](#motivation)
  - [Project Details](#project-details)
    - [Front-End](#front-end)
    - [Back-End](#back-end)


## Introduction

REALISER is (was) an AI-powered browser extension that detects fake news.

## Motivation

Fake news can be extremely malicious, inculcating misinformation into those who believe it. Amid the COVID-19 pandemic, fake news has spread rapidly within many communities. As more people pay attention to news, during the pandemic, the general population is more susceptible to the intake of fake news. 

[Local](https://www.straitstimes.com/singapore/4-in-5-singaporeans-confident-in-spotting-fake-news-but-90-per-cent-wrong-when-put-to-the) [surveys](https://www.straitstimes.com/tech/tech-news/many-in-singapore-confident-they-can-spot-fake-news-but-may-not-actually-be-able-to-study) conducted in Singapore by The Straits Times between 2018 and 2022 showed that although most Singaporeans were confident in identifying legitimate news, approximately 50% of Singaporeans **still failed** to detect fake news when put to the test. Moreover, an overwhelming 75% of Singaporeans **unknowingly shared** fake news to others.

This is not to say that there have not been solutions implemented in Singapore to tackle the worsening issue of fake news and misinformation. Such solutions include:
- [Factually by gov.sg](https://www.gov.sg/factually), a government website that points out falsehoods
- [POFMA Office](https://www.pofmaoffice.gov.sg/), a government agency that aims to protect the public from misinformation
- [VeriFactSG](https://twitter.com/VeriFactSG), a crowdsourced fact-checking platform
- [Black Dot Research](https://blackdotresearch.sg/), a social research agency that focuses on SIngaporean news 

However, the solutions mentioned above require **manual effort**, which can be **slow and ineffective** when the speed at which fake news is manufactured and spread is taken into account.

Therefore, REALISER was created to prevent the spreading of fake news and improve the quality of social perspectives held by social citzens in a quick and effective manner.

## Project Details

REALISER is split into two parts: the front-end browser extension (which is largely unfinished), and the back-end AI model and REST API (which is a fully functioning prototype).

### Front-End

The front-end parts of NoFakeNews consists of a [browser extension](./extension/) for major web browsers such as Chrome and Firefox where we automatically scan the headlines and embeds of news articles and inform users of potential fake news.

It was planned for users to be alerted of the legitimacy of the news article that they were viewing with the use of a 5-verdict system: icons that would appear on the website in accordance with the validity of the article as predicted by the AI model.

It was also planned for users to be able to provide feedback on the AI model's performance through the browser extension. This would allow the AI model to undergo re-evaluation and stay relevant even with more contemporary news.

### Back-End

The back-end parts of NoFakeNews, where we implement a [NLP artificial intelligence model](./model/) into a [deployed Flask REST API web application](app.py) so that necessary data can be easily sent and retrieved through the browser extension. 

The model was trained with over 11,000 news articles from both Singaporean and international news sources using a Word2Vec logistic regression approach. Genres included politics, entertainment, healthcare (with an emphasis on COVID-19), crime, and the job market. 

The average accuracy score of the model across several rounds of evaluation and testing turned out to be 0.92.

Furthermore, a [web scraper](./scraper/) was built for data collection that went into the supervised training of the AI model. Websites scraped consisted of ChannelNewsAsia, The Straits Times, which serve as "real news" websites, as well as The Onion, which serves as a "fake news" website. Articles of different genres were scraped to ensure that the AI model would work with multi-genre news.

It was planned for a cloud database to be implemented so that anonymous user data and feedback could be stored securely. This would allow for the re-evaluation of the model from time to time.


 



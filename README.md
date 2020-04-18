# Pierre: The Presentation Assistant
created at Enghacks 2019 in 48 hours by Penny Ji, Andrew Mourcos, Aidan Philpott and Robert Toyonaga.

#### What's the idea?
Pierre helps people to **overcome public speaking anxiety** by improving their presentation skills and giving them confidence.

Pierre is a presentation tool that makes use of natural language processing as well as computer vision heuristics in order to make you a better speaker. In real time, Pierre is able to catch utterances (ex: 'like', 'um', 'literally', ...) and visual nervous ticks (swaying, tapping, ...) which distract from your presentation. As Pierre catches these faults, he alerts the speaker in real-time (while practicing) via smartphone notifications and can display analytics afterwards.

#### How we built it
PocketSphinx was the framework used for live NLP, OpenCV was used to develop image processing heuristics for "tick detection" and Stdlib was used for notifying the speaker during the presentation and as a database for analytics.

#### Interaction design
Proper user research was conducted in order to evaluate the effectiveness of Pierre as a presentation tool. Additionally, several people at the event were interviewed in order to validate the utility of our solution.

#### What's next for Pierre: The Presentation Assistant
We will be conducting more user research to help us with our product direction. The next big update will be the addition of a GUI that allows users to view their live data as they are presenting and also compare their recent sessions. Additionally, we will be doing some research to develop more robust tick/utterance detection algorithms.

## Want to try it? 
Clone/download this repository and make sure you have Python3 (atleast 3.4) installed.
Use pip to collect the necessary dependancies:
```pip3 install -r requirements.txt```

Run main.py and give it a shot!

Note: we won't open up our STDlib API calls (to get SMS presentation feedback) for the time being. If you would like to try this feature, please contact one of the creators. The current demo will, however, show the equivalent feedback on the computer screen.

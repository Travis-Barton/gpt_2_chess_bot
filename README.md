# gpt_2_chess_bot
 Lets play a very bad game of chess in an interesting way!
 
 __The repository for the Medium Article [here](https://medium.com/@tbarton_16336/teaching-a-language-model-to-play-chess-1ea69dde40fd?source=your_stories_page-------------------------------------).__
 
Wanted to know what a chessgame looks like when you don't know the rules and only know what to play based on 10s of thousands of examples? Well look no further! 


Before you can run `the_bot.py` you have to train a model with `GPT2Mod.py`. The training will take some time but it only needs to be run once! 

To play a game post training simply run `python the_bot.py --player_color={'white' or 'black' or None if you want it to play itself}`

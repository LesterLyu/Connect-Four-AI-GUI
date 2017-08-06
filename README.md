# CSC384 Project
# TODO
## Back-end / Algorithm
 - [ ] Fix alpha-beta prune
 
## GUI
 - [ ] Add finish game dialog
 - [ ] Prevent user click when computer is thinking
 - [ ] Finish implement difficulty
 - [ ] Change "X" and "O" to images
 
  ### Hint
  - GUI must run on the main thread, back-end operations must run on other threads other than the main thread.
  - Once the windows shows, the code after display the windows will be blocked forever until the window closes


## Others
 - [ ] try to win the AI with difficult=4; if you won, try to fix the bug in heuristic function, and copy how you won.
 - [ ] Add run.sh script that make sure TA will be able to run the game with python3.5



# HOW TO USE
### two player mode
```
connect_four = ConnectFour(0, "Jerry", "Lester")
connect_four.play()
```
### one player vs AI
```
connect_four2 = ConnectFour(1, "Jerry", difficulty=3)
connect_four2.play()
```

--------
Due August 14, 11:59 p.m.
+ Useful links:
  - https://en.wikipedia.org/wiki/Connect_Four
  - https://www.gimu.org/connect-four-js/plain/minimax/index.html
  - https://github.com/cl4rke/connect-four-minimax
  - https://roadtolarissa.com/connect-4-ai-how-it-works/

## The Project Report(Due: August 14) (submitted as csc384-project.pdf)
### 1. Each report must have a title page containing the following information:
  - Title of the Project;
  - The names and teach.cs-login IDs of all team members;
  - The roles played by each member of the team (e.g. problem encoding, experimental assessment,
manuscript author, ...) and whether they were major or minor roles;
  - Type of Project: the problem solving technique employed, i.e., Search, Game Tree Search, CSP,
Bayes Net, KR, or Other.
### 2. Following the title page, include a report body. This can be a maximum of 5 single-spaced pages, formatted in 12pt font. Sections for the report body should be as follows:
- **Project Motivation/Background.** Here, you will describe the problem you are trying to solve
or the application you are trying to create. Also describe your approach to the problem (e.g.
Search, Game Tree Search, CSP, Bayes Nets, KR or other) and the rationale for choosing this
approach.
- **Methods.** Here, describe the details of your realization. How did you formulate your problem
and what algorithms did you employ to solve it? For example, depending on your problem type
you may need to describe your state encoding — what are the state variables and domains; what
are the successor functions; how you encoded your constraints (and why). If you developed
heuristics, describe whether they are admissible or not and any other properties they have. The
above are just examples and are not exhaustive.
- **Evaluation** and Results. Here, describe your evaluation objectives and strategy, and your
results. In particular, describe the way you’ve chosen to evaluate your approach (i.e. how you
will determine if your approach works). Evaluation metrics could include the number of nodes
expanded in a search algorithm or the amount of time or memory that you used. We encourage
the use of diagrams, graphs, and/or tables to summarize experimental results and to convey
important points. Note that it’s ok if your system proves to be inefficient in some way; that’s
still a result and we want to know. In addition to graphs and tables, provide a written summary
of your findings and their implications, if any.
- **Limitations/Obstacles.** Here, document any obstacles you encountered during your implementation
or shortcomings you discovered in your solution approach.
- **Conclusions.** Finally, explain what you learned and how you might improve or modify your
program were you to try again in the future. Other reflections are welcome.
### 3. You may include up to 2 additional pages after the report body for citations and references or any other attributions or acknowledgements.
## The Project Source Code (Due: August 14) ( submitted as csc384-source.zip)
The realization of your project must run on teach.cs. All source code to run your completed project on
teach.cs must be submitted, together with a README file explaining how to run the code, in a single zip file.

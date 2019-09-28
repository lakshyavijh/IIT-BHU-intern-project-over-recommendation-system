# IIT-BHU-intern-project-over-recommendation-system
We have done experiments which are as follows:
•	Implemented basic Hidden Markov Model for POS tagging over English language to learn the basics and get ideas about HMM.
The model returns the part of speech for every word in a sentence passed to it based on the previous record in which part of speech it was used.
•	Implementation of Knowledge Based Context Graph system has been tried. We Created a Knowledge graph based on our dataset using software known as ‘Neo4J’ which is a graph based management database used for creating graphs according to ones need. Though the work of knowledge graph based system was not completed as such we did not got the further resources that was needed to implement that model. The idea was taken from a paper [9] who applied the proposed Knowledge Graph Convolutional Networks with Label Smoothness regularization (KGCN-LS) to four real-world scenarios of movie, book, music, and restaurant recommendations.
•	Using the basic idea of Hidden Markov Model, we implemented the idea to our dataset to recommend items.
The algorithm is as follows:
Input: The dataset containing the item and its properties and user-item sequence.
Output: List of recommended items.
1.	Preprocessing the data to convert it into the vector form of 0 and 1.
2.	Properties are taken as context and hidden states refer to contexts.
3.	Finding the emission and transition probability.
4.	For every user:
?	Find the context related to the item belonging to that user having highest transition probability.
?	For that context find the next context which is highly related to previous context using emission probability.
?	Then from that context find the next item which is highly related to that context and recommend that item.
This will give the top-k recommended items to a user.
Now let’s take an example to understand the algorithm.
•	Consider a user-item sequence as:

	Item1 	Item2 	Item3 	Item4 	Item5 
User1 	1 	1 	0 	0 	0 
User2 	1 	0 	1 	1 	1 
User3 	0 	0 	1 	0 	1 

ss
•	Select a user from that sequence:


	Item1 	Item2 	Item2 	Item4 	Item5 
User1 	1 	1 	0 	0 	0 

•	For User1 consider Item1 , find the emission probability for that Item1 form training data:
    
	5 star 	A.C 	Pool 	T.V 	Wi-Fi 	Lawn 
Item1 	0.7 	0.75 	0.85 	0.9 	0.74 	0.45 

•	Find the max among them , in our case its T.V and find the transition probability corresponding to T.V



	5 star 	A.C 	Pool 	Wi-Fi 	lawn 	
T.V 	0.45 	0.78 	0.65 	0.88 	0.40 	

•	Now select the Context having highest probability corresponding to TV. 
•	Here it is Wi-Fi 
•	Now corresponding to Wi-Fi find the Items.

	Item3 	Item4 	Item5 	Item6 	Item7 
Wi-Fi 	0.8 	0.45 	0.32 	0.78 	0.64	

•	Now from this we recommend Item3 to user.
•	Similar process goes on and on .

1. How can I learn more about the relationship types in KGs? For e.g., what does gene-corelates-gene mean? pathways-upregulates-gene?
2. What does link prediction actually entail? Does it mean coming up with new relationships/paths/nodes? Can I see this in practice somewhere? Is there code I can go through that does this at a small scale to get an intuition?
3. Pointers to potential future work? Finding side effects of proposed drugs? Finding combinations of drugs that "amplify" effect, or don't work well together? 
4. 


Pathways - gene 

Structure of report:
Limitations, future work, summaries of techniques. Which methods exist for KGs and KGs for drug repurposing?


1. Which embeddings are used most in practice? Which ones have we (at ULB) used in the past for our research?
2. What do these similarity matrices mean in "2020 Biological applications of knowledge graph embedding models"? Page 9 - how do you read these graphs?


t-distributed stochastic neigbor embedding
PCA - ?

Next steps:
1. Finish overview Latex
2. Go over the KGE paper Inas shared
2. Outline of the prep work/review, narrative, connect diff pieces
    - look at the review paper again for the structure
3. Figure out future work


More questions:
1. The predictions and connections that result from a ML algo - how are they actually verified exerimentally? what is the criteria for them to qualify for this? do we work with any bio lab for this?
2. Scope of master thesis work
3. How KG data is validated/do we just take it for what it is (it's out of scope for us)
4. 


Flow of prep work for master thesis:-
1. Background and objective of the thesis, I can talk about what knowledge graphs and KGEs are. What drug repurposing means and why it's important, and how KG/KGEs can be used for this purpose. TODO Do I need to explain the different KGEs or assume that is not in scope?
2. Notation/abbreviations? TODO Check if there are any non-obvious ones
3. State-of-the-art overview: what different methods and approaches have been used, and how successful are they? What methods have been used in ensemble? Prob the biggest part of the report. ALso mention XAI in this: Explainability and XAI, why it's relevant in this field. Maybe could be a part of the previous section.
4. What are the problems in drug repurposing? Why is it hard, and what limitations do KG/KGEs have? What is the basic problem(s) we need to solve, what makes this difficult? 
5. In response to 3: Which of these methods show the most promise, what are their limitations and what could possible solutions to these problems be?
6. Preliminary testing of some methods, and how promising results could be, comparison?
7. Concrete directions the master thesis could take, or at least next steps of investigations?


Next steps:
1. Find 3-4 papers I like and see what changes i could propose to make. Small presentation for Prof Tom
2. Start writing the report



-> Incorporate the schema into how i figure out the 

data -> embedding method -> features -> classifier? -> link-prediction for drug-to-disease

embedding method can have various inputs: random walks, RL with random walks, other?
classifier can be various things: SVM (best performance), NN, RL, CNN, GNN, XGBoost, etc.


Questions for Inas:
1. we are building a classifier right? where the classes are the output diseases and the inputs are drugs?
2. citations - are 64 enough?
3. ablation testing - some papers do not have this, so hard to judge them empirically
4. how do you visualise embeddings esp random walk embeddings?
5. gut feeling about research direction, what areas still need to be explored?


KGE models:
random walk vs scoring func (50, 100, 200 dimensions?)

some random walk method
transE
distmult(prefered)/complEx
another path based one?

to combine drug+disease vectors, just concat (always same order)



classifiers:
svm
mlp/gnn
xgboost



## Prediction error

- The Paranoid Optimist: An Integrative Evolutionary Model of Cognitive Biases - Martie G. Haselton, Daniel Nettle
	- https://journals.sagepub.com/doi/pdf/10.1207/s15327957pspr1001_3
	- Review paper of Prediction error modelling and its implementations. Also shows some mathematical basis, but that might not be suited for opinion spreading.


## Opinion spreading

- OPINION EVOLUTION IN CLOSED COMMUNITY - KATARZYNA SZNAJD-WERON
	- https://www.worldscientific.com/doi/pdf/10.1142/S0129183100000936
	- Describes the Sznajd model for agent based opinion spreading built on the Ising model. It's an approach different from ours, but may be inspirational.


- OPINION SPREADING AND CONSENSUS FORMATION ON SQUARE LATTICE - JIAN-GUO LIU , ZHI-XI WU and FENG WANG
	- https://www.worldscientific.com/doi/pdfplus/10.1142/S0129183107011145?casa_token=Qr-ekFcWmCEAAAAA:wfvY77_pTl9tOCO5Z128IYixF8oN4bc5GjBknEPL1kKULyxc1l9HdUbEACJ5XYDz9rmTkv-g0p0
	- Basic agent-based model for opinion spreading. Could be useful for inspiration.


- Network Models of Minority Opinion Spreading: Using Agent-Based Modeling to Study Possible Scenarios of Social Contagion - Javier Alvarez-Galvez
	- https://journals.sagepub.com/doi/pdf/10.1177/0894439315605607?casa_token=M2Q4h2HEfWQAAAAA%3AIZvA6whTROB7VpMU-dM4X1E6-EidIWe9o9cJu8rDrW7XLm5HK55pCDAZElCRQzSHVmADhzpedn7z
	- Another agent-based model of opinion spreading, in a network scenario. This one focusses on the spreading of unpopular opinions.


## Network Reformation

- Coevolution of agents and networks: Opinion spreading and community 
disconnection - Santiago Gil, Damián H. Zanette
	- https://www.sciencedirect.com/science/article/pii/S037596010600418X
	- Discusses how agents can affect each other opinions and even 
how a network-based model may change the network over time based on 
similar opinions.
~~~~
For each step:
	For every two connectedagents:
		if agents agree:
			Continue
		else:
			if P1:    (P1 is a probability)
				Opinion is changed
			else:
				opinions not changed
				if P2:    (P2 is a probability)
					Break edge between the two agents
~~~~
	- This would be very interesting to implement when opinion holds a continuous value, as P1 and P2 will then also depend on the difference in opinion.

- Barabasi-Alberts model
	- Couldnt find the original paper, but http://barabasi.com/f/622.pdf is useful.
	- Creates new nodes and interconnects them with a probability based on the degree of every node. Only useful when building the initial network.
		- Chance that new node connects to i is P(i) = K<sub>i</sub>/(&sum;<sup>N</sup><sub>j=0</sub> K<sub>j</sub>), where K<sub>i</sub> is the degree of node i.
		- Also check out Bianconi-Barabasi model where fitness is added.

- Watts-Strogatz model
	- Starts with a circle of nodes with edges between the k closest neighbours. Then randomly rewires all edges. Appearantly very good, but probably not interesting for this project.


- Damage Spreading and Opinion Dynamics on Scale Free Networks - Santo Fortunato
	- https://arxiv.org/pdf/cond-mat/0405083.pdf
	- Constructed a Barabasi-Alberts model, and initiated random opinions on interval [0,1]. Every neighbouring agent shares opinion s<sub>i</sub> with j only when |s<sub>i</sub> - s<sub>j</sub>|<&epsilon;, where &epsilon; was set to 0.5 in this case.

- OPINION DYNAMICS AND BOUNDED CONFIDENCE MODELS, ANALYSIS, AND SIMULATION - Rainer Hegselmann 
	- https://www.math.fsu.edu/~dgalvis/journalclub/papers/02_05_2017.pdf
	- Describes dynamics of several opinion spreading models, but I dont get the math. 

- CONTINUOUS OPINION DYNAMICS UNDER BOUNDED CONFIDENCE: A SURVEY - JAN LORENZ
	- https://www.worldscientific.com/doi/pdfplus/10.1142/S0129183107011789?casa_token=1cmqrEeTgL0AAAAA:7u0ENlcrv-KSoc3gBp-4KJo2CnZ49IEkIE-0_kHLIcxgfS9Xt7G4WOxpGjrP_JwQmpgjNEHbuPY
	- opinion dynamics according to the Deffuant-Weisbuch model and the Hegselmann-Krausse model
	- Like other articles describe, the similarity in opinion will affect the consequence.
		- In case of the DW-model, if opinions i and j are similar, they both become the average of the two, else, nothing happens. We can easily make a hawk-dove game were the probability to be hawk or dove relies on the difference in opinion, where two doves try to find a middle ground, hawks direct doves to new opinions and hawks become polarised when they meet each other as they are not willing to agree and therefore tend to radicalize.
		- In case of the HK-model, opinion i becomes the average of all opinions that do not differ more than &epsilon;.

- There is a bunch of Ising-model-based-models which state that the opinion-change depends on the number of neighbours with a certain opinion. Although I think that these models are not entriely suited to this project, we may eventually implement such an effect. (See the Sznajd-model under the second header.)

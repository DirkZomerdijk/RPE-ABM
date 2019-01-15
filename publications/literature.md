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
	- Creates new nodes and interconnects them with a probability based on the degree of every node.
		- Chance that new node connects to i is P(i) = K<sub>i</sub>/(&Sigma;<sup>N</sup><sub>j=0</sub> K<sub>j</sub>), where K<sub>i</sub> is the degree of node i.

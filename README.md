{\rtf1\ansi\ansicpg1252\cocoartf2708
\cocoatextscaling0\cocoaplatform0{\fonttbl\f0\fswiss\fcharset0 Helvetica;}
{\colortbl;\red255\green255\blue255;}
{\*\expandedcolortbl;;}
\paperw11900\paperh16840\margl1440\margr1440\vieww11520\viewh8400\viewkind0
\pard\tx566\tx1133\tx1700\tx2267\tx2834\tx3401\tx3968\tx4535\tx5102\tx5669\tx6236\tx6803\pardirnatural\partightenfactor0

\f0\fs24 \cf0 # Multi-Agent Public Goods Challenge\
\
## Project Overview\
\
This project simulates an N-Person Public Goods Game to explore cooperative behaviors, strategic decision-making under uncertainty, and social dynamics among autonomous agents. The simulation uses personality traits like risk willingness and adaptability to model real-world decision-making processes.\
\
## Authors and Contributors\
\
  - Amelie Oberkirch \
  - Lucas Neves \
  - Rafael Maciel \
\
## Abstract\
\
The simulation aims to understand the dynamics of agent behavior in different scenarios and identify optimal personality traits for success in Public Goods Games. The agents adjust their risk appetite based on observed actions and received rewards, simulating real-world decision-making processes.\
\
## Gameplay Mechanics\
\
### Setup\
\
- The game is played with 4 players, each starting with 10 coins, over 10 rounds.\
- Players decide how many coins to contribute to a communal pot, which is then multiplied by a factor and redistributed.\
- A scoreboard displays each player's rank, coins, and contributions after each round.\
\
### Personality Traits\
\
- **Risk Willingness**: Indicates how much an agent is willing to contribute at the risk of punishment. Free riders have high risk willingness.\
- **Adaptability**: Indicates the agent's capacity to adapt its behavior based on the game's evolution and other agents' actions.\
\
### Punishment Mechanic\
\
- The agent with the least contribution to the communal pot does not receive their share of the split money, encouraging higher contributions.\
\
## Code Structure\
\
The project is implemented using Python, with the main components organized as follows:\
\
- **main.py**: The main script to run the simulation.\
- **agents.py**: Contains the implementation of agent behaviors and personality traits.\
- **environment.py**: Manages the game environment, including the communal pot and scoreboard.\
\
## Installation\
\
1. **Clone the Repository**:\
   - Open a terminal and clone the repository with the following command:\
     ```bash\
     git clone https://github.com/your-username/public-goods-challenge.git\
     ```\
   - Navigate into the project directory:\
     ```bash\
     cd public-goods-challenge\
     ```\
\
2. **Set Up the Environment**:\
   - Ensure you have Python installed (preferably version 3.7 or higher).\
   - Install the required dependencies:\
     ```bash\
     pip install -r requirements.txt\
     ```\
\
3. **Run the Simulation**:\
   - Start the simulation with the following command:\
     ```bash\
     python main.py\
     ```\
\
## Empirical Evaluation\
\
The project evaluates the effectiveness of various strategies induced by different personality traits in addressing collective action problems. Key evaluation metrics include:\
\
- **Win Percentage**: The percentage of wins by agents considering their personality traits.\
- **Evolution of Risk Willingness**: Changes in risk willingness of each agent over time.\
- **Evolution of Scoreboard**: The position and wealth of each agent in the scoreboard throughout the game.\
- **Correlation between Adaptability and Final Money**: The relationship between an agent's adaptability and their final wealth.\
- **Correlation between Risk Willingness and Final Money**: The relationship between an agent's risk willingness and their final wealth.\
\
## Technologies Used\
\
- **Python**: Main programming language used for the simulation.\
- **Matplotlib**: Library used for plotting graphs and visualizing results.\
\
## Conclusion\
\
This simulation study highlights the significant role of personality traits, particularly risk willingness and adaptability, in shaping cooperative behavior and strategic decision-making in Public Goods Games. High adaptability emerges as a critical factor for success, enabling agents to effectively respond to the dynamic game environment. These findings contribute to a deeper understanding of social dynamics in multi-agent systems and offer practical insights for fostering cooperation in real-world collective action problems.\
}
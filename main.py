
import numpy as np
import matplotlib.pyplot as plt
import tkinter as tk
from tkinter import messagebox
from tkinter import simpledialog


#########################################################
####                       AGENT                    #####
#########################################################

class Agent:
    def __init__(self, name, risk_level, adaptability, initial_money=10):
        self.name = name
        self.risk_level = risk_level
        self.adaptability = adaptability
        self.money = initial_money
        self.initial_money = initial_money
        self.risk_history = [risk_level]  # Store risk levels over rounds
        self.beliefs = {}
        self.money_history = [initial_money]
        self.received_money_this_round = False  # Track if money was received this round

    def adjust_risk_appetite(self, received_reward):
        average_belief_risk = np.mean(list(self.beliefs.values()))
        profit = self.money - self.initial_money

        adaptability_factor = 10  # A constant factor that adjusts the influence of adaptability
        adaptability_effect = adaptability_factor * self.adaptability

        # Adjusting risk levels based on perceived risk and profit

        if self.initial_money != 0:
            if received_reward:
                if average_belief_risk >= 0.5 and profit > 0:
                    self.risk_level += adaptability_effect * 0.02 * (profit / self.initial_money)
                elif average_belief_risk < 0.5 or profit < 0:
                    self.risk_level -= adaptability_effect * 0.02 * (abs(profit) / self.initial_money)
            else:
                # Reduced punishment if no profit was made
                self.risk_level -= adaptability_effect * 0.03 * (1 + abs(
                    profit) / self.initial_money)  # Slightly increased penalty compared to normal loss adjustments

        self.risk_level = np.clip(self.risk_level, 0, 1)
        self.risk_history.append(self.risk_level)
        self.initial_money = self.money

    def update_belief(self, agent_name, action):
        # Retrieve current belief about the specified agent
        current_belief = self.beliefs[agent_name]
        max_action = 10  # Maximum contribution possible

        # Define likelihoods based on observed action
        likelihood_risk_averse = action / max_action  # Higher actions imply risk aversion
        likelihood_risk_seeking = 1 - likelihood_risk_averse  # Lower actions imply risk seeking

        prior_belief = current_belief
        # Bayesian update of beliefs, adjusting based on observed action
        if action > 0:
            posterior_belief = prior_belief * likelihood_risk_averse / (
                    prior_belief * likelihood_risk_averse + (1 - prior_belief) * likelihood_risk_seeking)
        else:
            # If action is 0, consider it highly risk-seeking
            posterior_belief = prior_belief * likelihood_risk_seeking / (
                    prior_belief * likelihood_risk_seeking + (1 - prior_belief) * likelihood_risk_averse)

        # Update the belief with the new posterior
        self.beliefs[agent_name] = np.clip(posterior_belief, 0, 1)

    def initialize_beliefs(self, agents):
        # Set initial beliefs about every other agent to 0.5
        for agent in agents:
            if agent.name != self.name:
                self.beliefs[agent.name] = 0.5

    def observe_actions(self, actions):
        # Update beliefs based on the observed actions of other agents
        for agent_name, action in actions.items():
            if agent_name != self.name:
                self.update_belief(agent_name, action)

    def decide_action(self):
        # Calculate base contribution as a percentage of available money based on own risk aversion
        base_contribution_percentage = 1 - self.risk_level
        base_contribution = self.money * base_contribution_percentage

        # Combine own risk willingness with the average perceived risk willingness
        average_perceived_risk = np.mean(list(self.beliefs.values()))
        weighted_risk = (1 - self.risk_level) * 0.5 + 0.5 * (1 - average_perceived_risk)

        # Determine the contribution based on weighted risk assessment, normalized to current money
        contribution = np.random.normal(loc=weighted_risk * base_contribution, scale=1)
        if np.isnan(contribution):
            contribution = 0
        contribution = int(np.clip(contribution, 0, self.money))

        print(f"{self.name} puts {contribution:.2f} in the pool.")

        return contribution

    def receive_money(self, amount):
        # Add received money to the agent's total money
        self.money += amount
        print(f"{self.name} receives {amount:.2f} money.")


#########################################################
####                   ENVIRONMENT                  #####
#########################################################

class Environment:
    def __init__(self, agents):
        self.agents = agents
        self.round_number = 0

    def get_scores(self):
        ranked_agents = sorted(self.agents, key=lambda agent: agent.money)
        ranked_agents = ranked_agents[::-1]
        scores =f"----------------------- Round {self.round_number} ------------------------\n\n" + \
                "#########################################################\n######                  SCOREBOARD                 ######\n#########################################################"

        for i in range(len(self.agents)):
            scores += f"\n###### {str(i+1)}º place ######  {ranked_agents[i].name}   ->   {ranked_agents[i].money:.2f} €    ######"
        scores += "\n#########################################################"

        separator = "\n\n\n"

        log = separator + "------------------------- AGENTS ------------------------\n"

        for agent in self.agents:
            log += f"\n{agent.name} | risk-willingness: {agent.risk_level:.2f}, adaptability: {agent.adaptability:.2f}"
        log += "\n\n---------------------------------------------------------"
        return scores + log
    def play_round(self, round_number):
        # Reset the received_money flag at the start of the round
        for agent in self.agents:
            agent.received_money_this_round = False

        # Collect decisions from all agents and deduct money
        actions = {agent.name: agent.decide_action() for agent in self.agents}
        for agent in self.agents:
            action = actions[agent.name]
            if action > agent.money:
                action = agent.money
            agent.money -= action
            actions[agent.name] = action

        # Determine the minimal contribution
        if actions:
            min_contribution = min(actions.values())

        # Identify agents who made the minimal contribution
        minimal_contributors = [agent for agent in self.agents if actions[agent.name] == min_contribution]

        # Exclude these agents from receiving money this round
        excluded_agents = minimal_contributors
        excluded_agent_names = [agent.name for agent in excluded_agents]
        for agent in excluded_agents:
            print(f"{agent.name} is excluded from this round")

        # Calculate the total pool of contributions
        total_pool = sum(actions.values())

        # Find eligible agents (those not excluded)
        eligible_agents = [agent for agent in self.agents if agent.name not in excluded_agent_names]

        # Distribute the total pool among eligible agents
        if eligible_agents and total_pool > 0:
            distribution = total_pool / len(eligible_agents)
            for agent in eligible_agents:
                agent.receive_money(1.5 * distribution)
                agent.received_money_this_round = True  # Set flag when receiving money

        # After results are applied, observe actions and adjust risk appetite
        for agent in self.agents:
            agent.observe_actions(actions)
            agent.adjust_risk_appetite(agent.received_money_this_round)

        for agent in self.agents:
            agent.money_history.append(agent.money)

        # Display results
        print(f"--- Round {round_number + 1} ---")
        for agent in self.agents:
            print(
                f"{agent.name} decision: {actions[agent.name]}, risk-willingness: {agent.risk_level:.2f}, adaptability: {agent.adaptability:.2f}, money: {agent.money:.2f}")
        print("\n")

        self.round_number += 1

    def is_finished(self, number_of_rounds):
        return self.round_number >= number_of_rounds


def announce_winner(agents):
    # Find the agent with the most money
    winner = max(agents, key=lambda agent: agent.money)
    print(f"The winner is {winner.name} with final money of {winner.money:.2f}.")


#########################################################
####                       PLOTS                    #####
#########################################################


def plot_risk_willingness_evolution(agents):
    plt.figure(figsize=(12, 6))
    plt.title("Evolution of Agents' Risk Willingness")
    plt.xlabel("Round")
    plt.ylabel("Risk Willingness")

    for agent in agents:
        plt.plot(range(len(agent.risk_history)), agent.risk_history, label=agent.name)

    plt.legend(loc='center left', bbox_to_anchor=(1, 0.5))
    plt.grid(True)
    plt.show()


def plot_scoreboard_evolution(agents):
    plt.figure(figsize=(12, 8))
    plt.title("Scoreboard Evolution Over Rounds")
    plt.xlabel("Round")
    plt.ylabel("Total Money")

    for agent in agents:
        plt.plot(agent.money_history, label=agent.name)

    plt.legend(loc='upper left')
    plt.grid(True)
    plt.show()


def plot_final_correlations(agents):
    final_moneys = [agent.money for agent in agents]
    final_risks = [agent.risk_level for agent in agents]
    adaptabilities = [agent.adaptability for agent in agents]

    fig, ax = plt.subplots(1, 2, figsize=(14, 6))

    ax[0].scatter(final_moneys, final_risks, color='blue')
    ax[0].set_title("Final Money vs. Risk Willingness")
    ax[0].set_xlabel("Final Money")
    ax[0].set_ylabel("Risk Willingness")

    ax[1].scatter(final_moneys, adaptabilities, color='green')
    ax[1].set_title("Final Money vs. Adaptability")
    ax[1].set_xlabel("Final Money")
    ax[1].set_ylabel("Adaptability")

    plt.tight_layout()
    plt.show()


#########################################################
####               RUN A SIMULATION                 #####
#########################################################
# Define a function to run the simulation
def run_simulation_auto():
    global environment, agents, number_of_rounds
    # Get the number of agents from user input
    agents = []

    # Ask number of rounds and initial risk willingness for each agent
    number_of_rounds = simpledialog.askinteger("Number of rounds", "Enter Round Number (suggested: 10):")
    if number_of_rounds is None:
        return

    agents = [Agent(f"Agent_{i + 1}", np.random.uniform(0.2, 0.8), np.random.uniform(0.2, 0.8)) for i in range(4)]


    # Initialize beliefs for each agent
    for agent in agents:
        agent.initialize_beliefs(agents)

    # Create the environment and simulate the game
    environment = Environment(agents)

    exit_button.pack_forget()
    next_round_button.pack(pady=20)
    skip_all_rounds_button.pack(pady=20)
    exit_button.pack(pady=20)

def run_simulation_manual():
    global environment, agents, number_of_rounds
    # Get the number of agents from user input

    num_agents = simpledialog.askinteger("Number of Agents", "Enter the number of agents:")
    if num_agents is None:
        return
    agents = []

    # Ask number of rounds and initial risk willingness for each agent
    number_of_rounds = simpledialog.askinteger("Number of rounds", "Enter Round Number (suggested: 10):")
    if number_of_rounds is None:
        return

    for i in range(num_agents):

        # Ask for adaptability and initial risk willingness for each agent
        adaptability = simpledialog.askfloat(f"Agent {i + 1} Adaptability",
                                             f"Enter adaptability for Agent {i + 1} (0-1):")
        if adaptability is None:
            return
        initial_risk = simpledialog.askfloat(f"Agent {i + 1} Initial Risk",
                                             f"Enter initial risk willingness for Agent {i + 1} (0-1):")
        if initial_risk is None:
            return
        agents.append(Agent(f"Agent_{i + 1}", initial_risk, adaptability))

    # Initialize beliefs for each agent
    for agent in agents:
        agent.initialize_beliefs(agents)

    # Create the environment and simulate the game
    environment = Environment(agents)
    exit_button.pack_forget()
    next_round_button.pack(pady=20)
    skip_all_rounds_button.pack(pady=20)
    exit_button.pack(pady=20)




def next_round():
    global environment, agents, number_of_rounds
    if environment.round_number < number_of_rounds:
        environment.play_round(environment.round_number)
        scores = environment.get_scores()
        scoreboard.config(text=scores)
        root.update_idletasks()
    if environment.is_finished(number_of_rounds):
        announce_winner(agents)
        next_round_button.pack_forget()
        skip_all_rounds_button.pack_forget()
        scores = environment.get_scores()
        scoreboard.config(text=scores)
        root.update_idletasks()
        plot_risk_willingness_evolution(agents)
        plot_scoreboard_evolution(agents)
        plot_final_correlations(agents)


def skip_all_rounds():
    global environment, agents, number_of_rounds
    while not environment.is_finished(number_of_rounds):
        environment.play_round(environment.round_number)
    announce_winner(agents)
    next_round_button.pack_forget()
    skip_all_rounds_button.pack_forget()
    scores = environment.get_scores()
    scoreboard.config(text=scores)
    root.update_idletasks()
    plot_risk_willingness_evolution(agents)
    plot_scoreboard_evolution(agents)
    plot_final_correlations(agents)

def exit_program():
    root.destroy()

# Create a Tkinter window
root = tk.Tk()
root.title("Agent Simulation")

# Create a button to run the simulation
run_auto_button = tk.Button(root, text="Run Simulation Auto", command=run_simulation_auto)
run_auto_button.pack(pady=20)

run_button = tk.Button(root, text="Run Simulation Manual", command=run_simulation_manual)
run_button.pack(pady=20)

scoreboard = tk.Label(root, text="", justify=tk.LEFT, font=("Courier", 12))
scoreboard.pack(pady=20)

# Create a button to advance to the next round
next_round_button = tk.Button(root, text="Next Round", command=next_round)
next_round_button.pack_forget()

skip_all_rounds_button = tk.Button(root, text="Skip All Rounds", command=skip_all_rounds)
skip_all_rounds_button.pack_forget()

exit_button = tk.Button(root, text="Exit", command=exit_program)
exit_button.pack(pady=20)

# Run the Tkinter event loop
root.mainloop()




# what personality trait contributes more to success? Risk willingness


# In an envirenment where everyone else is risk willing and has a low adaptability,
# it pays off to start with a low risk and be highly adaptable


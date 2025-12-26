import numpy as np
import matplotlib.pyplot as plt
import random

initial_infected = 10
population = 10000
infection_prob = 0.035
mortality_prob = 0.01
contacts_per_day = 7
days = 180
resolution_duration = 13


def simulation():
    states = np.zeros(population)
    states[:initial_infected] = 1

    susceptible = []
    infected = []
    recovered = []
    dead = []

    for _ in range(days):
        susceptible.append(np.sum(states == 0))
        infected.append(np.sum(states == 1))
        recovered.append(np.sum(states == 2))
        dead.append(np.sum(states == 3))
        new_states = states.copy()

        infected_indices = np.where(states == 1)[0]
        alive_indices = np.where(states != 3)[0]

        for i in infected_indices:
            for _ in range(contacts_per_day):
                found = False
                while not found:
                    if random.random() < 0.95:
                        offset = random.randint(-50, 50)
                        target = (i + offset) % population
                    else:
                        target = random.choice(alive_indices)
                    if states[target] != 3:
                        found = True
                if random.random() < infection_prob and states[target] == 0:
                    new_states[target] = 1

            if random.random() < 1 / resolution_duration:
                if random.random() < mortality_prob:
                    new_states[i] = 3
                else:
                    new_states[i] = 2

        states = new_states

    return susceptible, infected, recovered, dead


def plot_results():
    for i in range(10):
        susceptible, infected, recovered, dead = simulation()
        if i == 0:
            plt.plot(infected, label="Infected", color="red")
            plt.plot(recovered, label="Recovered", color="green")
            plt.plot(dead, label="Dead", color="black")
            plt.plot(susceptible, label="Susceptible", color="blue")
        else:
            plt.plot(infected, color="red")
            plt.plot(recovered, color="green")
            plt.plot(dead, color="black")
            plt.plot(susceptible, color="blue")
    plt.legend()
    plt.title("Monte Carlo Simulation For Disease Spread (Covid-19)")
    plt.xlabel("Days")
    plt.ylabel("Number of People")
    plt.show()


plot_results()

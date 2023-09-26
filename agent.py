import pickle
import os
from network import NeuralNetwork
from cargame import CarGameAI
from plot import plot

MUTATE = 0.01

class Agent:
    def __init__(self) -> None:
        self.save_folder = './model'
        self.model_path = os.path.join(self.save_folder, 'model.pkl')

        self.plot_scores = []
        self.plot_mean_scores = []
        self.total_score = 0
        self.record = 0
        self.n_games = 0
        
        self.game = CarGameAI()
        self.bestModel = NeuralNetwork((11, 11, 6, 2))
        self.load()
        self.model = self.bestModel.mutate(MUTATE)

    def save(self):
        if not os.path.exists(self.save_folder):
            os.makedirs(self.save_folder)

        with open(self.model_path, 'wb') as file:
            data = (self.plot_scores, self.plot_mean_scores, self.total_score, self.record, self.n_games, self.bestModel)
            pickle.dump(data, file)

    def load(self):

        if os.path.exists(self.model_path):
            with open(self.model_path, 'rb') as file:
                loaded_data = pickle.load(file)
                self.plot_scores, self.plot_mean_scores, self.total_score, self.record, self.n_games, self.bestModel = loaded_data
            
    def reset(agent):
        
        agent.n_games += 1
        agent.plot_scores.append(agent.game.score)
        agent.total_score += agent.game.score
        agent.plot_mean_scores.append(agent.total_score / agent.n_games)
        plot(agent.plot_scores, agent.plot_mean_scores)

        if agent.game.score >= agent.record:
            print('New Record!')
            agent.bestModel = agent.model
            agent.record = agent.game.score
            agent.save()

        print('Game:', agent.n_games, 'Score:', agent.game.score, 'Record:', agent.record)
        agent.model = agent.bestModel.mutate(MUTATE)

    def train(agent):

        plot(agent.plot_scores, agent.plot_mean_scores)

        while agent.game.running:

            # perform move and get new state
            agent.game.play_step(agent.model.feedForward(agent.game.getModelInput()))

            if agent.game.game_over:

                agent.reset()
                agent.game.reset()

        agent.reset()
        agent.save()

if __name__ == '__main__':

    agent = Agent()
    agent.train()
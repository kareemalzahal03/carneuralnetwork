from random import uniform
import copy

def lerp(a, b, t):
    return a + (b - a) * t

class NeuralNetwork:
    def __init__(nn, neuronCounts) -> None:
        nn.levels = []
        for i in range(len(neuronCounts)-1):
            nn.levels.append(Level(neuronCounts[i], neuronCounts[i+1]))
        nn.mutate()

    def feedForward(nn, givenInputs):
    
        for level in nn.levels:
            givenInputs = level.feedForward(givenInputs)

        return givenInputs
    
    def mutate(nn, amount = 1):

        mutated = copy.deepcopy(nn)

        for level in mutated.levels:
            level.mutate(amount)

        return mutated

class Level:
    def __init__(level, inputCount, outputCount) -> None:

        level.inputCount = inputCount
        level.outputCount = outputCount
        level.biases = [0.0] * outputCount
        level.weights = [[0.0] * outputCount] * inputCount

    def feedForward(level, givenInputs):
    
        outputs = [0.0] * level.outputCount

        for i in range(level.outputCount):
            sum = 0
            for j in range(level.inputCount):
                sum += givenInputs[j] * level.weights[j][i]

            outputs[i] = sum > level.biases[i]

        return outputs
    
    def mutate(level, amount = 1):

        level.biases = [lerp(b, uniform(-1, 1), amount) for b in level.biases]
        level.weights = [[lerp(w, uniform(-1, 1), amount) for w in weights] for weights in level.weights]


# nn = NeuralNetwork([11, 7, 7, 7, 3])
# print(nn.feedForward([1,0,1,0,1,1,0,0,1,0,1]))

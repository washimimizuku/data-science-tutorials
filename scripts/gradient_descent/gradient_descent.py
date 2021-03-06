from typing import List, Callable, TypeVar, Iterator
import matplotlib.pyplot as plt
import random
import math

from scripts.linear_algebra.vectors import (
    Vector, 
    vector_mean, 
    scalar_multiply,
    add,
    distance)

T = TypeVar('T') # This allows us to type "generic" functions

def difference_quotient(f: Callable[[float], float],
                        x: float,
                        h: float) -> float:
    return(f(x + h) - f(x)) / h

def square(x: float) -> float:
    return x * x

def derivative(x: float) -> float:
    return 2 * x

def partial_difference_quotient(f: Callable[[Vector], float],
                                v: Vector,
                                i: int,
                                h: float) -> float:
    """Returns the i-th partial difference quotient of f at v"""
    w = [v_j + (h if j == i else 0) # Add h to just the ith element of v
        for j, v_j in enumerate(v)]
    
    return (f(w) - f(v)) / h

def gradient_step(v: Vector, gradient: Vector, step_size: float) -> Vector:
    """Moves 'step_size' in the 'gradient' direction from 'v'"""
    assert len(v) == len(gradient)
    step = scalar_multiply(step_size, gradient)
    return add(v, step)

def sum_of_squares_gradient(v: Vector) -> Vector:
    return [2 * v_i for v_i in v]

def linear_gradient(x: float, y: float, theta: Vector) -> Vector:
    slope, intercept = theta
    predicted = slope * x + intercept # The prediction of the model
    error = (predicted - y) # error is (predicted - actual)
    # squared_error = error ** 2 # We'll minimize squared error
    grad = [2 * error * x, 2 * error] # Using it's gradient
    return grad

def minibatches(dataset: List[T],
                batch_size: int,
                shuffle: bool = True) -> Iterator[List[T]]:
    """Generates `batch_size`-sized minibatches from the dataset"""
    # Start indexes 0, batch_size, 2 * batch_size, ...
    batch_starts = [start for start in range(0, len(dataset), batch_size)]

    if shuffle: random.shuffle(batch_starts) # Shuffle the batches

    for start in batch_starts:
        end = start + batch_size
        yield dataset[start:end]

def main():

    xs = range(-10, 11)
    actuals = [derivative(x) for x in xs]
    estimates = [difference_quotient(square, x, h=0.001) for x in xs]

    # Plot to show they're basically the same
    plt.title("Actual Derivates vs. Estimates")
    plt.plot(xs, actuals, 'rx', label='Actual') # red x
    plt.plot(xs, estimates, 'b+', label='Estimate') # blue +
    plt.legend(loc=9)
    plt.show()

    # Pick a random starting point
    v = [random.uniform(-10, 10) for i in range(3)]

    for epoch in range(1000):
        grad = sum_of_squares_gradient(v)    # compute the gradient at v
        v = gradient_step(v, grad, -0.01)    # take a negative gradient step
        print(epoch, v)
    print ('distance:', distance(v, [0,0,0]))
    assert distance(v, [0,0,0]) < 0.001 # v should be close to 0

    # x ranges from -50 to 49, y is always 20 * x + 5
    inputs = [(x, 20 * x + 5) for x in range(-50, 50)]

    # Start with random values for slope and intercept
    theta = [random.uniform(-1, 1), random.uniform(-1, 1)]

    learning_rate = 0.001

    for epoch in range(5000):
        # Compute the mean of the gradients
        grad = vector_mean([linear_gradient(x, y, theta) for x, y in inputs])
        # Take a step in that direction
        theta = gradient_step(theta, grad, -learning_rate)
        print(epoch, theta)

    slope, intercept = theta

    assert 19.9 < slope < 20.1, "Slope should be about 20"
    assert 4.9 < intercept < 5.1, "Intercept should be about 5"

    theta = [random.uniform(-1, 1), random.uniform(-1, 1)]

    for epoch in range(1000):
        for batch in minibatches(inputs, batch_size=20):
            grad = vector_mean([linear_gradient(x, y, theta) for x, y in batch])
            theta = gradient_step(theta, grad, -learning_rate)
        print(epoch, theta)

    slope, intercept = theta

    assert 19.9 < slope < 20.1, "Slope should be about 20"
    assert 4.9 < intercept < 5.1, "Intercept should be about 5"

    theta = [random.uniform(-1, 1), random.uniform(-1, 1)]

    for epoch in range(100):
        for x, y in inputs:
            grad = linear_gradient(x, y, theta)
            theta = gradient_step(theta, grad, -learning_rate)
        print(epoch, theta)

    slope, intercept = theta

    assert 19.9 < slope < 20.1, "Slope should be about 20"
    assert 4.9 < intercept < 5.1, "Intercept should be about 5"

if __name__ == "__main__": main()
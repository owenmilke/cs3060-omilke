import numpy as np
import matplotlib.pyplot as plt
import os

def plot_average_fitness():
    try:
        # Load single-run data for both variants
        fitness_A = np.load("A_fitness_history.npy")
        fitness_B = np.load("B_fitness_history.npy")
    except FileNotFoundError as e:
        print(f"Error loading data files: {e}")
        print("Please run both variants of the evolution first.")
        return

    # Calculate average fitness per generation
    avg_A = np.mean(fitness_A, axis=0)  # Average across population for each generation
    avg_B = np.mean(fitness_B, axis=0)

    # Create the plot
    plt.figure(figsize=(10, 6))
    plt.title("Average Fitness Comparison")
    plt.xlabel("Generation")
    plt.ylabel("Average Fitness")
    plt.grid(True, alpha=0.3)

    # Plot the average curves
    plt.plot(avg_A, 'b-', linewidth=2, label='Variant A (with arms)')
    plt.plot(avg_B, 'r-', linewidth=2, label='Variant B (without arms)')

    # Add legend and show plot
    plt.legend()
    plt.tight_layout()
    plt.savefig("average_fitness_comparison.png", dpi=300)
    plt.show()

    # Print final values for comparison
    print("\nFinal Average Fitness:")
    print(f"Variant A: {avg_A[-1]:.2f}")
    print(f"Variant B: {avg_B[-1]:.2f}")

if __name__ == "__main__":
    plot_average_fitness()
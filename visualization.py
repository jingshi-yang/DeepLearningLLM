"""
training_visualization.py - Visualization utilities for training metrics
"""
import matplotlib.pyplot as plt
import numpy as np
import json

# 1. loading JSON data
def load_history(json_path):
    with open(json_path) as f:
        return json.load(f)

# 2. Visualization in long form
def visualize_training_dynamics(history, save_path=None):
    """
    Enhanced visualization showing:
    - Loss curves (train/val)
    - Learning rate schedule
    - Teacher forcing ratio
    - All aligned by epoch for comparison
    
    Args:
        history: Dictionary containing training history
        save_path: Optional path to save the figure
    """
    plt.figure(figsize=(12, 10))
    epochs = np.arange(1, len(history['train_loss']) + 1)
    
    # Create main axis for loss
    ax1 = plt.subplot(3, 1, 1)
    ax1.plot(epochs, history['train_loss'], 'b-', label='Train Loss')
    ax1.plot(epochs, history['val_loss'], 'r-', label='Val Loss')
    ax1.set_ylabel('Loss')
    ax1.set_title('Training Dynamics Analysis')
    ax1.legend(loc='upper right')
    ax1.grid(True)
    
    # Create twin axis for learning rate (log scale)
    ax2 = ax1.twinx()
    ax2.plot(epochs, history['learning_rate'], 'g--', label='Learning Rate')
    ax2.set_yscale('log')
    ax2.set_ylabel('Learning Rate (log)')
    ax2.legend(loc='upper left')
    
    # Teacher forcing ratio plot
    plt.subplot(3, 1, 2)
    plt.plot(epochs, history['teacher_forcing_ratio'], 'm-', marker='o')
    plt.ylabel('Teacher Forcing Ratio')
    plt.xlabel('Epoch')
    plt.grid(True)
    plt.ylim(0, 1)
    
    # ROUGE scores plot (if any non-zero values)
    if any(v > 0 for v in history['rouge1'] + history['rouge2'] + history['rougeL']):
        plt.subplot(3, 1, 3)
        plt.plot(epochs, history['rouge1'], label='ROUGE-1')
        plt.plot(epochs, history['rouge2'], label='ROUGE-2')
        plt.plot(epochs, history['rougeL'], label='ROUGE-L')
        plt.ylabel('ROUGE Score')
        plt.xlabel('Epoch')
        plt.legend()
        plt.grid(True)
    
    plt.tight_layout()
    
    if save_path:
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
        print(f"Saved training dynamics plot to {save_path}")
    plt.show()
    
# 3. Visualization for 2-columned AAAI
def visualize_aaai_twocolumn(history, save_path='training_plot.png'):
    """
    AAAI 2-column formatted visualization (PNG output)
    Optimized for LaTeX documents with:
    - 3.5" width (fits single column)
    - 600 DPI resolution
    - Transparent background
    - Anti-aliased text
    """
    # Set up figure with exact dimensions
    plt.figure(figsize=(3.5, 4.0))  # Width: 3.5", Height: 4.0"
    
    # Configure fonts and styles
    plt.rcParams.update({
        'font.size': 10,
        'axes.titlesize': 10,
        'axes.labelsize': 10,
        'xtick.labelsize': 9,
        'ytick.labelsize': 9,
        'legend.fontsize': 9,
        'font.family': 'serif',
        'text.usetex': False,  # Set to True if you have LaTeX installed
        'figure.dpi': 600,
        'savefig.dpi': 600,
        'savefig.transparent': True
    })

    epochs = np.arange(1, len(history['train_loss']) + 1)
    
    # Main loss plot
    ax1 = plt.subplot(2, 1, 1)
    ax1.plot(epochs, history['train_loss'], color='#1f77b4', linestyle='-', 
            linewidth=1.5, label='Train')
    ax1.plot(epochs, history['val_loss'], color='#d62728', linestyle='--', 
            linewidth=1.5, label='Val')
    ax1.set_ylabel('Loss')
    ax1.grid(True, alpha=0.3)
    ax1.legend(frameon=True, framealpha=1, edgecolor='black')
    
    # Optimization parameters
    ax2 = plt.subplot(2, 1, 2)
    ax2.plot(epochs, history['learning_rate'], color='#2ca02c', 
            linestyle='-', linewidth=1.5, label='LR')
    ax2.set_xlabel('Epoch')
    ax2.set_ylabel('Learning Rate', color='#2ca02c')
    ax2.tick_params(axis='y', labelcolor='#2ca02c')
    ax2.grid(True, alpha=0.3)
    
    ax3 = ax2.twinx()
    ax3.plot(epochs, history['teacher_forcing_ratio'], color='#9467bd', 
            linestyle=':', linewidth=1.5, label='TF Ratio')
    ax3.set_ylabel('TF Ratio', color='#9467bd')
    ax3.tick_params(axis='y', labelcolor='#9467bd')
    
    # Combined legend
    lines = [ax2.get_lines()[0], ax3.get_lines()[0]]
    ax2.legend(lines, [l.get_label() for l in lines], 
                frameon=True, framealpha=1, edgecolor='black')

    plt.tight_layout(pad=0.8)
    
    # Save with exact dimensions and high quality
    if save_path:
        plt.savefig(
            save_path,
            format='png',
            bbox_inches='tight',
            pad_inches=0.05,
            transparent=True,
            dpi=600
        )
        print(f"Saved publication-ready figure to {save_path}")
    plt.close()  # Close the figure to free memory
    
# ==============================================
# MAIN EXECUTION BLOCK (for standalone usage)
# ==============================================
if __name__ == "__main__":
    # Example usage when run directly
    history = load_history("updated_baseline_history.json")
    visualize_aaai_twocolumn(history, save_path="sample_training_plot_2.png")
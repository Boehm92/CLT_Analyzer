import json
import os

import matplotlib.pyplot as plt


def main():
    _script_dir = os.path.dirname(os.path.abspath(__file__))
    _stats_path = os.path.join(_script_dir, "mfs_statistics.json")

    with open(_stats_path, "r") as f:
        _stats = json.load(f)

    _training_loss = _stats["training_loss"]
    _val_loss = _stats["val_loss"]
    _train_f1 = _stats["train_f1"]
    _val_f1 = _stats["val_f1"]
    _best_epoch = _stats["best_epoch"]
    _best_val_f1 = _stats["best_val_f1"]

    _epochs = list(range(1, len(_training_loss) + 1))
    _best_epoch_display = _best_epoch + 1  # 0-indexed -> 1-indexed

    # -- Graph 1: Loss --
    fig, ax = plt.subplots(figsize=(6, 4))
    ax.plot(_epochs, _training_loss, color="#1f77b4", linewidth=1.5, label="Training Loss")
    ax.plot(_epochs, _val_loss, color="#ff7f0e", linewidth=1.5, label="Validation Loss")
    ax.set_xlabel("Epoch", fontsize=12)
    ax.set_ylabel("Loss", fontsize=12)
    ax.set_title("MFS — Training & Validation Loss", fontsize=14)
    ax.legend(fontsize=11)
    ax.grid(True, alpha=0.3)
    fig.tight_layout()

    _loss_path = os.path.join(_script_dir, "mfs_loss.png")
    fig.savefig(_loss_path, dpi=100)
    plt.close(fig)
    print(f"Saved: {_loss_path}")

    # -- Graph 2: F1-Score --
    fig, ax = plt.subplots(figsize=(6, 4))
    ax.plot(_epochs, _train_f1, color="#1f77b4", linewidth=1.5, label="Training F1")
    ax.plot(_epochs, _val_f1, color="#ff7f0e", linewidth=1.5, label="Validation F1")
    ax.set_yticks([1.0])
    ax.set_yticklabels(["1.00"])
    ax.set_xlabel("Epoch", fontsize=12)
    ax.set_ylabel("F1-Score", fontsize=12)
    ax.set_title("MFS — Training & Validation F1-Score", fontsize=14)
    ax.legend(fontsize=11)
    ax.grid(True, alpha=0.3)
    fig.tight_layout()

    _f1_path = os.path.join(_script_dir, "mfs_f1_score.png")
    fig.savefig(_f1_path, dpi=100)
    plt.close(fig)
    print(f"Saved: {_f1_path}")


if __name__ == "__main__":
    main()

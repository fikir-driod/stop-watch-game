import tkinter as tk
from tkinter import messagebox, simpledialog
import time
import random
import pickle
import os

class StopwatchGame:
    def __init__(self, root):
        self.root = root
        self.root.title("Stopwatch Game")
        self.root.geometry("450x450") 
        
      
        self.target_time = random.uniform(3, 7)  
        self.start_time = None
        self.end_time = None
        self.best_difference = float('inf')
        self.total_score = 0
        self.countdown_running = False
        self.scores = self.load_scores() 
        self.info_label = tk.Label(root, text="Stop the timer as close as possible to the target time!", font=("Arial", 12))
        self.info_label.pack(pady=10)
        
        self.target_label = tk.Label(root, text=f"Target Time: {self.target_time:.2f} seconds", font=("Arial", 14))
        self.target_label.pack(pady=10)
        
        self.countdown_label = tk.Label(root, text="", font=("Arial", 14), fg="green")
        self.countdown_label.pack(pady=10)
        
        self.result_label = tk.Label(root, text="", font=("Arial", 12), fg="blue")
        self.result_label.pack(pady=10)
        
        self.score_label = tk.Label(root, text=f"Total Score: {self.total_score}", font=("Arial", 12))
        self.score_label.pack(pady=10)
        

        self.start_button = tk.Button(root, text="Start Timer", command=self.start_timer, font=("Arial", 12))
        self.start_button.pack(pady=10)
        
        self.stop_button = tk.Button(root, text="Stop Timer", command=self.stop_timer, font=("Arial", 12), state=tk.DISABLED)
        self.stop_button.pack(pady=10)
        
        self.play_again_button = tk.Button(root, text="Play Again", command=self.play_again, font=("Arial", 12), state=tk.DISABLED)
        self.play_again_button.pack(pady=10)
        
        self.leaderboard_button = tk.Button(root, text="View Leaderboard", command=self.view_leaderboard, font=("Arial", 12))
        self.leaderboard_button.pack(pady=10)
    
    def load_scores(self):
        """Load leaderboard scores from a file."""
        if os.path.exists("scores.pkl"):
            with open("scores.pkl", "rb") as file:
                return pickle.load(file)
        return []
    
    def save_scores(self, scores):
        """Save leaderboard scores to a file."""
        with open("scores.pkl", "wb") as file:
            pickle.dump(scores, file)
    
    def start_timer(self):
        self.start_time = time.time()
        self.start_button.config(state=tk.DISABLED)
        self.stop_button.config(state=tk.NORMAL)
        self.result_label.config(text="Timer started! Stop it as close as possible to the target time.")
        

        self.countdown_running = True
        self.update_countdown()
    
    def update_countdown(self):
        if not self.countdown_running:
            return
        
        elapsed_time = time.time() - self.start_time
        remaining_time = max(0, self.target_time - elapsed_time)
        self.countdown_label.config(text=f"Time left: {remaining_time:.2f} seconds")
        
        if remaining_time > 0:
            self.root.after(100, self.update_countdown) 
        else:
            self.countdown_label.config(text="Time's up!")  
    
    def stop_timer(self):
        self.end_time = time.time()
        elapsed_time = self.end_time - self.start_time
        difference = abs(elapsed_time - self.target_time)
        

        self.countdown_running = False
        

        self.result_label.config(text=f"You stopped the timer at {elapsed_time:.2f} seconds.\n"
                                      f"You were off by {difference:.2f} seconds.")
        

        if difference < 0.1:
            score = 100
            feedback = "Wow! You have perfect timing! +100 points"
        elif difference < 0.5:
            score = 50
            feedback = "Great job! Your timing is excellent. +50 points"
        elif difference < 1.0:
            score = 20
            feedback = "Not bad! Keep practicing to improve. +20 points"
        else:
            score = 0
            feedback = "Keep trying! You'll get better with practice. +0 points"
        
        self.total_score += score
        self.score_label.config(text=f"Total Score: {self.total_score}")
        self.result_label.config(text=self.result_label.cget("text") + f"\n{feedback}")
        

        if difference < self.best_difference:
            self.best_difference = difference
            self.result_label.config(text=self.result_label.cget("text") + f"\nNew best performance: {self.best_difference:.2f} seconds off!")
        
     
        self.stop_button.config(state=tk.DISABLED)
        self.play_again_button.config(state=tk.NORMAL)
    
    def play_again(self):
       
        name = tk.simpledialog.askstring("Save Score", "Enter your name:")
        if name:
            self.scores.append({"name": name, "score": self.total_score})
            self.scores.sort(key=lambda x: x["score"], reverse=True)
            self.save_scores(self.scores)

        
        self.target_time = random.uniform(3, 7) 
        self.start_time = None
        self.end_time = None
        self.best_difference = float('inf')  
        self.total_score = 0 
        self.result_label.config(text="")
        self.countdown_label.config(text="")
        self.target_label.config(text=f"Target Time: {self.target_time:.2f} seconds")
        self.score_label.config(text=f"Total Score: {self.total_score}")

      
        self.start_button.config(state=tk.NORMAL)
        self.stop_button.config(state=tk.DISABLED)
        self.play_again_button.config(state=tk.DISABLED)
    
    def view_leaderboard(self):
        leaderboard_window = tk.Toplevel(self.root)
        leaderboard_window.title("Leaderboard")
        leaderboard_window.geometry("300x300")
        
        leaderboard_label = tk.Label(leaderboard_window, text="Leaderboard", font=("Arial", 16))
        leaderboard_label.pack(pady=10)
        
        leaderboard_text = ""
        for i, entry in enumerate(self.scores[:10]):  # Show top 10 scores
            leaderboard_text += f"{i+1}. {entry['name']}: {entry['score']} points\n"
        
        if not leaderboard_text:
            leaderboard_text = "No scores yet!"
        
        leaderboard_display = tk.Label(leaderboard_window, text=leaderboard_text, font=("Arial", 12), justify="left")
        leaderboard_display.pack(pady=10)
    
    def run(self):
        """Start the tkinter main event loop."""
        self.root.mainloop()

# Create and run the app
if __name__ == "__main__":
    root = tk.Tk()
    game = StopwatchGame(root)
    game.run()
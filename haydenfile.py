import random
import tkinter as tk

def check_answer(event=None):
    user_answer = entry.get()
    try:
        user_answer = int(user_answer)
        if user_answer == answer:
            feedback_label.config(text="Correct!", fg="green")
        else:
            feedback_label.config(text="Wrong :(", fg="red")
        new_question()
    except ValueError:
        feedback_label.config(text="Please enter a valid number", fg="orange")

def new_question():
    global num1, num2, answer
    num1 = random.randint(1, 10)
    num2 = random.randint(1, 10)
    answer = num1 + num2
    question_label.config(text=f"What does {num1} + {num2} = ?")
    entry.delete(0, tk.END)

# Create the main window
root = tk.Tk()
root.title("Math Quiz Game")

# Create a label to display the question
question_label = tk.Label(root, text="", font=("Arial", 16))
question_label.pack(pady=20)

# Create an entry box for the user to input their answer
entry = tk.Entry(root, font=("Arial", 16))
entry.pack(pady=10)
entry.bind('<Return>', check_answer)  # Bind Enter key to check_answer

# Create a label to display feedback (Correct or Wrong)
feedback_label = tk.Label(root, text="", font=("Arial", 16))
feedback_label.pack(pady=10)

# Generate the first question
new_question()

# Start the GUI event loop
root.mainloop()


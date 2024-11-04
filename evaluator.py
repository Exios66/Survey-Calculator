import json

# Define the dictionary containing survey metrics and corresponding chatbot presets
# Each metric has a threshold value, and if the user's score meets or exceeds this threshold, the corresponding preset is selected
survey_presets = {
    "metric_a": {"threshold": 70, "preset": "Supportive and Empathetic"},
    "metric_b": {"threshold": 50, "preset": "Direct and Analytical"},
    "metric_c": {"threshold": 30, "preset": "Playful and Casual"},
}

# Function to input introductory survey metrics from user
def get_user_metrics():
    print("Please input your scores for each metric below:")
    metrics = {}  # Dictionary to store user metrics
    
    # Loop through each metric defined in survey_presets
    for metric in survey_presets.keys():
        while True:
            try:
                print(f"Processing input for {metric}...")  # Debug log to indicate current metric being processed
                score = int(input(f"Enter your score for {metric} (0-100): "))  # Get user input for the metric score
                
                # Ensure the input score is within the valid range (0-100)
                if score < 0 or score > 100:
                    raise ValueError("Score must be between 0 and 100.")
                
                # Store the valid score in the metrics dictionary
                metrics[metric] = score
                print(f"Recorded score for {metric}: {score}")  # Debug log to confirm the recorded score
                break  # Exit the loop if input is valid
            
            # Handle invalid input by prompting the user to enter the score again
            except ValueError as e:
                print(f"Invalid input: {e}. Please try again.")
    
    print(f"Final user metrics: {metrics}")  # Debug log to display all collected metrics
    return metrics  # Return the collected metrics

# Function to determine the appropriate chatbot preset based on user metrics
def determine_chatbot_preset(user_metrics):
    print("Determining chatbot preset based on user metrics...")  # Debug log to indicate start of preset determination
    chatbot_preset = []  # List to store selected chatbot presets
    
    # Loop through each user metric to determine if it meets the threshold for a preset
    for metric, value in user_metrics.items():
        print(f"Evaluating {metric} with value {value} against threshold {survey_presets[metric]['threshold']}...")  # Debug log for evaluation
        
        # If the user's score meets or exceeds the threshold, add the corresponding preset to the list
        if value >= survey_presets[metric]['threshold']:
            chatbot_preset.append(survey_presets[metric]['preset'])
            print(f"Preset '{survey_presets[metric]['preset']}' added for {metric}")  # Debug log to confirm preset addition
    
    print(f"Determined chatbot presets: {chatbot_preset}")  # Debug log to display the determined presets
    return chatbot_preset  # Return the list of selected presets

# Main function to orchestrate the flow of the program
def main():
    print("Starting main function...")  # Debug log to indicate the start of the main function
    
    # Get user metrics through survey input
    user_metrics = get_user_metrics()
    
    # Determine the chatbot presets based on the collected user metrics
    chatbot_presets = determine_chatbot_preset(user_metrics)
    
    # Output the determined presets to the user
    if chatbot_presets:
        print("\nBased on your survey metrics, the following chatbot preset(s) apply to you:")
        for preset in chatbot_presets:
            print(f"- {preset}")
    else:
        print("\nNo specific preset matched your survey results.")
    
    print("Main function completed.")  # Debug log to indicate the end of the main function

# Entry point for the script
if __name__ == "__main__":
    main()

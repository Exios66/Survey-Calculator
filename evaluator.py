import json
import logging
import sys
from typing import Dict, List, Optional

# Configure logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('survey_calculator.log'),
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)

# Define the dictionary containing survey metrics and corresponding chatbot presets
# Each metric has a threshold value, and if the user's score meets or exceeds this threshold, 
# the corresponding preset is selected
survey_presets = {
    "metric_a": {
        "threshold": 70, 
        "preset": "Supportive and Empathetic",
        "description": "Focuses on emotional support and understanding"
    },
    "metric_b": {
        "threshold": 50, 
        "preset": "Direct and Analytical",
        "description": "Emphasizes logical problem-solving and clear communication"
    },
    "metric_c": {
        "threshold": 30, 
        "preset": "Playful and Casual",
        "description": "Maintains a light, informal tone in interactions"
    },
}

def validate_score(score: int) -> bool:
    """
    Validate if the score is within acceptable range.
    
    Args:
        score (int): The score to validate
        
    Returns:
        bool: True if valid, False otherwise
    """
    return 0 <= score <= 100

def get_user_metrics() -> Dict[str, int]:
    """
    Collect and validate user input for survey metrics.
    
    Returns:
        Dict[str, int]: Dictionary mapping metric names to user scores
    """
    logger.info("Starting user metric collection...")
    metrics = {}  # Dictionary to store user metrics
    
    # Loop through each metric defined in survey_presets
    for metric in survey_presets.keys():
        attempts = 0
        max_attempts = 3
        
        while attempts < max_attempts:
            try:
                logger.debug(f"Processing input for {metric}...")
                score = int(input(f"Enter your score for {metric} (0-100): "))
                
                if not validate_score(score):
                    raise ValueError("Score must be between 0 and 100.")
                
                metrics[metric] = score
                logger.info(f"Successfully recorded score for {metric}: {score}")
                break
                
            except ValueError as e:
                attempts += 1
                remaining = max_attempts - attempts
                logger.warning(f"Invalid input for {metric}: {str(e)}")
                if remaining > 0:
                    print(f"Invalid input: {e}. {remaining} attempts remaining.")
                else:
                    logger.error(f"Max attempts reached for {metric}, defaulting to 0")
                    metrics[metric] = 0
                    print(f"Max attempts reached. Setting {metric} score to 0.")
    
    logger.info(f"Completed metric collection: {metrics}")
    return metrics

def determine_chatbot_preset(user_metrics: Dict[str, int]) -> List[Dict[str, str]]:
    """
    Determine appropriate chatbot presets based on user metrics.
    
    Args:
        user_metrics (Dict[str, int]): Dictionary of user metric scores
        
    Returns:
        List[Dict[str, str]]: List of selected preset configurations
    """
    logger.info("Starting chatbot preset determination...")
    chatbot_presets = []
    
    try:
        for metric, value in user_metrics.items():
            threshold = survey_presets[metric]['threshold']
            logger.debug(f"Evaluating {metric}: score={value}, threshold={threshold}")
            
            if value >= threshold:
                preset_config = {
                    'preset': survey_presets[metric]['preset'],
                    'description': survey_presets[metric]['description'],
                    'score': value,
                    'threshold': threshold
                }
                chatbot_presets.append(preset_config)
                logger.info(f"Added preset configuration: {preset_config}")
    
    except KeyError as e:
        logger.error(f"Error accessing preset configuration: {str(e)}")
        raise
        
    logger.info(f"Completed preset determination. Selected {len(chatbot_presets)} presets")
    return chatbot_presets

def main() -> None:
    """
    Main function to orchestrate the survey calculation process.
    """
    logger.info("Starting survey calculator application...")
    
    try:
        # Get user metrics through survey input
        user_metrics = get_user_metrics()
        
        # Determine the chatbot presets based on the collected user metrics
        chatbot_presets = determine_chatbot_preset(user_metrics)
        
        # Output the determined presets to the user
        if chatbot_presets:
            print("\nBased on your survey metrics, the following chatbot preset(s) apply to you:")
            for preset in chatbot_presets:
                print(f"\n- {preset['preset']}")
                print(f"  Description: {preset['description']}")
                print(f"  Your score: {preset['score']} (Threshold: {preset['threshold']})")
        else:
            logger.warning("No presets matched the user's metrics")
            print("\nNo specific preset matched your survey results.")
        
        # Save results to file
        with open('survey_results.json', 'w') as f:
            json.dump({
                'user_metrics': user_metrics,
                'selected_presets': chatbot_presets
            }, f, indent=4)
            logger.info("Survey results saved to survey_results.json")
            
    except Exception as e:
        logger.error(f"An unexpected error occurred: {str(e)}")
        print("An error occurred while processing your survey. Please try again.")
        
    logger.info("Survey calculator application completed.")

# Entry point for the script
if __name__ == "__main__":
    main()

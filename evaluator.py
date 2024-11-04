import json
import logging
import sys
import os
from datetime import datetime
from typing import Dict, List, Optional, Tuple, Any
from pathlib import Path

# Configure logging with more detailed settings
def setup_logging() -> logging.Logger:
    """Configure and return logger with detailed settings"""
    # Create logs directory if it doesn't exist
    log_dir = Path("logs")
    log_dir.mkdir(exist_ok=True)
    
    # Create log filename with timestamp
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    log_filename = log_dir / f"survey_calculator_{timestamp}.log"
    
    # Configure logging with both file and console handlers
    logging.basicConfig(
        level=logging.DEBUG,
        format='%(asctime)s - %(name)s - %(levelname)s - [%(filename)s:%(lineno)d] - %(message)s',
        handlers=[
            logging.FileHandler(log_filename),
            logging.StreamHandler(sys.stdout)
        ]
    )
    return logging.getLogger(__name__)

logger = setup_logging()

class SurveyMetric:
    """Class to represent a survey metric with validation"""
    def __init__(self, name: str, threshold: int, preset: str, description: str):
        self.name = name
        self.threshold = threshold
        self.preset = preset
        self.description = description
        
    def validate_threshold(self) -> bool:
        """Validate threshold is within acceptable range"""
        return 0 <= self.threshold <= 100

# Enhanced survey presets with more detailed configurations
survey_presets = {
    "metric_a": SurveyMetric(
        "Emotional Intelligence",
        70,
        "Supportive and Empathetic",
        "Focuses on emotional support and understanding"
    ),
    "metric_b": SurveyMetric(
        "Analytical Thinking",
        50,
        "Direct and Analytical",
        "Emphasizes logical problem-solving and clear communication"
    ),
    "metric_c": SurveyMetric(
        "Communication Style",
        30,
        "Playful and Casual",
        "Maintains a light, informal tone in interactions"
    ),
    "metric_d": SurveyMetric(
        "Problem Solving",
        60,
        "Strategic and Methodical",
        "Focuses on structured approach to problem resolution"
    )
}

class ScoreValidationError(Exception):
    """Custom exception for score validation errors"""
    pass

def validate_score(score: int) -> bool:
    """
    Validate if the score is within acceptable range.
    
    Args:
        score (int): The score to validate
        
    Returns:
        bool: True if valid, False otherwise
        
    Raises:
        ScoreValidationError: If score is invalid
    """
    if not isinstance(score, int):
        raise ScoreValidationError("Score must be an integer")
    if not 0 <= score <= 100:
        raise ScoreValidationError("Score must be between 0 and 100")
    return True

def get_user_metrics() -> Dict[str, int]:
    """
    Collect and validate user input for survey metrics.
    
    Returns:
        Dict[str, int]: Dictionary mapping metric names to user scores
        
    Raises:
        KeyboardInterrupt: If user cancels input
    """
    logger.info("Starting user metric collection...")
    metrics: Dict[str, int] = {}
    
    try:
        for metric_key, metric_obj in survey_presets.items():
            attempts = 0
            max_attempts = 3
            
            while attempts < max_attempts:
                try:
                    logger.debug(f"Processing input for {metric_obj.name}...")
                    score_input = input(f"Enter your score for {metric_obj.name} (0-100): ").strip()
                    
                    # Allow user to exit
                    if score_input.lower() in ['q', 'quit', 'exit']:
                        raise KeyboardInterrupt
                    
                    score = int(score_input)
                    validate_score(score)
                    
                    metrics[metric_key] = score
                    logger.info(f"Successfully recorded score for {metric_obj.name}: {score}")
                    break
                    
                except (ValueError, ScoreValidationError) as e:
                    attempts += 1
                    remaining = max_attempts - attempts
                    logger.warning(f"Invalid input for {metric_obj.name}: {str(e)}")
                    if remaining > 0:
                        print(f"Invalid input: {e}. {remaining} attempts remaining.")
                    else:
                        logger.error(f"Max attempts reached for {metric_obj.name}, defaulting to 0")
                        metrics[metric_key] = 0
                        print(f"Max attempts reached. Setting {metric_obj.name} score to 0.")
        
        logger.info(f"Completed metric collection: {metrics}")
        return metrics
        
    except KeyboardInterrupt:
        logger.info("User cancelled metric collection")
        print("\nSurvey cancelled by user.")
        sys.exit(0)

def determine_chatbot_preset(user_metrics: Dict[str, int]) -> List[Dict[str, Any]]:
    """
    Determine appropriate chatbot presets based on user metrics.
    
    Args:
        user_metrics (Dict[str, int]): Dictionary of user metric scores
        
    Returns:
        List[Dict[str, Any]]: List of selected preset configurations
        
    Raises:
        KeyError: If metric key is not found in presets
    """
    logger.info("Starting chatbot preset determination...")
    chatbot_presets = []
    
    try:
        for metric, value in user_metrics.items():
            if metric not in survey_presets:
                raise KeyError(f"Unknown metric: {metric}")
                
            metric_obj = survey_presets[metric]
            logger.debug(f"Evaluating {metric_obj.name}: score={value}, threshold={metric_obj.threshold}")
            
            if value >= metric_obj.threshold:
                preset_config = {
                    'name': metric_obj.name,
                    'preset': metric_obj.preset,
                    'description': metric_obj.description,
                    'score': value,
                    'threshold': metric_obj.threshold,
                    'exceeded_by': value - metric_obj.threshold
                }
                chatbot_presets.append(preset_config)
                logger.info(f"Added preset configuration: {preset_config}")
    
    except KeyError as e:
        logger.error(f"Error accessing preset configuration: {str(e)}")
        raise
        
    logger.info(f"Completed preset determination. Selected {len(chatbot_presets)} presets")
    return chatbot_presets

def save_results(user_metrics: Dict[str, int], chatbot_presets: List[Dict[str, Any]]) -> None:
    """Save survey results to JSON file with timestamp"""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f'survey_results_{timestamp}.json'
    
    results = {
        'timestamp': datetime.now().isoformat(),
        'user_metrics': user_metrics,
        'selected_presets': chatbot_presets
    }
    
    try:
        with open(filename, 'w') as f:
            json.dump(results, f, indent=4)
        logger.info(f"Survey results saved to {filename}")
    except IOError as e:
        logger.error(f"Failed to save results: {str(e)}")
        raise

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
                print(f"\n- {preset['preset']} ({preset['name']})")
                print(f"  Description: {preset['description']}")
                print(f"  Your score: {preset['score']} (Threshold: {preset['threshold']})")
                print(f"  Exceeded threshold by: {preset['exceeded_by']} points")
        else:
            logger.warning("No presets matched the user's metrics")
            print("\nNo specific preset matched your survey results.")
        
        # Save results
        save_results(user_metrics, chatbot_presets)
            
    except Exception as e:
        logger.error(f"An unexpected error occurred: {str(e)}", exc_info=True)
        print("An error occurred while processing your survey. Please check the logs for details.")
        
    logger.info("Survey calculator application completed.")

# Entry point for the script
if __name__ == "__main__":
    main()

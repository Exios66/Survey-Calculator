# Survey Calculator

A web application that helps determine the most suitable chatbot interaction style based on user preferences through a survey interface.

## Overview

The Survey Calculator is a full-stack web application that allows users to:
- Take a survey rating their preferences for different chatbot interaction styles
- Get personalized recommendations for chatbot presets based on their scores
- View detailed documentation about the different preset options
- Toggle between light and dark themes

## Features

### Frontend (index.html)
- Clean, modern UI built with HTML, CSS and vanilla JavaScript
- Responsive design that works on mobile and desktop
- Interactive survey form with real-time validation
- Loading states and error handling
- Dark/light theme toggle with CSS variables for consistent theming
- Tab navigation between survey and documentation
- Animated transitions and hover effects
- Custom Google Fonts integration (Roboto)
- Accessibility features including proper ARIA labels
- Error and success message handling

### Backend (app.py & evaluator.py)
- Flask REST API endpoint (/api/process-survey) for handling survey submissions
- CORS enabled for cross-origin requests
- Comprehensive error handling and logging
- Survey evaluation logic with configurable thresholds
- Score validation (0-100 range)
- Detailed logging of all operations with both file and console output
- Type hints and documentation for better code maintainability

### Chatbot Presets
Three distinct interaction styles are evaluated:

1. **Supportive and Empathetic**
   - Threshold: 70
   - Focuses on emotional support and understanding
   - Ideal for users seeking compassionate interaction

2. **Direct and Analytical**
   - Threshold: 50
   - Emphasizes logical problem-solving
   - Best for users preferring straightforward communication

3. **Playful and Casual**
   - Threshold: 30
   - Maintains a light, informal tone
   - Suitable for casual conversations and engagement

## Setup

1. **Create and activate a virtual environment**:
    ```bash
    python3 -m venv venv
    source venv/bin/activate  # On Windows: venv\Scripts\activate
    ```

2. **Install the required dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

## Usage

1. **Start the Flask server**:
    ```bash
    python app.py
    ```

2. **Open index.html in your browser** to access the survey interface

3. **Complete the survey** by rating your preferences for different interaction styles

4. **View your results** to see your recommended chatbot preset

## Contributing

We welcome contributions from the community. To contribute:

1. **Fork the repository**

2. **Create a new branch** for your feature or bugfix:
    ```bash
    git checkout -b feature-name
    ```

3. **Commit your changes**:
    ```bash
    git commit -m "Description of your changes"
    ```

4. **Push to the branch**:
    ```bash
    git push origin feature-name
    ```

5. **Open a pull request** and describe your changes

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Contributors

- **[Exios66](https://github.com/Exios66)**: The main contributor and maintainer of the project.

## Contact

For any questions or feedback, feel free to open an issue or contact [Exios66](https://github.com/Exios66).

## Additional Resources

- **Project Homepage**: [Survey-Calculator](https://exios66.github.io/Survey-Calculator/)
- **Repository URL**: [Survey-Calculator on GitHub](https://github.com/Exios66/Survey-Calculator)

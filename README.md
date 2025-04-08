# i95dev AI Engineering Intern - Take-Home Assignment

## AI-Powered Product Recommendation Engine

### Project Overview

This project implements a personalized product recommendation system using OpenAI's GPT-3.5-turbo. It features a Flask backend REST API integrated with a React frontend. The primary focus of this solution is advanced prompt engineering to generate precise and meaningful product recommendations based on user preferences and browsing history.

---

### Prompt Engineering Strategy

Prompt engineering was central to creating accurate, context-aware recommendations. The approach involved:

#### 1. Structured Prompt Creation
- Clearly segmented prompts with:
  - User Preferences (categories, brands, price range)
  - Browsing History
  - Candidate Products

#### 2. Candidate Product Selection
- Up to 15 highly relevant products selected through a scoring algorithm based on:
  - User preferences and browsing behaviors
  - Product attributes (category, brand, price similarity, rating, tags, features)

#### 3. Detailed User Context
- Explicitly included browsing history with detailed product attributes:
  - Names, categories, price points, brands, ratings, features, and tags
- Highlighted features and tags matching the user's demonstrated interests

#### 4. Strategic Recommendation Mix
- Prompted LLM to produce exactly 5 recommendations:
  - **Core Recommendations:** Closely matching user behavior and stated preferences
  - **Complementary Products:** Enhancing previously viewed items
  - **Discovery Products:** New yet relevant products to broaden user interests

#### 5. Quality Guidance
- Provided explicit examples contrasting excellent vs. poor explanations
- Ensured detailed reasoning explicitly linked recommendations to user behaviors and preferences

---

### Implementation Details

#### Backend (Flask)
- Integrated OpenAI's GPT-3.5-turbo
- Implemented caching for 24-hour storage of recommendations to optimize performance

#### Frontend (React)
- Product catalog with comprehensive filtering and sorting capabilities
- Tracking and visualization of browsing history
- Detailed user preference form capturing critical user-specific data

---

### Challenges and Solutions
- **Token Limitation**: Managed token constraints through strategic product selection
- **Robust Parsing**: Enhanced parsing logic for reliable extraction of structured recommendations from LLM responses

---

### Future Enhancements
- User authentication and profile persistence
- A/B testing for prompt variations
- Comprehensive unit and integration tests

---

## Setup Instructions

### Backend Setup
1. Navigate to the backend directory:
```bash
cd backend
```
2. Create and activate a virtual environment:
```bash
python -m venv venv

# Windows
venv\Scripts\activate

# macOS/Linux
source venv/bin/activate
```
3. Install dependencies:
```bash
pip install -r requirements.txt
```
4. Create a `.env` file from `.env.example` and add your OpenAI API key.

5. Run the Flask application:
```bash
python app.py
```

### Frontend Setup
1. Navigate to the frontend directory:
```bash
cd frontend
```
2. Install dependencies:
```bash
npm install
```
3. Start the React development server:
```bash
npm start
```

The frontend will open at [http://localhost:3000](http://localhost:3000).

---

Thank you for reviewing my submission!


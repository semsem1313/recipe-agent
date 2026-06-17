# 🍳 Recipe Recommendation Agent

A simple LLM-powered agent that suggests recipes based on whatever ingredients you have on hand, plus optional dietary restrictions, time limits, and serving size. Built with LangChain and OpenAI's API.

## How it works

You give it a list of ingredients (and optionally a diet, time limit, and serving count). It sends a structured prompt to an OpenAI model, gets back three recipe suggestions as JSON, and prints them nicely formatted in your terminal — name, cuisine, difficulty, ingredients, step-by-step instructions, and a recommended pick.

## Requirements

- Python 3.13 
- An OpenAI API key ([get one here](https://platform.openai.com/api-keys))

## Setup

**1. Clone the repo**
```bash
git clone https://github.com/semsem1313/recipe-agent.git
cd recipe-agent
```

**2. Create and activate a virtual environment**
```bash
python -m venv venv
```
- Windows: `venv\Scripts\activate`
- Mac/Linux: `source venv/bin/activate`

**3. Install dependencies**
```bash
python.exe -m pip install --upgrade pip 
pip install -r requirements.txt
```

**4. Add your API key**

Open `.env` and replace the placeholder with your real OpenAI API key.

## Usage

Run with default ingredients:
```bash
python agent.py
```

Or specify your own:
```bash
python agent.py --ingredients "chicken, garlic, lemon, rosemary"
```

With dietary restrictions, a time limit, and serving size:
```bash
python agent.py --ingredients "tofu, broccoli, soy sauce" --diet vegan --time 20 --servings 4
```

### Options

| Flag | Description | Default |
|------|-------------|---------|
| `--ingredients` | Comma-separated list of ingredients | chicken breast, garlic, lemon, olive oil, rosemary, potatoes |
| `--diet` | Dietary restriction (vegan, vegetarian, gluten-free, keto, etc.) | none |
| `--time` | Max total cooking time in minutes | none |
| `--servings` | Number of servings | 2 |

## Project structure

```
recipe-agent/
├── agent.py           # Main script
├── requirements.txt   # Python dependencies
├── metadata.yaml      # Project metadata
├── .env               # Template for API key
└── .gitignore
```

## Notes

This project is for learning and personal use — it's a small, readable example of building an LLM agent with LangChain rather than a production-ready tool.


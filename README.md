# Game Code Iterator

A free, locally-hosted tool that helps game developers improve code through AI-assisted suggestions.

## Video Demonstration

[![Watch the video demonstration](https://img.shields.io/badge/YouTube-Watch_Demo-red?style=for-the-badge&logo=youtube)](https://youtube.com/your_video_link_here)

## Features

- **Code Improvement Suggestions** with explanations
- **100% Free** - Uses open-source LLMs that run locally
- **Privacy-Preserving** - Your code never leaves your machine

## Getting Started

### Prerequisites

- Python 3.7+
- [Ollama](https://ollama.com/)

### Installation

```bash
# Clone the repository
git clone https://github.com/yourusername/game-code-iterator.git
cd game-code-iterator

# Install dependencies
pip install -r requirements.txt

# Install Ollama from ollama.com

# Download a language model
ollama pull llama3
```

### Running the Application

1. Make sure Ollama is running in the background
2. Start the application: `python game_code_iterator.py`
3. Open your browser: http://127.0.0.1:5000

## Usage

1. Paste your game code
2. Enter what you want to improve
3. Click "Improve Code"
4. Review the suggestions
5. Click "Integrate Changes" if you like the improvements

## Example

**Original Code:**
```python
class Player:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.width = 32
        self.height = 32
        self.velocity_x = 0
        self.velocity_y = 0
        self.is_jumping = False
    def update(self):
        # Apply gravity
        if self.is_jumping:
            self.velocity_y += 0.5
        
        # Update position
        self.x += self.velocity_x
        self.y += self.velocity_y
        
        # Simple ground collision
        if self.y > 400:
            self.y = 400
            self.velocity_y = 0
            self.is_jumping = False
    
    def jump(self):
        if not self.is_jumping:
            self.velocity_y = -10
            self.is_jumping = True
    
    def move_left(self):
        self.velocity_x = -5
    
    def move_right(self):
        self.velocity_x = 5
    
    def stop(self):
        self.velocity_x = 0
```

**Prompt:**
"Improve the physics and add double jump capability in Python"

**Improved Code:**
```python
class Player:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.width = 32
        self.height = 32
        self.velocity_x = 0
        self.velocity_y = 0
        self.is_jumping = False
        self.can_double_jump = False
        self.gravity = 0.5
        self.jump_strength = 10
        self.double_jump_strength = 7
        self.terminal_velocity = 12
        self.ground_friction = 0.15
        self.air_resistance = 0.02
    
    def update(self, delta_time=1.0):
        # Apply gravity with delta time scaling
        self.velocity_y += self.gravity * delta_time
        
        # Apply terminal velocity
        if self.velocity_y > self.terminal_velocity:
            self.velocity_y = self.terminal_velocity
        
        # Apply air/ground friction
        if self.is_jumping:
            # Air resistance
            if self.velocity_x > 0:
                self.velocity_x -= self.air_resistance * delta_time
            elif self.velocity_x < 0:
                self.velocity_x += self.air_resistance * delta_time
        else:
            # Ground friction
            if self.velocity_x > 0:
                self.velocity_x -= self.ground_friction * delta_time
                if self.velocity_x < 0:
                    self.velocity_x = 0
            elif self.velocity_x < 0:
                self.velocity_x += self.ground_friction * delta_time
                if self.velocity_x > 0:
                    self.velocity_x = 0
        
        # Update position with delta time scaling
        self.x += self.velocity_x * delta_time
        self.y += self.velocity_y * delta_time
        
        # Simple ground collision
        if self.y > 400:
            self.y = 400
            self.velocity_y = 0
            self.is_jumping = False
            self.can_double_jump = False  # Reset double jump when landing
    
    def jump(self):
        if not self.is_jumping:
            # First jump
            self.velocity_y = -self.jump_strength
            self.is_jumping = True
            self.can_double_jump = True  # Enable double jump
        elif self.can_double_jump:
            # Double jump
            self.velocity_y = -self.double_jump_strength
            self.can_double_jump = False  # Use up double jump
    
    def move_left(self):
        self.velocity_x = -5
    
    def move_right(self):
        self.velocity_x = 5
    
    def stop(self):
        self.velocity_x = 0
```

## Technical Details

- **Frontend**: HTML, CSS, JavaScript
- **Backend**: Flask web server
- **AI Engine**: Ollama with llama3/codellama

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.


---

Made with ❤️ for game developers


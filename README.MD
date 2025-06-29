# Budget Optimizer - Smart Financial Planning System

A comprehensive web-based budget optimization tool that uses machine learning models to provide personalized financial advice and expense optimization strategies.

## 🚀 Features

### Core Functionality
- **Smart Expense Analysis**: AI-powered analysis of spending patterns using fine-tuned ML models
- **Budget Optimization**: Greedy algorithm-based expense prioritization and optimization
- **EMI Planning**: Dynamic programming approach for optimal EMI plan selection
- **Financial Advice**: Decision tree-based personalized financial recommendations
- **Bank Statement Integration**: Automated processing and analysis of bank statements
- **Expense Forecasting**: ML model trained on Kaggle datasets for future expense prediction

### Advanced Features
- **Multi-User Support**: Individual user profiles with personalized recommendations
- **Real-time Analysis**: Instant financial insights and optimization suggestions
- **Export Functionality**: Save analysis results in JSON format
- **Responsive UI**: Modern, user-friendly interface
- **Transaction Pattern Recognition**: ML-powered spending behavior analysis

## 🛠️ Technology Stack

### Backend
- **Flask**: Web framework for API and server-side logic
- **Python 3.8+**: Core programming language
- **Machine Learning**: Custom models for financial analysis and forecasting

### ML Models & Algorithms
- **Expense Forecasting Model**: Fine-tuned on Kaggle financial datasets
- **Greedy Optimizer**: For expense prioritization and budget allocation
- **Dynamic Programming**: EMI plan optimization
- **Decision Trees**: Financial advice generation
- **Backtracking Algorithm**: Expense analysis and pattern recognition

### Frontend
- **HTML5/CSS3**: Modern responsive design
- **JavaScript**: Interactive user interface
- **Bootstrap**: UI framework for styling

### Data Processing
- **PDF Processing**: Bank statement extraction using pdfplumber
- **JSON**: Data storage and exchange format
- **Pandas/NumPy**: Data manipulation and analysis

## 📦 Installation

### Prerequisites
- Python 3.8 or higher
- pip package manager

### Setup Instructions

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd budgetplanner
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Install ML model dependencies**
   ```bash
   cd ml_models
   pip install -r requirements.txt
   cd ..
   ```

4. **Run the application**
   ```bash
   python app.py
   ```

5. **Access the application**
   - Open your browser and navigate to `http://localhost:5000`

## 🏗️ Project Structure

```
budgetplanner/
├── app.py                          # Main Flask application
├── requirements.txt                # Python dependencies
├── logic/                         # Core algorithms
│   ├── greedy_optimizer.py        # Expense optimization algorithm
│   ├── dp_emi_selector.py         # EMI planning with dynamic programming
│   ├── decision_tree_advice.py    # Financial advice generation
│   └── backtrack_expenses.py      # Expense analysis and backtracking
├── ml_models/                     # Machine learning components
│   ├── expense_forecasting_model.ipynb  # ML model for expense prediction
│   └── requirements.txt           # ML-specific dependencies
├── statement_analysis/            # Bank statement processing
│   ├── pdf_processor.py           # PDF extraction and processing
│   ├── enhanced_processor.py      # Advanced statement analysis
│   └── upload_handler.py          # File upload management
├── bank/                          # Sample bank statements
├── templates/                     # HTML templates
│   └── index.html                 # Main application interface
├── static/                        # Static assets
│   ├── style.css                  # Application styling
│   └── script.js                  # Frontend JavaScript
└── *.json                         # User analysis results
```

## 🤖 Machine Learning Models

### Expense Forecasting Model
Our custom ML model is trained on comprehensive financial datasets from Kaggle, fine-tuned for:
- **Expense Pattern Recognition**: Identifies recurring and seasonal spending patterns
- **Future Expense Prediction**: Forecasts upcoming expenses based on historical data
- **Anomaly Detection**: Flags unusual spending behavior
- **Category-wise Analysis**: Provides insights into spending across different categories

### Model Training Data
- **Source**: Kaggle financial datasets
- **Features**: Transaction history, spending categories, temporal patterns
- **Fine-tuning**: Customized for Indian financial context and spending patterns

### Model Performance
- **Accuracy**: Optimized for real-world financial scenarios
- **Scalability**: Handles multiple user profiles efficiently
- **Real-time Processing**: Provides instant analysis and recommendations

## 📊 Key Algorithms

### 1. Greedy Optimizer
- **Purpose**: Expense prioritization and budget allocation
- **Algorithm**: Greedy approach for optimal resource distribution
- **Use Case**: Maximizing savings while maintaining essential expenses

### 2. Dynamic Programming EMI Selector
- **Purpose**: Optimal EMI plan selection
- **Algorithm**: Dynamic programming for multi-dimensional optimization
- **Use Case**: Finding the best EMI plan considering multiple constraints

### 3. Decision Tree Advice
- **Purpose**: Personalized financial recommendations
- **Algorithm**: Rule-based decision tree system
- **Use Case**: Generating actionable financial advice based on user data

### 4. Backtracking Expenses
- **Purpose**: Expense analysis and pattern recognition
- **Algorithm**: Backtracking for comprehensive expense exploration
- **Use Case**: Deep analysis of spending patterns and optimization opportunities

## 🔧 Configuration

### Environment Variables
Create a `.env` file in the root directory:
```env
# Optional: For enhanced features
ENHANCED_ANALYSIS=true
DEBUG_MODE=false
```

### Bank Statement Processing
- Supported formats: PDF
- Automatic data extraction and categorization
- Transaction pattern analysis

## 📈 Usage Examples

### Basic Budget Analysis
1. Enter your monthly salary
2. Add your expenses with categories and priorities
3. Upload bank statement (optional)
4. Get instant optimization recommendations

### Advanced Features
- **EMI Planning**: Get optimal EMI recommendations
- **Expense Forecasting**: Predict future expenses using ML models
- **Pattern Analysis**: Identify spending patterns and anomalies
- **Personalized Advice**: Receive tailored financial recommendations

## 🎯 Key Benefits

### For Users
- **Personalized Insights**: ML-powered analysis tailored to individual spending patterns
- **Actionable Recommendations**: Specific, implementable financial advice
- **Real-time Optimization**: Instant budget optimization suggestions
- **Comprehensive Analysis**: Multi-dimensional financial assessment

### For Developers
- **Modular Architecture**: Easy to extend and maintain
- **Scalable Design**: Handles multiple users efficiently
- **ML Integration**: Seamless integration of machine learning models
- **API-Ready**: RESTful API design for integration

## 🔮 Future Enhancements

- **Mobile App**: Native mobile application
- **Advanced ML Models**: Deep learning for better predictions
- **Investment Integration**: Stock and mutual fund analysis
- **Real-time Banking**: Direct bank API integration
- **Multi-currency Support**: International financial planning

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 👥 Team

- **Aditya**: Backend Development & ML Model Integration
- **Anirudh**: Algorithm Development & Optimization
- **Alex**: Frontend Development & UI/UX
- **Akshay**: Data Processing & Analysis

## 📞 Support

For support and questions:
- Create an issue in the repository
- Contact the development team
- Check the documentation in the `docs/` folder

---

**Note**: This application uses machine learning models trained on Kaggle datasets and fine-tuned for financial analysis. The models provide intelligent insights but should not be considered as professional financial advice. Always consult with qualified financial advisors for important financial decisions. 

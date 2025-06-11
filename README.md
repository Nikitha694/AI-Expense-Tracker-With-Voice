# AI-Driven Expense Tracker with Voice 🎙️💸

A Streamlit-based AI-powered personal expense tracker that allows users to log daily expenses using voice commands. The system recognizes spoken input, extracts the amount and category, and visualizes expenses through charts.

## 🚀 Features
- 🎙️ **Voice to Text Conversion** using Google SpeechRecognition
- 🧠 **Natural Language Processing (NLP)** to extract amount & category
- 📄 **Expense Log Display** (Latest 10 records)
- 📝 **Edit & Delete** options for expenses
- 📊 **Pie Chart Visualization** for category-wise expense distribution
- 💰 **Overall and Category-wise Totals**
- 🖥️ User-friendly **Streamlit Web Interface**

## 🛠️ Technologies Used
- Python
- Streamlit
- SpeechRecognition
- PyAudio
- Matplotlib
- JSON (for data storage)

## To Run:

```bash
pip install -r requirements.txt
streamlit run app.py

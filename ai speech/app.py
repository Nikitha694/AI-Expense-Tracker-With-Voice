import streamlit as st
import speech_recognition as sr
import re
import json
import os
import matplotlib.pyplot as plt

# ------------------------ SETTINGS ------------------------
DATA_FILE = "expenses.json"
CATEGORIES = ['food', 'groceries', 'rent', 'transport', 'shopping', 'bills', 'entertainment', 'other']

# ------------------------ LOAD/SAVE ------------------------
def load_expenses():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as f:
            return json.load(f)
    return []

def save_expenses(expenses):
    with open(DATA_FILE, "w") as f:
        json.dump(expenses, f, indent=2)

# ------------------------ VOICE INPUT ------------------------
def get_voice_input():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        st.info("🎙️ Listening... Speak your expense clearly")
        audio = recognizer.listen(source)
    try:
        return recognizer.recognize_google(audio)
    except sr.UnknownValueError:
        return "Could not understand audio"
    except sr.RequestError:
        return "API unavailable"

# ------------------------ NLP PARSING ------------------------
def parse_expense(text):
    amount = re.findall(r'\d+', text)
    category = next((cat for cat in CATEGORIES if cat in text.lower()), 'other')
    return int(amount[0]) if amount else 0, category

# ------------------------ MAIN APP ------------------------
st.set_page_config(page_title="AI Expense Tracker", layout="centered")
st.title("💸 AI-Driven Expense Tracker with Voice")

if 'expenses' not in st.session_state:
    st.session_state.expenses = load_expenses()

if 'edit_index' not in st.session_state:
    st.session_state.edit_index = None

# ------------------------ VOICE INPUT ------------------------
if st.button("🎙️ Speak Expense"):
    text = get_voice_input()
    st.write("You said:", f"**{text}**")
    amount, category = parse_expense(text)

    if amount > 0:
        st.session_state.expenses.append({"amount": amount, "category": category})
        save_expenses(st.session_state.expenses)
        st.success(f"✅ Logged ₹{amount} under **{category}**")
    else:
        st.error("❌ Could not extract amount. Please try again.")

# ------------------------ DISPLAY EXPENSES ------------------------
st.subheader("📄 Expense Log (Last 10 Entries)")

if st.session_state.expenses:
    for i, e in enumerate(reversed(st.session_state.expenses[-10:])):
        index = len(st.session_state.expenses) - 1 - i  # real index in list

        col1, col2, col3 = st.columns([5, 1, 1])
        with col1:
            st.markdown(f"**{i+1}. ₹{e['amount']} - {e['category'].capitalize()}**")

        with col2:
            if st.button("✏️ Edit", key=f"edit_{i}"):
                st.session_state.edit_index = index

        with col3:
            if st.button("🗑️ Delete", key=f"delete_{i}"):
                st.session_state.expenses.pop(index)
                save_expenses(st.session_state.expenses)
                st.success("Deleted successfully.")

# ------------------------ EDIT FORM ------------------------
if st.session_state.edit_index is not None:
    st.subheader("✏️ Edit Expense")

    edit_expense = st.session_state.expenses[st.session_state.edit_index]

    new_amount = st.number_input("New Amount:", min_value=0, value=edit_expense['amount'], key="edit_amount_input")
    new_category = st.selectbox("New Category:", CATEGORIES, index=CATEGORIES.index(edit_expense['category']), key="edit_category_input")

    if st.button("✅ Save Changes", key="save_edit"):
        st.session_state.expenses[st.session_state.edit_index]['amount'] = new_amount
        st.session_state.expenses[st.session_state.edit_index]['category'] = new_category
        save_expenses(st.session_state.expenses)
        st.success("Updated successfully.")
        st.session_state.edit_index = None  # Close edit form

    if st.button("❌ Cancel Edit", key="cancel_edit"):
        st.session_state.edit_index = None  # Cancel edit

else:
    st.info("No expenses to edit.")

# ------------------------ TOTAL CALCULATION ------------------------
st.subheader("💰 Total Expenditures by Category")

if st.session_state.expenses:
    total_expense = 0
    category_totals = {cat: 0 for cat in CATEGORIES}

    for e in st.session_state.expenses:
        cat = e['category']
        amt = e['amount']
        total_expense += amt
        category_totals[cat] += amt

    for cat, amt in category_totals.items():
        if amt > 0:
            st.write(f"**{cat.capitalize()}**: ₹{amt}")

    st.markdown(f"### 🧾 **Overall Total Expenditure: ₹{total_expense}**")
else:
    st.warning("No expenses to calculate.")

# ------------------------ PIE CHART ------------------------
st.subheader("📊 Spending Breakdown Chart")

if st.session_state.expenses:
    chart_data = {cat: amt for cat, amt in category_totals.items() if amt > 0}
    if chart_data:
        categories = list(chart_data.keys())
        values = list(chart_data.values())

        fig, ax = plt.subplots()
        ax.pie(values, labels=categories, autopct='%1.1f%%', startangle=90)
        ax.axis('equal')
        st.pyplot(fig)
    else:
        st.info("No data for chart.")
else:
    st.info("Add some expenses to see the chart.")

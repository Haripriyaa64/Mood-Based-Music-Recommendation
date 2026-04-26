# 🎧 Smart Mood-Based Music Recommender

An AI-powered music recommendation system that suggests songs based on **user mood, activity, and language preference**.

Unlike traditional platforms, this system focuses on **context-aware and emotion-driven recommendations** to enhance user experience.

---

# Project Review 

# Dashboard Page
<img width="1815" height="873" alt="image" src="https://github.com/user-attachments/assets/58b7f550-cbbe-4031-a9aa-c594aa15c54c" />

# Search Result
<img width="1648" height="860" alt="image" src="https://github.com/user-attachments/assets/46023dfd-0fd9-496e-914f-d58a228b2b5d" />


## 🚀 Features

* 🧠 **Mood Detection (NLP)**

  * Detects emotions like happy, sad, angry, stressed, calm using TextBlob

* 🏋️ **Context Awareness**

  * Identifies user activity (gym, study, party, sleep, travel)
  * Detects language preference (Punjabi, Hindi, English)

* ⚙️ **Smart Recommendation Engine**

  * Generates filters like energy, tempo, valence, genre

* 🎧 **Real-Time Music Suggestions**

  * Dynamically builds queries and fetches songs using YouTube search

* 🎨 **Modern UI**

  * Dark theme interface
  * Song cards with thumbnails
  * Quick mode buttons (Gym, Study, Relax, Party)

* ⚡ **Fast & Lightweight**

  * No heavy datasets required
  * Real-time response

---

## 🛠️ Tech Stack

### 🔹 Backend

* Python
* Flask
* TextBlob (NLP)
* Flask-CORS

### 🔹 Frontend

* HTML
* CSS
* JavaScript (Fetch API)

### 🔹 Integration

* YouTube (search-based recommendations)

---

## ⚙️ How It Works

1. User enters input (e.g. *"gym punjabi songs"*)
2. NLP module analyzes text and detects mood
3. Context extractor identifies activity & language
4. Filter engine generates parameters:

   * Energy
   * Tempo
   * Valence
   * Genre
5. System builds a smart search query
6. Fetches relevant music from YouTube
7. Displays results in UI

---


## 🧪 Example Inputs

* gym punjabi songs
* feeling sad
* study lofi music
* party dance songs

---

## ⚠️ Limitations

* Uses YouTube search (not exact API results)
* No user login or personalization
* No embedded music player

---

## 🚀 Future Enhancements

* 🎤 Voice input support
* 🤖 Chatbot-based interaction
* 🎧 Embedded music player
* 👤 User login & history tracking
* 📊 Mood analytics dashboard
* 🔗 Spotify API integration


---

## 📜 License

This project is for educational purposes.

---

## 👩‍💻 Author

**Haripriya Pawar**

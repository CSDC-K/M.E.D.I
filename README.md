# 🏥 M.E.D.A | Medical Exercise Data Interface 🤖

![Rust](https://img.shields.io/badge/Rust-000000?style=for-the-badge&logo=rust&logoColor=white)
![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Mediapipe](https://img.shields.io/badge/Mediapipe-008080?style=for-the-badge&logo=google&logoColor=white)
![Status](https://img.shields.io/badge/Status-MVP-orange?style=for-the-badge)

**MEDA** is a high-performance **Hybrid System Architecture** designed to bridge the gap between doctors and patients during physical therapy. By leveraging AI-driven exercise tracking, the project combines the flexibility of Python's AI ecosystem with the memory safety and blazing speed of Rust. 🚀

---

## 🛠 Technical Architecture (System Stack)

The project is engineered as a multi-layered system, ensuring high stability and real-time performance:

* **🧠 Logic & AI Layer (Python):** Utilizes `MediaPipe` and `OpenCV` for real-time biomechanical analysis. It tracks human landmarks to ensure exercises are performed with the correct form.
* **⚙️ System & UI Layer (Rust):** Features an embedded Python interpreter via the `pyo3` library. The frontend is built with `Slint UI`, providing a lightweight, native desktop experience with minimal resource overhead.
* **🔒 Safety & Concurrency:** Implements Rust's `Arc`, `Mutex`, and `AtomicBool` primitives to manage the AI lifecycle and UI thread safely, preventing race conditions during high-frequency data streaming.

---

## ✨ Key Features

* **👁️ Real-Time AI Tracking:** Automated detection and counting of exercises (e.g., squats) with goal-based feedback.
* **🔗 FFI Integration:** Seamless Foreign Function Interface communication between Python's data processing and Rust's system management.
* **⚡ High Performance:** Processed at 30 FPS (approx. 33ms latency) for a lag-free user experience.
* **👨‍⚕️ Doctor Control Panel:** A dedicated management module for patient registration and graphical data analysis.

---

## 📦 Installation

1.  Clone the repository:
    ```bash
    git clone [https://github.com/yourusername/MEDA.git](https://github.com/CSDC-K/MEDA.git)
    ```
2.  Install Python dependencies:
    ```bash
    pip install -r requirements.txt
    ```
3.  Build and run the Rust application:
    ```bash
    cargo run --release
    ```

---

## 🗺️ Future Roadmap & Vision

MEDA is currently in its **MVP (Minimum Viable Product)** phase. While the core AI detection is fully functional, the following architectural expansions are planned:

### ✉️ Automated Data Synchronization & Mail Integration
> **[DEVELOPER NOTE]:** 💡 If I were to implement the mail integration, first i'm gonna create a 'completed-exercises.json' in that file there is completed projects with a 'KEY' this key is created when doctor sends exercise mail (the key changes every mail with a algorithm.) keys will created with algoritm
> algorithm: SQUAT : SQ - AMOUNT like that doctor enters amount of exercise and algorithm created key like that : SQ15|20260101|RANDOMKEY program is reading that key and encoding, What doctor wants? 15 Squat, When it sended? 20260101, how i have to save that exercise? RANDOMKEY

---

## 👨‍💻 Developer

* **Kuzey** - *Lead Software Architect*
* 🛠️ **Focus:** Rust Systems, Python AI, FFI, and Desktop UI Engineering.
* 🎯 **Goal:** Engineering production-ready, safety-critical software.

---

### 🌟 Acknowledgments
This project was developed for the **TUBITAK** science competition to showcase how complex, cross-language systems (Rust & Python) can solve real-world healthcare challenges.

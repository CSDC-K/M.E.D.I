use chrono::{Duration, Utc};
use imap::Session;
use mailparse::{parse_mail, MailHeaderMap};
use native_tls::TlsConnector;
use regex::Regex;
use serde::{Deserialize, Serialize};
use std::collections::HashMap;
use std::fs::{self, OpenOptions};
use std::io::Write;
use std::net::TcpStream;
use std::path::Path;

// --- VERİ YAPILARI ---

/// UI ve Program içinde kullanılacak Egzersiz Verisi
#[derive(Debug, Clone)]
pub struct ExerciseDetails {
    pub squat: u32,
    pub up: u32,
    pub down: u32,
    pub feet: u32,
    pub raw_code: String, // RandomKod (Benzersiz ID)
    pub date: String,
}

/// history.json dosya yapısı
#[derive(Debug, Serialize, Deserialize)]
struct HistoryData {
    // RandomKod -> Tarih
    #[serde(default)] // Eğer JSON'da bu alan yoksa boş oluştur
    pub COMPLETED: HashMap<String, String>,
}

// --- YARDIMCI FONKSİYONLAR ---

/// E-posta gövdesinden Regex ile verileri ayıklar
/// Beklenen Format: CODE-s15u20d10f10|RANDOMKOD|TARİH
fn parse_email_body(body: &str) -> Option<ExerciseDetails> {
    // 1. Ana kalıbı yakala
    // Captures: 1=s...f..., 2=RANDOMKOD, 3=TARİH
    let re_main = Regex::new(r"CODE-([a-z0-9]+)\|([^|]+)\|(.+)").ok()?;
    
    if let Some(caps) = re_main.captures(body) {
        let exercise_str = caps.get(1)?.as_str(); // örn: s15u20d10f10
        let raw_code = caps.get(2)?.as_str().trim().to_string(); // örn: XH52KL
        let date = caps.get(3)?.as_str().trim().to_string(); // örn: 12.12.2023

        // 2. Egzersiz sayılarını çekmek için yardımcı closure
        let get_val = |key: char, text: &str| -> u32 {
            // "s(\d+)" şeklinde regex oluşturur
            let re = Regex::new(&format!(r"{}(\d+)", key)).unwrap();
            re.captures(text)
                .and_then(|c| c.get(1))
                .map(|m| m.as_str().parse().unwrap_or(0))
                .unwrap_or(0)
        };

        Some(ExerciseDetails {
            squat: get_val('s', exercise_str),
            up: get_val('u', exercise_str),
            down: get_val('d', exercise_str),
            feet: get_val('f', exercise_str),
            raw_code,
            date,
        })
    } else {
        None
    }
}

/// Kodun daha önce yapılıp yapılmadığını kontrol eder ve kaydeder.
/// True dönerse: Yeni kod (işle), False dönerse: Eski kod (atla)
fn check_and_save_history(code: &str, date: &str) -> bool {
    let dir_path = "Data";
    let file_path = "Data/history.json";

    // Klasör yoksa oluştur
    if !Path::new(dir_path).exists() {
        let _ = fs::create_dir_all(dir_path);
    }

    // 1. Mevcut Geçmişi Oku
    let mut history: HistoryData = if Path::new(file_path).exists() {
        let data = fs::read_to_string(file_path).unwrap_or_else(|_| "{}".to_string());
        serde_json::from_str(&data).unwrap_or(HistoryData { COMPLETED: HashMap::new() })
    } else {
        HistoryData { COMPLETED: HashMap::new() }
    };

    // 2. Kontrol Et: Zaten var mı?
    if history.COMPLETED.contains_key(code) {
        println!("History Check: '{}' kodu zaten yapılmış. Atlanıyor.", code);
        return false;
    }

    // 3. Yoksa Ekle ve Kaydet
    println!("History Check: '{}' yeni kod. Kaydediliyor...", code);
    history.COMPLETED.insert(code.to_string(), date.to_string());

    if let Ok(json_output) = serde_json::to_string_pretty(&history) {
        if let Ok(mut file) = OpenOptions::new().write(true).create(true).truncate(true).open(file_path) {
            let _ = file.write_all(json_output.as_bytes());
        }
    }

    true
}

// --- ANA FONKSİYON ---

pub fn get_recent_emails_imap(
    domain: &str,
    username: &str,
    password: &str,
) -> Result<Vec<ExerciseDetails>, Box<dyn std::error::Error>> {
    
    // 1. BAĞLANTI (TCP + TLS)
    let tcp_stream = TcpStream::connect((domain, 993))?;
    let tls_connector = TlsConnector::builder().build()?;
    let tls_stream = tls_connector.connect(domain, tcp_stream)?;
    
    let client = imap::Client::new(tls_stream);

    // 2. OTURUM AÇMA
    let mut session = client
        .login(username, password)
        .map_err(|e| e.0)?;

    // 3. ARAMA PARAMETRELERİ (Tarih + Konu)
    let two_weeks_ago = Utc::now() - Duration::days(14);
    let date_query = two_weeks_ago.format("%d-%b-%Y").to_string();

    session.select("INBOX")?;
    
    // SORGUSU: Son 14 gün AND Konu içinde "MEDA-H" geçenler
    let search_query = format!("SINCE {} SUBJECT \"MEDA-H\"", date_query);
    println!("IMAP aranıyor: {}", search_query);

    let uids_set = session.search(&search_query)?;

    // E-posta yoksa boş dön
    if uids_set.is_empty() {
        session.logout()?;
        return Ok(Vec::new());
    }

    // UID setini string'e çevir ("1,2,3")
    let sequence_set_string: String = uids_set.iter()
        .map(|uid| uid.to_string())
        .collect::<Vec<String>>()
        .join(",");

    // 4. VERİ ÇEKME (FETCH)
    let messages = session.fetch(&sequence_set_string, "RFC822")?;
    
    let mut valid_exercises = Vec::new();

    for message in messages.iter() {
        let body = match message.body() {
            Some(b) => b,
            None => continue,
        };

        // Mailparse ile içeriği al
        if let Ok(parsed) = parse_mail(body) {
            // Sadece text body'i almaya çalış
            let body_text = parsed.get_body().unwrap_or_default();

            // 5. REGEX PARSING ve HISTORY KONTROLÜ
            if let Some(details) = parse_email_body(&body_text) {
                
                // History kontrolü: Eğer TRUE dönerse (yeni), listeye ekle.
                if check_and_save_history(&details.raw_code, &details.date) {
                    valid_exercises.push(details);
                }

            } else {
                // Konu MEDA-H ama içerik formatı uymuyor
                // println!("Mail bulundu ama CODE formatı uymuyor.");
            }
        }
    }

    session.logout()?;
    
    // Geçerli, yeni ve formatı uygun egzersizleri döndür
    Ok(valid_exercises)
}
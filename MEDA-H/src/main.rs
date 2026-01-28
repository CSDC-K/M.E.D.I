// main.rs
#![cfg_attr(not(debug_assertions), windows_subsystem = "windows")]

use std::error::Error;
use slint::{SharedString, Image, SharedPixelBuffer, Rgba8Pixel};
use serde::{Deserialize, Serialize};
use std::fs;
use std::sync::{Arc, Mutex};
use std::sync::atomic::{AtomicBool, Ordering};
use std::path::{Path, PathBuf};
use std::thread;
use std::time::Duration;
use pyo3::prelude::*;
use pyo3::types::PyTuple;

slint::include_modules!();

#[derive(Serialize ,Deserialize, Debug)]
struct User{
    username : String,
    useremail : String,
    userkey : String,
    usergender : String,
    userage : i32,
    docemail : String
}

fn main() -> Result<(), Box<dyn Error>> {
    let exe_path = std::env::current_exe().expect("Uygulama yolu bulunamadı.");
    

    let root_dir = exe_path.parent().expect("Ana dizin bulunamadı."); 


    let interpreter_path: PathBuf = root_dir.join("interpreter");
    

    let lib_path: PathBuf = interpreter_path.join("Lib");
    let site_packages_path: PathBuf = lib_path.join("site-packages");


    unsafe {
        std::env::set_var("PYTHONHOME", interpreter_path.to_str().expect("Yol geçersiz")); 

        let python_path_value = format!(
            "{};{}", 
            lib_path.to_str().expect("Yol geçersiz"), 
            site_packages_path.to_str().expect("Yol geçersiz")
        );
        std::env::set_var("PYTHONPATH", python_path_value); 
    }
 
    let stop_ai = Arc::new(AtomicBool::new(false));
    let ui = AppWindow::new()?;
    let ui_handle = ui.as_weak();

    let is_running = Arc::new(Mutex::new(false));
    let is_running_clone = is_running.clone();

    // --- Settings & Save Callbacks ---
    let settings_handle = ui_handle.clone();
    ui.on_settings_up(move || { 
        if let Some(mut ui) = settings_handle.upgrade() {
            _event_load_lines(&mut ui);
            ui.set_active_page("settings".into());
        }
    });

    let save_handle = ui_handle.clone();
    ui.on_save_up(move || { 
        if let Some(mut ui) = save_handle.upgrade(){
            let settings_inputs = [ui.get_line_name(), ui.get_line_email(), ui.get_line_apikey(), ui.get_line_gender(), ui.get_line_docemail(), ui.get_line_age()];
            let has_empty = settings_inputs.iter().any(|s| s.is_empty());

            if has_empty{
                ui.set_popup_type("error".into());
                ui.set_popup_msg("Girilen değerlerden biri boş! Lütfen tüm alanları doldurun.".into());
                ui.set_popup_active(true);
            } else{
                _event_save_changes(&ui);
                _event_load_lines(&mut ui);
                ui.set_popup_type("success".into());
                ui.set_popup_msg("Kullanıcı bilgileri başarıyla kaydedildi.".into());
                ui.set_popup_active(true);
            }
        }
    });

    // --- START CAMERA AI LOGIC ---
    let start_up_handle = ui_handle.clone();
    let stop_ai_clone = stop_ai.clone();

    ui.on_start_up(move || {
        stop_ai_clone.store(false, Ordering::SeqCst);

        if let Some(main_ui) = start_up_handle.upgrade() {
            let thread_ui_handle = main_ui.as_weak();
            let is_running = is_running_clone.clone();
            let stop_flag = stop_ai_clone.clone();
            
            // Bilgi mesajı
            main_ui.set_popup_type("info".into());
            main_ui.set_popup_msg("Yapay zeka başlatılıyor...".into());
            main_ui.set_popup_active(true);

            // AI Thread Başlangıcı
            thread::spawn(move || {
                // Thread kilidi
                let mut running = is_running.lock().unwrap();
                if *running { return; }
                *running = true;
                drop(running);

                // Python Context Hazırlığı
                pyo3::prepare_freethreaded_python();
                Python::with_gil(|py| {
                    let sys = py.import("sys").unwrap();
                    let current_dir = std::env::current_dir().unwrap();
                    let lib_path = current_dir.join("Lib").join("ai-integration");
                    sys.getattr("path").unwrap().call_method1("append", (lib_path.to_str().unwrap(),)).unwrap();

                    // Kamerayı başlat (Global değişkenler sıfırlanır)
                    let module = py.import("ai_model").unwrap();
                    module.getattr("start_camera").unwrap().call0().unwrap();
                });

                // UI de sayfayı değiştir
                let _ = thread_ui_handle.upgrade_in_event_loop(move |ui| {
                    ui.set_active_page("aipage".into());
                    // Popupı kapatabiliriz (isteğe bağlı active false yaparak)
                    // ui.set_popup_active(false); 
                });

                // --- AI Döngüsü ---
                loop {
                    if stop_flag.load(Ordering::SeqCst) {
                        break;
                    }

                    // Python dan 5li veri çekme: (bytes, w, h, counter, finished)
                    let frame_data: Option<(Vec<u8>, u32, u32, i32, bool)> = Python::with_gil(|py| -> PyResult<Option<(Vec<u8>, u32, u32, i32, bool)>> {
                        let module = py.import("ai_model")?;
                        let result = module.getattr("get_ai_frame")?.call0()?;
                        if result.is_none() {
                            return Ok(None);
                        }

                        let tuple: &PyTuple = result.downcast()?;
                        let bytes: &[u8] = tuple.get_item(0)?.extract()?;
                        let width: u32 = tuple.get_item(1)?.extract()?;
                        let height: u32 = tuple.get_item(2)?.extract()?;
                        let counter: i32 = tuple.get_item(3)?.extract()?;   // Squat Sayısı
                        let finished: bool = tuple.get_item(4)?.extract()?; // Bitti mi

                        Ok(Some((bytes.to_vec(), width, height, counter, finished)))
                    }).unwrap_or(None);

                    if let Some((pixels, width, height, _count, finished)) = frame_data {
                        // Görüntü işle
                        let _ = thread_ui_handle.upgrade_in_event_loop(move |ui| {
                            let buffer = SharedPixelBuffer::<Rgba8Pixel>::clone_from_slice(&pixels, width, height);
                            let image = Image::from_rgba8(buffer);
                            ui.set_RPID(image);

                            // Hedef tamamlandıysa SUCCESS Popupını aç
                            if finished {
                                ui.set_popup_type("success".into());
                                ui.set_popup_msg("Tebrikler! 10 Squat Hedefine Ulaştınız!".into());
                                ui.set_popup_active(true);
                            }
                        });


                        if finished {
                             thread::sleep(Duration::from_secs(1));
                             break;
                        }

                    } else {
                        // Kamera hatası
                        let _ = thread_ui_handle.upgrade_in_event_loop(move |ui| {
                            ui.set_active_page("home".into());
                            ui.set_popup_type("error".into());
                            ui.set_popup_msg("Kamera bağlantısı kesildi!".into());
                            ui.set_popup_active(true);
                        });                   
                        break;
                    }

                    // FPS Limiti (30 FPS)
                    thread::sleep(Duration::from_millis(33));
                }

                // Kamera kapatma işlemi
                Python::with_gil(|py| {
                    let module = py.import("ai_model").ok();
                    if let Some(m) = module {
                        let _ = m.getattr("stop_camera").and_then(|f| f.call0());
                    }
                });

                let mut running = is_running.lock().unwrap();
                *running = false;
            });
        }
    });

    let close_ai_handle = ui_handle.clone();
    let stop_ai_handle = stop_ai.clone();
    ui.on_close_ai(move || {
        if let Some(main_ui) = close_ai_handle.upgrade() {
            stop_ai_handle.store(true, Ordering::SeqCst);
            let nocamimg = load_image_to_rpid("ui/Img/nocam.png");
            main_ui.set_RPID(nocamimg);
        }
    });

    ui.run()?;
    Ok(())
}

fn _event_load_lines(ui_model : &mut AppWindow){
    let user_data_file = fs::read_to_string("Data\\User.json").expect("Error!");
    let user: User = serde_json::from_str(&user_data_file).expect("Error!");
    ui_model.set_username(SharedString::from(&user.username));
    ui_model.set_useremail(SharedString::from(&user.useremail));
    ui_model.set_userkey(SharedString::from(&user.userkey));
    ui_model.set_usergender(SharedString::from(&user.usergender));
    ui_model.set_userage(user.userage);
    ui_model.set_docemail(SharedString::from(&user.docemail));
}

fn _event_save_changes(ui_model : &AppWindow){
    let user_data_file = fs::read_to_string("Data\\User.json").unwrap();
    let _ : serde_json::Value = serde_json::from_str(&user_data_file).unwrap();
    let user_name = ui_model.get_line_name().to_string();
    let user_api = ui_model.get_line_apikey().to_string();
    let user_gender = ui_model.get_line_gender().to_string();
    let user_email = ui_model.get_line_email().to_string();
    let user_age : i32 = ui_model.get_line_age().parse().expect("Error!");
    let doc_email = ui_model.get_line_docemail().to_string();

    let usersave_struct = User {
        username : user_name,
        userkey : user_api,
        usergender : user_gender,
        userage : user_age,
        useremail : user_email,
        docemail : doc_email
    };
    let json_data = serde_json::to_string_pretty(&usersave_struct).unwrap();
    fs::write("Data\\User.json", json_data).unwrap();
}

fn load_image_to_rpid(path: &str) -> Image {
    let bytes = fs::read(path).expect("Dosya okunamadı");
    let img = image::load_from_memory(&bytes).unwrap().to_rgba8();
    let width = img.width() as u32;
    let height = img.height() as u32;
    let buffer = SharedPixelBuffer::<Rgba8Pixel>::clone_from_slice(img.as_raw(), width, height);
    Image::from_rgba8(buffer)
}
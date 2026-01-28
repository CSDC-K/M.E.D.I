fn main() {
    slint_build::compile_with_config("ui/app-window.slint", slint_build::CompilerConfiguration::new().with_style(String::from("fluent-dark"))).expect("Error!");
}

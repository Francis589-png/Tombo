use crate::lexer::Lexer;
use crate::parser::Parser;
use crate::interpreter::Interpreter;
use rustyline::DefaultEditor;

pub fn run() -> anyhow::Result<()> {
    println!("╔══════════════════════════════════════════╗");
    println!("║       TOMBO LANGUAGE INTERPRETER        ║");
    println!("║              v1.0.0 REPL                ║");
    println!("╚══════════════════════════════════════════╝");
    println!();
    println!("Type code and press Enter to execute");
    println!("Type 'exit' or 'quit' to exit");
    println!();

    let mut editor = DefaultEditor::new()?;
    let mut interp = Interpreter::new();

    let mut buffer: Vec<String> = Vec::new();
    loop {
        let prompt = if buffer.is_empty() { ">> " } else { "...   > " };
        let readline = editor.readline(prompt);
        match readline {
            Ok(line) => {
                let trimmed = line.trim();
                if buffer.is_empty() && (trimmed == "exit" || trimmed == "quit") {
                    break;
                }

                // add to buffer
                buffer.push(line.clone());

                // if user entered an empty line while building a block, try to parse what we have
                if trimmed.is_empty() && !buffer.is_empty() {
                    let source = buffer.join("\n");
                    match run_code(&source, &mut interp) {
                        Ok(_) => {
                            buffer.clear();
                        }
                        Err(e) => {
                            println!("Error: {}", e);
                            buffer.clear();
                        }
                    }
                    continue;
                }

                // try to parse/execute current buffer
                let source = buffer.join("\n");
                match run_code(&source, &mut interp) {
                    Ok(_) => {
                        buffer.clear();
                    }
                    Err(_e) => {
                        // assume incomplete input; continue reading lines
                        continue;
                    }
                }
            }
            Err(_) => break,
        }
    }

    println!("Goodbye!");
    Ok(())
}

fn run_code(source: &str, interp: &mut Interpreter) -> Result<(), String> {
    let mut lexer = Lexer::new(source);
    let tokens = lexer.tokenize().map_err(|e| e.to_string())?;
    let mut parser = Parser::new(tokens);
    let ast = parser.parse().map_err(|e| e.message)?;
    interp.evaluate(&ast)?;
    Ok(())
}

mod lexer;
mod parser;
mod interpreter;
mod ast;
mod cli;
mod repl;

use std::fs;
use std::path::PathBuf;
use clap::Parser;

#[derive(Parser, Debug)]
#[command(name = "TOMBO")]
#[command(about = "A universal interpreted programming language")]
#[command(version = "1.0.0")]
struct Args {
    /// File to execute
    file: Option<PathBuf>,

    /// Run interactive REPL
    #[arg(short, long)]
    repl: bool,

    // (version flag handled by clap automatically)
    // version: bool,
}

fn main() -> anyhow::Result<()> {
    let args = Args::parse();

    if args.repl || args.file.is_none() {
        repl::run()?;
    } else if let Some(file) = args.file {
        run_file(&file)?;
    }

    Ok(())
}

fn run_file(path: &PathBuf) -> anyhow::Result<()> {
    let source = fs::read_to_string(path)?;
    let mut lexer = lexer::Lexer::new(&source);
    let tokens = lexer.tokenize().map_err(|e| anyhow::anyhow!(e.to_string()))?;
    let mut parser = parser::Parser::new(tokens);
    let ast = parser.parse().map_err(|e| anyhow::anyhow!(e.message))?;
    let mut interpreter = interpreter::Interpreter::new();
    interpreter.evaluate(&ast).map_err(|e| anyhow::anyhow!(e))?;
    Ok(())
}

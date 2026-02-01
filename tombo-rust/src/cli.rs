pub mod cli {
    use clap::Parser;
    use std::path::PathBuf;

    #[derive(Parser, Debug)]
    #[command(name = "TOMBO")]
    #[command(about = "A universal interpreted programming language")]
    #[command(version = "1.0.0")]
    pub struct Args {
        /// File to execute
        pub file: Option<PathBuf>,

        /// Run interactive REPL
        #[arg(short, long)]
        pub repl: bool,

        /// Print version
        #[arg(short, long)]
        pub version: bool,
    }
}

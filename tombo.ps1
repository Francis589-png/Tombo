# Tombo Language Interpreter - PowerShell Wrapper

param(
    [string]$Script
)

$TomboPath = Split-Path -Parent $MyInvocation.MyCommand.Path
$PythonScript = Join-Path $TomboPath "tombo.py"

if ($Script) {
    python $PythonScript $Script
} else {
    python $PythonScript
}

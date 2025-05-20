python -m venv venv

.\venv\Scripts\Activate.ps1

$envFile = ".env"
Get-Content $envFile | ForEach-Object {
    $name, $value = $_ -split '='
    [System.Environment]::SetEnvironmentVariable($name, $value, [System.EnvironmentVariableTarget]::User)
}

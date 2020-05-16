conda activate py37
$watcher = New-Object System.IO.FileSystemWatcher
$watcher.Path = "C:\Users\sk\OneDrive\Documents\gnucash\suica"
$watcher.Filter = "*.*"
$watcher.IncludeSubdirectories = $false
$watcher.EnableRaisingEvents = $true  

$action = {$path = $Event.SourceEventArgs.FullPath
    $str = "python C:\Users\sk\code\gnucash_import_util\importcsv2gnucash.py C:\Users\sk\OneDrive\Documents\gnucash\kakeibo_jpy_sql_migrated.gnucash $path"
    Invoke-Expression $str
}

$job = Register-ObjectEvent $watcher "Created" -Action $action
echo "Starting the watcher job for importing csvs to gnucash..."
$job
echo "Import logs:"
while ($true) {
    Receive-Job -Job $job
    sleep 5
}
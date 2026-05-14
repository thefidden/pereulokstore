"" | Out-File all_code.txt -Encoding utf8

git ls-files | ForEach-Object {
    $file = $_

    Add-Content all_code.txt "`n=============================="
    Add-Content all_code.txt "FILE: $file"
    Add-Content all_code.txt "==============================`n"

    Get-Content $file | Add-Content all_code.txt
}
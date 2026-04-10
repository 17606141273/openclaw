# -*- coding: utf-8 -*-
[Console]::OutputEncoding = [System.Text.Encoding]::UTF8
$env:PYTHONIOENCODING = "utf-8"
python "$PSScriptRoot\tavily_search.py" --query $args[0] --max-results $args[1] --format $args[2]

def html_head(target_raw):
    code = '''
    <!DOCTYPE html>
        <html lang="ko">
            <head>
                <meta charset="utf-16">
                <title>출력 결과: %s</title>
                <style>
                    div.pa {
                        padding: 0px 1000px 15px 15px;
                    }                    
                    body {
                        background-color: #000000;
                    }
                    p {
                        color: #FFFFFF;
                    }
                </style>
            </head>
            <body>
                <div class="pa">
            '''%target_raw
    
    return code

def html_tail():
    code = "</div></body></html>"

    return code
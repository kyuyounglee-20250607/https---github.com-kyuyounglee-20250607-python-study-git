# node.js 다운로드 및 설치
# gemini cli 설치
```
npm install -g @google/gemini-cli
```

# Google AI Studio에서 API 키 발급

https://aistudio.google.com/apikey
접속

# 구글 계정 로그인

“Create API key” (API 키 만들기) 클릭

# 키가 생성되면 복사해 둡니다. (예: AIzaSy... 형태)

# PowerShell 또는 CMD에서 아래 명령 실행
```
setx GEMINI_API_KEY "<당신의키>"
```

등록 후 PowerShell을 닫고 새 창을 열어야 적용됩니다.

확인하려면:
```
echo %GEMINI_API_KEY%
gemini init
settings.json파일이 생김 단 실행한 폴더에 git이나 기타 프로젝트가 없으면
안생기면 직접 생성
```



# settings.json 생성 및 수정
```
C:\Users\사용자\.gemini
직접파일 생성 및 mcp 서버 추가
```
# mcp서버
```
smithery.ai 를 이용해도 되지만.. 안되면 claud에서 사용했던 mcp 시도
설정후 터미널에서
gemini mcp list 입력
서버가 연결된 것을 확인
```
```
{
  "mcpServers": {
    "filesystem": {
        "command": "npx",
        "args": [
            "-y",
            "@modelcontextprotocol/server-filesystem",
            "D:/week_src",
            "C:/Users/tj/Downloads"
            ]
        }
    }
}

```

# gemini mcp 사용
```
확장프로그램  Gemini Code Assist를 설치해서 에이전트로 사용
예) filesystme mcp가 동작한다면
"로컬 파일 목록 보여줘"
```

# sequentialthinking
```
smethery.ai 에서 검색해서 등록한다.
ex)
{
  "mcpServers": {
    "server-sequential-thinking": {
      "command": "cmd",
      "args": [
        "/c",
        "npx",
        "-y",
        "@smithery/cli@latest",
        "run",
        "@smithery-ai/server-sequential-thinking",
        "--key",
        "당신의 키.. 자동으로 셋팅되어 있음",
        "--profile",
        "parliamentary-tahr-EbBoPy"
      ]
    }
  }
}
```

# gemini mcp list 입력해서 mcp서버들이 연결되는것을 확인
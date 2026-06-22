class Commit:
    # git 단일 커밋 노드 객체
    def __init__ (self, commit_hash, message, author, timestamp, parents):
        self.hash = commit_hash
        self.message = message
        self.author = author
        self.timestamp = timestamp
        self.parents = parents # 부모 커밋 해시 문자열 리스트

    def __str__(self):
        return f"commit {self.hash} ({self.author}, {self.timestamp})\n{self.message}"
        
import uuid
from datetime import datetime
from model import Commit
from algorithms import insertion_sort, topological_sort_dfs, find_shortest_path


class InvertedIndex:
    # 역색인 통한 빠른 commit 검색 기능
    def __init__(self):
        self.keyword_index = {} #dict: 키 = 키워드, 값 = set(commit 해시)
        self.author_index = {} #dict: 키 = 작성자(소문자), 값 = set(commit 해시)

    def add_commit(self, commit):
        # 작성자 기반 역색인
        author_lower = commit.author.lower()
        # 처음 등장하는 작성자인 경우 새로운 set 생성
        if author_lower not in self.author_index:
            self.author_index[author_lower] = set() 
        # 해당 작성자의 commit hash를 집합에 추가
        self.author_index[author_lower].add(commit.hash) 

        # 메시지 키워드 역색인
        tokens = commit.message.lower().split()
        for token in tokens:
            # 처음 등장하는 키워드인 경우 새로운 set 생성
            if token not in self.keyword_index:
                self.keyword_index[token] = set()
            # 해당 키워드의 commit hash를 집합에 추가
            self.keyword_index[token].add(commit.hash)

    def search_keyword(self, keyword):
        return self.keyword_index.get(keyword.lower(), set())

    def search_author(self, author):
        return self.author_index.get(author.lower(), set())

class MiniGit:
    def __init__(self):
        self.is_initialized = False
        self.current_user = None
        self.commits = {} #hash를 키, Commit 객체를 value로 가진다
        self.branches = {} #branch 이름을 키, Commit 해시를 value로 가진다
        self.current_branch = None
        self.index = InvertedIndex() # 역색인용 인덱싱

    def init(self, user_name): # 초기 저장소 및 사용자 설정
        self.is_initialized = True
        self.current_user = user_name
        self.branches["main"] = None # 초기에는 commit이 없으므로 None.
        self.current_branch = "main" # 초기 브랜치는 main
        print("저장소 초기화")
        print(f"현재 branch: {self.current_branch}")
        print(f"현재 user: {self.current_user}")

    def branch(self, branch_name): # branch 생성
        if branch_name in self.branches: # 이미 생성된 branch인지 확인
            print(f"이미 {branch_name} branch가 존재합니다.")
            return
        # 새로운 branch가 현재 branch의 최신 commit을 가리키도록 생성
        self.branches[branch_name] = self.branches[self.current_branch]
        print(f"{branch_name} branch 생성")

    def switch(self, branch_name): # branch 전환하기
        if branch_name not in self.branches: # 전환 대상 branch가 없을 경우
            print(f"에러: {branch_name} branch를 찾을 수 없습니다.")
            return
        self.current_branch = branch_name
        print(f"branch를 {branch_name}로 전환합니다.")

    
    def commit(self, message):
        while True: #hash 값이 중복되지 않을때까지 반복
            new_hash = uuid.uuid4().hex[:6]
            if new_hash not in self.commits:
                break

        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        parent = self.branches[self.current_branch] # 현재 branch hash를 parent로 저장
        parents = [parent] if parent else [] # 현재 branch 
        # parent, timestamp, parents를 사용하여 Commit 객체 생성
        new_commit = Commit(new_hash, message, self.current_user, timestamp, parents)
        self.commits[new_hash] = new_commit
        self.branches[self.current_branch] = new_hash

        # 역색인 업데이트
        self.index.add_commit(new_commit)
        print(f"[{self.current_branch} {new_hash}] {message}")
        
    
    def log(self, sort_by=None):
        if not self.commits:
            print("커밋이 없습니다.")
            return

        if sort_by == "date":
            # 날짜 순 정렬
            commits_list = list(self.commits.values())
            sorted_commits = insertion_sort(commits_list, lambda a, b: a.timestamp > b.timestamp)
        elif sort_by =="author":
            # 작성자 순 정렬
            commits_list = list(self.commits.values())
            sorted_commits = insertion_sort(commits_list, lambda a, b: a.author > b.author)
        else:
            #단순 위상정렬
            sorted_commits = topological_sort_dfs(self.commits)

        for commit in sorted_commits:
            # 커밋이 가리키는 branch tag 표시
            tags = [b for b, h in self.branches.items() if h == commit.hash] # b는 branch 이름, h는 branch의 hash 값
            tag_str = f"[{', '.join(tags)}]" if tags else "" # tags 리스트를 ,로 연결해 문자열로 만들기, tags에 아무것도 없으면 빈 문자열
            print(f"commit {commit.hash} ({commit.author} {commit.timestamp}){tag_str}\n{commit.message}")

            
    def path(self, hash1, hash2):
        # 두 커밋의 최단 경로 찾기
        path_str = find_shortest_path(self.commits, hash1, hash2)
        if path_str:
            print(f"Path: {path_str}")
        else:
            print("no Path")


    def ancestors(self, commit_hash):
        # 조상 커밋 찾기
        if commit_hash not in self.commits: # 존재하지 않는 커밋이면 에러 출력
            print(f"Unknown commit: {commit_hash}")
            return
        
        visited = set()
        def dfs(c_hash): # dfs 기반으로 조상 커밋 찾기
            visited.add(c_hash)
            for p in self.commits[c_hash].parents: # 부모 커밋 순회
                if p not in visited:
                    dfs(p)

        dfs(commit_hash)
        visited.remove(commit_hash) # 자신은 조상 목록에서 제외할 것.
        # 조상 목록 출력
        if not visited:
            print("No ancestors.")
        else:
            print("Ancestors:", ", ".join(visited))

    def search(self, keyword=None, author=None):
        # 역색인 기반으로 커밋 검색
        results = set()
        if keyword:
            results = self.index.search_keyword(keyword)
        elif author:
            results = self.index.search_author(author)

        # 검색 목록 출력
        print(f"Found {len(results)} commits")
        for c_hash in results:
            print(f"- {c_hash}: {self.commits[c_hash].message}")

    
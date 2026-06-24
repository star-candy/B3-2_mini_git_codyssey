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

        
from collections import deque

def insertion_sort(arr, comp_func):
    # 삽입정렬 구현
    # comp_func가 true라면 a가 b보다 큼을 의미함.
    sorted_arr = arr[:] # input arr 복사

    # 0번째는 초기 정렬됨 가정, 1~i까지 정렬함
    for i in range(1, len(sorted_arr)):
        key_item = sorted_arr[i]
        j = i - 1
        # 앞 원소가 키보다 크다면 뒤로 밀어냄 - 오름차순 swap 작업
        while j >= 0 and comp_func(sorted_arr[j], key_item):
            sorted_arr[j + 1] = sorted_arr[j]
            j -= 1
        sorted_arr[j + 1] = key_item
    return sorted_arr
        
def topological_sort_dfs(commits_dict):
    # dfs 기반 위상정렬 (부모가 자식보다 먼저 구성되도록 정렬)
    visited = set() #이미 방문한 node key 저장
    result = [] # 정렬된 node key 저장

    def dfs(commit_hash):
        # 노드가 이미 방문했다면 부모 찾기 종료
        if commit_hash in visited:
            return
        visited.add(commit_hash)

        commit = commits_dict[commit_hash]
        for parent_hash in commit.parents:
            dfs(parent_hash) #부모 노드에 대해 재귀적으로 dfs 수행

        # 재귀 종료 시점에 결과에 추가됨
        # 따라서 조상부터 부모 순으로 정렬됨.
        result.append(commit) 

    # 사전순으로 input순서 정렬 및 dfs 수행
    # 동일 depth간 input 순서 유지 위해 사용
    # commits_dict.keys의 경우 순서 보장 x 따라서 정렬 필요 (재현성 유지 위함)
    sorted_hashes = insertion_sort(list(commits_dict.keys()), lambda a, b: a > b)
    for c_hash in sorted_hashes:
        if c_hash not in visited:
            dfs(c_hash)

    return result


def find_shortest_path(commits_dict, start, end):
    # 두 커밋간 최단 경로 bfs로 탐색하기
    if start not in commits_dict or end not in commits_dict:
        return None

    # 무방향 인접 리스트 구성
    # adj는 각 key에 대해 빈 리스트를 value로 가짐
    adj = {h: [] for h in commits_dict} 
    for h, c in commits_dict.items(): #h에 key(hash), c에 commit 객체 저장
        # 부모 자식 인접 리스트에 해시를 양방향으로 저장 (무방향 그래프 구성)
        for p in c.parents:
            adj[h].append(p)
            adj[p].append(h)

    queue = deque([(start, [start])]) # (현재 커밋 해시, 현재 커밋까지의 경로)
    visited_len = {start: 1} # 각 노드까지 도달한 거리 저장
    shortest_paths = [] #최단경로 저장
    min_length = float('inf') #최단경로 길이 저장

    while queue:
        curr, path = queue.popleft() # 현재 커밋 해시, 커밋까지의 경로 pop

        if len(path) > min_length: # 현재 경로가 최단경로보다 길면 탐색 종료
            break

        if curr == end:
            if len(path) < min_length: # 현재 경로가 최단 경로보다 짧다면 업데이트
                min_length = len(path)
                shortest_paths = [path]
            elif len(path) == min_length: # 동차 최단경로시 path append
                shortest_paths.append(path) 
            continue

        for nxt in adj[curr]: # adj[curr]는 curr의 이웃 노드들을 저장
            # 더 짧거나 같은 길이로 도달되는 경우 탐색한다.
            if nxt not in visited_len or visited_len[nxt] >= len(path) + 1:
                visited_len[nxt] = len(path) + 1
                queue.append((nxt, path + [nxt]))

    if not shortest_paths:
        return None

    # 사전순으로 가장 앞서는 경로 문자열 생성, 반환
    path_strs = ["->".join(p) for p in shortest_paths]
    sorted_paths = insertion_sort(path_strs, lambda a, b: a > b)
    return sorted_paths[0]
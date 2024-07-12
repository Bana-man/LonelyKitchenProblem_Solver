import math
import copy
from typing import List, Tuple

# menghasilkan list node yang dapat dikunjungi dan masih memiliki task yang perlu dikerjakan
def availNode(n: int, mv: List[List[int]]) -> List[int]: 
    listAvail = []
    for i in range(n):
        if mv[i] != []: 
            listAvail.append(i)
        
    return listAvail

# fungsi rekursif me-return nilai minimum dan path yang harus dilalui
def rekursif(n:int, mt: List[int], mv: List[List[int]], nodeNow: int) -> Tuple[int, List[int]]:
    listNode = availNode(n, mv)

    if (listNode == []): # Basis: saat seluruh pekerjaan telah selesai
        return [0, [nodeNow]]
    
    min_time = math.inf
    min_path = []
    for nodeDikunjungi in listNode: # mengecek setiap jalur yang bisa dikunjungi
        time = 0
        time += mk[nodeNow][nodeDikunjungi] # menambah waktu perjalanan dari nodeNow ke nodeDikunjungi

        tempMT = copy.deepcopy(mt)
        tempMV = copy.deepcopy(mv)

        tempMT[nodeDikunjungi] -= time
        if (tempMT[nodeDikunjungi] > 0): # jika pada saat sampai nodeDikunjungi, masih ada waktu tersisa
            time += tempMT[nodeDikunjungi] # menambah waktu tersisa pada nodeDikunjungi
        tempMT[nodeDikunjungi] = 0
        tempMV[nodeDikunjungi].pop()

        for y in range(len(tempMT)): # mengurangi setiap timer dengan waktu yang telah dilalui
            tempMT[y] -= time
            if (tempMT[y] < 0):
                tempMT[y] = 0

        if (tempMV[nodeDikunjungi] != []): # mengupdate timer nodeDikunjungi dengan proses yg dilakukan
            tempMT[nodeDikunjungi] = tempMV[nodeDikunjungi][-1]

        hasil = rekursif(n, tempMT, tempMV, nodeDikunjungi)
        time += hasil[0]

        if (time < min_time): # mencari waktu paling minimum
            min_time = time
            min_path = [nodeNow] + hasil[1]

    return [min_time, min_path]

def read_file() -> Tuple[int, List[List[int]], List[List[int]], int]:
    file_name = input("Masukkan nama file: ")

    try:
        mk = []; mv = []
        with open("../test/" + file_name, 'r') as file:
            n = int(file.readline())
            startNode = int(file.readline())
            if (startNode >= n or startNode < 0):
                print("Start Node invalid!")
                return None

            for _ in range(n):
                line = file.readline()
                line = list(map(int, line.split(' ')))
                if (len(line) != n):
                    print("Jumlah node tidak sesuai pada matriks ketetanggan!")
                    return None
                mk.append(line)

            for _ in range(n):
                line = file.readline()
                line = list(map(int, line.split(' '))) + [0]
                mv.append(line)

        return [n, mv, mk, startNode]

    except FileNotFoundError:
        print(f"File `{file_name}` tidak ditemukan pada folder `test`!")
        return None


if (__name__ == "__main__"):
    read = None
    while (read == None):
        read = read_file()

    n = read[0] # banyak node
    mv = read[1] # Matriks Value ( mv[i] -> List waktu pekerjaan yang dikerjakan pada node ke-i )
    mk = read[2] # Matriks Ketetanggaan ( mk[i][j] -> Waktu yang ditempuh untuk pindah dari node ke-i ke node ke-j )
    mt = [0 for _ in range(n)] # Matriks Timer ( mt[i] -> Waktu untuk menyelesaikan pekerjaan yang berlangsung di node ke-i )
    startNode = read[3] # node yang pertama dikunjungi

    print("\nMatriks Ketetanggan: ")
    for i in mk:
        print(i)

    print("\nList Waktu Pekerjaan: ")
    for i in range(n):
        print(f"Node ke-{i}: {mv[i]}")

    print(f"\nStart Node: {startNode}")

    # mengunjungi startNode
    mv[startNode].pop()
    mt[startNode] = mv[startNode][-1]

    hasil = rekursif(n, mt, mv, startNode)
    print(f"\nWaktu minimum: {hasil[0]} \nJalur Dilalui: {hasil[1]}")

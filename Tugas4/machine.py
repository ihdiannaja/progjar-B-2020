from handler import Handle
import json
import logging

'''
        PROTOCOL FORMAT

string terbagi menjadi 2 bagian yang dipisahkan oleh spasi
Format : command *spasi* parameter *spasi* parameter

        FITUR

a. Meletakkan File (untuk menambahkan file ke dalam folder Tugas4.1) 
   Request   : meletakkanfile
   Parameter : namafile *spasi* isi dari file
   Response  : Jika berhasil, print "Meletakkan file berhasil" dan jika gagal print "CEK ULANG"

b. Mengambil File (untuk mengambil file berdasarkan nama file dari folder Tugas4.1)
   Request   : getfile
   Parameter : [namafile yang ingin diambil]
   Response  : Jika berhasil, print "file berhasil diambil" dan jika gagal print "CEK ULANG"

c. Melihat Daftar File (untuk melihat list file di dalam folder Tugas4.1)
   Request : listfile
   Parameter: -
   Response: daftar file dalam folder Tugas 4.1

d. Jika command tidak dikenali akan merespon dengan ERRCMD

'''
p = Handle()

class Machine:
    def proses(self,string_to_process):
        s = string_to_process
        cstring = s.split(" ")
        try:
            command = cstring[0].strip()
            if (command=='meletakkanfile'):
                print("meletakkanfile")
                filename = cstring[1].strip()
                file = cstring[2].strip()
                # print(file)
                print("Meletakkan",filename)
                # print()
                p.add(filename,file.encode())
                return "Meletakkan file berhasil"

            elif (command=='ambilfile'):
                print("mengambilfile")
                filename = cstring[1].strip()
                print("Mengambil", filename)
                hasil = p.get(filename)
                return hasil

            elif (command=='daftarfile'):
                logging.info("daftarfile")
                print("daftar file")
                hasil = p.list()
                dict = {"keterangan":"berhasil","isi folder":hasil}
                return json.dumps(dict)
            else:
                return "ERRCMD"
        except:
            return "CEK ULANG"


if __name__=='__main__':
    machine = Machine()
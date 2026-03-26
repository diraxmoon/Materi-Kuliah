#membuat struktur data dictionary
userLogin = {"name": "Fathiya", "age":19, "role":"ilustratorhandal"}
print(type(userLogin))
# Mengakses Data

print(f"Nama Akun : {userLogin['name']}")
print(f"Umur Akun : {userLogin['age']} Tahun")
print(f"Role Akun : {userLogin['role']}")

#akses data seluruh
print(userLogin.items())
print(userLogin.keys())
print(userLogin.values())

# Menambah Data kedalam dictionary big-O O(1)
userLogin["email"] = "fathiyafadhilah@gmail.com"
print(userLogin)

# Menghapus Data dari dictionary big-O O(1)
userLogin.pop("age")
print(userLogin)

#mengubah data dalam dictionary big-O O(1)
userLogin["role"] = "ilustrator rajin"
print(userLogin)

#nested dictionary
dbUser = {"user1": {"name": "Fathiya", "age": 19, "role": "ilustrator rajin"},
          "user2": {"name": "Dira", "age": 20, "role": "artist pemula"},
          "user3": {"name": "Moon", "age": 21, "role": "artist pembaik"}}

print(dbUser)

#akses value base key
print(dbUser["user1"])

#melakukan pencarian data dalam dictionary
finword = input("Masukkan nama user yang ingin dicari: ")
if finword in dbUser:
    print("Data ditemukan")
    print(dbUser[finword])
else:
    print("Data tidak ditemukan")
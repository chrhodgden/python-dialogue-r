import dialoguer

src_fil_r = dialoguer.Dialogue('source_file.r')
print('active:', src_fil_r.active)
src_fil_r.open()
print('active:', src_fil_r.active)

msg_1 = src_fil_r.import_variable('msg_1')
print(msg_1)

msg_2 = src_fil_r.import_variable('msg_2')
print(msg_2)

print('active:', src_fil_r.active)
src_fil_r.close()
print('active:', src_fil_r.active)

print("end launcher")


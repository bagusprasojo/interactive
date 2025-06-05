# kuis/models.py
from django.db import models

class Kuis(models.Model):
    nama_kuis = models.CharField(max_length=255)
    waktu_mulai = models.DateTimeField()
    is_active = models.BooleanField(default=False)

    def __str__(self):
        return self.nama_kuis
    

class Soal(models.Model):
    kuis = models.ForeignKey(Kuis, on_delete=models.CASCADE, related_name='soal_set', default=1)
    pertanyaan = models.TextField()
    jawaban_a = models.CharField(max_length=255)
    jawaban_b = models.CharField(max_length=255)
    jawaban_c = models.CharField(max_length=255)
    jawaban_d = models.CharField(max_length=255)
    jawaban_benar = models.CharField(max_length=1, choices=[('A','A'), ('B','B'), ('C','C'), ('D','D')])

    def __str__(self):
        return self.pertanyaan
    
class Peserta(models.Model):
    nama = models.CharField(max_length=255)
    kuis = models.ForeignKey(Kuis, on_delete=models.CASCADE)
    skor = models.IntegerField(default=0)

    def __str__(self):
        return self.nama
    
class JawabanPeserta(models.Model):
    peserta = models.ForeignKey(Peserta, on_delete=models.CASCADE)
    soal = models.ForeignKey(Soal, on_delete=models.CASCADE)
    jawaban = models.CharField(max_length=1)  # A, B, C, D
    benar = models.BooleanField(default=False)
    waktu_dijawab = models.DateTimeField(auto_now_add=True)



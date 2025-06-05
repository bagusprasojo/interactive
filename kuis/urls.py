# kuis/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('daftar/<int:kuis_id>/', views.daftar_kuis, name='kuis_daftar'),
    path('kuis/<int:kuis_id>/', views.tampilkan_soal, name='kuis_soal'),
    path('api/kuis/<int:kuis_id>/soal/<int:nomor>/', views.get_soal_ke),
    path('kuis/admin/kontrol/<int:kuis_id>/', views.admin_kontrol, name='admin_kontrol'),
    path('api/status_kuis/<int:kuis_id>/', views.status_kuis_api),
    path('kuis/soal/<int:kuis_id>/', views.tampilkan_soal, name='tampilkan_soal'),
    path('api/submit_jawaban/', views.submit_jawaban, name='submit_jawaban'),   
    path('kuis/<int:kuis_id>/leaderboard/', views.leaderboard, name='leaderboard')


]

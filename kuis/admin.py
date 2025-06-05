from django.contrib import admin
from .models import Soal, Kuis, Peserta, JawabanPeserta
from django.urls import path, reverse
from django.http import HttpResponseRedirect
from django.template.response import TemplateResponse


# Register your models here.
class SoalAdmin(admin.ModelAdmin):
    list_display = ('kuis' ,'pertanyaan', 'jawaban_a', 'jawaban_b', 'jawaban_c', 'jawaban_d', 'jawaban_benar')
    search_fields = ('pertanyaan',) 

class KuisAdmin(admin.ModelAdmin):
    list_display = ('nama_kuis', 'waktu_mulai', 'is_active')
    search_fields = ('nama_kuis',)

class PesertaAdmin(admin.ModelAdmin):
    list_display = ('nama', 'kuis', 'skor')
    search_fields = ('nama',)

class JawabanPesertaAdmin(admin.ModelAdmin):
    list_display = ('peserta', 'soal', 'jawaban', 'benar', 'waktu_dijawab')
    search_fields = ('peserta__nama', 'soal__pertanyaan')

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('jawaban_peserta/<int:peserta_id>/', self.admin_site.admin_view(self.jawaban_peserta_view), name='jawaban_peserta'),
        ]
        return custom_urls + urls

    def jawaban_peserta_view(self, request, peserta_id):
        peserta = Peserta.objects.get(id=peserta_id)
        jawaban_list = JawabanPeserta.objects.filter(peserta=peserta)
        context = {
            'jawaban_list': jawaban_list,
            'peserta': peserta,
        }
        return TemplateResponse(request, 'kuis/jawaban_peserta.html', context)

admin.site.register(Soal, SoalAdmin)
admin.site.register(Kuis, KuisAdmin)
admin.site.register(Peserta, PesertaAdmin)
admin.site.register(JawabanPeserta, JawabanPesertaAdmin)


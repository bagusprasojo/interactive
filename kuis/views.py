from django.shortcuts import render
from .models import Soal, Kuis, Peserta
from django.shortcuts import get_object_or_404, redirect
from django.http import JsonResponse
from firebase_admin import db as firebase_db
from django.views.decorators.csrf import csrf_exempt
import json
from .models import Kuis, Peserta, Soal, JawabanPeserta

def leaderboard(request, kuis_id):
    kuis = get_object_or_404(Kuis, id=kuis_id)
    return render(request, 'kuis/leaderboard.html', {'kuis': kuis})

@csrf_exempt
def submit_jawaban(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            print(f"Data yang diterima: {data}")  # Debugging line
            
            kuis_id = data.get('kuis_id')
            print(f"Kuis ID: {kuis_id}")  # Debugging line

            peserta_id = data.get('peserta_id')  # Pastikan frontend kirim ini
            print(f"Peserta ID: {peserta_id}")  # Debugging line

            jawaban = data.get('jawaban')
            print(f"Jawaban: {jawaban}")  # Debugging line


            # Ambil kuis dan status soal aktif
            ref = firebase_db.reference(f'kuis/{kuis_id}')
            print(f"Referensi Firebase untuk kuis {kuis_id}: {ref}")  # Debugging line
            
            status_data = ref.get()
            print(f"Status data dari Firebase: {status_data}")  # Debugging line

            soal_index = status_data.get('soal_aktif') - 1
            print(f"Soal aktif index: {soal_index}")  # Debugging line

            kuis = Kuis.objects.get(id=kuis_id)
            soal = Soal.objects.filter(kuis=kuis).order_by('id')[soal_index]
            peserta = Peserta.objects.get(id=peserta_id)

            # Cek apakah peserta sudah menjawab soal ini
            sudah_jawab = JawabanPeserta.objects.filter(peserta=peserta, soal=soal).exists()
            if sudah_jawab:
                return JsonResponse({'message': 'Sudah menjawab soal ini.'})

            benar = (jawaban.upper() == soal.jawaban_benar.upper())

            JawabanPeserta.objects.create(
                peserta=peserta,
                soal=soal,
                jawaban=jawaban.upper(),
                benar=benar
            )

            # Update leaderboard
            leaderboard_ref = firebase_db.reference(f'leaderboard/{kuis_id}/{peserta.id}')
            leaderboard_ref.set({
                'nama': peserta.nama,
                'skor': JawabanPeserta.objects.filter(peserta=peserta, benar=True).count()
            })

            return JsonResponse({'message': 'Jawaban disimpan', 'benar': benar})

        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)
    else:
        return JsonResponse({'error': 'Method not allowed'}, status=405)

def status_kuis_api(request, kuis_id):
    ref = firebase_db.reference(f'kuis/{kuis_id}')
    data = ref.get() or {'status': 'menunggu', 'soal_aktif': -1}
    return JsonResponse(data)

def admin_kontrol(request, kuis_id):
    kuis = get_object_or_404(Kuis, id=kuis_id)
    soal_count = Soal.objects.filter(kuis=kuis).count()
    print(f"Jumlah soal untuk kuis {kuis_id}: {soal_count}")

    ref = firebase_db.reference(f'kuis/{kuis_id}')
    print(f"Referensi Firebase untuk kuis {kuis_id}: {ref}")
    status_data = ref.get() or {'status': 'menunggu', 'soal_aktif': -1}

    if request.method == 'POST':
        aksi = request.POST.get('aksi')
        if aksi == 'mulai':
            redaksi_soal = Soal.objects.filter(kuis=kuis).order_by('id').first()
            status_data = {'status': 'lanjut', 'soal_aktif': 1, 'redaksi_soal': redaksi_soal.pertanyaan if redaksi_soal else ''}
        elif aksi == 'lanjut':
            if status_data['soal_aktif'] + 1 <= soal_count:                
                redaksi_soal = Soal.objects.filter(kuis=kuis).order_by('id')[status_data['soal_aktif']]
                soal_aktif = status_data['soal_aktif'] + 1
                status_data = {'status': 'lanjut', 'soal_aktif': soal_aktif, 'redaksi_soal': redaksi_soal.pertanyaan}
            else:
                status_data = {'status': 'selesai', 'soal_aktif': status_data['soal_aktif']}
        elif aksi == 'kembali':
            if status_data['soal_aktif'] - 1 > 0:                
                soal_aktif = status_data['soal_aktif'] - 1
                redaksi_soal = Soal.objects.filter(kuis=kuis).order_by('id')[soal_aktif - 1]
                status_data = {'status': 'lanjut', 'soal_aktif': soal_aktif, 'redaksi_soal': redaksi_soal.pertanyaan}
            else:
                status_data = {'status': 'selesai', 'soal_aktif': status_data['soal_aktif']}
        elif aksi == 'selesai':
            status_data['status'] = 'selesai'

        ref.set(status_data)

    context = {
        'kuis': kuis,
        'status': status_data.get('status', 'menunggu'),
        'soal_aktif': status_data.get('soal_aktif', -1),
        'redaksi_soal': status_data.get('redaksi_soal', -1),
        'soal_count': soal_count,
    }

    return render(request, 'kuis/admin_kontrol.html', context)

def main_kuis(request):
    soals = Soal.objects.all()
    return render(request, 'kuis/main.html', {'soals': soals})

def daftar_kuis(request, kuis_id):
    kuis = get_object_or_404(Kuis, id=kuis_id)
    if request.method == 'POST':
        nama = request.POST['nama']
        peserta = Peserta.objects.create(nama=nama, kuis=kuis)
        request.session['peserta_id'] = peserta.id
        return redirect('tampilkan_soal', kuis_id=kuis.id)
    
    return render(request, 'kuis/daftar.html', {'kuis': kuis})

def kuis_soal(request, kuis_id, peserta_id):
    kuis = get_object_or_404(Kuis, id=kuis_id)
    peserta = get_object_or_404(Peserta, id=peserta_id)

    return render(request, 'kuis/kuis_soal.html', {
        'kuis': kuis,
        'peserta': peserta,
    })

def tampilkan_soal(request, kuis_id):
    peserta_id = request.session.get('peserta_id')
    if not peserta_id:
        return redirect('kuis_daftar', kuis_id=kuis_id)
    peserta = get_object_or_404(Peserta, id=peserta_id)
    return render(request, 'kuis/soal.html', {'peserta': peserta, 'kuis_id': kuis_id})


def leaderboard(request, kuis_id):
    return render(request, 'kuis/leaderboard.html', {'kuis_id': kuis_id})

def get_soal_ke(request, kuis_id, nomor):
    soal = Soal.objects.filter(kuis_id=kuis_id).order_by('id')[nomor-1]
    return JsonResponse({
        'pertanyaan': soal.pertanyaan,
        'jawaban_a': soal.jawaban_a,
        'jawaban_b': soal.jawaban_b,
        'jawaban_c': soal.jawaban_c,
        'jawaban_d': soal.jawaban_d,
    })

def api_soal_list(request, kuis_id):
    soal_qs = Soal.objects.filter(kuis_id=kuis_id).order_by('id')
    soal_list = [
        {
            'id': s.id,
            'pertanyaan': s.pertanyaan,
            'jawaban_a': s.jawaban_a,
            'jawaban_b': s.jawaban_b,
            'jawaban_c': s.jawaban_c,
            'jawaban_d': s.jawaban_d,
        }
        for s in soal_qs
    ]
    return JsonResponse({'soal_list': soal_list})
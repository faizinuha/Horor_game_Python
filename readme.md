# 🎮 Pixel Adventure Game - Dokumentasi Lengkap

## Fitur Utama

### 1. Pixel Art Style

- ✅ Player pixel art dengan animasi berjalan
- ✅ NPC pixel art dengan warna berbeda untuk setiap karakter
- ✅ Environment pixel art (rumah, pohon, tembok, dll)
- ✅ UI pixel art dengan efek retro

### 2. NPC & Dialog System

- ✅ Banyak NPC unik: Elder, Blacksmith, Merchant, Guide, Villager, Farmer, Child, Old Woman, Hermit, Hunter
- ✅ Dialog interaktif dengan animasi text
- ✅ Quest giver dengan tanda seru kuning
- ✅ Interaction range - mendekati NPC untuk bicara

### 3. Quest System

- ✅ Quest log (tekan Q)
- ✅ Collect quests dengan progress tracking
- ✅ Quest completion system
- ✅ Multiple active quests

### 4. Cutscene Intro

- ✅ Animated cutscene saat start game
- ✅ Player berjalan dengan background village
- ✅ Story text yang berganti otomatis
- ✅ Skip cutscene dengan SPACE

### 5. Enhanced Features

- ✅ Camera system yang mengikuti player
- ✅ Particle effects untuk visual feedback
- ✅ Health & Mana bars
- ✅ Minimap dengan posisi player & NPC
- ✅ Weather effects (rain/snow/storm/fog)
- ✅ Day/night cycle detail (pagi, siang, sore, malam, fajar, senja)

### 6. Dynamic World & Auto Events

- ✅ Multi-area: Village, Forest, Mountain, River, Cave, Farm, Cemetery
- ✅ Terrain generator: gunung, sungai, bukit, danau, hutan otomatis
- ✅ Dekorasi otomatis: pohon, batu, bunga, semak
- ✅ Sistem waktu detail: pagi, siang, sore, malam, fajar, senja
- ✅ Sistem cuaca: cerah, hujan, badai, kabut, salju
- ✅ Event otomatis: perubahan cuaca, waktu, dan kondisi lingkungan
- ✅ Area transisi otomatis (masuk gua, keluar gua, dsb)

---

## 📖 Dokumentasi Lengkap

### Struktur Dunia

- **Village**: Area utama, banyak NPC, rumah, pasar, quest utama.
- **Forest**: Area luas, banyak pohon, herbs, monster, quest collect.
- **Mountain**: Area tinggi, gunung dengan salju, monster kuat.
- **River/Lake**: Sungai dan danau, bisa ada jembatan, ikan, dan dekorasi air.
- **Cave**: Area gelap, banyak hantu, loot, dan quest khusus.
- **Farm**: Area pertanian, NPC petani, tanaman, dan quest sampingan.
- **Cemetery**: Area kuburan, suasana horror, quest misteri.

### Sistem Utama

- **NPC & Dialog**: Setiap NPC punya dialog unik, beberapa memberi quest.
- **Quest System**: Quest collect, progress, log, dan reward.
- **Cutscene**: Intro animasi, transisi antar area.
- **Camera**: Kamera mengikuti player, smooth scrolling.
- **Particle & Visuals**: Efek visual untuk interaksi, cuaca, dan event.
- **Health/Energy**: Bar HP/MP, stamina, efek saat terkena monster.
- **Minimap**: Menampilkan posisi player, NPC, dan area sekitar.
- **Weather & Time**: Siklus waktu detail, cuaca dinamis, efek visual dan gameplay.
- **Terrain & Dekorasi**: Dunia diisi otomatis dengan terrain dan dekorasi pixel art.
- **Area Transition**: Pindah area otomatis (misal: masuk gua, keluar ke desa).

### Event & Kondisi Otomatis

- **Cuaca berubah otomatis**: Hujan, badai, kabut, salju, cerah.
- **Waktu berjalan otomatis**: Pagi, siang, sore, malam, fajar, senja.
- **NPC & monster spawn**: Berdasarkan area dan waktu.
- **Dekorasi & terrain**: Di-generate otomatis setiap area.

### Kontrol Lengkap

- **WASD/Arrow Keys**: Gerak & navigasi menu
- **SPACE/ENTER**: Interaksi, lanjut dialog, skip cutscene
- **Q**: Quest log
- **I**: Inventory (placeholder)
- **ESC**: Pause/menu
- **F5**: Save game
- **R**: Restart (saat game over)

### Cara Menambah Area/Quest Baru

1. Tambahkan area di `environment.py` dan terrain di `terrain.py`.
2. Tambahkan NPC/monster di area baru pada `main.py`.
3. Tambahkan quest baru di `quest_system.py` dan hubungkan ke NPC.
4. Tambahkan dekorasi/terrain baru di `decorations.py`.

### Catatan

- Semua file Python saling terhubung dan digunakan (tidak ada yang sia-sia).
- Dunia dan event di-generate otomatis, jadi setiap main bisa berbeda.
- Sistem cuaca dan waktu mempengaruhi gameplay dan visual.
- Dokumentasi ini akan terus diupdate sesuai fitur baru.

---

Selamat bermain dan bereksplorasi di dunia pixel adventure yang dinamis! 🌄🌧️🌲🏘️

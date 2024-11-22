# KELOMPOK Om Gabe

## Team Members

1. **Wafi Afdi Alfaruqhi** - 22/503393/TK/55000  
2. **Gabriel Syailendra Fernandez** - 22/503450/TK/55009  
3. **Nur Rochman** - 22/493623/TK/54086  

## Links
[Video Demonstrasi](https://www.youtube.com/watch?v=c4gGS7nHrBo)

[Blog Proyek](https://wafiafdialfaruqhi.notion.site/ETL-Pipeline-Publisher-Stock-and-Steam-Game-Data-144a84a3d51e80d3b13cf01c0dc0f655?pvs=4)

[Video Presentasi](https://drive.google.com/file/d/1cjp551cJCt_NLLXVTX2lrKpMv3eDv4fR/view?usp=sharing)

## Latar Belakang Proyek

Pada proyek ini, kita akan mencoba untuk membuat ETL (Extract, Transform, Load) Pipeline untuk dapat mendapatkan data saham dan data dari steam. Proyek ini akan didukung oleh teknologi Pandas, Selenium, BeautifulSoup, Airflow, PostgreSQL, dan Azure. Sumber data akan diekstrak melalui web scrapping dan juga API publik. Data ditransform agar bersih dan siap untuk di load pada database PostgreSQL. Visualisasi data akan dilakukan dengan Tableue. Airflow akan membantu agar proses ETL dilakukan secara berkala dalam waktu setiap bulannya.

## Getting Started

### Prerequisites

- Python 3.8+  
- `venv` module for creating virtual environments  

## .ENV
Pastikan anda menaruh .env ini dalam folder airflow
```
DB_NAME=<nama_db>
DB_USER=<user_sb>
DB_HOST=<link_db>
DB_PASSWORD=<pass_db>
DB_PORT=<port_db>

FILE_PATH=<tmp_buffer>

PATH_TO_CA=<lokasi_ca_pem_untuk_db>

API_KEY_ALPHA=<api_key_alpha_vintage>
API_KEY_ITAD=<api_key_alpha_ITAD>

STOCK_SYMBOl="TM17.L"
URL_STEAM_PUB="https://store.steampowered.com/publisher/Team17"
```

### Instalasi

```bash
# Clone the repository
git clone [repository-url]
cd [repository-name]

# Create a virtual environment
python -m venv venv

# Activate the virtual environment
# On Windows
venv\Scripts\activate
# On macOS/Linux
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt



```
dasd

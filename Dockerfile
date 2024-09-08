# Python 3.9 asosida qurish
FROM python:3.11

# Ishchi katalogni yaratish
WORKDIR /app

# Talablar faylini nusxalash
COPY requirements.txt .

# Talablarni o'rnatish
RUN pip install --no-cache-dir -r requirements.txt

# Bot faylini nusxalash
COPY . .

# Botni ishga tushirish
CMD ["python", "bot.py"]
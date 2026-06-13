# Elasticsearch — Index Management (ILM، Alias، Reindex)

> مدیریت چرخه‌ی حیات index برای production: ILM، alias برای zero-downtime، و reindex.

---

## 📖 مفاهیم

### Mapping، Analyzer، Settings

**توضیح:**

هنگام ساخت index، settings (تعداد shard/replica، analyzer سفارشی) و mapping (نوع فیلدها) تعریف می‌شود. analyzer سفارشی برای زبان‌های خاص (مثل فارسی با normalization).

**مثال کد:**

```json
PUT /articles
{
  "settings": {
    "number_of_shards": 3,
    "number_of_replicas": 1,
    "analysis": {
      "analyzer": {
        "persian_custom": {
          "type": "custom",
          "tokenizer": "standard",
          "filter": ["lowercase", "persian_normalization"]
        }
      }
    }
  }
}
```

**نکات کلیدی:**

- تعداد shard بعد از ساخت قابل‌تغییر نیست (با دقت انتخاب کنید).
- analyzer روی نحوه‌ی index و search اثر می‌گذارد.

---

### ILM، Alias، Reindex

**توضیح:**

- **ILM (Index Lifecycle Management):** چرخه‌ی hot → warm → cold → delete برای داده‌ی time-series (مثل logها). داده‌ی قدیمی به storage ارزان‌تر منتقل و نهایتاً حذف می‌شود.
- **Index Template:** policy برای indexهای جدید (نام‌گذاری الگو، settings).
- **Alias:** یک نام مجازی که به یک یا چند index اشاره می‌کند — برای **zero-downtime reindex** (تغییر mapping با ساخت index جدید و switch atomic alias).
- **Reindex API:** کپی داده بین indexها (برای تغییر mapping/migration).

**نکات کلیدی:**

- alias برای zero-downtime reindex (switch بدون downtime).
- ILM برای مدیریت خودکار logهای time-series.

---

## 🎯 سوالات مصاحبه

### سوال ۱: چطور mapping یک index موجود را بدون downtime تغییر می‌دهی؟

**سطح:** Senior / Lead
**تکرار:** متوسط

**جواب کامل:**

mapping برخی فیلدها بعد از ساخت قابل‌تغییر نیست (مثل تغییر type). راه‌حل zero-downtime با **alias + reindex**: (۱) index جدید با mapping درست بسازید. (۲) داده را با **Reindex API** از index قدیمی به جدید کپی کنید (می‌توان همزمان write جدید را به هر دو فرستاد یا از alias استفاده کرد). (۳) با **alias** (که اپ همیشه از آن می‌خواند به‌جای نام مستقیم index)، به‌صورت **atomic** alias را از index قدیمی به جدید switch کنید — یک عملیات اتمیک که downtime صفر می‌دهد. (۴) index قدیمی را حذف کنید. کلید: اپ از ابتدا باید با alias کار کند نه نام مستقیم index، تا این switch ممکن باشد.

**نکته مصاحبه:**

Senior به alias atomic switch و reindex اشاره می‌کند.

---

### سوال ۲: ILM چه مشکلی را حل می‌کند؟

**سطح:** Senior
**تکرار:** کم

**جواب کامل:**

برای داده‌ی time-series (مثل log، metric) که حجم زیاد و ارزش کاهنده با زمان دارد، نگه‌داری همه روی storage گران (hot، SSD) ناکارآمد است. ILM چرخه‌ی خودکار تعریف می‌کند: داده‌ی جدید در **hot** (سریع، قابل‌نوشتن)، بعد از مدتی به **warm** (read-only، storage ارزان‌تر)، سپس **cold** (به‌ندرت دسترسی)، و نهایتاً **delete** (حذف خودکار بعد از retention). مزایا: کاهش هزینه‌ی storage، performance بهتر hot index (کوچک می‌ماند)، و حذف خودکار بدون cron دستی. معمولاً با rollover (وقتی index به اندازه/سن مشخص رسید، index جدید) ترکیب می‌شود.

**نکته مصاحبه:**

Senior به hot/warm/cold/delete و کاهش هزینه اشاره می‌کند.

---

## ⚠️ اشتباهات رایج

### اشتباه ۱: استفاده از نام مستقیم index به‌جای alias

```text
❌ اپ به index مستقیم وصل → reindex بدون downtime ممکن نیست
✅ اپ به alias وصل شود
```

**توضیح:** alias برای switch بدون downtime لازم است.

---

### اشتباه ۲: shard بیش از حد زیاد

```text
❌ تعداد shard زیاد برای داده‌ی کم → overhead (oversharding)
✅ تعداد shard متناسب با حجم داده
```

**توضیح:** هر shard overhead دارد؛ oversharding performance را کم می‌کند.

---

## 🔗 ارتباط با سایر مفاهیم

- ILM با **log retention (ELK 10.4)**.
- alias/reindex با **zero-downtime migration**.
- shard با **sharding (4.4)** و scaling.

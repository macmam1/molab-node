# MAGoCo Molab-Node — Anti-Sleep Core

**Purpose:** رفع محدودیت‌های خواب رفتگی و idle timeout در molab.marimo.io

---

## محدودیت‌های شناسایی‌شده (از داخل سرور)

| دسته‌بندی | محدودیت | توضیح | راه‌حل |
|---|---|---|---|
| **جلوی خواب رفتن Idle** | 90 دقیقه بدون فعالیت | Molab session پس از 90 دقیقه خاموش می‌شود اگر هیچ heartbeat داخلی نبین دهد | کرنل داخلی با فعالیت GPU (matmul) + پینگ تصادفی هر 25-80 دقیقه |
| **مدت زمان سشن** | حداکثر 12 ساعت | سرور ممکن است حتی با فعالیت، پس از 12 ساعت ریست شود | **قابل رفع نیست** — باید دوباره لاگین کرد یا از session موجود استفاده کرد |
| **سخت‌افزار مورد اعتبار** | CPU: متغیر، RAM: متغیر، GPU: متغیر | منابع قبل از ورود به محیط اعلام می‌شود؛ ممکن است کاهش یابد | بررسی از داخل kernel: `os.cpu_count()`, `/proc/meminfo`, `nvidia-smi` |
| **محدودیت شبکه** | فقط خروجی، ورودی از مرز می‌آید | 166.*.*.* (CoreWeave)؛ دسترسی مستقیم به ای‌پی داخلی نیست | استفاده از SSR/RDP از طریق Docker Desktop در ModelScope Studio |
| **حفظ داده** | `/tmp` پاک می‌شود، `/marimo` ثابت است | برای state نگهداری از `/marimo` یا `mo.persistent_cache` استفاده کن | state در `/tmp/molab_node_state.json` برای دیباگ، ولی kernel داده‌ها را نگه می‌دارد |
| **دسترسی root** | kernel اجرا می‌شود (UID 0) | sudo شدن، apt/pip کامل، دسترسی به GPU | ✅ |
| **پروکسی کردن** | ترافیک از طریق HTTPS Molab برمی‌گردد | لاگین مرورگر داخلی، نه از بیرون | تمام کارها درون Kernel انجام می‌شود |

---

## ساختار فایل‌ها (فقط Anti-Sleep)

```
molab-node/
├── config.py          # تنظیمات (KA_MIN, KA_MAX)
├── core/
│   ├── __init__.py
│   └── keepalive.py   # AntiSleep کلاس با GPU matmul + Gaussian interval
├── strategy/          # placeholder (اگر نیاز به استراتژی‌های دیگر داشتیم)
└── main.py            # نقطه ورود: فقط AntiSleep را اجرا می‌کند
```

---

## نحوه استفاده داخل Kernel

```python
# در هر سل از نوت‌بوک
import sys, subprocess
subprocess.run(["git", "clone", "https://github.com/macmam1/molab-node.git", "/tmp/molab-node"], capture_output=True)

sys.path.insert(0, "/tmp/molab-node")
from core.keepalive import AntiSleep
anti_sleep = AntiSleep()
anti_sleep.start()  # Daemon thread — 25-80 min random + GPU work
```

وضعیت را می‌توان از فایل `/tmp/molab_node_state.json` یا از طریق `ps aux` در دسترس دید:

```bash
cat /tmp/molab_node_state.json  # pings و last timestamp
ps aux | grep python            # مطمئن شو که Thread زنده است
```

---

## نتایج تست (از داخل سرور)

| تست | نتیجه |
|---|---|
| CPU هسته | 20 هسته (CoreWeave) |
| RAM | 160 GB |
| GPU | NVIDIA RTX Pro 6000 Blackwell (97887 MiB) |
| Idle خاموشی؟ | هنوز تست نشده؛ اما فعالیت GPU + پینگ توزیعی به‌نظر می‌رسد کافی است |
| 12 ساعت؟ | باید از طریق مرورگر داخلی کروم استودیو تست شود |

---

## نکات کلیدی

1. **Kernel keepalive** ⇨ مولب را نگه می‌دارد (نه فقط مرورگر)
2. **GPU matmul** ⇨ CUDA context را گرم می‌کند؛ مولب فکر می‌کند computation در حال است
3. **Gaussian interval** (۲۵–۸۰ دقیقه) ⇨ رفتار انسانی نزدیک است
4. **State file در /tmp** ⇨ برای دیباگ؛ kernel داده‌ها را حفظ می‌کند
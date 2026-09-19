import os
import time
import random
import itertools
import threading
import unicodedata
import telebot
from telebot.apihelper import ApiTelegramException

# --- CẤU HÌNH ---
ADMIN_ID = 7548148236

BOT_TOKENS = [
    "8843102639:AAGivNjH9aVD0j9FaIsKuSjdk6QcpJKWSVM",
    "8814689200:AAFEc3iPOKpFGdyTL6LQ8fX7eP6TsEoeYsg",
    "8951339873:AAEcTd91gA_mHuHYK35hmYKuC22AvjUuZh0",
    "8843296488:AAFVI6FPR28uFCCeiHBKLLkZUjaImeAqVwk",
    "8660578406:AAENFWs7_JU3usMuRwxp-FSL3U3PzDzvhYw"
]

FILE_NAME = "mhoa.txt"

# Bảng chữ cái chuẩn
NORMAL_CHARS = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789"

# Bảng font Unicode nghệ thuật
FONT_MAPS = [
    # Sans Bold
    "𝗔𝗕𝗖𝗗𝗘𝗙𝗚𝗛𝗜𝗝𝗞𝗟𝗠𝗡𝗢𝗣𝗤𝗥𝗦𝗧𝗨𝗩𝗪𝗫𝗬𝗭𝗮𝗯𝗰𝗱𝗲𝗳𝗴𝗵𝗶𝗷𝗸𝗹𝗺𝗻𝗼𝗽𝗾𝗿𝘀𝘁𝘂𝘃𝘄𝘅𝘆𝘇𝟬𝟭𝟮𝟯𝟰𝟱𝟲𝟳𝟴𝟵",
    # Sans Bold Italic
    "𝘼𝘽𝘾𝘿𝙀𝙁𝙂𝙃𝙄𝙅𝙆𝙇𝙈𝙉𝙊𝙋𝙌𝙍𝙎𝙏𝙐𝙑𝙒𝙓𝙔𝙕𝙖𝙗𝙘𝙙𝙚𝙛𝙜𝙝𝙞𝙟𝙠𝙡𝙢𝙣𝙤𝙥𝙦𝙧𝙨𝙩𝙪𝙫𝙬𝙭𝙮𝙯0123456789",
    # Monospace (Máy đánh chữ)
    "𝙰𝙱𝙲𝙳𝙴𝙵𝙶𝙷𝙸𝙹𝙺𝙻𝙼𝙽𝙾𝙿𝚀𝚁𝚂𝚃𝚄𝚅𝚆𝚇𝚈𝚉𝚊𝚋𝚌𝚍𝚎𝚏𝚐𝚑𝚒𝚓𝚔𝚕𝗺𝗻𝚘𝚙𝚚𝚛𝚜𝚝𝚞𝚟𝚠𝚡𝚢𝚣𝟶𝟷𝟸𝟹𝟺𝟻𝟼𝟽𝟾𝟿",
    # Serif Bold
    "𝐀𝐁𝐂𝐃𝐄𝐅𝐆𝐇𝐈𝐉𝐊𝐋𝐌𝐍𝐎𝐏𝐐𝐑𝐒𝐓𝐔𝐕𝐖𝐗𝐘𝐙𝐚𝐛𝐜𝐝𝐞𝐟𝐠𝐡𝐢𝐣𝐤𝐥𝐦𝐧𝐨𝐩𝐪𝐫𝐬𝐭𝐮𝐯𝐰𝐱𝐲𝐳𝟎𝟏𝟐𝟑𝟒𝟓𝟔𝟕𝟖𝟗",
    # Serif Bold Italic
    "𝑨𝑩𝑪𝑫𝑬𝑭𝑮𝑯𝑰𝑱𝑲𝑳𝑴𝑵𝑶𝑷𝑸𝑹𝑺𝑻𝑼𝑽𝑾𝑿𝒀𝒁𝒂𝒃𝒄𝒅𝒆𝒇𝒈𝒉𝒊𝒋𝒌𝒍𝒎𝒏𝒐𝒑𝒒𝒓𝒔𝒕𝒖𝒗𝒘𝒙𝒚𝒛0123456789",
    # Gothic Bold
    "𝕬𝕭𝕮𝕯𝕰𝕱𝕲𝕳𝕴𝕵𝕶𝕷𝕸𝕹𝕺𝕻𝕼𝕽𝕾𝕿𝖀𝖁𝖂𝖃𝖄𝖅𝖆𝖇𝖈𝖉𝖊𝖋𝖌𝖍𝖎𝖏𝖐𝖑𝖒𝖓𝖔𝖕𝖖𝖗𝖘𝖙𝖚𝖛𝖜𝖝𝖞𝖟0123456789",
    # Double Struck
    "𝔸𝔹ℂ𝔻𝔼𝔽𝔾ℍ𝕀𝕁𝕂𝕃𝕄ℕ𝕆ℙℚℝ𝕊𝕋𝕌𝕍𝕎𝕏𝕐ℤ𝕒𝓫𝕔𝕕𝕖𝕗𝕘𝕙𝕚𝕛𝕜𝕝𝕞𝕟𝕠𝕡𝕢𝕣𝕤𝕥𝕦𝕧𝕨𝕩𝕪𝕫𝟘𝟙𝟚𝟛𝟜𝟝𝟞𝟟𝟠𝟡",
    # Circled
    "ⒶⒷⒸⒹⒺⒻⒼⒽⒾⒿⓀⓁⓂⓃⓄⓅⓆⓇⓈⓉⓊⓋⓌⓍⓎⓏⓐⓑⓒⓓⓔⓕⓖⓗⓘⓙⓚⓛⓜⓝⓞⓟⓠⓡⓢⓣⓤⓥⓦⓧⓨⓩ⓪①②③④⑤⑥⑦⑧⑨",
    # Script Bold
    "𝓐𝓑𝓒𝓓𝓔𝓕𝓖𝓗𝓘𝓙𝓚𝓛𝓜𝓝𝓞𝓟𝓠𝓡𝓢𝓣𝓤𝓥𝓦𝓧𝓨𝓩𝓪𝓫𝓬𝓭𝓮𝓯𝓰𝓱𝓲𝓳𝓴𝓵𝓶𝓷𝓸𝓹𝓺𝓻𝓈𝓉𝓊𝓋𝓌𝓍𝓎𝓏0123456789"
]

TRANSLATION_TABLES = [str.maketrans(NORMAL_CHARS, f) for f in FONT_MAPS]


def remove_vietnamese_tones(text: str) -> str:
    """Khử dấu tiếng Việt để toàn bộ chữ ăn chuẩn font Unicode mà không bị lỗi layout."""
    text = text.replace("Đ", "D").replace("đ", "d")
    normalized = unicodedata.normalize("NFD", text)
    return "".join(c for c in normalized if unicodedata.category(c) != "Mn")


def make_fancy_text(text: str) -> str:
    """Chuyển đổi toàn bộ khối văn bản sang font nghệ thuật ngẫu nhiên."""
    table = random.choice(TRANSLATION_TABLES)
    clean_text = remove_vietnamese_tones(text)
    return clean_text.translate(table)


# Quản lý trạng thái
chat_status = {}
chat_delays = {}
chat_threads = {}
default_delay = 2.0

bots = [telebot.TeleBot(token) for token in BOT_TOKENS]
bot_cycle = itertools.cycle(bots)


def read_content():
    """
    Đọc file kq.txt theo từng khối văn bản.
    Các khối cách nhau bởi dấu '---' hoặc '==='.
    Nếu không có dấu ngăn cách, toàn bộ file được coi là 1 khối duy nhất.
    """
    if not os.path.exists(FILE_NAME):
        return []
    with open(FILE_NAME, "r", encoding="utf-8") as f:
        content = f.read().strip()

    if not content:
        return []

    # Tách các khối bài khác nhau bằng '---' hoặc '==='
    if "\n---\n" in content:
        blocks = [b.strip() for b in content.split("\n---\n") if b.strip()]
    elif "\n===\n" in content:
        blocks = [b.strip() for b in content.split("\n===\n") if b.strip()]
    else:
        blocks = [content]

    return blocks


def treo_worker(chat_id):
    """Luồng gửi nguyên khối văn bản qua 5 bot luân phiên."""
    while chat_status.get(chat_id, False):
        blocks = read_content()
        if not blocks:
            for bot in bots:
                try:
                    bot.send_message(chat_id, "⚠️ File kq.txt đang trống!")
                    break
                except Exception:
                    continue
            chat_status[chat_id] = False
            break

        for block in blocks:
            if not chat_status.get(chat_id, False):
                break

            # Đổi toàn bộ khối văn bản sang kiểu chữ ngẫu nhiên
            styled_text = make_fancy_text(block)

            # Cắt ngắn nếu vượt ngưỡng 4096 ký tự của Telegram
            if len(styled_text) > 4000:
                styled_text = styled_text[:4000]

            current_bot = next(bot_cycle)
            try:
                current_bot.send_message(chat_id, styled_text)
            except ApiTelegramException:
                time.sleep(0.5)
            except Exception:
                pass

            delay = chat_delays.get(chat_id, default_delay)
            time.sleep(delay)


def setup_handlers(bot_instance):
    @bot_instance.message_handler(commands=["treo"])
    def handle_treo(message):
        if message.from_user.id != ADMIN_ID:
            return

        args = message.text.split()
        if len(args) < 2:
            bot_instance.reply_to(message, "Cú pháp: /treo on hoặc /treo off")
            return

        action = args[1].lower()
        chat_id = message.chat.id

        if action == "on":
            if chat_status.get(chat_id, False):
                bot_instance.reply_to(message, "⚠️ Nhóm đang treo rồi!")
                return

            if not os.path.exists(FILE_NAME) or os.stat(FILE_NAME).st_size == 0:
                bot_instance.reply_to(message, "⚠️ File kq.txt không có nội dung!")
                return

            chat_status[chat_id] = True
            t = threading.Thread(target=treo_worker, args=(chat_id,), daemon=True)
            chat_threads[chat_id] = t
            t.start()
            current_delay = chat_delays.get(chat_id, default_delay)
            bot_instance.reply_to(message, f"🚀 Bắt đầu treo full khối!\n⏱ Tốc độ: {current_delay}s/lần")

        elif action == "off":
            if not chat_status.get(chat_id, False):
                bot_instance.reply_to(message, "⚠️ Nhóm chưa bật treo!")
                return

            chat_status[chat_id] = False
            bot_instance.reply_to(message, "🛑 Đã dừng treo!")

    @bot_instance.message_handler(commands=["delay"])
    def handle_delay(message):
        if message.from_user.id != ADMIN_ID:
            return

        args = message.text.split()
        if len(args) < 2:
            current = chat_delays.get(message.chat.id, default_delay)
            bot_instance.reply_to(message, f"⏱ Delay hiện tại: {current}s\nĐổi delay: /delay <số giây>")
            return

        try:
            new_delay = float(args[1])
            if new_delay < 0.1:
                bot_instance.reply_to(message, "⚠️ Delay tối thiểu 0.1s!")
                return
            chat_delays[message.chat.id] = new_delay
            bot_instance.reply_to(message, f"✅ Đã đổi delay thành: {new_delay}s")
        except ValueError:
            bot_instance.reply_to(message, "⚠️ Vui lòng nhập số hợp lệ!")


for b in bots:
    setup_handlers(b)


def run_bot(bot_instance):
    while True:
        try:
            bot_instance.infinity_polling(timeout=20, long_polling_timeout=10)
        except Exception:
            time.sleep(3)


if __name__ == "__main__":
    print(f"Bot khởi động với Admin ID: {ADMIN_ID}...")
    threads = []
    for b in bots:
        t = threading.Thread(target=run_bot, args=(b,), daemon=True)
        threads.append(t)
        t.start()

    for t in threads:
        t.join()
            if 1 <= number <= maximum and number not in result:
                result.append(number)

        except ValueError:
            pass

    return result


class Bot(ZaloAPI):

    def __init__(self, imei, cookies):
        super().__init__(
            "api_key",
            "secret_key",
            imei,
            cookies
        )

    def get_groups(self):
        groups = []

        try:
            data = self.fetchAllGroups()

            for group_id in data.gridVerMap.keys():

                try:
                    info = self.fetchGroupInfo(group_id)

                    if (
                        info
                        and hasattr(info, "gridInfoMap")
                        and group_id in info.gridInfoMap
                    ):
                        group_data = info.gridInfoMap[group_id]

                        groups.append({
                            "id": group_id,
                            "name": group_data.get(
                                "name",
                                "Không có tên"
                            )
                        })

                except Exception as e:
                    log(
                        f"[⚠️] Bỏ qua nhóm {group_id}: {e}",
                        "yellow"
                    )

            return groups

        except Exception as e:
            log(
                f"[❌] Không lấy được danh sách nhóm: {e}",
                "red"
            )
            return []


def main():

    console.clear()

    console.print(
        Panel(
            "[bold cyan]GỬI NỘI DUNG VÀO NHIỀU NHÓM ZALO[/bold cyan]\n\n"
            "Gửi 1 lần vào các nhóm mà tài khoản hiện đang tham gia.",
            title="ZALO",
            border_style="cyan",
            box=DOUBLE
        )
    )

    # =========================
    # ĐĂNG NHẬP
    # =========================

    imei = Prompt.ask(
        "[📱] Nhập IMEI"
    ).strip()

    cookie_text = Prompt.ask(
        "[🍪] Nhập Cookie"
    ).strip()

    try:
        cookies = ast.literal_eval(cookie_text)

        if not isinstance(cookies, dict):
            raise ValueError()

    except Exception:
        log(
            "[❌] Cookie phải có dạng dictionary.",
            "red"
        )
        return

    # =========================
    # KẾT NỐI
    # =========================

    try:
        log(
            "\n[⏳] Đang kết nối Zalo...",
            "cyan"
        )

        bot = Bot(
            imei,
            cookies
        )

        log(
            "[✅] Kết nối thành công!",
            "green"
        )

    except Exception as e:
        log(
            f"[❌] Lỗi kết nối: {e}",
            "red"
        )
        return

    # =========================
    # LẤY NHÓM
    # =========================

    log(
        "\n[⏳] Đang lấy danh sách nhóm...",
        "cyan"
    )

    groups = bot.get_groups()

    if not groups:
        log(
            "[❌] Không tìm thấy nhóm nào.",
            "red"
        )
        return

    # =========================
    # HIỂN THỊ NHÓM
    # =========================

    table = Table(
        show_header=True,
        box=None
    )

    table.add_column(
        "STT",
        justify="center"
    )

    table.add_column(
        "Tên nhóm"
    )

    for index, group in enumerate(groups, 1):
        table.add_row(
            str(index),
            group["name"]
        )

    console.print(
        Panel(
            table,
            title="[bold cyan]📋 NHÓM HIỆN CÓ[/bold cyan]",
            border_style="cyan"
        )
    )

    # =========================
    # CHỌN NHÓM
    # =========================

    selection = Prompt.ask(
        "\n[🔹] Chọn nhóm "
        "(VD: 1,2,3 hoặc ALL)"
    )

    selected_indexes = parse_selection(
        selection,
        len(groups)
    )

    if not selected_indexes:
        log(
            "[❌] Bạn chưa chọn nhóm hợp lệ.",
            "red"
        )
        return

    selected_groups = [
        groups[index - 1]
        for index in selected_indexes
    ]

    # =========================
    # NỘI DUNG
    # =========================

    console.print()

    content = Prompt.ask(
        "[✏️] Nhập nội dung/link cần gửi"
    )

    if not content.strip():
        log(
            "[❌] Nội dung không được để trống.",
            "red"
        )
        return

    # =========================
    # DELAY
    # =========================

    while True:

        delay_text = Prompt.ask(
            "[⏱️] Delay giữa các nhóm (giây)",
            default="3"
        )

        try:
            delay = float(delay_text)

            if delay < 0:
                raise ValueError()

            break

        except ValueError:
            log(
                "[❌] Delay phải là số >= 0.",
                "red"
            )

    # =========================
    # XÁC NHẬN
    # =========================

    console.print()

    console.print(
        Panel(
            "\n".join(
                f"• {group['name']}"
                for group in selected_groups
            ),
            title=(
                f"[bold yellow]"
                f"ĐÃ CHỌN {len(selected_groups)} NHÓM"
                f"[/bold yellow]"
            ),
            border_style="yellow"
        )
    )

    console.print(
        Panel(
            content,
            title="[bold cyan]NỘI DUNG[/bold cyan]",
            border_style="cyan"
        )
    )

    confirm = Prompt.ask(
        "\n[❓] Bắt đầu gửi?",
        choices=["y", "n"],
        default="n"
    )

    if confirm != "y":
        log(
            "[🛑] Đã hủy.",
            "yellow"
        )
        return

    # =========================
    # GỬI
    # =========================

    success = 0
    failed = 0

    console.print(
        "\n[bold cyan]=== BẮT ĐẦU ===[/bold cyan]\n"
    )

    for index, group in enumerate(
        selected_groups,
        1
    ):

        try:

            bot.send(
                Message(text=content),
                thread_id=group["id"],
                thread_type=ThreadType.GROUP
            )

            success += 1

            log(
                f"[{index}/{len(selected_groups)}] "
                f"✅ {group['name']}",
                "green"
            )

        except Exception as e:

            failed += 1

            log(
                f"[{index}/{len(selected_groups)}] "
                f"❌ {group['name']}: {e}",
                "red"
            )

        # Delay giữa các nhóm
        if index < len(selected_groups):
            time.sleep(delay)

    # =========================
    # KẾT QUẢ
    # =========================

    console.print()

    console.print(
        Panel(
            f"[green]Thành công: {success}[/green]\n"
            f"[red]Thất bại: {failed}[/red]\n"
            f"[cyan]Tổng nhóm: {len(selected_groups)}[/cyan]",
            title="[bold cyan]HOÀN TẤT[/bold cyan]",
            border_style="cyan"
        )
    )


if __name__ == "__main__":
    try:
        main()

    except KeyboardInterrupt:
        print("\nĐã dừng.")

    except Exception as e:
        print(f"\nLỗi: {e}")

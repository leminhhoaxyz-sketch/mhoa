import ast
import time

from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.prompt import Prompt
from rich.box import DOUBLE

from zlapi import ZaloAPI, Message, ThreadType


console = Console()


def log(text, style="white"):
    console.print(text, style=style)


def parse_selection(value, maximum):
    value = value.strip()

    if value.upper() == "ALL":
        return list(range(1, maximum + 1))

    result = []

    for item in value.split(","):
        item = item.strip()

        if not item:
            continue

        try:
            number = int(item)

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

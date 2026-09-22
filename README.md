# BRMods package — repo `hoanganh-alex/BRMODS`, dùng với LAUNCHER

## Files (trong folder này)
| File | Mô tả |
|------|-------|
| `ok.dll` | stub login — upload làm asset `ok.dll` |
| `minduin.dll` | payload mod — upload làm asset `minduin.dll` |
| `BR.Mods.Launcher.exe` | **bản patch** (tải `ok.dll` + `minduin.dll` từ release repo này) SHA `075349BB…` |

## Up lên GitHub
1. Push repo (lệnh trong `New Text Document.txt`).
2. **Releases → new release**, Tag `v1`, upload 2 file với ĐÚNG tên:
   - `ok.dll`
   - `minduin.dll`
3. Test: `BR.Mods.Launcher.exe --verify-downloads` (exit 0 = tải OK).

## Dùng (máy chơi game, giữ launcher)
1. Server authswap 443 đang chạy (bắt buộc, như cũ).
2. Mở HD-Player → chạy `BR.Mods.Launcher.exe` (bản patch) → `Injecao concluida!`.
3. Nhập key trong game → main menu.

SHA-256 `brmod_loader.dll`: `9CE36AB997A3520F60CEB970BFD79A036C3BB2988909DC37A49E32B8D948BC7C`

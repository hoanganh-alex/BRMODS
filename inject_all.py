"""Inject all BRMods DLLs into HD-Player.exe (elevated). Order: stok -> minduin -> loader."""
import ctypes
import os
import sys
import time
from ctypes import wintypes

k32 = ctypes.WinDLL("kernel32", use_last_error=True)
k32.OpenProcess.restype = wintypes.HANDLE
k32.OpenProcess.argtypes = [wintypes.DWORD, wintypes.BOOL, wintypes.DWORD]
k32.VirtualAllocEx.restype = wintypes.LPVOID
k32.VirtualAllocEx.argtypes = [wintypes.HANDLE, wintypes.LPVOID, ctypes.c_size_t,
                               wintypes.DWORD, wintypes.DWORD]
k32.WriteProcessMemory.restype = wintypes.BOOL
k32.WriteProcessMemory.argtypes = [wintypes.HANDLE, wintypes.LPVOID, wintypes.LPCVOID,
                                   ctypes.c_size_t, ctypes.POINTER(ctypes.c_size_t)]
k32.GetModuleHandleW.restype = wintypes.HMODULE
k32.GetModuleHandleW.argtypes = [wintypes.LPCWSTR]
k32.GetProcAddress.restype = wintypes.LPVOID
k32.GetProcAddress.argtypes = [wintypes.HMODULE, wintypes.LPCSTR]
k32.CreateRemoteThread.restype = wintypes.HANDLE
k32.CreateRemoteThread.argtypes = [wintypes.HANDLE, wintypes.LPVOID, ctypes.c_size_t,
                                   wintypes.LPVOID, wintypes.LPVOID,
                                   wintypes.DWORD, wintypes.LPDWORD]
k32.WaitForSingleObject.restype = wintypes.DWORD
k32.WaitForSingleObject.argtypes = [wintypes.HANDLE, wintypes.DWORD]
k32.GetExitCodeThread.restype = wintypes.BOOL
k32.GetExitCodeThread.argtypes = [wintypes.HANDLE, wintypes.LPDWORD]
k32.CreateToolhelp32Snapshot.restype = wintypes.HANDLE
k32.CreateToolhelp32Snapshot.argtypes = [wintypes.DWORD, wintypes.DWORD]
k32.Process32FirstW.restype = wintypes.BOOL
k32.Process32NextW.restype = wintypes.BOOL

PROCESS_ALL = 0x1F0FFF
TH32CS_SNAPPROCESS = 0x2


class PE(ctypes.Structure):
    _fields_ = [("dwSize", wintypes.DWORD),
                ("cntUsage", wintypes.DWORD),
                ("th32ProcessID", wintypes.DWORD),
                ("th32DefaultHeapID", ctypes.c_ulonglong),
                ("th32ModuleID", wintypes.DWORD),
                ("cntThreads", wintypes.DWORD),
                ("th32ParentProcessID", wintypes.DWORD),
                ("pcPriClassBase", wintypes.LONG),
                ("dwFlags", wintypes.DWORD),
                ("szExeFile", wintypes.WCHAR * 260)]


def find_pid(name):
    snap = k32.CreateToolhelp32Snapshot(TH32CS_SNAPPROCESS, 0)
    pe = PE()
    pe.dwSize = ctypes.sizeof(pe)
    ok = k32.Process32FirstW(snap, ctypes.byref(pe))
    while ok:
        if pe.szExeFile.lower() == name.lower():
            k32.CloseHandle(snap)
            return pe.th32ProcessID
        ok = k32.Process32NextW(snap, ctypes.byref(pe))
    k32.CloseHandle(snap)
    return 0


def inject(pid, dll_path):
    dll = os.path.abspath(dll_path).encode("ascii")
    h = k32.OpenProcess(PROCESS_ALL, False, pid)
    if not h:
        return "OpenProcess FAILED err=%d" % ctypes.get_last_error()
    try:
        mem = k32.VirtualAllocEx(h, None, len(dll) + 1, 0x3000, 0x04)
        if not mem:
            return "VirtualAllocEx FAILED err=%d" % ctypes.get_last_error()
        if not k32.WriteProcessMemory(h, mem, dll, len(dll) + 1, None):
            return "WriteProcessMemory FAILED err=%d" % ctypes.get_last_error()
        ll = k32.GetProcAddress(k32.GetModuleHandleW("kernel32.dll"), b"LoadLibraryA")
        th = k32.CreateRemoteThread(h, None, 0, ll, mem, 0, None)
        if not th:
            return "CreateRemoteThread FAILED err=%d" % ctypes.get_last_error()
        k32.WaitForSingleObject(th, 30000)
        code = wintypes.DWORD()
        k32.GetExitCodeThread(th, ctypes.byref(code))
        k32.CloseHandle(th)
        return "OK base=0x%X" % code.value
    finally:
        k32.CloseHandle(h)


if __name__ == "__main__":
    here = os.path.dirname(os.path.abspath(__file__))
    pid = find_pid("HD-Player.exe")
    if not pid:
        print("HD-Player.exe not running. Mo game truoc.")
        sys.exit(1)
    print("target PID=%d" % pid)
    # stok chi 1: uu tien ok.dll
    order = ["ok.dll" if os.path.exists(os.path.join(here, "ok.dll")) else "stok-khoahihi.dll",
             "minduin.dll", "brmod_loader.dll"]
    for dll in order:
        p = os.path.join(here, dll)
        if not os.path.exists(p):
            print("SKIP %s (missing)" % dll)
            continue
        print("%s -> %s" % (dll, inject(pid, p)))
        time.sleep(4)
    print("done. Nhap key trong game de vao main.")
